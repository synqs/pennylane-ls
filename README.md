# PennyLane Labscript Plugin
Our pennylane plugin for labscript. Our attempt to connect the [Labscript Suite](https://github.com/labscript-suite/) to some circuit diagrams. We choose [Pennylane](https://pennylane.ai/).

This repo is based on [the plugin template](https://github.com/XanaduAI/pennylane-plugin-template) provided by pennylane. An example Pennylane plugin is of [ProjectQ](https://github.com/XanaduAI/pennylane-pq). It is well-designed and written by C. Gogolin. 

## Features
- Proposes an interface to the low-level experimental control of the Labscript Suite by generating experimental sequence files on the fly through a higher-level framework.
- Includes two devices for the SynQS group at the Kirchhoff-Institute for Physics of Prof. Fred Jendrzejewski.

## Installation

Clone or download the repository wherever you like. The _pennylane_ls_ module in the _pythonlib_ of your Labscript suite installation folder structure ie. _labscript_suite\userlib\pythonlib_. This is the directory to put all of your own modules or functions to use with Labscript. The files in the _tests/_ directory should all live in _labscript_suite\userlib\labscriptlib\ProjectName_ where all experimental sequence files are saved and run from. In priciple, they could live in another directory but the paths in the plugin folder need to be modified.

### pennylane_ls files
The core files in the plugin folder _pennylane_ls_ are:

- _SynQSDevice.py_ -- Defines the SynQS device framework class for connecting with Labscript through the Pennylane interface.
- _NaLiExperiment.py_ -- Specific NaLi device that generates experimental sequence files to be run with labscript 
- _SoPaExperiment.py_ -- Specific SoPa device that generates experimental sequence files to be run with labscript
- _NaLiOps.py_ -- Operations and Observables of the _SoPaExperiment_ device. 
- _SoPaOps.py_ -- Operations and Observables of the _NaLiExperiment_ device. 

**Notes for the _SynQSDevice.py_ framework device:**
This is the framework device, as mandated by the PennyLane template. It is the framework for writing an Experiment.py file that can be executed in the Runmanager of the Labscript Suite. The _apply()_ as well as the _pre_apply()_ and _post_apply()_ methods are defined here which can be used out of the box. _pre_apply()_ writes function 'Experiment.prepare_initial()' into the file and _post_apply()_ the function 'Experiment.finishing()'. Those need to be defined in the pythonlib of the Labscript suite.  
The _apply()_ method is flexibly writes the operation into the Experiment.py file with the corresponding passed parameters. For this, the \_operation_map variable needs to be defined that maps the high-level Pennylane operation to the name of the function in the experiment environment. This approach does not support any reasonable definition of _wires_ from Pennylane. In order to implement those, you need to override the _apply()_ method in the device derived from the framework device and implement the functionality accordingly.

### Testing the plugin
The directory _/tests_ contains  a Jupyter/IPython notebook _test_plugin.ipynb_ to test the most basic features of the plugin. If _dummy_output_ is True for the device you instantiate, the observable output at the end will be generic and not circuit-dependent. The handle _remote_runmanager_ requires the Runmanager and Blacs of the Labscript suite to be open and the experiment to be ready to run.
_/tests_ also contains the headers for the to-be-generated experimental sequences. To clean up the Experiment.py, the Experiment class for the experiment functions is also outsourced in _NaLiExpClass.py_ or _SoPaExpClass.py_.

## How-To add a new machine or write your own device

Best read for general instructions is the [plugin developement](https://pennylane.readthedocs.io/en/stable/development/plugins.html) site of Pennylane. For general purposes, the following changes need to be made to adapt a plugin to new hardware:

1. **Define the PennyLane Operations and Observables** that are implemented in your device/experiment.
2. **Override some device methods** to make them specific to your quantum device. For standard application, at least the methods apply() and expval() of the device.
3. **Set up header and function files** in the correct directories.

Nr 1. is especially important for quantum devices that do not implement commonly used and widely known operations such as X,Y,Z rotations, Hadamard H gates, entangling CNOT or XX gates, and oberservables like <img src="https://render.githubusercontent.com/render/math?math=\sigma^z"> expectations.

Nr 2. entails the most amount of developer work and is crucial to build a smooth and understandable interface with the machine.  
The job of apply() is to queue the operations in a way that is understandable by your experiment. It is called for every operation in the quantum circuit with the passed parameters, e.g. X(<img src="https://render.githubusercontent.com/render/math?math=\pi/2">). The plugin author needs to decide what is the most sensible way to queue the operations ready to run on the experiment. The useful methods pre_apply() and post_apply() are called before the first operation and after the last operation is queued respectively.  
Expval() is called at the end of execute() and is responsible for sending the entire queued circuit to the experiment, running it and returning the expectation of the observable.  
There are more methods that can be adapted that are otherwise inherited by the [_Device_ class](https://pennylane.readthedocs.io/en/stable/code/api/pennylane.Device.html) in Pennylane. Quantum circuits are evaluated by running the [_execute()_](https://pennylane.readthedocs.io/en/stable/code/api/pennylane.Device.html#pennylane.Device.execute). Instead of overwriting this, consider implementing a suitable subset of the functions called inside _execute()_.

Nr 3. is to stream-line the functionality of the framework device. Similar to the _NaliHeader.py_ and _SoPaHeader.py_ files, you need to specify the necessary header for your experiment. This is likely your connection table.  
Also requred for the curret approach is the _ExperimentClass()_ that keeps track of the time variable during the sequence and has all of your experimental functions as class methods. You need to define an experiment class either in the header directly (which is clumsy) or in an extra Python file like the ones privided in _/tests_. Don't forget to import it and instantiate an object of that class in the header.

## ToDo / Future steps
- Develop a pennylane_ls template for other groups in the community to use this general approach.
  - In that, move _pre_apply()_ and _post_apply()_ to the framework device such that _prepare_initial()_ and _finishing()_ (to be renamed) are always printed and only the specific operations of the experiment need to be specified in the device.

- Give operations parameter ranges that don’t break the lab
- Implement full result post-processing that is currently used in the lab.
- Triggering of hardware, i.e. cameras, that are not coordinated by Labscript. (Set Zyla to acquire in SoPa)
- Potentially implement useful applications for the plugin in the lab, e.g. scanning paramters, plotting images/histograms, …
- Find higher-level operations for SoPa
- Calibrate NaLi Rabi/X rotation angle in NaLi relative to time (Is likely required for communication with theorists)
