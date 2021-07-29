# we always import NumPy directly
import numpy as np
import scipy

from pennylane import Device, DeviceError
from pennylane.operation import Observable

# observables
from .FermionOps import ParticleNumber

# operations
from .FermionOps import Load, HartreeFock, Hop, Inter, Phase, PauliZ

# classes
from .FermionOps import FermionObservable, FermionOperation

# operations for local devices
import requests
import json

class FermionDevice(Device):
    ## Define operation map for the experiment
    _operation_map = {
        'Load': Load,
        'Hop': Hop,
        'Tunneling': Hop,
        'Inter':Inter,
        'OnSiteInteraction':Inter,
        'Phase':Phase,
        'ChemicalPotential':Phase,
        'HartreeFock':HartreeFock
    }

    name = "Fermion Quantum Simulator Simulator plugin"
    pennylane_requires = ">=0.16.0"
    version = '0.2.0'
    author = "Vladimir and Donald"

    short_name = "synqs.ls"

    _observable_map = {
        'ParticleNumber': ParticleNumber,
        'PauliZ': PauliZ,
    }

    def __init__(self, wires=8, shots=1, username=None, password=None):
        """
        The initial part.
        """
        if not wires <= 8:
            raise ValueError()
        super().__init__(wires=wires,shots=shots)
        self.username = username
        self.password = password
        self.url_prefix = "http://qsimsim.synqs.org/fermions/"
        self._samples = None

    def pre_apply(self):
        self.reset()
        self.job_payload = {
        'experiment_0': {
            'instructions': [],
            'num_wires': 1,
            'shots': self.shots
            },
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
                self.job_payload['experiment_0']['instructions'].append(l_obj_element)
        else:
            raise NotImplementedError()

    def expval(self, observable=None, wires=None, par=None):
        """
        Retrieve the requested observable expectation value.
        """
        shots = self.sample(observable, wires, par)
        if self._observable_map[observable] == PauliZ:
            shots = np.ones(shots.shape) - 2*shots
        mean = np.mean(shots, axis=0)
        return sum(mean[wires.tolist()])

    def var(self, observable=None, wires=None, par=None):
        """
        Retrieve the requested observable variance.
        """
        shots = self.sample(observable, wires, par)
        if self._observable_map[observable] == PauliZ:
            shots = np.ones(shots.shape) - 2*shots
        var = np.var(shots, axis=0)
        return sum(var[wires.tolist()])

    def sample(self, observable, wires, par):
        """
        Retrieve the requested observable expectation value.
        """
        observable_class = self._observable_map[observable]
        if issubclass(observable_class, FermionObservable):
            return self._samples
        raise NotImplementedError()

    def pre_measure(self):
        # submit the job
        wires = self.wires
        for wire in wires:
            m_obj = ('measure', [wire], [])
            self.job_payload['experiment_0']['instructions'].append(m_obj)
        url= self.url_prefix + "post_job/"
        job_response = requests.post(url, data={'json':json.dumps(self.job_payload),
                                                     'username': self.username,'password':self.password})

        job_id = (job_response.json())['job_id']

        # obtain the job result
        result_payload = {'job_id': job_id}
        url= self.url_prefix + "get_job_result/"

        result_response = requests.get(url, params={'json':json.dumps(result_payload),
                                                    'username': self.username,'password':self.password})
        results_dict = json.loads(result_response.text)
        if "results" not in results_dict:
            raise DeviceError(result_response.text)
        results = results_dict["results"][0]['data']['memory']

        num_obs = len(wires)
        out = np.zeros((self.shots,num_obs))
        for i1 in np.arange(self.shots):
            temp = results[i1].split()
            for i2 in np.arange(num_obs):
                out[i1,i2] = int(temp[i2])
        self._samples = out

    @property
    def operations(self):
        return set(self._operation_map.keys())

    @property
    def observables(self):
        return set(self._observable_map.keys())

    def reset(self):
        self._samples = None
