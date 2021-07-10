from pennylane.operation import Operation
from pennylane.operation import Observable
import numpy as np


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

class ZZ(Operation):
    """The ZZ operation"""
    num_params = 1
    num_wires = 1
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
