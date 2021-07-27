import abc

from pennylane.operation import Operation, AnyWires, AllWires
from pennylane.operation import Observable
import numpy as np

class FermionOperation(Operation):

    @classmethod
    @abc.abstractmethod
    def fermion_operator(cls, wires,par):
        '''the function that transforms the received samples into the appropiate
        operation

        Args:
            par: parameter for the gate
        '''
        raise NotImplementedError()

class FermionObservable(Observable):

    @classmethod
    @abc.abstractmethod
    def fermion_operator(cls,samples):
        '''the function that transforms the received samples into the appropiate
        observable

        Args:
            samples: a numpy array of samples
        '''
        raise NotImplementedError()

class load(FermionOperation):
    """The load operation"""
    num_params = 0
    num_wires = 1
    par_domain = None

    grad_method = None
    grad_recipe = None

    @classmethod
    def fermion_operator(cls, wires,par):
        l_obj = ('load', wires.tolist(), [])
        return l_obj

class hop(FermionOperation):
    """The hop operation"""
    num_params = 1
    num_wires = 4
    par_domain = 'R'

    grad_method = None
    grad_recipe = None

    @classmethod
    def fermion_operator(cls, wires,par):
        theta = par[0];
        l_obj = ('hop', wires.tolist(), [theta%(2*np.pi)])
        return l_obj

class inter(FermionOperation):
    """The onsite-interaction operation"""
    num_params = 1
    num_wires = AllWires#AnyWires
    par_domain = 'R'

    grad_method = None
    grad_recipe = None

    @classmethod
    def fermion_operator(cls, wires,par):
        theta = par[0];
        l_obj = ('int', wires.tolist(), [theta%(2*np.pi)])
        return l_obj

class phase(FermionOperation):
    """The phase operation"""
    num_params = 1
    num_wires = 2
    par_domain = 'R'

    grad_method = None
    grad_recipe = None

    @classmethod
    def fermion_operator(cls, wires,par):
        theta = par[0];
        l_obj = ('phase', wires.tolist(), [theta%(2*np.pi)])
        return l_obj


class ParticleNumber(FermionObservable):
    """ParticleNumber observable"""
    num_params = 0
    num_wires = AnyWires
    par_domain = None


    @classmethod
    def fermion_operator(cls,samples):
        return samples
