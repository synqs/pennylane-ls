"""
Define the base class for communication with the Django API as laid out for
`labscript-qc`
"""

import time
import json
import requests
from pennylane import Device


class DjangoDevice(Device):
    """
    The base class for all devices that call to an external server.
    """

    _operation_map = {}
    _observable_map = {}

    # pylint: disable=R0913
    def __init__(
        self,
        url: str,
        wires=1,
        shots=1,
        username=None,
        password=None,
        job_id=None,
        blocking=True,
    ):
        """
        The initial part.
        """
        super().__init__(wires=wires, shots=shots)
        self.username = username
        self.password = password
        self.blocking = blocking
        self.job_id = job_id
        self.url_prefix = url
        self.job_payload = {}

    def check_job_status(self) -> str:
        """
        Check remotely if the job was done already.
        """
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
        job_status_detail = (status_response.json())["detail"]
        if job_status == "ERROR":
            raise SyntaxError(job_status_detail)
        return job_status

    def wait_till_done(self):
        """
        The waiting function that blocks the program
        """
        while True:
            time.sleep(2)
            job_status = self.check_job_status()
            if job_status == "DONE":
                break

    def pre_apply(self):
        """
        Set up the necessary dictonaries that will be later send to the server.
        """
        self.reset()
        self.job_payload = {
            "experiment_0": {"instructions": [], "num_wires": 1, "shots": self.shots},
        }

    @property
    def operations(self):
        return set(self._operation_map.keys())

    @property
    def observables(self):
        return set(self._observable_map.keys())
