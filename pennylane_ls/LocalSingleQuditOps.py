from pennylane.operation import Operation
from pennylane.operation import Observable
import numpy as np

import scipy
from scipy.sparse.linalg import expm
from scipy.sparse import coo_matrix, csc_matrix, diags, identity

import abc

class LocalQuditOperation(Operation):

    @classmethod
    @abc.abstractmethod
    def qudit_generator(cls, wires):
        raise NotImplementedError()

class LocalQuditObservable(Observable):

    @classmethod
    @abc.abstractmethod
    def qudit_operator(cls, wires, par):
        raise NotImplementedError()


class RotX(LocalQuditOperation):
    """The rLx operation"""
    num_params = 1
    num_wires = 1
    par_domain = 'R'

    grad_method = None
    grad_recipe = None

    @classmethod
    def qudit_generator(cls, wires):
        l = 3 # spin length

        # let's put together spin matrices
        dim_qudit = 2*l+1
        qudit_range = np.arange(l, -(l+1),-1)
        Lx  =  scipy.sparse.csc_matrix(1/2*diags([np.sqrt([(l-m+1)*(l+m) for m in qudit_range[:-1]]), np.sqrt([(l+m+1)*(l-m) for m in qudit_range[1:]]) ], [-1, 1]))
        Lx = Lx.toarray()
        return Lx


class rLz(LocalQuditOperation):
    """The rLz operation"""
    num_params = 1
    num_wires = 1
    par_domain = 'R'

    grad_method = None
    grad_recipe = None

    @classmethod
    def qudit_generator(cls, wires):
        l = 3 # spin length

        # let's put together spin matrices
        dim_qudit = 2*l+1
        qudit_range = np.arange(l, -(l+1),-1)
        Lx  =  scipy.sparse.csc_matrix(1/2*diags([np.sqrt([(l-m+1)*(l+m) for m in qudit_range[:-1]]), np.sqrt([(l+m+1)*(l-m) for m in qudit_range[1:]]) ], [-1, 1]))
        Lx = Lx.toarray()
        Lx = jnp.array(Lx)
        return Lx


class rLz2(LocalQuditOperation):
    """The rLz operation"""
    num_params = 1
    num_wires = 1
    par_domain = 'R'

    grad_method = None
    grad_recipe = None

class Id(LocalQuditOperation):
    """Custom gate"""
    num_params = 1
    num_wires = 1
    par_domain = 'R'

    grad_method = None
    grad_recipe = None

class Lz(LocalQuditObservable):
    """Custom observable"""
    num_params = 0
    num_wires = 1
    par_domain = 'R'

    @classmethod
    def qudit_operator(cls, wires):
        l = 3 # spin length

        # let's put together spin matrices
        dim_qudit = 2*l+1
        qudit_range = np.arange(l, -(l+1),-1)
        Lz  =  scipy.sparse.csc_matrix(diags([qudit_range], [0]))
        Lz = Lz.toarray()
        return Lz
