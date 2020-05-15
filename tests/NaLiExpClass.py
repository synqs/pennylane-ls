
from set_initial_values import SetChannels
from MOT_Na_Li import loadsodiumMOT, getsodiumMOT,End_NaMOT
from Spin_polarization import UMPUMP,SpinPol
from Magnetic_trap import LoadMT, OpenMT, EndMT, Compress_MT,  MWclean, RFcooling1, RFcooling2
from ODT import Hold_ODT_MT,load_Waveguide,load_dimple, ODT_off, Offset_Ramp,MW_transfer,ODT_ramp
from Imaging_retiga_test import Image_atoms ,Na_dark_pic
from SG import Stern_Gerlach, RabiOsc
from Sirah_lattice import Sirah_lattice
from PennyLaneOps import X, H_mb, prepare_initial, finishing
##
class ExperimentClass():
    def __init__(self):
        self.t = 0
##
ExperimentClass.SetChannels = SetChannels
ExperimentClass.loadsodiumMOT = loadsodiumMOT
ExperimentClass.End_NaMOT = End_NaMOT
ExperimentClass.getsodiumMOT = getsodiumMOT
ExperimentClass.UMPUMP = UMPUMP
ExperimentClass.SpinPol = SpinPol
ExperimentClass.LoadMT = LoadMT
ExperimentClass.OpenMT = OpenMT
ExperimentClass.EndMT = EndMT
ExperimentClass.Compress_MT = Compress_MT
ExperimentClass.MWclean = MWclean
ExperimentClass.RFcooling1 = RFcooling1
ExperimentClass.RFcooling2 = RFcooling2
ExperimentClass.Hold_ODT_MT = Hold_ODT_MT
ExperimentClass.load_Waveguide = load_Waveguide
ExperimentClass.load_dimple = load_dimple
ExperimentClass.ODT_off = ODT_off
ExperimentClass.Offset_Ramp = Offset_Ramp
ExperimentClass.MW_transfer = MW_transfer
ExperimentClass.ODT_ramp = ODT_ramp
ExperimentClass.Image_atoms = Image_atoms
ExperimentClass.Na_dark_pic = Na_dark_pic
ExperimentClass.Stern_Gerlach = Stern_Gerlach
ExperimentClass.Sirah_lattice = Sirah_lattice
## High-level Pennylane functions
ExperimentClass.X = X
ExperimentClass.H_mb = H_mb
ExperimentClass.prepare_initial = prepare_initial
ExperimentClass.finishing = finishing
##