# we always import NumPy directly
import numpy as np
import scipy

from pennylane import Device
from pennylane.operation import Observable

# observables
from .FermionOps import ParticleNumber

# operations
from .FermionOps import load, hop, inter, phase

# classes
from .FermionOps import FermionObservable, FermionOperation

# operations for local devices
import requests
import json

class FermionDevice(Device):
    ## Define operation map for the experiment
    _operation_map = {
        'load': load,
        'hop': hop,
        'inter':inter,
        'phase':phase,
    }

    name = "Fermion Quantum Simulator Simulator plugin"
    pennylane_requires = ">=0.16.0"
    version = '0.0.1'
    author = "Vladimir and Donald"

    short_name = "synqs.fqe"

    _observable_map = {
        'ParticleNumber': ParticleNumber,
    }

    def __init__(self, shots=1, username = None, password = None):
        """
        The initial part.
        """
        super().__init__(wires=8,shots=shots)
        self.username = username
        self.password = password
        self.url_prefix = "http://qsimsim.synqs.org/fermions/"

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
            l_obj = operation_class.fermion_operator(wires,par)

            self.job_payload['experiment_0']['instructions'].append(l_obj)
        else:
            raise NotImplementedError()

    def expval(self,  observable=None, wires=None, par=None):
        """
        Retrieve the requested observable expectation value.
        """
        try:
            shots = self.sample(observable, wires, par)
            return np.mean(shots, axis=0)
        except:
            raise NotImplementedError()

    def var(self, observable=None, wires=None, par=None):
        """
        Retrieve the requested observable variance.
        """
        try:
            shots = self.sample(observable, wires, par)
            return np.var(shots, axis=0)
        except:
            raise NotImplementedError()

    def sample(self, observable, wires, par):
        """
        Retrieve the requested observable expectation value.
        """
        observable_class = self._observable_map[observable]
        if issubclass(observable_class, FermionObservable):
            # submit the job
            wires = wires.tolist()
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
            results = results_dict["results"][0]['data']['memory']

            num_obs = len(wires)
            out = np.zeros((self.shots,num_obs))
            for i1 in np.arange(self.shots):
                temp = results[i1].split()
                for i2 in np.arange(num_obs):
                    out[i1,i2] = int(temp[i2])
            return out
        raise NotImplementedError()

    @property
    def operations(self):
        return set(self._operation_map.keys())

    @property
    def observables(self):
        return set(self._observable_map.keys())

    def reset(self):
        pass
