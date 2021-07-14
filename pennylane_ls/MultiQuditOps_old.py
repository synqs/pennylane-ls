import abc

from pennylane.operation import Operation
from pennylane.operation import Observable
import numpy as np

class MultiQuditObservable(Observable):

    @classmethod
    @abc.abstractmethod
    def qudit_operator(cls, samples, qdim):
        '''the function that transforms the received samples into the appropiate
        observable

        Args:
            samples: a numpy array of samples
        '''
        raise NotImplementedError()

class load(Operation):
    """The load operation"""
    num_params = 1
    num_wires = 1
    par_domain = 'N'

    grad_method = None
    grad_recipe = None

class rLx(Operation):
    """The rLx operation"""
    num_params = 1
    num_wires = 1
    par_domain = 'R'

    grad_method = None
    grad_recipe = None


class rLz(Operation):
    """The rLz operation"""
    num_params = 1
    num_wires = 1
    par_domain = 'R'

    grad_method = None
    grad_recipe = None

class rLz2(Operation):
    """The rLz operation"""
    num_params = 1
    num_wires = 1
    par_domain = 'R'

    grad_method = None
    grad_recipe = None

class LxLy(Operation):
    """Custom gate"""
    num_params = 1
    num_wires = 2
    par_domain = 'R'

    grad_method = None
    grad_recipe = None

class LzLz(Operation):
    """Custom gate"""
    num_params = 1
    num_wires = 2
    par_domain = 'R'

    grad_method = None
    grad_recipe = None

class Id(Operation):
    """Custom gate"""
    num_params = 1
    num_wires = 1
    par_domain = 'R'

    grad_method = None
    grad_recipe = None

class Lz(Observable):
    """Custom observable"""
    num_params = 0
    num_wires = 1
    par_domain = 'R'

class Z(MultiQuditObservable):
    """Custom observable"""
    num_params = 0
    num_wires = 1
    par_domain = 'R'

    @classmethod
    def qudit_operator(cls,samples, qdim):
        return samples
