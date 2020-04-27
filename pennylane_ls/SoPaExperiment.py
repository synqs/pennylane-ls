# we always import NumPy directly
import numpy as np

from .SoPaDevice import SoPaDevice

from lyse import *
from pylab import *
import h5py
import os
import glob

class SoPaExperiment(SoPaDevice):
    ## Define operation map for the experiment
    _operation_map = {
        "LoadMOT": 'load_Mot',
        "Id": 'idle'
    }

    def __init(self, boson_wires=2, fermion_wires=0, shots=11, hardware_options=None):
        super().__init__(wires=boson_wires + fermion_wires, shots=shots)
        super().reset()

    def reset(self):
        pass

    def pre_apply(self):
        self.reset()
        self.Expfile = open("Experiment_Pennylane.py", "w")
        ## copy the header ##
        header = open("header.py", "r")
        for line in header:
            self.Expfile.write(line)
        header.close()
        ## start command ##
        self.Expfile.write("start()\n\n")
        self.Expfile.write('## Begin of Preparation ##\n')
        ## initial preparation ##
        self.Expfile.write('Experiment.prepare_initial()\n')
        ## take background image ##
        self.Expfile.write('Experiment.take_reference()\n')
        ##
        self.Expfile.write('## End of Preparation ##\n\n')
        self.Expfile.write('## Begin Sequence of Gates ##\n')

    def post_apply(self):
        self.Expfile.write('## End Sequence of Gates ##\n\n')
        self.Expfile.write('## Finishing ##\n')
        ## measure ##
        self.Expfile.write('Experiment.meas()\n')
        ## reset after measure ##
        self.Expfile.write('Experiment.reset_after()\n')
        ##
        self.Expfile.write("stop(Experiment.t+2)")
        self.Expfile.close()

    def apply(self, operation, wires, par):
        # check with different operations ##
        if operation is 'LoadMOT':
            self.Expfile.write('Experiment.load_MOT({}) \n'.format(par[0]))
        if operation is 'Id':
            self.Expfile.write('Experiment.idle({}) \n'.format(par[0]))

    def expval(self, observable, wires, par):
        """Retrieve the requested observable expectation value.
        """
        inp = False
        while inp != 'y':
            inp = input('Has the experiment been run? Enter y, N or Exit: ')
            if inp == 'N':
                print('Please run the experiment!')
            if inp == 'Exit':
                return
        ## find the file
        import os
        #print(os.path.dirname(os.path.abspath(__file__)))
        h5name = input('Enter the .h5 file with the result. For test -> h5testfile. No ".h5" needed. ')
        print('Results in the file ' + h5name)
        path = '..\\tests\{}.h5'.format(h5name)
        r = Run(path, no_write=False)

        orientation = 'test';
        name = 'frame';

        Iat = r.get_image(orientation, 'gaussian', 'gaussian');
        Iref = r.get_image(orientation, 'gaussian', 'reference');
        Ibg = 0.0 * Iat

        ## calculate everything
        Iat = 1.0 * Iat + Iref
        Iref = 1.0 * Iref

        od = Iat - Iref
        # od=-np.log((Iat)/(Iref))

        odx = np.sum(od, axis=0)
        ody = np.sum(od, axis=1)

        back = Iref
        fluo = Iat
        subtracted = (1.0 * fluo) - (1.0 * back)
        return sum(od) / (np.shape(od)[0] * np.shape(od)[1])