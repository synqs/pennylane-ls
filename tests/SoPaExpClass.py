from SoPaFunctions import prepare_initial, take_reference, meas, reset_after
from SoPaFunctions import load_MOT, idle
##
class ExperimentClass():
    def __init__(self):
        self.t = 0
ExperimentClass.prepare_initial = prepare_initial
ExperimentClass.take_reference = take_reference
ExperimentClass.meas = meas
ExperimentClass.reset_after = reset_after
ExperimentClass.load_MOT = load_MOT
ExperimentClass.idle = idle