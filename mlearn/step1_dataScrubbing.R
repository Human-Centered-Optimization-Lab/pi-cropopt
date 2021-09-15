#install.packages("arrow")
#install.packages("caret")
#install.packages("tidymodels")
#install.packages("tibble")

library(magrittr)
library(tidymodels)
library(caret)
library(feather);
library(tibble)
library(dplyr)


## Constants
TAB_PATH = "Z:\\Gilgamesh\\kroppian\\agovization_results\\mlearning\\2021-09-10_13-31_attr_tab.feather"
#TAB_PATH = "/Users/iankropp/Projects/agovization/mlearn/2021-09-10_13-31_attr_tab.feather"
STAGES <- c("P","V6",  "V7", "V8", "V9", "V10",  "V11", "V12", "V13", "V14", "R1", "R2", "R3", "R4")
PREDICTOR_COLS = c()



targets <- c('yield_',
             'total_irrigation',
             'leaching',
             'front')

predictors <- c('application_count',
               'minimum_irr',
               'maximum_irr',
               'number_of_precipitation_events',
               'growth_period_of_second_N_app' ,
               'total_irr_during_v6',
               'total_irr_during_v7',
               'total_irr_during_v8',
               'total_irr_during_v9',
               'total_irr_during_v10',
               'total_irr_during_v11',
               'total_irr_during_v12',
               'total_irr_during_v13',
               'total_irr_during_v14',
               'total_irr_during_R1',
               'total_irr_during_R2',
               'total_irr_during_R3',
               'total_irr_during_R4',
               'total_precip_during_v6',
               'total_precip_during_v7',
               'total_precip_during_v8',
               'total_precip_during_v9',
               'total_precip_during_v10',
               'total_precip_during_v11',
               'total_precip_during_v12',
               'total_precip_during_v13',
               'total_precip_during_v14',
               'total_precip_during_R1',
               'total_precip_during_R2',
               'total_precip_during_R3',
               'total_precip_during_R4',
               'freq_irr_during_v6',
               'freq_irr_during_v7',
               'freq_irr_during_v8',
               'freq_irr_during_v9',
               'freq_irr_during_v10',
               'freq_irr_during_v11',
               'freq_irr_during_v12',
               'freq_irr_during_v13',
               'freq_irr_during_v14',
               'freq_irr_during_R1',
               'freq_irr_during_R2',
               'freq_irr_during_R3',
               'freq_irr_during_R4',
               'freq_precip_during_v6',
               'freq_precip_during_v7',
               'freq_precip_during_v8',
               'freq_precip_during_v9',
               'freq_precip_during_v10',
               'freq_precip_during_v11',
               'freq_precip_during_v12',
               'freq_precip_during_v13',
               'freq_precip_during_v14',
               'freq_precip_during_R1',
               'freq_precip_during_R2',
               'freq_precip_during_R3',
               'freq_precip_during_R4')

## Functions
stage2num <- function(stage){
  grep(toString(stage), STAGES)
}


print("Reading data...")
## Read data
attribute_tab_raw <- arrow::read_feather(TAB_PATH)
attribute_tab <- as_tibble(attribute_tab_raw)

print("Done. Tidying up data...")
attribute_tab['growth_period_of_second_N_app'] <- 
  attribute_tab['growth_period_of_second_N_app'] %>%
  apply(MARGIN=1, stage2num)

# Exclude columns with zero variance (all the same values)
# Note 1: nearZeroVar(attribute_tab, saveMetrics = TRUE) for more granular results
# Note 2: change the frequency cut-off if you want to remove features that are
#         very low variance but don't have zero 
zeroVars = nearZeroVar(attribute_tab, freqCut = 10000)

predictors <- colnames(attribute_tab)[-zeroVars]

attribute_tab <- attribute_tab[, -zeroVars]


## Split up into features and targets
features <-
  attribute_tab %>%
  select(all_of(predictors))

targets <- 
  attribute_tab %>%
  select(all_of(targets))

## Correlation analysis
print("Done. Running correlation analysis...")
# TODO remove this once we've figured out the proper reason there's NA in the data
nanVals <- which(!is.finite(features$minimum_irr))
features <- features[-nanVals,]
targets <- targets[-nanVals,]

corrMat <- cor(features)
corrs <- findCorrelation(corrMat, cutoff=0.75)

non_corr_features = features[-corrs]

# TODO Should I center and scale? 
# print("Done. Scaling and centering ")
# features <- preProcess(features, method = c("center", "scale"))
  

# Thoughts: 
# Machine learning algorithm should be non-black box in order to find innovations
# https://towardsdatascience.com/machine-learning-interpretability-techniques-662c723454f3




