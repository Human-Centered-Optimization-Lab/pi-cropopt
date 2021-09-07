from multiprocessing import Pool
from multiprocessing import Manager
import sys 
import pickle
from attr_processors import AttProcessors
import pandas as pd
import tabloo
import numpy as np



if len(sys.argv) != 2:
    print("Usage: python %s RUNRECORD.pkl" % sys.argv[0])
    print("Example: python mlearn/step0_build_attr_tab.py postprocess/master_run_record.pkl")
    sys.exit(1)

# Functions
def process_year(arg):

    # unpack the argument
    (tab, att_functs, year, attribProcr, single_val_per_year) = arg

    rows = np.shape(tab)[0]

    results = []

    # For every attribute function 
    result_count = -1

    for (a, att_funct) in enumerate(att_functs):

        svpy = single_val_per_year[a]                   

        func = getattr(attribProcr, att_funct)
        
        # Do we need to run this for every row? Or just once for the whole year
        if svpy: 
            single_res = func(tab.iloc[0,:])
            att_results = [single_res] * rows
        else:
            att_results = tab.apply(func, axis=1)

        results.append(att_results)
    
    print("Completed year %d" % year)
    return (year, np.transpose(np.array(results)))


# Main

if __name__ == "__main__":


    threads = 23

    if threads != 1:
        # This somehow prevents this weird error while using multiprocessing
        # AttributeError: module '__main__' has no attribute '__spec__'
        __spec__ = None


    # Read in the master record
    file_name = sys.argv[1]

    # Read the GDD table
    gdd_tab_csv = "management_dates.csv"
    gdd_tab = pd.read_csv(gdd_tab_csv)
   
    # Read the weather table
    wth_file_path = "dhome/Weather/CASSREPR.WTH"
    wth_tab = pd.read_fwf(wth_file_path, skiprows=4)


    infile = open(file_name, 'rb')
    tab = pickle.load(infile)


    years = set(tab['year'])

    att_functs = [ 
                    'application_count', 
                    'total_irrigation', 
                    'yield_', 
                    'front',
                    'leaching',
                    'minimum_irr',
                    'maximum_irr', 
                    'number_of_precipitation_events', 
                    'growth_period_of_second_N_app' ,
                    'total_irr_during_v6', 
                    'total_irr_during_v7',
                    'total_irr_during_v8',
                    'total_irr_during_v9',
                    'total_irr_during_v10', 
                    'total_irr_during_v11',
                    'total_irr_during_v12',
                    'total_irr_during_v13',
                    'total_irr_during_v14',
                    'total_irr_during_R1', 
                    'total_irr_during_R2', 
                    'total_irr_during_R3', 
                    'total_irr_during_R4',
                    'total_precip_during_v6',
                    'total_precip_during_v7',
                    'total_precip_during_v8',
                    'total_precip_during_v9',
                    'total_precip_during_v10',
                    'total_precip_during_v11',
                    'total_precip_during_v12',
                    'total_precip_during_v13',
                    'total_precip_during_v14',
                    'total_precip_during_R1', 
                    'total_precip_during_R2',
                    'total_precip_during_R3',
                    'total_precip_during_R4']


    

    # Do we calculate this term for every row, or just once per year? 
    single_val_per_year = [ False,  #  application_count
                            False,  #  total_irrigation
                            False,  #  yield_
                            False,  #  front
                            False,  #  leaching
                            False,  #  minimum_irr
                            False,  #  maximum_irr
                            False,  #  number_of_precipitation_events
                            True,   #  growth_period_of_second_N_app 
                            False,  #  total_irr_during_v6
                            False,  #  total_irr_during_v7
                            False,  #  total_irr_during_v8
                            False,  #  total_irr_during_v9
                            False,  #  total_irr_during_v10
                            False,  #  total_irr_during_v11
                            False,  #  total_irr_during_v12
                            False,  #  total_irr_during_v13
                            False,  #  total_irr_during_v14
                            False,  #  total_irr_during_R1
                            False,  #  total_irr_during_R2
                            False,  #  total_irr_during_R3
                            False,  #  total_irr_during_R4
                            False,  # total_precip_during_v6
                            False,  # total_precip_during_v7
                            False,  # total_precip_during_v8
                            False,  # total_precip_during_v9
                            False,  # total_precip_during_v10
                            False,  # total_precip_during_v11
                            False,  # total_precip_during_v12
                            False,  # total_precip_during_v13
                            False,  # total_precip_during_v14
                            False,  # total_precip_during_R1
                            False,  # total_precip_during_R2
                            False,  # total_precip_during_R3
                            False ] # total_precip_during_R4

    raw_table = {'year': []}

    # initialize the attribute functions
    for att_funct in att_functs: 
        raw_table[att_funct] = []

    # Split up the data by year, with each thread focusing on a single year
    # preventing race conditions while using shared tables
    tab_by_years = {}
    procr_by_years = {}

    print("Splitting parameters and input tables")
    for year in years: 
        tab_by_years[year] = (tab[tab['year'] == year])

        # Set up the processing agent 
        year_modded = int((year  % 1e2) * 1e3)
        wth_year_mask = np.logical_and(wth_tab['@DATE'] > year_modded, wth_tab['@DATE'] <= (year_modded + 366))
        specific_wth_tab = wth_tab[wth_year_mask]

        specific_gdd_tab = gdd_tab[gdd_tab['Year'] == year]

        procr_by_years[year] = AttProcessors(specific_wth_tab, specific_gdd_tab)

    print("Done.")


    # Pack up arguments
    argz = [(tab_by_years[year], att_functs, year, procr_by_years[year], single_val_per_year) for year in years]

    print("Starting attribute processing")
    if threads == 1: 
        # Eschew multiprocessing for debugging ease
        results = [process_year(arg) for arg in argz]
    else: 
        with Pool(threads) as p: 
            results = p.map(process_year, argz)


    # unpack results by year
    run_results = {}
    for result_by_year in results:
        (year, attrs) = result_by_year
        run_results[year] = attrs

    for year in years:

        result_count = -1

        for (i, att_funct) in enumerate(att_functs): 
            attr = run_results[year]

            new_results = attr[:, i].tolist()
            raw_table[att_funct] = raw_table[att_funct] + new_results

            if result_count == -1:
                result_count = len(new_results)

        raw_table['year'] = raw_table['year'] +  [year] * result_count

    # Build the attribute table    
    attribute_table = pd.DataFrame(raw_table)

    output_dir = "/".join(sys.argv[0].split("/")[0:-1])

    output = open('%s/attr_tab.pkl' % output_dir, 'wb')
    pickle.dump(attribute_table, output)


