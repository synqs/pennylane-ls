# we always import NumPy directly
import numpy as np
import scipy

from pennylane import Device
from pennylane.operation import Observable

# operations for remote devices
from .SingleQuditOps import Lz

import requests
import json

class MultiQuditDevice(Device):
    ## Define operation map for the experiment
    _operation_map = {
        "rLx": 'rLx',
        "rLz": 'rLz',
        "rLz2": 'rLz2',
        "XY": 'XY',
        "ZZ": 'ZZ',
    }

    name = "Multi Qudit Quantum Simulator plugin"
    pennylane_requires = ">=0.16.0"
    version = '0.0.1'
    author = "Fred Jendrzejewski"

    short_name = "synqs.sqs"

    _observable_map = {
        'Lz': Lz
    }

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
            returns_probs=True,
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

        observable_class = self._observable_map[observable]
        if issubclass(observable_class, Observable):

            # submit the job
            m_obj = ('measure', [wires[0]], [])
            url= self.url_prefix + "post_job/"
            self.job_payload['experiment_0']['instructions'].append(m_obj)
            job_response = requests.post(url, data={'json':json.dumps(self.job_payload),
                                                         'username': self.username,'password':self.password})

            job_id = (job_response.json())['job_id']

            # obtain the job result
            result_payload = {'job_id': job_id}
            url= self.url_prefix + "get_job_result/"

            result_response = requests.get(url, params={'json':json.dumps(result_payload),
                                                        'username': self.username,'password':self.password})
            results_dict = json.loads(result_response.text)
            shots = results_dict["results"][0]['data']['memory']
            shots = np.array([int(shot) for shot in shots])
            return shots.mean()
        raise NotImplementedError()

    def sample(self, observable, wires, par):
        """
        Retrieve the requested observable expectation value.
        """

        observable_class = self._observable_map[observable]
        if issubclass(observable_class, Observable):

            # submit the job
            m_obj = ('measure', [0], [])
            url= self.url_prefix + "post_job/"
            self.job_payload['experiment_0']['instructions'].append(m_obj)
            job_response = requests.post(url, data={'json':json.dumps(self.job_payload),
                                                         'username': self.username,'password':self.password})

            job_id = (job_response.json())['job_id']

            # obtain the job result
            result_payload = {'job_id': job_id}
            url= self.url_prefix + "get_job_result/"

            result_response = requests.get(url, params={'json':json.dumps(result_payload),
                                                        'username': self.username,'password':self.password})
            results_dict = json.loads(result_response.text)
            shots = results_dict["results"][0]['data']['memory']
            return shots
        raise NotImplementedError()

    @property
    def operations(self):
        return set(self._operation_map.keys())

    @property
    def observables(self):
        return set(self._observable_map.keys())

    def reset(self):
        pass
