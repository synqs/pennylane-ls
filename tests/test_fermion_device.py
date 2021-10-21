import unittest

import pennylane as qml
from pennylane_ls import *
import numpy as np


class TestFermionDevice(unittest.TestCase):
    def setUp(self):
        self.username = "synqs_test"
        self.password = "Cm2TXfRmXennMQ5"
        self.testDevice = qml.device(
            "synqs.fs",
            shots=50,
            username=self.username,
            password=self.password,
            blocking=True,
        )

    def test_creation(self):
        testDevice = qml.device("synqs.fs")
        self.assertEqual(
            testDevice.operations,
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
        testDevice = qml.device(
            "synqs.fs",
            shots=50,
            username=self.username,
            password=self.password,
            blocking=False,
        )
        self.assertEqual(
            testDevice.operations,
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

        @qml.qnode(self.testDevice)
        def simple_loading():
            """
            The circuit that simulates the experiments.

            theta ... angle of the hopping
            """
            # load atoms
            FermionOps.Load(wires=0)
            FermionOps.Load(wires=1)

            obs = FermionOps.ParticleNumber([0, 1, 2, 3])
            return qml.expval(obs)

        res = simple_loading()
        self.assertListEqual(list(res), [1.0, 1.0, 0.0, 0.0])
