#install.packages("arrow")
#install.packages("caret")
#install.packages("tidymodels")
#install.packages("tibble")

library(magrittr)
library(caret)
library(feather);
library(tibble)
library(dplyr)


## Constants

OUTPUT_FEATURES = "Z:\\Gilgamesh\\kroppian\\agovization_results\\mlearning\\features.feather"
OUTPUT_TARGETS = "Z:\\Gilgamesh\\kroppian\\agovization_results\\mlearning\\targets.feather"
OUTPUT_ATTRIB_TAB = "Z:\\Gilgamesh\\kroppian\\agovization_results\\mlearning\\attrib_tab.feather"
#OUTPUT_FEATURES = "/Volumes/data/Gilgamesh/kroppian/agovization_results/mlearning/features.feather"
#OUTPUT_TARGETS = "/Volumes/data/Gilgamesh/kroppian/agovization_results/mlearning/targets.feather"
#OUTPUT_ATTRIB_TAB = "/Volumes/data/Gilgamesh/kroppian/agovization_results/mlearning/attrib_tab.feather"


TAB_PATH = "Z:\\Gilgamesh\\kroppian\\agovization_results\\mlearning\\2021-11-03_14-34_attr_tab.feather"
#TAB_PATH = "/Volumes/data/Gilgamesh/kroppian/agovization_results/mlearning/2021-11-03_14-34_attr_tab.feather"
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
               'freq_precip_during_R4',
               'climate',
               'total_p',
               'dry_days_before_N',
               'total_p_1_day_prior_N',
               'total_p_3_day_prior_N',
               'total_p_5_day_prior_N',
               'max_p_1_day_prior_N',
               'max_p_3_day_prior_N',
               'max_p_5_day_prior_N')

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
predictors <- predictors[-which(predictors == "front")]
predictors <- predictors[-which(predictors == "yield_")]
predictors <- predictors[-which(predictors == "leaching")]
predictors <- predictors[-which(predictors == "year")]


attribute_tab <- attribute_tab[, -zeroVars]

## Add the total_wat cols 
attribute_tab$total_wat_during_v6  <- attribute_tab$total_irr_during_v6  + attribute_tab$total_precip_during_v6;
attribute_tab$total_wat_during_v7  <- attribute_tab$total_irr_during_v7  + attribute_tab$total_precip_during_v7;
attribute_tab$total_wat_during_v8  <- attribute_tab$total_irr_during_v8  + attribute_tab$total_precip_during_v8;
attribute_tab$total_wat_during_v9  <- attribute_tab$total_irr_during_v9  + attribute_tab$total_precip_during_v9;
attribute_tab$total_wat_during_v10 <- attribute_tab$total_irr_during_v10 + attribute_tab$total_precip_during_v10;
attribute_tab$total_wat_during_v11 <- attribute_tab$total_irr_during_v11 + attribute_tab$total_precip_during_v11;
attribute_tab$total_wat_during_v12 <- attribute_tab$total_irr_during_v12 + attribute_tab$total_precip_during_v12;
attribute_tab$total_wat_during_v13 <- attribute_tab$total_irr_during_v13 + attribute_tab$total_precip_during_v13;
attribute_tab$total_wat_during_v14 <- attribute_tab$total_irr_during_v14 + attribute_tab$total_precip_during_v14;
attribute_tab$total_wat_during_R1  <- attribute_tab$total_irr_during_R1  + attribute_tab$total_precip_during_R1;
attribute_tab$total_wat_during_R2  <- attribute_tab$total_irr_during_R2  + attribute_tab$total_precip_during_R2;
attribute_tab$total_wat_during_R3  <- attribute_tab$total_irr_during_R3  + attribute_tab$total_precip_during_R3;
attribute_tab$total_wat_during_R4  <- attribute_tab$total_irr_during_R4  + attribute_tab$total_precip_during_R4;



## Split up into features and targets
features <-
  attribute_tab %>%
  dplyr::select(all_of(predictors))

targets <- 
  attribute_tab %>%
  dplyr::select(all_of(targets))


## Write to output
arrow::write_feather(features, OUTPUT_FEATURES)
arrow::write_feather(targets, OUTPUT_TARGETS)
arrow::write_feather(attribute_tab, OUTPUT_ATTRIB_TAB)
