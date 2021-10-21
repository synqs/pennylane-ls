import unittest

import pennylane as qml


class TestMultiQuditDevice(unittest.TestCase):
    def test_creation(self):
        testDevice = qml.device("synqs.mqs")
        self.assertEqual(
            testDevice.operations, {"LxLy", "LzLz", "load", "rLx", "rLz", "rLz2"}
        )
