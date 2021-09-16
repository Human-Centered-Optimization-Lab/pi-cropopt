
#install.packages("caret")

library(caret)

INPUT_FEATURES = "Z:\\Gilgamesh\\kroppian\\agovization_results\\mlearning\\features.feather"
INPUT_TARGETS = "Z:\\Gilgamesh\\kroppian\\agovization_results\\mlearning\\targets.feather"

## Fetch data

features_raw <- arrow::read_feather(INPUT_FEATURES)
features <- as_tibble(features_raw)

targets_raw <- arrow::read_feather(INPUT_TARGETS)
targets <- as_tibble(targets_raw)

## Split data

set.seed(20210915)
inTraining <- createDataPartition(targets$front, p = .75, list = FALSE)

trainingFeatures <- features[inTraining,]
trainingTargets <- targets[inTraining,]

testFeatures <- features[-inTraining,]
testTargets <- targets[-inTraining,]


## Train model 
#lassoFit <- train(trainingFeatures, 
#                  trainingTargets$front, 
#                  method="lasso", 
#                  verbose = TRUE)

