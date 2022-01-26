"""
Tests for the multi qudit device.
"""
import unittest
import numpy as np

import pennylane as qml
from pennylane_ls import multi_qudit_ops


class TestMultiQuditDevice(unittest.TestCase):
    """
    The test case for the multi qudit device.
    """

    def setUp(self):
        self.username = "synqs_test"
        self.password = "Cm2TXfRmXennMQ5"
        self.test_device = qml.device(
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
        test_device = qml.device("synqs.mqs")
        self.assertEqual(
            test_device.operations, {"RLXLY", "RLZLZ", "Load", "RLX", "RLZ", "RLZ2"}
        )

    def test_rX_gate(self):
        """
        Test the rX gate
        """

        @qml.qnode(self.test_device)
        def quantum_circuit():
            multi_qudit_ops.Load(50, wires=0)
            multi_qudit_ops.RLX(np.pi, wires=0)
            return qml.expval(multi_qudit_ops.ZObs(0))

        res = quantum_circuit()
        self.assertEqual(int(res), 50)
