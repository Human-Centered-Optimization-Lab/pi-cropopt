
import numpy as np
import pandas as pd
import random
from pico.dssatmod.dssat4dum import Dssat4Dum
import shutil


def dateFormat(year, doy): 
    return doy + year * 1000

def dateFormatDSSAT(year, doy): 
    return doy + ((year % 100) * 1000)


def estimateApplication(year, application_number = 10, home_dir="/home/ian"):

    # Setup 

    print("Estimating application")

    result = {"initialApp" : -99, "maxApp": -99}

    plant_date = 135
    first_nitro_app_date = 135
    second_nitro_app_date = 196

    first_nitro_app_date = 135
    second_nitro_app_date = 196

    first_nitro_app_amount = 70
    second_nitro_app_amount = 150

    # Determine irrigation periods 
    # Agricultural parameters
    app_man_csv = "%s/Projects/pi-cropopt/management_dates.csv" % home_dir
    app_man = pd.read_csv(app_man_csv)

    irr_date_lb = min(app_man[app_man.Year < 2010].V8)
    irr_date_ub = max(app_man[app_man.Year < 2010].R2)

    # Account for leap years
    if (year % 4 == 0) and (year % 100 != 0): 
        plant_date += 1
        irr_date_lb += 1
        irr_date_ub += 1

        first_nitro_app_date += 1
        second_nitro_app_date += 1

        first_nitro_app_date += 1
        second_nitro_app_date += 1

    # DSSAT variables

    dssat_home  = "%s/Projects/pi-cropopt/dhome" % home_dir
    dssat_exe   = "%s/Projects/pi-cropopt/dhome/dscsm04758-linux" % home_dir
    dssat_inp   = "%s/Projects/pi-cropopt/dhome/DSSAT47.INP" % home_dir
    wth_file    = "%s/Projects/pi-cropopt/dhome/weather/CASS.WTH" % home_dir

    tmp_dir = "/dev/shm/prerun/"

    formatted_year = dateFormat(year, plant_date)
    year_updates = { 'pdate': formatted_year, 'sdate': formatted_year, 'icdat': formatted_year }

    # Figure out what irrigation amounts we want to trial 
    min_irr_trial = 5
    max_irr_trial = 80
    steps = int((max_irr_trial - min_irr_trial) / 5) + 1

    max_water_reqs = 800

    realizations = 100
    runs_per_batch = 100

    irr_amounts = np.linspace(min_irr_trial, max_irr_trial, num=steps)
    irr_amounts = np.expand_dims(irr_amounts, axis=1)


    def build_random_application(irr_amount):

        # Create a list of random dates 
        irr_dates = random.sample(range(irr_date_lb, irr_date_ub), application_number)
        irr_dates.sort()

        irr_dates = [dateFormat(year, id) for id in irr_dates]

        # Make empty application numpy array 
        applications = np.zeros((application_number + 2, 5)) 

        applications[0:application_number, 0] = irr_dates
        applications[0:application_number, 1] = irr_amount

        return applications


    def build_rainfed_trial():

        applications = np.zeros((1, 2, 5)) 

        applications[0][0, 2]  = first_nitro_app_amount
        applications[0][1, 2]  = second_nitro_app_amount

        applications[0][0, 0]  = dateFormat(year, first_nitro_app_date)
        applications[0][1, 0]  = dateFormat(year, second_nitro_app_date)

        return applications

    final_app_arr = []

    # For each irrigation amount in question
    for irr_amount in irr_amounts: 

        for r in range(realizations):
            # Install the irrigation applications
            application = build_random_application(irr_amount)

            application[application_number, 0]  = dateFormat(year, first_nitro_app_date)
            application[application_number + 1, 0]  = dateFormat(year, second_nitro_app_date)

            application[application_number, 2]  = first_nitro_app_amount
            application[application_number + 1, 2]  = second_nitro_app_amount

            final_app_arr.append(application)


    final_app_arr = np.array(final_app_arr)


    runner = Dssat4Dum(dssat_home, dssat_inp, dssat_exe, tmp_dir)

    print("Running simulation...")

    batches = int(final_app_arr.shape[0] / runs_per_batch)

    current_app = 0

    raw_results = np.zeros((final_app_arr.shape[0], 3))

    for b in range(batches): 

        runner.clean_workspace()

        print(f"Running application {current_app} to {current_app + runs_per_batch}")

        current_applications = final_app_arr[current_app: current_app + runs_per_batch, :]

        current_batch_res = runner.run_batch(current_applications, threads = 20, updates=year_updates)

        irr_totals = np.expand_dims(np.sum(current_applications, axis=1)[:,1], axis=1)

        current_batch_res = np.concatenate((current_batch_res, irr_totals), axis=1)

        raw_results[current_app: current_app + runs_per_batch, :] = current_batch_res


        current_app += runs_per_batch

    rainfed_application = build_rainfed_trial()
    runner.clean_workspace()
    res_np = runner.run_batch(rainfed_application, threads = 1, updates=year_updates)

    res_df = pd.DataFrame(res_np, columns=["yield", "leaching"])

    rain_fed_yield = res_df['yield'][0]

    s75th_perc = res_df['yield'].quantile(q=0.75)


    print(f"Rainfed irrigation yield: {rain_fed_yield}")
    print(f"75th percentile: {s75th_perc}")

    results = pd.DataFrame(raw_results, columns=["yield", "leaching", "irr_total"])

    results["irr_app_size"] = results["irr_total"] / application_number

    results.irr_app_size = results.irr_app_size.round().astype(int)
    results.irr_total = results.irr_total.round().astype(int)

    best_app_amount = results.groupby(by="irr_app_size")['yield'].median().idxmax()
    print(f"Best initial application amount for {year}: {best_app_amount}")

    result["initialApp"] = int(best_app_amount)

    results.groupby(by="irr_app_size")['yield'].median() 

    weather = pd.read_fwf(wth_file, skiprows=4)

    lb = dateFormatDSSAT(year, irr_date_lb)
    ub = dateFormatDSSAT(year, irr_date_ub)

    grow_s_wth = weather[np.logical_and(weather["@DATE"] >= lb, weather["@DATE"] <= ub)]

    total_rain = np.sum(grow_s_wth['RAIN'])

    max_app_amount = (max_water_reqs - total_rain)/application_number

    print(f"Max application amount: %d" % max_app_amount)

    result["maxApp"] = int(max_app_amount)

    return result





if __name__ == "__main__": 

    estimateApplication(1992)

