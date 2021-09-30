
library(feather);
library(AppliedPredictiveModeling)
library(caret)
library(dplyr)

# Get data 
FEATURES_PATH <- "/Volumes/data/Gilgamesh/kroppian/agovization_results/mlearning/features.feather"
TARGETS_PATH <- "/Volumes/data/Gilgamesh/kroppian/agovization_results/mlearning/targets.feather"
features <- arrow::read_feather(FEATURES_PATH)
targets <- arrow::read_feather(TARGETS_PATH)

# what features to investigate
#cols <- c("application_count","total_irrigation","minimum_irr","maximum_irr","number_of_precipitation_events","growth_period_of_second_N_app","total_irr_during_v6","total_irr_during_v7","total_irr_during_v8","total_irr_during_v9","total_irr_during_v10","total_irr_during_v11","total_irr_during_v12","total_irr_during_v13","total_irr_during_v14","total_irr_during_R1","total_irr_during_R2","total_irr_during_R3","total_irr_during_R4","total_precip_during_v6","total_precip_during_v7","total_precip_during_v8","total_precip_during_v9","total_precip_during_v10","total_precip_during_v11","total_precip_during_v12","total_precip_during_v13","total_precip_during_v14","total_precip_during_R1","total_precip_during_R2","total_precip_during_R3","total_precip_during_R4","freq_irr_during_v6","freq_irr_during_v7","freq_irr_during_v8","freq_irr_during_v9","freq_irr_during_v10","freq_irr_during_v11","freq_irr_during_v12","freq_irr_during_v13","freq_irr_during_v14","freq_irr_during_R1","freq_irr_during_R2","freq_irr_during_R3","freq_irr_during_R4","freq_precip_during_v8","freq_precip_during_v9","freq_precip_during_v10","freq_precip_during_v11","freq_precip_during_v12","freq_precip_during_v13","freq_precip_during_v14","freq_precip_during_R1","freq_precip_during_R2","freq_precip_during_R3","freq_precip_during_R4","climate","total_p")
cols <- c("application_count","total_irrigation","minimum_irr","maximum_irr","number_of_precipitation_events","growth_period_of_second_N_app","total_irr_during_v6","total_irr_during_v7","total_irr_during_v8","total_irr_during_v9","total_irr_during_v10","total_irr_during_v11","total_irr_during_v12","total_irr_during_v13","total_irr_during_v14","total_irr_during_R1","total_irr_during_R2","total_irr_during_R3","total_irr_during_R4","total_precip_during_v6","total_precip_during_v7","total_precip_during_v8","total_precip_during_v9","total_precip_during_v10","total_precip_during_v11","total_precip_during_v12","total_precip_during_v13","total_precip_during_v14","total_precip_during_R1","total_precip_during_R2","total_precip_during_R3","total_precip_during_R4","climate","total_p")

# Feature plot of Pareto Optimal solutions
optimal_mask <- targets$front == 0;
features_po <- features[which(optimal_mask),cols]
dummy_y <- integer(nrow(features_po))

caret::featurePlot(x = features_po, 
            y = dummy_y, 
            plot = "pairs",
            ## Add a key at the top
            auto.key = list(columns = 3))




