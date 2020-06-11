#!/bin/bash 

set -e 

mkdir -p sigs 

cp build/libdssat4py.dylib build/libdssat4py.so

#f2py --overwrite-signature -m dssat4py -h sigs/dssat4py.pyf src/dssat4py.for 

f2py -c sigs/dssat4py.pyf -m dssat4py  build/libdssat4py.so

python runPy.py

