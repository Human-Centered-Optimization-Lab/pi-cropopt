
#install.packages("caret")

library(caret)

INPUT_FEATURES = "/Users/iankropp/Projects/agovization/mlearn/features.feather"
INPUT_TARGETS = "/Users/iankropp/Projects/agovization/mlearn/targets.feather"
ATTRIB_TAB_PATH = "/Users/iankropp/Projects/agovization/mlearn/attr_tab_cleaned.feather"

OUTPUT_RESULTS = "/Users/iankropp/Projects/agovization/mlearn/lassoResults"

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

# Bootstrap by default 
# 25 bootstrapped iterations by default 
# No repeats (only for cross validation)
fitControl <- trainControl(verboseIter = TRUE) 

## Train model 
#lassoFitFront <- train(trainingFeatures, 
#                  trainingTargets$front,
#                  method="lasso",
#                  trControl = fitControl)

#lassoFitYield <- train(trainingFeatures, 
#                  trainingTargets$yield_,
#                  method="lasso",
#                  trControl = fitControl)


lassoFitLeaching <- train(trainingFeatures, 
                  trainingTargets$leaching,
                  method="lasso",
                  trControl = fitControl)

save(lassoFitLeaching, lassoFitYield, file=OUTPUT_RESULTS)
