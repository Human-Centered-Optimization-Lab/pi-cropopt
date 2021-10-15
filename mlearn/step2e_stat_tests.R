library(dplyr)
library(fitdistrplus)

ATTRIB_TAB <- "/Volumes/data/Gilgamesh/kroppian/agovization_results/mlearning/attrib_tab.feather"

attrib_tab <- arrow::read_feather(ATTRIB_TAB)

## Normalize yield across all years
max_yields <- attrib_tab %>%
              group_by(year) %>%
              summarize(year_max_yield = max(yield_)) 

norm_yield <- attrib_tab %>%
              inner_join(max_yields) %>%
              select(yield_, year_max_yield) %>%
              mutate(norm_yield = yield_ / year_max_yield) %>%
              pull(norm_yield)
       
attrib_tab$norm_yield <- norm_yield


## find high yielding solutions

# Get the threshold for high yields
  
high_yielders <- filter(attrib_tab, norm_yield > 0.75) %>%
                 filter(front == 0)

#high_yielders <- filter(attrib_tab, front == 0)


growth_stages <- c('total_wat_during_v6', 
                   'total_wat_during_v7', 
                   'total_wat_during_v8', 
                   'total_wat_during_v9',
                   'total_wat_during_v10', 
                   'total_wat_during_v11',
                   'total_wat_during_v12',
                   'total_wat_during_v13',
                   'total_wat_during_v14',
                   'total_wat_during_R1', 
                   'total_wat_during_R2',
                   'total_wat_during_R3',
                   'total_wat_during_R4')


dev.off(dev.list()["RStudioGD"]) # Clears plots

for(s in 1:length(growth_stages)){
  stage <- growth_stages[s]
  data <- high_yielders[,stage] %>% pull(stage) 

  print(min(data))
  
  hist(data, main=stage, xlab="Total irrigation")
  
}

