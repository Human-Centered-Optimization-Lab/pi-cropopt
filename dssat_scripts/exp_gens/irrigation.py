



template = """@I  EFIR  IDEP  ITHR  IEPT  IOFF  IAME  IAMT IRNAME
%s     1   -99   -99   -99   -99   -99   -99 -99
@I IDATE  IROP IRVAL
%s %s200 IR001     0"""

start_year = 1980
end_year = 2020


for (i,year) in enumerate(range(start_year, end_year)):

    i_str = "{:>2}".format(i+1)

    year_str = str(year)[2:4]
    print(template % (i_str, i_str, year_str))



