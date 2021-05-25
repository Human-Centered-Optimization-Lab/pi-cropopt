# Agricultural Innovization

## Files
* **SparseSampler.py** Python implementation of Sparse Population Sampler
* **appCounter.py** Takes the genome of an irrigation optimization run and 
* **cropopt.py** The optimization problem fed into pymoo, including objective function 
* **cropover.py** Implementation of the cropover routine
* **dssat4dum.py** Simple dssat wrapper
* **main_cropverVsSPS.py** Script I used to compare the performance of cropover and sparse population sampling
* **plotAnnotatedPF.py** Plots a Pareto front that also shows the number of applications in each solution
* **plotHV.py** Plots the hyper-volume of a given run
* **plotRuns.py** Plots irrigation, yield, and number of applications in each solution
* **runPy.py** Test file for running dssat4dum
* **main.py** The main file for the optimization portion of agricultural innovization

## Installing

```
conda create --name my_project_env
pip install -r requirements.txt
```
