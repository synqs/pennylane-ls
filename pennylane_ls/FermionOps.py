import abc

from pennylane.wires import Wires
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

class Load(FermionOperation):
    """The load preparation"""
    num_params = 0
    num_wires = 1
    par_domain = None

    grad_method = None
    grad_recipe = None

    @classmethod
    def fermion_operator(cls, wires, par):
        l_obj = ('load', wires.tolist(), [])
        return l_obj

class HartreeFock(FermionOperation):
    """The Hartree Fock preparation"""
    num_params = 2
    num_wires = AllWires
    par_domain = 'I'

    @classmethod
    def fermion_operator(cls, wires, par):
        nalpha, nbeta = par
        l_obj = list()
        for idx, wire in enumerate(wires):
            if idx % 2 == 0 and idx//2 < nalpha:
                l_obj.append(Load.fermion_operator(Wires(wire), None))
            elif (idx-1) % 2 == 0 and (idx-1)//2 < nbeta:
                l_obj.append(Load.fermion_operator(Wires(wire), None))
        return l_obj

class Hop(FermionOperation):
    """The hop operation"""
    num_params = 1
    num_wires = 4
    par_domain = 'R'

    grad_method = None
    grad_recipe = None

    @classmethod
    def fermion_operator(cls, wires,par):
        theta = par[0];
        l_obj = ('hop', wires.tolist(), [theta/2%(2*np.pi)])
        return l_obj

class Inter(FermionOperation):
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

class Phase(FermionOperation):
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
    def fermion_operator(cls, samples):
        return samples

class PauliZ(FermionObservable):
    """PauliZ observable

    This should return 1-2*ParticleNumber
    """
    num_params = 0
    num_wires = 1
    par_domain = None

    @classmethod
    def fermion_operator(cls, samples):
        return samples

class Identity(FermionObservable):
    """PauliZ observable

    This should return 1-2*ParticleNumber
    """
    num_params = 0
    num_wires = AnyWires
    par_domain = None

    @classmethod
    def fermion_operator(cls, samples):
        return samples
