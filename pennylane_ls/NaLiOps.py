from pennylane.operation import Operation
from pennylane.operation import Observable
import numpy as np
class X(Operation):
    """Custom gate"""
    num_params = 1
    num_wires = 1
    par_domain = 'R'

    grad_method = None
    grad_recipe = None


class H_mb(Operation):
    """Custom gate"""
    num_params = 1
    num_wires = 1
    par_domain = 'R'

    grad_method = None
    grad_recipe = None

class NumberOperator(Observable):
    """Custom observable"""
    num_params = 0
    num_wires = 1
    par_domain = 'R'
    eigvals = np.array([0, 1])

    def diagonalizing_gates(self):
        return []
