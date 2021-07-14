import unittest

import pennylane as qml


class TestSingleQuditDevice(unittest.TestCase):
    def test_creation(self):
        testDevice = qml.device("synqs.sqs")
        self.assertEqual(testDevice.operations, {'load', 'rLx', 'rLz', 'rLz2'})
