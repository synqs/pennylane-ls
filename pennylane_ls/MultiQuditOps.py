import abc

from pennylane.operation import Operation
from pennylane.operation import Observable
import numpy as np

class MultiQuditOperation(Operation):

    @classmethod
    @abc.abstractmethod
    def qudit_operator(cls, par, wires):
        '''the function that transforms the received samples into the appropiate
        operation

        Args:
            par: parameter for the gate
        '''
        raise NotImplementedError()

class MultiQuditObservable(Observable):

    @classmethod
    @abc.abstractmethod
    def qudit_operator(cls,samples, qdim):
        '''the function that transforms the received samples into the appropiate
        observable

        Args:
            samples: a numpy array of samples
        '''
        raise NotImplementedError()

## Single qudit gates

class load(MultiQuditOperation):
    """The load operation"""
    num_params = 1
    num_wires = 1
    par_domain = 'N'

    grad_method = None
    grad_recipe = None

    @classmethod
    def qudit_operator(cls, par, wires):
        l_obj = ('load', [wires[0]], par)
        qdim = par[0]+1
        return l_obj, qdim

class rLx(MultiQuditOperation):
    """The rLx operation"""
    num_params = 1
    num_wires = 1
    par_domain = 'R'

    grad_method = None
    grad_recipe = None

    @classmethod
    def qudit_operator(cls, par, wires):
        theta = par[0]

        l_obj = ('rLx', [wires[0]], [theta%(2*np.pi)])
        return l_obj, False

class rLz(MultiQuditOperation):
    """The rLz operation"""
    num_params = 1
    num_wires = 1
    par_domain = 'R'

    grad_method = None
    grad_recipe = None

    @classmethod
    def qudit_operator(cls, par, wires):
        theta = par[0]
        l_obj = ('rLz', [wires[0]], [theta%(2*np.pi)])
        return l_obj, False

class rLz2(MultiQuditOperation):
    """The rLz operation"""
    num_params = 1
    num_wires = 1
    par_domain = 'R'

    grad_method = None
    grad_recipe = None

    @classmethod
    def qudit_operator(cls, par, wires):
        theta = par[0]
        l_obj = ('rLz2', [wires[0]], [theta%(2*np.pi)])
        return l_obj, False

class Id(MultiQuditOperation):
    """Identity gate"""
    num_params = 1
    num_wires = 1
    par_domain = 'R'

    grad_method = None
    grad_recipe = None

    @classmethod
    def qudit_operator(cls, par, wires):
        pass

## Two qudit gates

class LxLy(MultiQuditOperation):
    """LxLy or FlipFlop gate"""
    num_params = 1
    num_wires = 2
    par_domain = 'R'

    @classmethod
    def qudit_operator(cls, par, wires):
        theta = par[0]
        l_obj = ('LxLy', [wires[0],wires[1]], [theta%(2*np.pi)])
        return l_obj, False

class LzLz(MultiQuditOperation):
    """LzLz or generalized Ising gate"""
    num_params = 1
    num_wires = 2
    par_domain = 'R'

    @classmethod
    def qudit_operator(cls, par, wires):
        theta = par[0]
        l_obj = ('LzLz', [wires[0],wires[1]], [theta%(2*np.pi)])
        return l_obj, False

## Observables

class Z(MultiQuditObservable):
    """Number of atoms operator"""
    num_params = 0
    num_wires = 1
    par_domain = 'R'

    @classmethod
    def qudit_operator(cls,samples, qdim):
        return samples

class Lz(MultiQuditObservable):
    """Lz observable"""
    num_params = 0
    num_wires = 1
    par_domain = 'R'

    @classmethod
    def qudit_operator(cls,samples, qdim):
        return samples - qdim/2
