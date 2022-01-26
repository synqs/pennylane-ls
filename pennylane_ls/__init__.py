"""
The initialization of the pennylane-ls module
"""
from .single_qudit_device import SingleQuditDevice
from .single_qudit_ops import RLX, LZ, RLZ, RLZ2

from .multi_qudit_device import MultiQuditDevice

from .fermion_ops import Hop, Inter, Phase, ParticleNumber, PauliZ, HartreeFock
from .fermion_device import FermionDevice

from ._version import __version__
