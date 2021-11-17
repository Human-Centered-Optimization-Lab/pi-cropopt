library(dplyr)
library(fitdistrplus)
library(magrittr)



## Reading data 

ROOT_PATH <- "/Volumes/data/Gilgamesh/kroppian/agovization_results/validation/"
ROOT_PATH <- "Z:/Gilgamesh/kroppian/agovization_results/validation/"

COMM_PRACT_PATH <- paste(ROOT_PATH, "comm_pract.feather", sep = "")

comm_pract <- arrow::read_feather(COMM_PRACT_PATH)     

## Pre-processing

comm_pract <- comm_pract %>%
              mutate(yield_dev_from_med = median(comm_pract$yield) - comm_pract$yield)


comm_pract <- comm_pract %>%
              mutate(leaching_dev_from_med = median(comm_pract$leaching) - comm_pract$leaching)

comm_pract_clim <- comm_pract %>% filter(year < 2010)


## Clear the decks
if(! is.null(dev.list())){
  dev.off(dev.list()["RStudioGD"]) # Clears plots
}


## Get basic visual 

hist(comm_pract_clim$yield_dev_from_med)
hist(comm_pract_clim$leaching_dev_from_med)


## Calculate deviation from median value



## Determine the best distribution
descdist(comm_pract_clim$yield_dev_from_med, discrete = FALSE, boot=500)

descdist(comm_pract_clim$leaching_dev_from_med, discrete = FALSE, boot=500)


# Log-normal looks nice...
lnorm_dist_yield <- fitdist(comm_pract_clim$yield_dev_from_med, "lnorm", method="mme", boot=100)
plot(lnorm_dist_yield)


lnorm_dist_leaching <- fitdist(comm_pract_clim$leaching_dev_from_med, "lnorm", method="mme", boot=100)
plot(lnorm_dist_leaching)



