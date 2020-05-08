"""
Base Framework device class
===========================

**Module name:** :mod:`plugin_name.device`

.. currentmodule:: plugin_name.device

An abstract base class for constructing Target Framework devices for PennyLane.

This should contain all the boilerplate for supporting PennyLane
from the Target Framework, making it easier to create new devices.
The abstract base class below should contain all common code required
by the Target Framework.

This abstract base class will not be used by the user. Add/delete
methods and attributes below where needed.

See https://pennylane.readthedocs.io/en/latest/API/overview.html
for an overview of how the Device class works.

Classes
-------

.. autosummary::
   FrameworkDevice

Code details
~~~~~~~~~~~~
"""
import abc
import itertools

# we always import NumPy directly
import numpy as np

from pennylane import QubitDevice, Device

from ._version import __version__


class NaLiDevice(Device):
    r"""Abstract Framework device for PennyLane.

    Args:
        wires (int): the number of modes to initialize the device in
        shots (int): Number of circuit evaluations/random samples used
            to estimate expectation values of observables.
            For simulator devices, 0 means the exact EV is returned.
        additional_option (float): as many additional arguments can be
            added as needed
    """
    name = 'KIP MaLi Experiment Framework '
    short_name = 'NaLiQC'
    pennylane_requires = '0.8.1'
    version = __version__
    author = 'Fred Jendrzejewski, Manuel Rudolph'
    ##
    _operation_map = {}
    _observable_map = {}
    _capabilities = {'backend': list(["NaLiExperiment"]),
                     'model': 'qubit'}  # it's not actually qubit but cv does not work with the new operations
    operations = {"X", "H_mb"}
    observables = {"NumberOperator"}  # NumberOperator still needs to be defined

    _operation_map = {}

    def __init__(self, boson_wires=2, fermion_wires=0, shots=11, hardware_options=None):
        super().__init__(wires=boson_wires + fermion_wires,
                         shots=shots)  # TODO: implement the fermion boson split
        self.boson_wires = boson_wires
        self.fermion_wires = fermion_wires
        self.n_wires = self.boson_wires + self.fermion_wires
        self.reset()

    def reset(self):
        """Reset the device"""
        pass

    @property
    def operations(self):
        """Get the supported set of operations.

        Returns:
            set[str]: the set of PennyLane operation names the device supports
        """
        return set(self._operation_map.keys())