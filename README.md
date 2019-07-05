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
	
## To Start the web Interface (**NEW**)
1. Go to the "Interfaced" repertory.
1. Execute "SuperMarineGui.py". 
1. Connect to "localhost:9000" on your favorite web browser.

## TO DO
- [ ] Clean the code
- [ ] Finish the manual
- [x] Add a simple interface
- [ ] Add an interface autostart at the root
- [x] Add an example
- [x] Add more examples

## Documentations

## Quick Introduction
To use *superMarine* copy the superMarine.py script to the case folder, then execute the script (`$python3 setup.py`).
The "`./constant/polyMesh`" directory must exist.

| Variables | Description |
|-----------|-------------|
| **DIVI** |  Angular, Radial and Vertical divisions per block |
| **RQUAD** | Radius of each QUADran. This parameter must be a list of at least two elements,The first being the center hole/square section. |
| **NSEC** |  The Number of SECtors to create.Must be a multiple of 4 (12,24 and 36 are useful multiple of 4!) |
| **HLAY** |    Height of each LAYers. This parameter must be a list of at least one element |
| **SHAFT** | Section on which the SHAFT exists. This parameter must be a list which as the same number of elements of HLAY. |
| **IMPELLERCUT** |   Where to CUT for the IMPELLER. This parameter must be a NSEC by NCAR by NHLAY 3d matrix. A 1 in a region means to cut that region for the impeller. |
| **SQRRATIO** | The RATIO for the distance between the center SQuaRe region and the Outer cylinder. Must be larger than 0 and smaller than 1. |

## Special Tanks
- Denis Groleau
- Pierre Proulx
- Ehsan Askari

