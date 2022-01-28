"""
Tests for the femrion device.
"""
import unittest
import numpy as np
import pennylane as qml

from pennylane_ls import fermion_ops


class TestFermionDevice(unittest.TestCase):
    """
    The test case for the fermion device.
    """

    def setUp(self):
        self.username = "synqs_test"
        self.password = "Cm2TXfRmXennMQ5"
        self.test_device = qml.device(
            "synqs.fs",
            shots=50,
            username=self.username,
            password=self.password,
            blocking=True,
        )

    def test_creation(self):
        """
        Test that it is possible to create the device.
        """
        test_device = qml.device("synqs.fs")
        self.assertEqual(
            test_device.operations,
            {
                "ChemicalPotential",
                "HartreeFock",
                "Hop",
                "Inter",
                "Load",
                "OnSiteInteraction",
                "Phase",
                "Tunneling",
            },
        )

    def test_creation_with_user(self):
        """
        Test creation with username
        """
        test_device = qml.device(
            "synqs.fs",
            shots=50,
            username=self.username,
            password=self.password,
            blocking=False,
        )
        self.assertEqual(
            test_device.operations,
            {
                "ChemicalPotential",
                "HartreeFock",
                "Hop",
                "Inter",
                "Load",
                "OnSiteInteraction",
                "Phase",
                "Tunneling",
            },
        )

    def test_load_gate(self):
        """
        Test the load gate
        """

        @qml.qnode(self.test_device)
        def simple_loading():
            """
            The circuit that simulates the experiments.

            theta ... angle of the hopping
            """
            # load atoms
            fermion_ops.Load(wires=0)
            fermion_ops.Load(wires=1)

            obs = fermion_ops.ParticleNumber([0, 1, 2, 3])
            return qml.expval(obs)

        res = simple_loading()
        self.assertListEqual(list(res), [1.0, 1.0, 0.0, 0.0])

    def test_hop_gate(self):
        """
        Test the hopping gate
        """

        @qml.qnode(self.test_device)
        def simple_hopping():
            """
            The circuit that simulates the experiments.

            theta ... angle of the hopping
            """
            # load atoms
            fermion_ops.Load(wires=0)
            fermion_ops.Load(wires=1)
            fermion_ops.Hop(np.pi, wires=[0, 1, 2, 3])
            obs = fermion_ops.ParticleNumber([0, 1, 2, 3])
            return qml.expval(obs)

        res = simple_hopping()
        self.assertListEqual(list(res), [0.0, 0.0, 1.0, 1.0])

    def test_probs(self):
        """
        Test the probs gate
        """

        @qml.qnode(self.test_device)
        def simple_hopping():
            """
            The circuit that simulates the experiments.

            theta ... angle of the hopping
            """
            # load atoms
            fermion_ops.Load(wires=0)
            fermion_ops.Load(wires=1)
            fermion_ops.Hop(np.pi, wires=[0, 1, 2, 3])
            fermion_ops.ParticleNumber([0, 1, 2, 3])
            return qml.probs(wires=[3])

        res = simple_hopping()
        self.assertListEqual(list(res), [0.0, 1.0])

    def test_var(self):
        """
        Test that the variance is properly defined.
        """

        @qml.qnode(self.test_device)
        def simple_hopping():
            """
            The circuit that simulates the experiments.

            theta ... angle of the hopping
            """
            # load atoms
            fermion_ops.Load(wires=0)
            fermion_ops.Load(wires=1)
            fermion_ops.Hop(np.pi, wires=[0, 1, 2, 3])
            obs = fermion_ops.ParticleNumber([0, 1, 2, 3])
            return qml.var(obs)

        res = simple_hopping()
        self.assertListEqual(list(res), [0.0, 0.0, 0.0, 0.0])
