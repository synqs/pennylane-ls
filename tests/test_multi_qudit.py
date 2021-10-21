import unittest

import pennylane as qml


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
        testDevice = qml.device("synqs.mqs")
        self.assertEqual(
            testDevice.operations, {"LxLy", "LzLz", "load", "rLx", "rLz", "rLz2"}
        )
