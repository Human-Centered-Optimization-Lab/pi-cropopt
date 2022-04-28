import pandas as pd


def printRow(contents, indent_count=0):
   
    indent = "".join(["  "] * indent_count)

    print("%s%s" % (indent, contents))

PRETTY_TAB_PATH = '/mnt/nas/kroppian/agovization_results/validation/pretty_tab.csv'
PRETTY_TAB_OUT  = '/mnt/nas/kroppian/agovization_results/validation/pretty_tab.html'

pretty_tab = pd.read_csv(PRETTY_TAB_PATH)



printRow("<table>")

# For every row
for index, row in pretty_tab.iterrows():

    # Start -- row
    printRow("<tr>", 1)
     
    # Start -- Year
    printRow("<td>", 2)

    year = int(row['year'])
      
    # Add climate letter
    if row['climate'] == 0:
        clime_text = "d"
    elif row['climate'] == 1:
        clime_text = "n"
    elif row['climate'] == 2:
        clime_text = "w"


    year_text  = "%d<sup><i>%s</i></sup>" % (year, clime_text)

    printRow(year_text, 3)

    printRow("</td>", 2)
    # End -- Year

   
    # Start -- common practices

    printRow("<td>%d</td>" % row['yield'], 2)
    printRow("<td>%.2f</td>" % row['leaching'], 2)
    printRow("<td>%.2f</td>" % row['total_wat'], 2)
    printRow("<td>%.2f</td>" % row['wat_eff'], 2)

    # End -- common practices
    

    # Start -- innovized practices

    for strategy in ["irr_only_", "nitr_only_", "all_rec_"]:

        yield_key = strategy + 'yield'
        leaching_key = strategy + 'leaching'
        total_wat_key = strategy + 'total_wat'
        wat_eff_key = strategy + 'wat_eff'

        yield_ = row[yield_key]
        leaching = row[leaching_key]
        total_wat = row[total_wat_key]
        wat_eff = row[wat_eff_key]


        # Yield 

        if yield_ > row['yield']:
            super_script = "+"
        elif yield_ < row['yield']:
            super_script = "−"
        else:
            super_script = "="

        printRow("<td>%d<sup><i>%s</i></sup></td>" %   (yield_, super_script), 2)

        # Leaching
        if leaching < row['leaching']:
            super_script = "+"
        elif leaching > row['leaching']:
            super_script = "−"
        else:
            super_script = "="

        printRow("<td>%.2f<sup><i>%s</i></sup></td>" % (leaching, super_script), 2)

        # Total water 
        if total_wat < row['total_wat']:
            super_script = "+"
        elif total_wat > row['total_wat']:
            super_script = "−"
        else:
            super_script = "="

        printRow("<td>%.2f<sup><i>%s</i></sup></td>" % (total_wat, super_script), 2)

        # Water efficiency 
        if wat_eff > row['wat_eff']:
            super_script = "+"
        elif wat_eff  < row['wat_eff']:
            super_script = "−"
        else:
            super_script = "="

        printRow("<td>%.2f<sup><i>%s</i></sup></td>" % (wat_eff, super_script), 2)

    # End -- innovized practices


    # End row
    printRow("</tr>", 1)


printRow("</table>")

