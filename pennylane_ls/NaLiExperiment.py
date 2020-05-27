# we always import NumPy directly
import numpy as np

from .SynQSDevice import SynQSDevice

from lyse import *
from pylab import *
import h5py
import os
import glob

class NaLiExperiment(SynQSDevice):
    ## Define operation map for the experiment
    _operation_map = {
        "X": "Rabi",
        "H_mb": "H_mb"
    }
    observables = {"NumberOperator"}

    def __init__(self,wires=1, shots=11, remote_runmanager=False,dummy_output=False):
        super().__init__(wires=wires, shots=shots)
        super().reset()
        self.remote_runmanager = remote_runmanager
        self.dummy_output = dummy_output
        self.file_name = "NaLiExperiment_Sequence.py"
        self.header_name = "NaLiHeader.py"


    def expval(self, observable, wires, par):
        """Retrieve the requested observable expectation value.
        """
        if self.remote_runmanager:
            import runmanager.remote                                                               ### can you tell me if this works for you? otherwise change path
            remoteClient = runmanager.remote.Client()
            remoteClient.set_labscript_file("C:\\labscript_suite\\userlib\\labscriptlib\\SoPa_Experiment\\"+self.file_name)  #### Set Project_name
            remoteClient.set_run_shots = True
            remoteClient.set_view_shots = False
            remoteClient.reset_shot_output_folder()
            h5folder = remoteClient.get_shot_output_folder()
            remoteClient.engage()
            if self.remote_runmanager==True and self.dummy_output:
                return 1
        else:
            inp = False
            while inp != 'y':
                inp = input('Has the experiment been run? Enter y, N or Exit: ')
                if inp == 'N':
                    print('Please run the experiment!')
                if inp == 'Exit':
                    return

        if self.dummy_output:
            path = '..\\tests\h5testfile.h5'
            r = Run(path, no_write=False)

            orientation = 'test'

            Iat = r.get_image(orientation, 'gaussian', 'gaussian')
            Iref = r.get_image(orientation, 'gaussian', 'reference')
        else:
            if self.remote_runmanager:
                path = h5folder + '\\' + os.listdir(h5folder)[0]
                #path = h5folder + '\\' + input('Name of h5 shot file: ')
            if not self.remote_runmanager:
                path = input('Full path to result h5 file:\n')
            r = Run(path, no_write=False)

            orientation = 'NaZyla'

            Iat = r.get_image(orientation, 'fluorescence', 'NaAtoms')
            Iref = r.get_image(orientation, 'fluorescence', 'NaReference')
        #Ibg = 0.0 * Iat

        ## calculate everything
        Iat = 1.0 * Iat
        Iref = 1.0 * Iref

        od = Iat - Iref
        # od=-np.log((Iat)/(Iref))

        odx = np.sum(od, axis=0)
        ody = np.sum(od, axis=1)

        back = Iref
        fluo = Iat
        subtracted = (1.0 * fluo) - (1.0 * back)
        return sum(od) / (np.shape(od)[0] * np.shape(od)[1])