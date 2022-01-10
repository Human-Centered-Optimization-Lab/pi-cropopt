library(dplyr)
library(fitdistrplus)
library(magrittr)

## Reading data 

ROOT_PATH <- "Z:/Gilgamesh/kroppian/agovization_results/validation/"
ROOT_PATH <- "/Volumes/data/Gilgamesh/kroppian/agovization_results/validation/"

COMM_PRACT_PATH           <- paste(ROOT_PATH,           "comm_pract.feather", sep = "")
IRR_ONLY_RESULT_PATH      <- paste(ROOT_PATH,      "irr_only_result.feather", sep = "")
NITRO_ONLY_RESULT_PATH    <- paste(ROOT_PATH,    "nitro_only_result.feather", sep = "")
ALL_RECS_RESULT_PATH      <- paste(ROOT_PATH, "all_recs_full_result.feather", sep = "")

comm_pract           <- arrow::read_feather(COMM_PRACT_PATH)     
irr_only_result      <- arrow::read_feather(IRR_ONLY_RESULT_PATH)  
nitro_only_result    <- arrow::read_feather(NITRO_ONLY_RESULT_PATH)
all_recs_result      <- arrow::read_feather(ALL_RECS_RESULT_PATH)

## Clear the decks
if(! is.null(dev.list())){
  dev.off(dev.list()["RStudioGD"]) # Clears plots
}

## Get basic visual 
hist(comm_pract$yield        , main="Common practices")
hist(irr_only_result$yield   , main="Irrigation only")
hist(nitro_only_result$yield , main = "Nitrogen only")
hist(all_recs_result$yield   , main = "All recommendations")


## Analyze shape of distribution
descdist(comm_pract$yield        , discrete = FALSE, boot=500)
descdist(irr_only_result$yield   , discrete = FALSE, boot=500)
descdist(nitro_only_result$yield , discrete = FALSE, boot=500)
descdist(all_recs_result$yield   , discrete = FALSE, boot=500)

## Log-normal looks good...
lnorm_dist_comm_pract <- fitdist(comm_pract$yield        , "norm", method="mme", boot=100)
lnorm_dist_irr_only   <- fitdist(irr_only_result$yield   , "norm", method="mme", boot=100)
lnorm_dist_nitro_only <- fitdist(nitro_only_result$yield , "norm", method="mme", boot=100)
lnorm_dist_all_recs   <- fitdist(all_recs_result$yield   , "norm", method="mme", boot=100)


plot(lnorm_dist_comm_pract  )
plot(lnorm_dist_irr_only   )
plot(lnorm_dist_nitro_only )
plot(lnorm_dist_all_recs   )



t.test(comm_pract$yield, irr_only_result$yield)
wilcox.test(comm_pract$yield, irr_only_result$yield)
