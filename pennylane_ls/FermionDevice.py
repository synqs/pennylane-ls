# we always import NumPy directly
import numpy as np
import scipy

from pennylane import Device, DeviceError
from pennylane.operation import Observable

from collections import OrderedDict

# observables
from .FermionOps import ParticleNumber

# operations
from .FermionOps import Load, HartreeFock, Hop, Inter, Phase, PauliZ, Identity

# classes
from .FermionOps import FermionObservable, FermionOperation

# operations for local devices
import requests
import json
import time


class FermionDevice(Device):
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

    def __init__(
        self,
        wires=8,
        shots=1,
        username=None,
        password=None,
        url=None,
        job_id=None,
        blocking=True,
    ):
        """
        The initial part.
        """
        if not wires <= 8:
            raise ValueError()
        super().__init__(wires=wires, shots=shots)
        self.username = username
        self.password = password
        self._samples = None
        self.blocking = blocking
        self.job_id = None

        if url:
            self.url_prefix = url
        else:
            self.url_prefix = "http://qsimsim.synqs.org/fermions/"

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
        return mean[wires.tolist()]

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
        return var[wires.tolist()]

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
        if issubclass(observable_class, FermionObservable):
            return self._samples
        raise NotImplementedError()

    def probability(self, wires=None):
        shots = self._samples
        if wires is not None:
            shots = shots[:, wires.tolist()]

        # np.sort(np.unique(shots, axis=0, return_counts=True, dtype=[('pattern', ), ('probability', )]), order='pattern')

        patterns, probabilities = np.unique(shots, axis=0, return_counts=True)

        patterns_decimal_repr = np.packbits(patterns.astype("int32"), axis=1)
        patterns_decimal_repr = patterns_decimal_repr.ravel()
        sort_labels = np.argsort(patterns_decimal_repr, axis=0)

        patterns = patterns[sort_labels]
        probabilities = probabilities[sort_labels]

        probabilities = probabilities / probabilities.sum()

        return OrderedDict(zip(map(tuple, patterns), probabilities))

    def pre_measure(self):
        # submit the job
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

        # job_id = (job_response.json())["job_id"]
        self.job_id = (job_response.json())["job_id"]
        if self.blocking == True:
            self.wait_till_done(self.job_id)
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
        out = np.zeros((self.shots, num_obs))
        for i1 in np.arange(self.shots):
            temp = results[i1].split()
            for i2 in np.arange(num_obs):
                out[i1, i2] = int(temp[i2])
        self._samples = out

    @property
    def operations(self):
        return set(self._operation_map.keys())

    @property
    def observables(self):
        return set(self._observable_map.keys())

    def reset(self):
        self._samples = None
        self.job_id = None
