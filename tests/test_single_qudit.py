"""
Tests for the single qudit device.
"""

import unittest
import numpy as np

import pennylane as qml
from pennylane_ls import single_qudit_ops


class TestSingleQuditDevice(unittest.TestCase):
    """
    The test case for the single qudit device.
    """

    def setUp(self):
        self.username = "synqs_test"
        self.password = "Cm2TXfRmXennMQ5"
        self.test_device = qml.device(
            "synqs.sqs",
            shots=50,
            username=self.username,
            password=self.password,
            blocking=True,
        )

    def test_creation(self):
        """
        Make sure that we can create the device.
        """
        test_device = qml.device("synqs.sqs")
        self.assertEqual(test_device.operations, {"Load", "RLX", "RLZ", "RLZ2"})

    def test_creation_with_user(self):
        """
        Test creation with username
        """
        test_device = qml.device(
            "synqs.sqs",
            shots=50,
            username=self.username,
            password=self.password,
            blocking=True,
        )
        self.assertEqual(test_device.operations, {"Load", "RLX", "RLZ", "RLZ2"})

    def test_load_gate(self):
        """
        Test the load gate
        """

        @qml.qnode(self.test_device)
        def quantum_circuit():
            single_qudit_ops.Load(50, wires=0)
            single_qudit_ops.RLX(np.pi, wires=0)
            return qml.expval(single_qudit_ops.ZObs(0))

        res = quantum_circuit()
        self.assertEqual(int(res), 50)

    def test_rX_gate(self):
        """
        Test the rX gate
        """

        @qml.qnode(self.test_device)
        def quantum_circuit():
            single_qudit_ops.Load(50, wires=0)
            single_qudit_ops.RLX(np.pi, wires=0)
            return qml.expval(single_qudit_ops.ZObs(0))

        res = quantum_circuit()
        self.assertEqual(int(res), 50)
