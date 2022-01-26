"""
A device that allows us to implement operation on a single qudit. The backend is a remote simulator.
"""

import json
import requests
import numpy as np

from .django_device import DjangoDevice

# observables
from .single_qudit_ops import LZ, LZ2, ZObs

# operations
from .single_qudit_ops import RLX, RLZ, RLZ2, Load

# classes
from .single_qudit_ops import SingleQuditObservable, SingleQuditOperation

# operations for local devices


class SingleQuditDevice(DjangoDevice):
    """
    The single qudit device class, which is remotely calling the simulator.
    """

    ## Define operation map for the experiment
    _operation_map = {"RLX": RLX, "RLZ": RLZ, "RLZ2": RLZ2, "Load": Load}

    name = "Single Qudit Quantum Simulator Simulator plugin"
    pennylane_requires = ">=0.16.0"
    version = "0.0.1"
    author = "Fred Jendrzejewski"

    short_name = "synqs.sqs"

    _observable_map = {"LZ": LZ, "ZObs": ZObs, "LZ2": LZ2}

    def __init__(
        self,
        shots=1,
        username=None,
        url="http://qsimsim.synqs.org/api/singlequdit/",
        password=None,
        job_id=None,
        blocking=True,
    ):
        """
        The initial part.
        """
        super().__init__(
            url=url,
            wires=1,
            shots=shots,
            username=username,
            password=password,
            blocking=blocking,
            job_id=job_id,
        )
        self.qdim = 2

    def apply(self, operation, wires, par):
        """
        Apply the gates.
        """
        # check with different operations
        operation_class = self._operation_map[operation]
        if issubclass(operation_class, SingleQuditOperation):
            l_obj, qdim = operation_class.qudit_operator(par)

            # qdim is only non zero if the load gate is implied.
            # so only in this case we will change it.
            if qdim:
                self.qdim = qdim
            self.job_payload["experiment_0"]["instructions"].append(l_obj)
        else:
            raise NotImplementedError()

    def expval(self, observable, wires, par):
        """
        Retrieve the requested observable expectation value.
        """

        try:
            if self.job_id is None:
                self.sample(observable, wires, par)
            if self.check_job_status() != "DONE":
                return "Job_not_done"
            shots = self.sample(observable, wires, par)
            return shots.mean()
        except ValueError as exc:
            raise NotImplementedError() from exc

    def var(self, observable, wires, par):
        """
        Retrieve the requested observable variance.
        """

        try:
            if self.job_id is None:
                self.sample(observable, wires, par)
            if self.check_job_status() != "DONE":
                return "Job_not_done"
            shots = self.sample(observable, wires, par)
            return shots.var()
        except ValueError as exc:
            raise NotImplementedError() from exc

    def sample(self, observable, wires, par):
        """
        Retrieve the requested observable expectation value.
        """

        observable_class = self._observable_map[observable]
        if issubclass(observable_class, SingleQuditObservable):

            # submit the job
            if self.job_id is None:
                m_obj = ("measure", [0], [])
                url = self.url_prefix + "post_job/"
                self.job_payload["experiment_0"]["instructions"].append(m_obj)
                job_response = requests.post(
                    url,
                    data={
                        "json": json.dumps(self.job_payload),
                        "username": self.username,
                        "password": self.password,
                    },
                )

                self.job_id = (job_response.json())["job_id"]
                if self.blocking is True:
                    self.wait_till_done()
                else:
                    return self.job_id

            if self.blocking is True:
                self.wait_till_done()
            elif self.check_job_status() != "DONE":
                return self.job_id
            # obtain the job result
            result_payload = {"job_id": self.job_id}
            url = self.url_prefix + "get_job_result/"

            result_response = requests.get(
                url,
                params={
                    "json": json.dumps(result_payload),
                    "username": self.username,
                    "password": self.password,
                },
            )
            results_dict = json.loads(result_response.text)
            shots = results_dict["results"][0]["data"]["memory"]
            shots = np.array([int(shot) for shot in shots])

            # and give back the appropiate observable.
            shots = observable_class.qudit_operator(shots, self.qdim)
            return shots
        raise NotImplementedError()

    def reset(self):
        self.qdim = 2
        self.job_id = None
        self.job_payload = None
