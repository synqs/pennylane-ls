# PennyLane Plugin for Cold Atoms and Labscript

The `pennylane_ls` plugin works on the connection between cold atoms and quantum information circuits.This is basically the technical implementation for the connection of cold atoms and quantum circuits, which we described in [this blog post](https://www.synqs.org/post/2020-atomic-quantum-circuits/).

We also provide a few examples, where we describe published experiments with quantum circuits:

- A circuit description for tunneling of single bosons is examplified [here](https://github.com/synqs/pennylane-ls/blob/master/examples/Example_Hopping_Bosons.ipynb).
- A circuit description for squeezing in spinor Bose-Einstein condensate, which forms a long collective spin is presented [here](https://github.com/synqs/pennylane-ls/blob/master/examples/Fisher_information.ipynb).


In the future it will allow us to run experiments that are controlled by the [Labscript Suite](https://github.com/labscript-suite/) through the interface and the with the features that [Pennylane](https://pennylane.ai/) offers. It will connect to a control server which exposes the atoms through a json interface. The development for that server is happening in [labscript-qc](https://github.com/synqs/labscript-qc).
