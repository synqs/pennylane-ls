import abc

from pennylane.operation import Operation
from pennylane.operation import Observable
import numpy as np

class SingleQuditOperation(Operation):

    @classmethod
    @abc.abstractmethod
    def qudit_operator(cls, par):
        '''the function that transforms the received samples into the appropiate
        operation

        Args:
            par: parameter for the gate
        '''
        raise NotImplementedError()

class SingleQuditObservable(Observable):

    @classmethod
    @abc.abstractmethod
    def qudit_operator(cls,samples, qdim):
        '''the function that transforms the received samples into the appropiate
        observable

        Args:
            samples: a numpy array of samples
        '''
        raise NotImplementedError()

class load(SingleQuditOperation):
    """The load operation"""
    num_params = 1
    num_wires = 1
    par_domain = 'N'

    grad_method = None
    grad_recipe = None

    @classmethod
    def qudit_operator(cls, par):
        l_obj = ('load', [0], par)
        qdim = par[0]+1
        return l_obj, qdim

class rLx(SingleQuditOperation):
    """The rLx operation"""
    num_params = 1
    num_wires = 1
    par_domain = 'R'

    grad_method = None
    grad_recipe = None

    @classmethod
    def qudit_operator(cls, par):
        theta = par[0];

        l_obj = ('rLx', [0], [theta%(2*np.pi)])
        return l_obj, False

class rLz(SingleQuditOperation):
    """The rLz operation"""
    num_params = 1
    num_wires = 1
    par_domain = 'R'

    grad_method = None
    grad_recipe = None

    @classmethod
    def qudit_operator(cls, par):
        theta = par[0];
        l_obj = ('rLz', [0], [theta%(2*np.pi)])
        return l_obj, False

class rLz2(SingleQuditOperation):
    """The rLz operation"""
    num_params = 1
    num_wires = 1
    par_domain = 'R'

    grad_method = None
    grad_recipe = None

    @classmethod
    def qudit_operator(cls, par):
        l_obj = ('rLz2', [0], par)
        return l_obj, False

class Id(SingleQuditOperation):
    """Custom gate"""
    num_params = 1
    num_wires = 1
    par_domain = 'R'

    grad_method = None
    grad_recipe = None

    @classmethod
    def qudit_operator(cls, par):
        pass

class Z(SingleQuditObservable):
    """Custom observable"""
    num_params = 0
    num_wires = 1
    par_domain = 'R'


    @classmethod
    def qudit_operator(cls,samples, qdim):
        return samples


class Lz(SingleQuditObservable):
    """Custom observable"""
    num_params = 0
    num_wires = 1
    par_domain = 'R'

    @classmethod
    def qudit_operator(cls,samples, qdim):
        return samples - qdim/2

class Lz2(SingleQuditObservable):
    """Custom observable"""
    num_params = 0
    num_wires = 1
    par_domain = 'R'

    @classmethod
    def qudit_operator(cls,samples, qdim):
        Lz = samples - qdim/2;
        return Lz**2
