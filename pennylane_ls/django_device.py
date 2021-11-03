"""
Define the base class for communication with the Django API as laid out for
`labscript-qc`
"""

from pennylane import Device


class DjangoDevice(Device):
    """
    The base class for all devices that call to an external server.
    """

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
        super().__init__(wires=1, shots=shots)
        self.username = username
        self.password = password
        self.blocking = blocking
        self.job_id = job_id
        self.url_prefix = url
        self.job_payload = {}
