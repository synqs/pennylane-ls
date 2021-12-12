"""
A device that allows us to implement operation ons a fermion tweezer experiments.
The backend is a remote simulator.
"""
import json
from collections import OrderedDict

import numpy as np
import requests

from pennylane import DeviceError


from .django_device import DjangoDevice

# observables
from .FermionOps import ParticleNumber

# operations
from .FermionOps import Load, HartreeFock, Hop, Inter, Phase, PauliZ, Identity

# classes
from .FermionOps import FermionObservable, FermionOperation


class FermionDevice(DjangoDevice):
    """
    The device that allows us to implement operation on a fermion tweezer experiments.
    The backend is a remote simulator.
    """

    ## Define operation map for the experiment
    _operation_map = {
        "Load": Load,
        "Hop": Hop,
        "Tunneling": Hop,
        "Inter": Inter,
        "OnSiteInteraction": Inter,
        "Phase": Phase,
        "ChemicalPotential": Phase,
        "HartreeFock": HartreeFock,
    }

    name = "Fermion Quantum Simulator Simulator plugin"
    pennylane_requires = ">=0.16.0"
    version = "0.2.0"
    author = "Rohit P. Bhatt, Christian Gogolin, Fred Jendrzejewski, Valentin Kasper"

    short_name = "synqs.fs"

    _observable_map = {
        "ParticleNumber": ParticleNumber,
        "PauliZ": PauliZ,
        "Identity": Identity,
    }

    # pylint: disable=R0913
    def __init__(
        self,
        wires=8,
        shots=1,
        url="http://qsimsim.synqs.org/fermions/",
        username=None,
        password=None,
        job_id=None,
        blocking=True,
    ):
        """
        The initial part.
        """

        super().__init__(
            url=url,
            wires=wires,
            shots=shots,
            username=username,
            password=password,
            blocking=blocking,
            job_id=job_id,
        )

        if not self.num_wires <= 8:
            raise ValueError("Number of wires may be at most 8")
        self._samples = None

    @classmethod
    def capabilities(cls):

        capabilities = super().capabilities().copy()
        capabilities.update(
            model="fermions",
            supports_finite_shots=True,
            supports_tensor_observables=True,
            returns_probs=False,
        )

        return capabilities

    def apply(self, operation, wires, par):
        """
        Apply the gates.
        """
        # check with different operations
        operation_class = self._operation_map[operation]
        if issubclass(operation_class, FermionOperation):
            l_obj = operation_class.fermion_operator(wires, par)
            if not isinstance(l_obj, list):
                l_obj = [l_obj]
            for l_obj_element in l_obj:
                self.job_payload["experiment_0"]["instructions"].append(l_obj_element)
        else:
            raise NotImplementedError()

    def expval(self, observable=None, wires=None, par=None):
        """
        Retrieve the requested observable expectation value.
        """
        if self._observable_map[observable] == Identity:
            return 1.0

        shots = self.sample(observable, wires, par)
        if self._observable_map[observable] == PauliZ:
            shots = np.ones(shots.shape) - 2 * shots
        mean = np.mean(shots, axis=0)
        result = mean[wires.tolist()]
        return result.item() if len(result) == 1 else result

    def var(self, observable=None, wires=None, par=None):
        """
        Retrieve the requested observable variance.
        """
        if self._observable_map[observable] == Identity:
            return 0.0

        shots = self.sample(observable, wires, par)
        if self._observable_map[observable] == PauliZ:
            shots = np.ones(shots.shape) - 2 * shots
        var = np.var(shots, axis=0)
        result = var[wires.tolist()]
        return result.item() if len(result) == 1 else result

    def sample(self, observable, wires, par):
        """
        Retrieve the requested observable sample.
        """
        observable_class = self._observable_map[observable]
        if issubclass(observable_class, FermionObservable):
            return self._samples
        raise NotImplementedError()

    def probability(self, wires=None):
        """
        Generates the probibility distribution for all observed outcomes.
        """
        # pylint: disable=R1728
        shots = self._samples
        if wires is not None:
            shots = shots[:, wires.tolist()]

        patterns, counts = np.unique(shots, axis=0, return_counts=True)

        probabilities = np.zeros(2 ** len(wires))
        denominator = counts.sum()
        for pattern, count in zip(patterns, counts):
            probability = count / denominator
            probabilities[
                sum(2 ** idx for idx, d in enumerate(pattern[::-1]) if d == 1)
            ] = probability

        patterns = [
            tuple([int(d) for d in bin(comp_state_index)[2:].zfill(len(wires))])
            for comp_state_index in range(2 ** len(wires))
        ]

        return OrderedDict(zip(patterns, probabilities))

    # pylint: disable=R1710
    def pre_measure(self):
        """
        Apply the operations that are necessary to submit the job.
        """

        wires = self.wires
        for wire in wires:
            m_obj = ("measure", [wire], [])
            self.job_payload["experiment_0"]["instructions"].append(m_obj)
        url = self.url_prefix + "post_job/"
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
        if "results" not in results_dict:
            raise DeviceError(result_response.text)
        results = results_dict["results"][0]["data"]["memory"]

        num_obs = len(wires)
        out = np.zeros((self.shots, num_obs), dtype=int)
        for ind_1 in np.arange(self.shots):
            temp = results[ind_1].split()
            for ind_2 in np.arange(num_obs):
                out[ind_1, ind_2] = int(temp[ind_2])
        self._samples = out

    def reset(self):
        self._samples = None
        self.job_id = None
