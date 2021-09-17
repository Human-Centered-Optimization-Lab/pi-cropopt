
#install.packages("caret")
#install.packages("arrow")

library(caret)
library(arrow)
library(tibble)
library(dplyr)


setwd(dirname(rstudioapi::getActiveDocumentContext()$path))


INPUT_FEATURES = "features.feather"
INPUT_TARGETS = "targets.feather"

OUTPUT_RESULTS = "ctreeResults"

## Fetch data

#features_raw <- arrow::read_feather(INPUT_FEATURES)
#features <- as_tibble(features_raw)
#
#targets_raw <- arrow::read_feather(INPUT_TARGETS)
#targets <- as_tibble(targets_raw)


features <- arrow::read_feather(INPUT_FEATURES)

targets <- arrow::read_feather(INPUT_TARGETS)



## Build data tables

# front (convert to a logical column)

targets <- targets %>%
  mutate_at(c('front'), 
            function(x){ 
              unlist(lapply(x, function(q){if(q == 0){1}else{0}}))
            })

# create front data table
front <- targets$front
frontData <- cbind(front, features)


fitControl <- trainControl(verboseIter = TRUE) 


frontFit <- train(front ~ ., data = frontData, 
                 method = "ctree", 
                 trControl = fitControl)
