import pickle
import tabloo
import sys
import pandas as pd

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)


file_name = sys.argv[1]

infile = open(file_name, 'rb')
tab = pickle.load(infile)



print(tab)

