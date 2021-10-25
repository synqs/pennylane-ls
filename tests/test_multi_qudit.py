import unittest

import pennylane as qml
from pennylane_ls import *
import numpy as np


class TestMultiQuditDevice(unittest.TestCase):
    def setUp(self):
        self.username = "synqs_test"
        self.password = "Cm2TXfRmXennMQ5"
        self.testDevice = qml.device(
            "synqs.mqs",
            shots=50,
            username=self.username,
            password=self.password,
            blocking=True,
        )

    def test_creation(self):
        """
        Test the creation of the Device
        """
        testDevice = qml.device("synqs.mqs")
        self.assertEqual(
            testDevice.operations, {"LxLy", "LzLz", "load", "rLx", "rLz", "rLz2"}
        )

    def test_rX_gate(self):
        """
        Test the rX gate
        """

        @qml.qnode(self.testDevice)
        def quantum_circuit():
            load(50, wires=0)
            rLx(np.pi, wires=0)
            return qml.expval(SingleQuditOps.Z(0))

        res = quantum_circuit()
        self.assertEqual(int(res), 50)
