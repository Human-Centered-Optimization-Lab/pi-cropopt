import pickle
import pandas as pd
import sys

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)


input_file_name = sys.argv[1]
output_file = sys.argv[2]

infile = open(input_file_name, 'rb')
tab = pickle.load(infile)

with pd.ExcelWriter(output_file) as writer:  
    tab.to_excel(writer, sheet_name='Sheet')


