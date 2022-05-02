# Agricultural Innovization

## Overview

This project contains an innovization framework, which entails: 

1. Optimization of crop management practices over many years of climate data (the `optimization` folder)
2. Converting data into a single data table (`postprocess` folder) 
3. Further preprocessing and innovization procedure (`mlearn` folder)
4. Validation and analysis of the innovization (`validation` folder)

## Supporting folders
* `dhome` contains the DSSAT model configuration and executables
* `dssatmod` contains python scripts for automatically running and interpreting DSSAT simulations
* `utilities` contains various single-purpose helping scripts 

## Installation

```
conda create -c conda-forge --name agovization python=3.8 -y
conda activate agovization
conda install -c conda-forge pyarrow==0.17.0
conda install -c conda-forge --file requirements.txt
pip install -r indie-requirements.txt

```

