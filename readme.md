# Progressively Interactive Crop Optimization 

## Overview

This is an experiment to test the effects of using progressively interactive EMO techniques in crop optimizatin

## Supporting folders
* `dhome` contains the DSSAT model configuration and executables
* `dssatmod` contains python scripts for automatically running and interpreting DSSAT simulations
* `utilities` contains various single-purpose helping scripts 

## Installation

```
conda create -c conda-forge --name pi-cropopt python=3.8 -y
conda activate agovization
conda install -c conda-forge pyarrow==0.17.0
conda install -c conda-forge --file requirements.txt
pip install -r indie-requirements.txt

```

