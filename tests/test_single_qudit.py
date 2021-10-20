import unittest

import pennylane as qml


class TestSingleQuditDevice(unittest.TestCase):
    def test_creation(self):
        testDevice = qml.device("synqs.sqs")
        self.assertEqual(testDevice.operations, {'load', 'rLx', 'rLz', 'rLz2'})

    def test_creation_with_user(self):
        '''
        Test creation with username
        '''
        username = 'synqs_test'
        password = 'Cm2TXfRmXennMQ5'
        testDevice = qml.device("synqs.sqs", shots = 50, username = username, password = password, blocking=True)
        self.assertEqual(testDevice.operations, {'load', 'rLx', 'rLz', 'rLz2'})
