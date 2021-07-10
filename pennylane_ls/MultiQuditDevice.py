# we always import NumPy directly
import numpy as np
import scipy

from pennylane import Device
from pennylane import QubitDevice
from pennylane.operation import Observable
from .MultiQuditOps import Lz, rLx, rLz, rLz2, XY, ZZ

# operations for remote devices

import requests
import json

class MultiQuditDevice(Device):
    ## Define operation map for the experiment

    name = "Multi Qudit Quantum Simulator plugin"
    pennylane_requires = ">=0.16.0"
    version = '0.0.1'
    author = "Fred Jendrzejewski"

    short_name = "synqs.sqs"

    observables = {"Lz"}
    operations  = {"rLz", "rLx", "RX", "CNOT", "ZZ", "XY"}

    _observable_map = {
        "Lz": Lz
    }

    _operation_map = {
        "rLx": rLx,
        "rLz": rLz,
        "rLz2": rLz2,
        "XY": XY,
        "ZZ": ZZ,
    }

    @property
    def operations(self):
        return set(self._operation_map.keys())

    @property
    def observables(self):
        return set(self._observable_map.keys())

    def __init__(self, wires=1,shots=1, username = None, password = None):
        """
        The initial part.
        """
        super().__init__(wires=wires,shots=shots)
        self.username = username
        self.password = password
        self.url_prefix = "http://qsimsim.synqs.org/multiqudit/"

    @classmethod
    def capabilities(cls):

        capabilities = super().capabilities().copy()
        capabilities.update(
            model="qudit",
            supports_finite_shots=True,
            supports_tensor_observables=True,
            #returns_probs=True,
        )
        
        return capabilities

    def pre_apply(self):
        self.reset()
        self.job_payload = {
        'experiment_0': {
            'instructions': [],
            'num_wires': len(self.wires),
            'shots': self.shots
            },
        }

    def apply(self, operation, wires, par):
        """
        The initial part.
        """
        # check with different operations ##
        if par:
            l_obj = (operation, wires.labels, par)
            self.job_payload['experiment_0']['instructions'].append(l_obj)
        else:
            l_obj = (operation, wires.labels, [])
            self.job_payload['experiment_0']['instructions'].append(l_obj)

    def expval(self, observable, wires, par):
        """
        Retrieve the requested observable expectation value.
        """
        try:
            shots = self.sample(observable, wires, par)
            return np.mean(shots, axis=0)
        except:
            raise NotImplementedError()
        #raise NotImplementedError()

    def sample(self, observable, wires, par):
        """
        Retrieve the requested observable expectation value.
        """
        # observable_class = self._observable_map[observable]
        # if issubclass(observable_class, Observable):

        # submit the job
        wires = wires if isinstance(wires, list) else [wires]
        for position, name in enumerate(wires):
            m_obj = ('measure', [name.labels[0]], [])
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
        out     = np.zeros((self.shots,num_obs))
        for i1 in np.arange(self.shots):
            temp = results[i1].split()
            for i2 in np.arange(num_obs):
                out[i1,i2] = int(temp[i2])
        return out
        #raise NotImplementedError()

    def reset(self):
        pass
