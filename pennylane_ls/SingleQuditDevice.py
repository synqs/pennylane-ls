# we always import NumPy directly
import numpy as np
import scipy

from pennylane import Device
from pennylane.operation import Observable

# observables
from .SingleQuditOps import Lz, Lz2, Z

# operations
from .SingleQuditOps import rLx, rLz, rLz2, load

# classes
from .SingleQuditOps import SingleQuditObservable, SingleQuditOperation

# operations for local devices
import requests
import json
import time


class SingleQuditDevice(Device):
    ## Define operation map for the experiment
    _operation_map = {"rLx": rLx, "rLz": rLz, "rLz2": rLz2, "load": load}

    name = "Single Qudit Quantum Simulator Simulator plugin"
    pennylane_requires = ">=0.16.0"
    version = "0.0.1"
    author = "Fred Jendrzejewski"

    short_name = "synqs.sqs"

    _observable_map = {"Lz": Lz, "Z": Z, "Lz2": Lz2}

    def __init__(
        self,
        shots=1,
        username=None,
        url=None,
        password=None,
        job_id=None,
        blocking=True,
    ):
        """
        The initial part.
        """
        super().__init__(wires=1, shots=shots)
        self.username = username
        self.password = password
        self.blocking = blocking
        self.job_id = None
        # dimension of the qudit
        self.qdim = 2
        if url:
            self.url_prefix = url
        else:
            self.url_prefix = "http://qsimsim.synqs.org/singlequdit/"

    def pre_apply(self):
        self.reset()
        self.job_payload = {
            "experiment_0": {"instructions": [], "num_wires": 1, "shots": self.shots},
        }

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
            if self.job_id == None:
                self.sample(observable, wires, par)
            if self.check_job_status(self.job_id) != "DONE":
                return "Job_not_done"
            else:
                shots = self.sample(observable, wires, par)
                return shots.mean()
        except:
            raise NotImplementedError()

    def var(self, observable, wires, par):
        """
        Retrieve the requested observable variance.
        """

        try:
            if self.job_id == None:
                self.sample(observable, wires, par)
            if self.check_job_status(self.job_id) != "DONE":
                return "Job_not_done"
            else:
                shots = self.sample(observable, wires, par)
                return shots.var()
        except:
            raise NotImplementedError()

    def check_job_status(self, job_id):
        status_payload = {"job_id": self.job_id}
        url = self.url_prefix + "get_job_status/"
        status_response = requests.get(
            url,
            params={
                "json": json.dumps(status_payload),
                "username": self.username,
                "password": self.password,
            },
        )
        job_status = (status_response.json())["status"]
        return job_status

    def wait_till_done(self, job_id):
        while True:
            time.sleep(2)
            job_status = self.check_job_status(job_id)
            if job_status == "DONE":
                break
            else:
                pass
                # print(job_status)
        return

    def sample(self, observable, wires, par):
        """
        Retrieve the requested observable expectation value.
        """

        observable_class = self._observable_map[observable]
        if issubclass(observable_class, SingleQuditObservable):

            # submit the job
            if self.job_id == None:
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
                if self.blocking == True:
                    self.wait_till_done(self.job_id)
                else:
                    return self.job_id

            if self.blocking == True:
                self.wait_till_done(self.job_id)
            elif self.check_job_status(self.job_id) != "DONE":
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

    @property
    def operations(self):
        return set(self._operation_map.keys())

    @property
    def observables(self):
        return set(self._observable_map.keys())

    def reset(self):
        self.qdim = 2
        self.job_id = None
        self.job_payload = None
        pass
