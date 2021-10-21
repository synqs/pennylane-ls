import unittest

import pennylane as qml
from pennylane_ls import *
import numpy as np


class TestSingleQuditDevice(unittest.TestCase):
    def setUp(self):
        self.username = "synqs_test"
        self.password = "Cm2TXfRmXennMQ5"
        self.testDevice = qml.device(
            "synqs.sqs",
            shots=50,
            username=self.username,
            password=self.password,
            blocking=True,
        )

    def test_creation(self):
        testDevice = qml.device("synqs.sqs")
        self.assertEqual(testDevice.operations, {"load", "rLx", "rLz", "rLz2"})

    def test_creation_with_user(self):
        """
        Test creation with username
        """
        testDevice = qml.device(
            "synqs.sqs",
            shots=50,
            username=self.username,
            password=self.password,
            blocking=True,
        )
        self.assertEqual(testDevice.operations, {"load", "rLx", "rLz", "rLz2"})

    def test_load_gate(self):
        """
        Test the load gate
        """

        @qml.qnode(self.testDevice)
        def quantum_circuit():
            load(50, wires=0)
            rLx(np.pi, wires=0)
            return qml.expval(SingleQuditOps.Z(0))

        res = quantum_circuit()
        self.assertEqual(int(res), 50)

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
