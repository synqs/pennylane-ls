"""
Define the operations that can be applied on a single_qudit device.
"""

from typing import List, Tuple
import abc

from pennylane.operation import Operation
from pennylane.operation import Observable
import numpy as np


class SingleQuditOperation(Operation):
    """
    A base class for all the single qudit operation that will later inherit from it.
    """

    @classmethod
    @abc.abstractmethod
    def qudit_operator(cls, par: List[float]) -> Tuple:
        """the function that transforms the received samples into the appropiate
        operation

        Args:
            par: parameter for the gate
        """
        raise NotImplementedError()


class SingleQuditObservable(Observable):
    """
    A base class for all the single qudit observables that will later inherit from it.
    """

    @classmethod
    @abc.abstractmethod
    def qudit_operator(cls, samples: np.ndarray, qdim: List[int]):
        """the function that transforms the received samples into the appropiate
        observable

        Args:
            samples: a numpy array of samples
            qdim: the dimension of the qudit
        """
        raise NotImplementedError()


class Load(SingleQuditOperation):
    """The load operation"""

    num_params = 1
    num_wires = 1
    par_domain = "N"

    grad_method = None
    grad_recipe = None

    @classmethod
    def qudit_operator(cls, par):
        l_obj = ("load", [0], par)
        qdim = par[0] + 1
        return l_obj, qdim


class RLX(SingleQuditOperation):
    """The RLX operation"""

    num_params = 1
    num_wires = 1
    par_domain = "R"

    grad_method = None
    grad_recipe = None

    @classmethod
    def qudit_operator(cls, par):
        theta = par[0]

        l_obj = ("rlx", [0], [theta % (2 * np.pi)])
        return l_obj, False


class RLZ(SingleQuditOperation):
    """The rLz operation"""

    num_params = 1
    num_wires = 1
    par_domain = "R"

    grad_method = None
    grad_recipe = None

    @classmethod
    def qudit_operator(cls, par):
        theta = par[0]
        l_obj = ("rlz", [0], [theta % (2 * np.pi)])
        return l_obj, False


class RLZ2(SingleQuditOperation):
    """The rLz operation"""

    num_params = 1
    num_wires = 1
    par_domain = "R"

    grad_method = None
    grad_recipe = None

    @classmethod
    def qudit_operator(cls, par):
        l_obj = ("rlz2", [0], par)
        return l_obj, False


class ID(SingleQuditOperation):
    """Custom gate"""

    num_params = 1
    num_wires = 1
    par_domain = "R"

    grad_method = None
    grad_recipe = None

    @classmethod
    def qudit_operator(cls, par):
        pass


class ZObs(SingleQuditObservable):
    """Custom observable"""

    num_params = 0
    num_wires = 1
    par_domain = "R"

    @classmethod
    def qudit_operator(cls, samples, qdim):
        return samples


class LZ(SingleQuditObservable):
    """Custom observable"""

    num_params = 0
    num_wires = 1
    par_domain = "R"

    @classmethod
    def qudit_operator(cls, samples, qdim):
        return samples - qdim / 2


class LZ2(SingleQuditObservable):
    """Custom observable"""

    num_params = 0
    num_wires = 1
    par_domain = "R"

    @classmethod
    def qudit_operator(cls, samples, qdim):
        lz = samples - qdim / 2
        return lz ** 2
