
class dssat4dum():


    def __init__(self, home, fileio, tmp_dir):

        self.home = home
        self.fileio = fileio
        self.tmp_dir = tmp_dir

        # Set up run directories 


    def editIrr(self, irrsched):

        # Read data 
        file_name = "DSSAT47.INP"
        reader = open(file_name, "r")

        raw_txt = reader.readlines()

        # Constants
#        dat = np.array([
#                [2017150,1.0],
#                [2017161,3.22],
#                [2017171,14.1],
#                [2017181,34.1],
#                [2017191,3.6],
#                [2017201,7.4],
#                [2017211,4.4],
#                [2017222,31.2],
#                [2017232,5.7],
#                [2017242,1.1]
#            ])

        frmdatarr = np.apply_along_axis(
                (lambda a : "   %d IR001  %f" % (a[0], a[1])),
                1,irrsched
                )

        frmdat = reduce(
                lambda a,b : "%s\n\r%s" % (a,b) 
                ,frmdatarr
                )

        # Parse file and insert values 

        raw_result = ""
        irrigation_it = -1

        for line in raw_txt:

            if "*IRRIGATION" in line:
                irrigation_it += 1

            if irrigation_it >= 0: 
                irrigation_it += 1        

            if irrigation_it <= 2 :
                raw_result = "%s%s" % (raw_result, line)

            if irrigation_it == 3:
                raw_result = "%s%s\n\r" % (raw_result, frmdat)

            if "*FERTILIZERS" in line:
                raw_result = "%s%s" % (raw_result, line)
                irrigation_it = -1


        print(raw_result)


