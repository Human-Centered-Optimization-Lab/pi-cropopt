
import numpy as np

x_test = np.array([[8.96974835,4.24981969,15.40060848,7.38144512,7.2217787,13.35792159,8.3815397,12.36294695,9.01902257,16.77818999,18.50918099],[8.38196054,11.09590262,9.50832788,3.41864267,1.23497674,19.28186103, 17.45579774,16.50748783,17.68503801,12.55233018,7.85086274],[10.03317502,6.90240853,5.74250271,11.01573132,18.36455383,15.11673411, 5.51344392,2.74220688,4.15210609,2.29368001,17.47098477], [11.7808606,4.62367014,8.24435338,8.33908889,11.15099752,7.74199703, 1.07489177,17.12679691,12.89792451,7.99779897,2.77245013], [1.80591082,1.8934317,1.89904564,3.27843295,9.69201471,1.86741162, 14.06751382,14.67847153,13.36613686,10.0733742,2.93633576], [15.30882873,18.93717429,16.49167567,6.82126282,16.06309392,4.79008814, 12.17775499,11.87885256,17.57782846,0.49956635,8.03242551], [1.58390138,2.6979587,18.70615039,18.42152749,15.70259525,14.69495897, 10.44709095,17.53772159,4.45254853,1.81441945,16.77494849], [18.54359918,1.82954508,6.46771175,2.29796448,17.56415679,8.68669003, 0.24358004,11.00593966,14.63585026,14.6103312,11.44652677]])

date_ranges_test = np.array([[2018135, 2018140,1,20], [2018200, 2018204,0,19]])



def _calc_period_indices(date_ranges):
    
    res = []  
    
    offset = 0 
    for period in range(0, np.size(date_ranges, 0)):
        MIN_DATE = 0
        MAX_DATE = 1
        minDate = date_ranges[period,MIN_DATE]
        maxDate = date_ranges[period,MAX_DATE]

        minindex = offset
        maxindex = minindex + (maxDate - minDate)  + 1

        res.append((minindex, maxindex))
        
        offset = (maxDate - minDate) + 1
        
    return res

def _build_applications(x, date_ranges): 

    app_count = np.size(x, 1)

    pop_size = np.size(x, 0)

    irrscheds = np.ones((pop_size, app_count, 2)) * -1

    period_inds = _calc_period_indices(date_ranges)

    # plug in the genome
    irrscheds[:, :, 1 ] = x

    # Plug in the dates
    for periodInd, period in enumerate(period_inds): 

        startInd = period[0]
        endInd = period[1]

        startDate = date_ranges[periodInd][0]
        endDate = date_ranges[periodInd][1]
        irrscheds[:,startInd:endInd, 0 ] = np.array(range(startDate,endDate+1))    

    print(irrscheds)
    print(np.shape(irrscheds))

_build_applications(x_test, date_ranges_test)

print(np.shape(x_test))
print(np.shape(date_ranges_test))

