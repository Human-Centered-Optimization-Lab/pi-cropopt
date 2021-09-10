import pickle
import pandas as pd
import sys


if len(sys.argv) != 3:
    print("Usage: %s INPUT.PKL OUTPUT.FEATHER" % sys.argv[0])
    sys.exit(1)

input_file_name = sys.argv[1]
file_output_path = sys.argv[2]


infile = open(input_file_name, 'rb')
tab = pickle.load(infile)

tab.to_feather(file_output_path)

