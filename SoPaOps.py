from pennylane.operation import Operation

class LoadMOT(Operation):
    """Custom gate"""
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
