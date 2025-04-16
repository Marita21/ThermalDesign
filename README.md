# Thermal Simulation of a Satellite Subsystem.

This project models the thermal behavior of a satellite subsystem using the Finite Difference Method (FDM). It calculates node temperatures over time for various spacecraft components, including radiators, structures, and multilayer insulation (MLI).

## Files Included

- `MOD_16_NODO_T_N.py`: Main script that defines the thermal network, nodes, conductances, admittances, and solves the transient temperature distribution.
- `solve.py`: Custom solver implementing explicit finite difference methods for thermal analysis.

## How It Works

- Nodes represent physical components with thermal mass and initial temperature.
- Conductive and radiative links between nodes are modeled via conductances and admittances.
- The `FDMExplicit` solver calculates the time evolution of each node's temperature.

## How to Run

1. Make sure Python 2 is installed..
2. Run the main script:



python MOD_16_NODO_T_N.py


<img src="img/Captura.JPG" alt="Captura" width="400">
