library(dplyr)

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
  
high_yielders <- filter(attrib_tab, norm_yield > 0.75) 

#high_yielders <- filter(attrib_tab, front == 0)

dev.off(dev.list()["RStudioGD"]) # Clears plots
histogram(high_yielders$total_wat_during_v6,  nint=60)
histogram(high_yielders$total_wat_during_v7,  nint=60)
histogram(high_yielders$total_wat_during_v8,  nint=60)
histogram(high_yielders$total_wat_during_v9,  nint=60)
histogram(high_yielders$total_wat_during_v10, nint=60)
histogram(high_yielders$total_wat_during_v11, nint=60)
histogram(high_yielders$total_wat_during_v12, nint=60)
histogram(high_yielders$total_wat_during_v13, nint=60)
histogram(high_yielders$total_wat_during_v14, nint=60)
histogram(high_yielders$total_wat_during_R1,  nint=60)
histogram(high_yielders$total_wat_during_R2,  nint=60)
histogram(high_yielders$total_wat_during_R3,  nint=60)
histogram(high_yielders$total_wat_during_R4,  nint=60)


