# pennylane_ls
Our pennylane plugin for labscript. Our attempt to connect the [labscript suite](https://github.com/labscript-suite/) to some circuit diagrams. We choose [Pennylane](https://pennylane.ai/).

This repo is based on [the plugin template](https://github.com/XanaduAI/pennylane-plugin-template) provided by pennylane. An example Pennylane plugin is of [ProjectQ](https://github.com/XanaduAI/pennylane-pq). It is well-designed and written by C. Gogolin. 

### The plugin
The core files in the plugin folder _pennylane_ls_ are:

- _SoPaDevice.py_ -- Defines the SoPa device framework class which can be inherited to define a specific device
- _SoPaExperiment.py_ -- Specific SoPa device that generates experimental sequence files to be run with labscript 
- _SoPaOps.py_ -- Operations that are accepted in the SoPa device framework and experiment. 
- _SoPaFunctions.py_  -- Low-level decomposition of the functions that are run in the experiment. This should live in the pythonlib of your labscript installation.

### tests
Open and run the Jupyter/IPython notebook _test_plugin.py_ to test the most basic features of the plugin. The observable output at the end is currently generic and not circuit-dependent!

# Installation

You should clone this repo to ???

# How-To add a new machine

Best read for general instructions is the [plugin developement](https://pennylane.readthedocs.io/en/stable/development/plugins.html) site of Pennylane. For general purposes, the following changes need to be made to adapt a plugin to new hardware:

- Adapt the _apply()_ method to your needs. This method is called for every operation in the quantum circuit and you queue them in a way that is most suitable to you. The methods _pre_apply()_ or _post_apply()_ can be useful.
- Adapt the _expval()_ method to your needs. This method is called when evaluating the expectation of an observable and should contain the execution of the circuit on your hardware with subsequent evaluation of the results. It is commonly the heart of the plugin and where most specification of your exact device is required.
- There are more methods that can be adapted that are otherwise inherited by the [_Device_ class](https://pennylane.readthedocs.io/en/stable/code/api/pennylane.Device.html) in Pennylane. Quantum circuits are evaluated by running the [_execute()_](https://pennylane.readthedocs.io/en/stable/code/api/pennylane.Device.html#pennylane.Device.execute). Instead of overwriting this, consider implementing a suitable subset of the functions called inside _execute()_.
- Add Operations and Observables that correspond to your machine

Of course specify name, author, version, etc for your plugin and/or device.
