# PennyLane Plugin for Cold Atoms

The `pennylane_ls` plugin works on the connection between cold atoms and quantum information circuits.This is basically the technical implementation for the connection of cold atoms and quantum circuits, which we described in [this blog post](https://www.synqs.org/post/2020-atomic-quantum-circuits/).

We also provide a few examples, where we describe published experiments with quantum circuits:

- A circuit description for tunneling of single bosons is examplified [here](https://github.com/synqs/pennylane-ls/blob/master/examples/Example_Hopping_Bosons.ipynb).
- A circuit description for squeezing in spinor Bose-Einstein condensate, which forms a long collective spin is presented [here](https://github.com/synqs/pennylane-ls/blob/master/examples/Fisher_information.ipynb).


Internally, it allows us to run experiments that are controlled by the [Labscript Suite](https://github.com/labscript-suite/) through the interface and the with the features that [Pennylane](https://pennylane.ai/) offers. It will connect to a control server which exposes the atoms through a json interface. The development for that server is happening in [labscript-qc](https://github.com/synqs/labscript-qc).

# Get started

The released versions are installed with a simple:

`pip install pennylane-ls`

Then you can simply start hacking on one of the provided [examples](https://github.com/synqs/pennylane-ls/tree/master/examples). Make sure that you got your credentials right. 

- We are internally working with a [quantum hardware simulator](http://qsimsim.synqs.org/) to which everyone can register. 
- For connecting real hardware you can check out [our labscript-qc](https://github.com/synqs/labscript-qc) repo.
