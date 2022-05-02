template = """@F FDATE  FMCD  FACD  FDEP  FAMN  FAMP  FAMK  FAMC  FAMO  FOCD FERNAME
%s %s200 FE001 AP001    10     0   -99   -99   -99   -99   -99 -99"""


start_year = 1980
end_year = 2020


for (i,year) in enumerate(range(start_year, end_year)):

    i_str = "{:>2}".format(i+1)

    year_str = str(year)[2:4]
    print(template % (i_str, year_str))







