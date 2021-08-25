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
    """The load preparation

    Loads one fermionic particle into a wire.

    Args:
        arg1 (int): number of the wire

    **Example**

    FermionicDevice = FermionDevice(shots = 5, username = username, password = password)

    @qml.qnode(FermionicDevice)
    def quantum_circuit(alpha=0):
        Load(wires = 0)
        Load(wires = 3)
        return qml.sample(ParticleNumber(wires=FermionicDevice.wires))

    """
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
    """The Hartree Fock preparation

        Loads one fermionic particle into a wire.

    Args:
        arg1 (int): number of the wire

    **Example**

    FermionicDevice = FermionDevice(shots = 5, username = username, password = password)

    @qml.qnode(FermionicDevice)
    def quantum_circuit(alpha=0):
        Load(wires = 0)
        Load(wires = 3)
        return qml.sample(ParticleNumber(wires=FermionicDevice.wires))

    """
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
    """The hop operation
    
        One fermionic particle moves from one wire to another wire.

    Args:
        arg1 (int): number of the wire

    **Example**

    FermionicDevice = FermionDevice(shots = 5, username = username, password = password)

    @qml.qnode(FermionicDevice)
    def quantum_circuit(alpha=0):
        Load(wires = 0)
        Hop.
        return qml.sample(ParticleNumber(wires=FermionicDevice.wires))

    """

    num_params = 1
    num_wires = 4
    par_domain = 'R'

    grad_method = None
    grad_recipe = None

    @classmethod
    def fermion_operator(cls, wires,par):
        theta = par[0]
        l_obj = ('hop', wires.tolist(), [theta/2%(2*np.pi)])
        return l_obj

class Inter(FermionOperation):
    """The interaction of fermionic modes
 
        fermionic particle interact with each other

    Args:
        arg1 (int): number of the wire

    **Example**

    FermionicDevice = FermionDevice(shots = 5, username = username, password = password)

    @qml.qnode(FermionicDevice)
    def quantum_circuit(alpha=0):
        Load(wires = 0)
        Load(wires = 3)
        return qml.sample(ParticleNumber(wires=FermionicDevice.wires))

    """

    num_params = 1
    num_wires = AllWires #AllWires#AnyWires
    par_domain = 'R'

    grad_method = None
    grad_recipe = None

    @classmethod
    def fermion_operator(cls, wires, par ):
        theta = par[0]
        l_obj = ('int', wires.tolist(), [theta%(2*np.pi)])
        return l_obj

class Phase(FermionOperation):
    """The phase operation
 
        fermionic particle interact with each other

    Args:
        arg1 (int): number of the wire

    **Example**

    FermionicDevice = FermionDevice(shots = 5, username = username, password = password)

    @qml.qnode(FermionicDevice)
    def quantum_circuit(alpha=0):
        Load(wires = 0)
        Load(wires = 3)
        return qml.sample(ParticleNumber(wires=FermionicDevice.wires))

    """

    num_params = 1
    num_wires = 2
    par_domain = 'R'

    grad_method = None
    grad_recipe = None

    @classmethod
    def fermion_operator(cls, wires,par):
        theta = par[0]
        l_obj = ('phase', wires.tolist(), [theta%(2*np.pi)])
        return l_obj


class ParticleNumber(FermionObservable):
    """ParticleNumber observable

    expectation value of particle number operator of all wires

    Args:
        arg1 (int): number of the wire

    **Example**

    FermionicDevice = FermionDevice(shots = 5, username = username, password = password)

    @qml.qnode(FermionicDevice)
    def quantum_circuit(alpha=0):
        Load(wires = 0)
        Load(wires = 3)
        return qml.sample(ParticleNumber(wires=FermionicDevice.wires))

    """

    num_params = 0
    num_wires = AnyWires
    par_domain = None

    @classmethod
    def fermion_operator(cls, samples):
        return samples

class PauliZ(FermionObservable):
    """PauliZ observable

    expectation value of 1-2*ParticleNumber on a specific wire.
    """
    num_params = 0
    num_wires = 1
    par_domain = None

    @classmethod
    def fermion_operator(cls, samples):
        return samples

class Identity(FermionObservable):
    """Identity observable

    expectation value of the identity operator
    """
    num_params = 0
    num_wires = AnyWires
    par_domain = None

    @classmethod
    def fermion_operator(cls, samples):
        return samples
