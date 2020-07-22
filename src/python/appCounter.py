import numpy as np
from plotHV import get_nondoms

def app_counter(varz, obj, vars2exclude=[], objs2exclude=[]):

    objs_to_include = set(range(np.size(obj, 1)))

    for obj2exclude in objs2exclude:
        objs_to_include.remove(obj2exclude)

    # Ignore the middle column, because it's all zeros 
    varz = varz[get_nondoms(obj[:,list(objs_to_include)]),:]

    col_count = np.size(varz,1)

    cols = set(range(col_count))

    for col2ex in vars2exclude: 
        cols.remove(col2ex)

    varz = varz[:,list(cols)]

    varz[varz != 0] = 1

    totals_ones = np.sum(varz,1)    

    return totals_ones


if __name__ == '__main__':

    var_file = "/Users/iankropp/tempMount/run4/batch2020-07-16_16-23-26/gendat_with_run/run0000_gen0199_var.csv"
    obj_file = "/Users/iankropp/tempMount/run4/batch2020-07-16_16-23-26/gendat_with_run/run0000_gen0199_obj.csv"

    varz = np.genfromtxt(var_file, delimiter=',')
    obj  = np.genfromtxt(obj_file, delimiter=',')

    o2exclude = [1]

    v2exclude = [102]

    print(app_counter(varz, obj, v2exclude, o2exclude))



