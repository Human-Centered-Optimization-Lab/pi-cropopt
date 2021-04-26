import pickle
import tabloo


infile = open('step1_optAndPesFronts.pkl', 'rb')
candid_tab = pickle.load(infile)

tabloo.show(candid_tab)

