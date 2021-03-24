import numpy as np
import sys


var_file = sys.argv[1]
indv_num = sys.argv[2]

# Format [yyyyddd,yyyyddd;yyyyddd,yyyyddd]
raw_date_ranges = sys.argv[3]

print(var_file)
print(indv_num)

date_ranges = np.array(np.matrix(raw_date_ranges))

print(date_ranges)




