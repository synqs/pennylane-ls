"""
Define the operations that can be applied on a multi_qudit device.
"""

from typing import List, Tuple
import abc

from pennylane.operation import Operation
from pennylane.operation import Observable
import numpy as np


class MultiQuditOperation(Operation):
    """
    A base class for all the single qudit operation that will later inherit from it.
    """

    @classmethod
    @abc.abstractmethod
    def qudit_operator(cls, par: List[float], wires: List[int]) -> Tuple:
        """the function that transforms the received samples into the appropiate
        operation

        Args:
            par: parameter for the gate
            wires: The wires onto which we should apply the gates.
        """
        raise NotImplementedError()


class MultiQuditObservable(Observable):
    """
    A base class for all the multi qudit observables that will later inherit from it.
    """

    @classmethod
    @abc.abstractmethod
    def qudit_operator(cls, samples: List[int], qdim: List[int]):
        """the function that transforms the received samples into the appropiate
        observable

        Args:
            samples: a numpy array of samples
            qdim: the dimension of the qudit we are working with
        """
        raise NotImplementedError()


## Single qudit gates
class Load(MultiQuditOperation):
    """The load operation"""

    num_params = 1
    num_wires = 1
    par_domain = "N"

    grad_method = None
    grad_recipe = None

    @classmethod
    def qudit_operator(cls, par, wires):
        l_obj = ("load", [wires[0]], par)
        qdim = par[0] + 1
        return l_obj, qdim


class RLX(MultiQuditOperation):
    """The RLX operation"""

    num_params = 1
    num_wires = 1
    par_domain = "R"

    grad_method = None
    grad_recipe = None

    @classmethod
    def qudit_operator(cls, par, wires):
        theta = par[0]

        l_obj = ("rlx", [wires[0]], [theta % (2 * np.pi)])
        return l_obj, False


class RLZ(MultiQuditOperation):
    """The RLZ operation"""

    num_params = 1
    num_wires = 1
    par_domain = "R"

    grad_method = None
    grad_recipe = None

    @classmethod
    def qudit_operator(cls, par, wires):
        theta = par[0]
        l_obj = ("rlz", [wires[0]], [theta % (2 * np.pi)])
        return l_obj, False


class RLZ2(MultiQuditOperation):
    """The RLZ2 operation"""

    num_params = 1
    num_wires = 1
    par_domain = "R"

    grad_method = None
    grad_recipe = None

    @classmethod
    def qudit_operator(cls, par, wires):
        theta = par[0]
        l_obj = ("rlz2", [wires[0]], [theta % (2 * np.pi)])
        return l_obj, False


class ID(MultiQuditOperation):
    """Identity gate"""

    num_params = 1
    num_wires = 1
    par_domain = "R"

    grad_method = None
    grad_recipe = None

    @classmethod
    def qudit_operator(cls, par, wires):
        pass


## Two qudit gates


class RLXLY(MultiQuditOperation):
    """LxLy or FlipFlop gate"""

    num_params = 1
    num_wires = 2
    par_domain = "R"

    @classmethod
    def qudit_operator(cls, par, wires):
        theta = par[0]
        l_obj = ("rlxly", [wires[0], wires[1]], [theta % (2 * np.pi)])
        return l_obj, False


class RLZLZ(MultiQuditOperation):
    """LzLz or generalized Ising gate"""

    num_params = 1
    num_wires = 2
    par_domain = "R"

    @classmethod
    def qudit_operator(cls, par, wires):
        theta = par[0]
        l_obj = ("rlzlz", [wires[0], wires[1]], [theta % (2 * np.pi)])
        return l_obj, False


## Observables
class ZObs(MultiQuditObservable):
    """Number of atoms operator"""

    num_params = 0
    num_wires = 1
    par_domain = "R"

    @classmethod
    def qudit_operator(cls, samples, qdim):
        return samples


class LZ(MultiQuditObservable):
    """Lz observable"""

    num_params = 0
    num_wires = 1
    par_domain = "R"

    @classmethod
    def qudit_operator(cls, samples, qdim):
        return samples - qdim / 2
