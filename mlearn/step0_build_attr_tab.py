from multiprocessing import Pool
from multiprocessing import Manager
import sys 
import pickle
from attr_processors import AttProcessors
import pandas as pd
import numpy as np
import statistics


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


    if len(sys.argv) != 2 and len(sys.argv) != 4:
        print("Usage: %s /PATH/TO/MASTER_RECORD.PKL [/PATH/TO/ATTRIB_TAB.PKL /PATH/TO/NEW/TAB.PKL]" % sys.argv[0])
        sys.exit(1)

    if len(sys.argv) == 4: 
        append_mode = True
        tab_to_append_path = sys.argv[2]
        new_tab_path = sys.argv[3]

        print('Append mode on to file %s' % tab_to_append_path)
    else:
        append_mode = False

    # Read in the master record
    file_name = sys.argv[1]

    

    # Read the GDD table
    gdd_tab_csv = "management_dates.csv"
    gdd_tab = pd.read_csv(gdd_tab_csv)



    # Read the weather table
    wth_file_path = "dhome/Weather/CASSREPR.WTH"
    wth_tab = pd.read_fwf(wth_file_path, skiprows=4)

    START_TRAIN = 1980; 
    END_TRAIN = 2009

    infile = open(file_name, 'rb')
    tab = pickle.load(infile)


    years = set(tab['year'])



    att_functs = [  'max_p_1_day_prior_N' ,
                    'max_p_3_day_prior_N',
                    'max_p_5_day_prior_N',
                    'dry_days_before_N',
                    'total_p_1_day_prior_N',
                    'total_p_3_day_prior_N',
                    'total_p_5_day_prior_N',
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
                    'total_precip_during_R4',
                    'freq_irr_during_v6',
                    'freq_irr_during_v7',
                    'freq_irr_during_v8',
                    'freq_irr_during_v9',
                    'freq_irr_during_v10',
                    'freq_irr_during_v11',
                    'freq_irr_during_v12',
                    'freq_irr_during_v13',
                    'freq_irr_during_v14',
                    'freq_irr_during_R1',
                    'freq_irr_during_R2',
                    'freq_irr_during_R3',
                    'freq_irr_during_R4',
                    'freq_precip_during_v6',
                    'freq_precip_during_v7',
                    'freq_precip_during_v8',
                    'freq_precip_during_v9',
                    'freq_precip_during_v10',
                    'freq_precip_during_v11',
                    'freq_precip_during_v12',
                    'freq_precip_during_v13',
                    'freq_precip_during_v14',
                    'freq_precip_during_R1',
                    'freq_precip_during_R2',
                    'freq_precip_during_R3',
                    'freq_precip_during_R4', 
                    'climate',
                    'total_p']
    

    # Do we calculate this term for every row, or just once per year? 
    single_val_per_year = [ False, # 'max_p_1_day_prior_N' 
                            False, # 'max_p_3_day_prior_N',
                            False, # 'max_p_5_day_prior_N',
                            False, # dry_days_before_N
                            False, # total_wat_1_day_prior_N
                            False, # total_wat_3_day_prior_N
                            False, # total_wat_5_day_prior_N
                            False, # application_count', 
                            False, # total_irrigation', 
                            False, # yield_', 
                            False, # front',
                            False, # leaching',
                            False, # minimum_irr',
                            False, # maximum_irr', 
                            True,  # number_of_precipitation_events', 
                            False, # growth_period_of_second_N_app' ,
                            False, # total_irr_during_v6', 
                            False, # total_irr_during_v7',
                            False, # total_irr_during_v8',
                            False, # total_irr_during_v9',
                            False, # total_irr_during_v10', 
                            False, # total_irr_during_v11',
                            False, # total_irr_during_v12',
                            False, # total_irr_during_v13',
                            False, # total_irr_during_v14',
                            False, # total_irr_during_R1', 
                            False, # total_irr_during_R2', 
                            False, # total_irr_during_R3', 
                            False, # total_irr_during_R4',
                            True,  # total_precip_during_v6',
                            True,  # total_precip_during_v7',
                            True,  # total_precip_during_v8',
                            True,  # total_precip_during_v9',
                            True,  # total_precip_during_v10',
                            True,  # total_precip_during_v11',
                            True,  # total_precip_during_v12',
                            True,  # total_precip_during_v13',
                            True,  # total_precip_during_v14',
                            True,  # total_precip_during_R1', 
                            True,  # total_precip_during_R2',
                            True,  # total_precip_during_R3',
                            True,  # total_precip_during_R4',
                            False, # freq_irr_during_v6',
                            False, # freq_irr_during_v7',
                            False, # freq_irr_during_v8',
                            False, # freq_irr_during_v9',
                            False, # freq_irr_during_v10',
                            False, # freq_irr_during_v11',
                            False, # freq_irr_during_v12',
                            False, # freq_irr_during_v13',
                            False, # freq_irr_during_v14',
                            False, # freq_irr_during_R1',
                            False, # freq_irr_during_R2',
                            False, # freq_irr_during_R3',
                            False, # freq_irr_during_R4',
                            True,  # freq_precip_during_v6',
                            True,  # freq_precip_during_v7',
                            True,  # freq_precip_during_v8',
                            True,  # freq_precip_during_v9',
                            True,  # freq_precip_during_v10',
                            True,  # freq_precip_during_v11',
                            True,  # freq_precip_during_v12',
                            True,  # freq_precip_during_v13',
                            True,  # freq_precip_during_v14',
                            True,  # freq_precip_during_R1',
                            True,  # freq_precip_during_R2',
                            True,  # freq_precip_during_R3',
                            True,  # freq_precip_during_R4',
                            True,  # climate
                            True]  # total_p


    # Sanity checks
    if len(single_val_per_year) != len(att_functs):
        print("Error: attribute function list and single-val-per-year different sizes (%d vs %d)" % (len(single_val_per_year) , len(att_functs)))
        sys.exit(1)

    if len(set(att_functs)) != len(att_functs):
        print("Error: duplicate attributes found. Please fix")
        sys.exit(1)


    # Take data from previous runs into consideration
    if append_mode:
        infile = open(tab_to_append_path, 'rb')           
        print('Loading output file...')
        tab_to_append = pickle.load(infile) 
        print('Done')
        cols_calculated = tab_to_append.columns.values.tolist()
        to_skip = {att_functs.index(col) for col in cols_calculated[1:]}

        att_functs = [col for (i, col) in enumerate(att_functs) if i not in to_skip ]
        single_val_per_year = [col for (i, col) in enumerate(single_val_per_year) if i not in to_skip ]


        if len(att_functs) == 0: 
            print("Nothing to do. All attributes already calculated")
            sys.exit(1)

        print("Calculating the following attributes")
        print(att_functs)

    raw_table = {'year': []}


    # Calculate dry, normal, and wet years in this climate

    total_p = {}
    
    for year in years: 

        year_modded = int((year  % 1e2) * 1e3) 
        season_start_doy = int(gdd_tab[gdd_tab['Year'] == year].P)
        season_end_doy  = int(gdd_tab[gdd_tab['Year'] == year].R6)

        season_start_date = year_modded + season_start_doy
        season_end_date  = year_modded + season_end_doy

        wth_mask = np.logical_and(wth_tab['@DATE'] >= season_start_date, wth_tab['@DATE'] <=  season_end_date)

        total_p[year] = sum(wth_tab[wth_mask]['RAIN']) 


    test_total_p = {year: total_p[year] for year in total_p if year >= START_TRAIN and year <= END_TRAIN }

    sorted_p = list(test_total_p.values())
    
    sorted_p.sort()

    print(len(sorted_p))

    oneThird = int(len(sorted_p)/3);
    twoThird = int((len(sorted_p)*2)/3);

    normalThreshold = statistics.mean([sorted_p[oneThird-1], sorted_p[oneThird]])
    wetThreshold = statistics.mean([sorted_p[twoThird-1], sorted_p[twoThird]])


    # initialize the attribute functions
    for att_funct in att_functs: 
        raw_table[att_funct] = []

    # Split up the data by year, with each thread focusing on a single year
    # preventing race conditions while using shared tables
    tab_by_years = {}
    procr_by_years = {}

    print("Splitting parameters and input tables")
    for year in years: 
        tab_by_years[year] = (tab[tab['year'] == year]).copy()

        # Set up the processing agent 
        year_modded = int((year  % 1e2) * 1e3)

        wth_year_mask = np.logical_and(wth_tab['@DATE'] > year_modded, wth_tab['@DATE'] <= (year_modded + 366))
        specific_wth_tab = wth_tab[wth_year_mask].copy()
        specific_gdd_tab = gdd_tab[gdd_tab['Year'] == year].copy()

        procr_by_years[year] = AttProcessors(specific_wth_tab, specific_gdd_tab, total_p[year], normalThreshold, wetThreshold)

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


    if append_mode:

        print("Appending to existing table...")
        for key in raw_table.keys():
            if key == "year": 
                continue
            else: 
                tab_to_append[key] = raw_table[key]
       
        new_tab_file = open(new_tab_path, 'wb')

        pickle.dump(tab_to_append, new_tab_file) 
                        

    else:
        # Build the attribute table    
        attribute_table = pd.DataFrame(raw_table)

        output_dir = "/".join(sys.argv[0].split("/")[0:-1])

        output = open('%s/attr_tab.pkl' % output_dir, 'wb')
        pickle.dump(attribute_table, output)


