#!/usr/bin/env Rscript

args = commandArgs(trailingOnly=TRUE)
png(filename="plot.png", width = 960, height = 960, units = "px", pointsize = 20 )


currentMax1 = 0
currentMax2 = 0

xmax = 200
ymax = 13000
ymin = 0

# Get the file names of the data
withFiles = args[grepl("with_run.*\\.csv", args)]
withoutFiles = args[grepl("without_run.*\\.csv", args)]

# Establish labels
xlabel = expression('Y'[1])
ylabel = expression('Y'[2])
#title = paste("Sampling Sparsity", sparsity)
#title = paste("60 Variables, 16 Non-Zero Variables")
title = "Test"

filesFoundWith = length(withFiles)
filesFoundWithout = length(withoutFiles)

if(filesFoundWith != filesFoundWithout){
  print("Files with and files with out don't match") 
  stop()
}

if(filesFoundWith == 0){
  print("No files given") 
  stop()
}

# Iterate through without files
i = 0
for (file in withoutFiles){
  data = read.csv(file)
  data[,1] = data[,1]*-1

  if (i == 0)
    plot(data[,3],data[,1],col = "red", xlab=xlabel, ylab=ylabel, main=title, xlim=c(0,xmax), ylim=c(ymin,ymax))
  else
    points(data[,3],data[,1],col = "red")
  i = i + 1
  currentMax1 = max(c(currentMax1, data[,1])) 
  currentMax2 = max(c(currentMax2, data[,3])) 
}

# Iterate through with files
for (file in withFiles){
  data = read.csv(file)
  data[,1] = data[,1]*-1
  points(data[,3],data[,1],col = "blue")

  i = i + 1
  currentMax1 = max(c(currentMax1, data[,1])) 
  currentMax2 = max(c(currentMax2, data[,3])) 
}

print(paste("Max 1:", currentMax1))
print(paste("Max 2:", currentMax2))

