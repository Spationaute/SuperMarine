# SuperMarine

## What is superMarine?
SuperMarine is a geometry generator for OpenFOAM that can be used for stirred tanks commonly used in chemical and biochemical engineering.
It aims to give an easy solution for academic research and students that which to use OpenFOAM on common and simple geometry.
The scripts create a blockMesh file ready to be used within a OpenFOAM case.

SuperMarine was first developed to build a marine impeller, but can also be used to create a wide variety of impeller.
The present version of the code is sufficient to create accurately a basic stirred tank design with its impeller,
but can be tweaked in order to have more sophisticated shapes.
Since it is a python script, the user can change the code has he wish and adapt it to his case.

## To Execute the spMarine-demo
1. Load the openFoam toolkit in your environment.
1. Switch to the directory and enter:
	1. `$ python3 setup.py`
	1. `$ mpirun -n4 interFoam -parallel`
	1. **The number of processor can be changed in the decomposePar dictionary**

## TO DO
- [ ] Clean the code
- [ ] Finish the manual
- [ ] Add examples

## Documentations
