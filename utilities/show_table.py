import pickle
import tabloo
import sys

file_name = sys.argv[1]

infile = open(file_name, 'rb')
tab = pickle.load(infile)

tabloo.show(tab)

