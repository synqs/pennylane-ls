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

- _SynQSDevice.py_ -- Defines the SynQS device framework class which can be inherited to define a specific device
- _NaLiExperiment.py_ -- Specific NaLi device that generates experimental sequence files to be run with labscript 
- _SoPaExperiment.py_ -- Specific SoPa device that generates experimental sequence files to be run with labscript
- _NaLiOps.py_ -- Operations and Observables of the _SoPaExperiment_ device. 
- _SoPaOps.py_ -- Operations and Observables of the _NaLiExperiment_ device. 

### Testing the plugin
The directory _/tests_ contains  a Jupyter/IPython notebook _test_plugin.ipynb_ to test the most basic features of the plugin. If _dummy_output_ is True for the device you instantiate, the observable output at the end will be generic and not circuit-dependent. The handle _remote_runmanager_ requires the Runmanager and Blacs of the Labscript suite to be open and the experiment to be ready to run.
_/tests_ also contains the headers for the to-be-generated experimental sequences. To clean up the Experiment.py, the Experiment class for the experiment functions is also outsourced here.

## How-To add a new machine

Best read for general instructions is the [plugin developement](https://pennylane.readthedocs.io/en/stable/development/plugins.html) site of Pennylane. For general purposes, the following changes need to be made to adapt a plugin to new hardware:

- Adapt the _apply()_ method to your needs. This method is called for every operation in the quantum circuit and you queue them in a way that is most suitable to you. The methods _pre_apply()_ or _post_apply()_ can be useful.
- Adapt the _expval()_ method to your needs. This method is called when evaluating the expectation of an observable and should contain the execution of the circuit on your hardware with subsequent evaluation of the results. It is commonly the heart of the plugin and where most specification of your exact device is required.
- There are more methods that can be adapted that are otherwise inherited by the [_Device_ class](https://pennylane.readthedocs.io/en/stable/code/api/pennylane.Device.html) in Pennylane. Quantum circuits are evaluated by running the [_execute()_](https://pennylane.readthedocs.io/en/stable/code/api/pennylane.Device.html#pennylane.Device.execute). Instead of overwriting this, consider implementing a suitable subset of the functions called inside _execute()_.
- Add Operations and Observables that correspond to your machine

Of course specify name, author, version, etc for your plugin and/or device.


## ToDo / Future steps
- Develop a pennylane_ls template for other groups in the community to use this general approach.
  - In that, move _pre_apply()_ and _post_apply()_ to the framework device such that _prepare_initial()_ and _finishing()_ (to be renamed) are always printed and only the specific operations of the experiment need to be specified in the device.

- Give operations parameter ranges that don’t break the lab
- Triggering of hardware, i.e. cameras, that are not coordinated by Labscript. (Set Zyla to acquire in SoPa)
- Potentially implement useful applications for the plugin in the lab, e.g. scanning paramters, plotting images/histograms, …
- Find higher-level operations for SoPa
- Calibrate NaLi Rabi/X rotation angle relative to time
