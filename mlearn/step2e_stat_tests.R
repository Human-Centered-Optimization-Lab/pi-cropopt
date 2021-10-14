library(dplyr)

ATTRIB_TAB <- "/Volumes/data/Gilgamesh/kroppian/agovization_results/mlearning/attrib_tab.feather"

attrib_tab <- arrow::read_feather(ATTRIB_TAB)

## find high yielding solutions

# Get the threshold for high yields
yields <- attrib_tab$yield_
yield_count <- length(yields)
sorted_yields <- sort(yields)
quartile_locale <- round(yield_count * 0.75)
quartile_threshold <- sorted_yields[quartile_locale]
  
high_yielders <- filter(attrib_tab, yield_ > quartile_threshold) %>%
                 filter(front == 0) %>%
                 filter(climate == 2) 

#high_yielders <- filter(attrib_tab, front == 0)

dev.off(dev.list()["RStudioGD"]) # Clears plots
histogram(high_yielders$total_wat_during_v6,  nint=30)
histogram(high_yielders$total_wat_during_v7,  nint=30)
histogram(high_yielders$total_wat_during_v8,  nint=30)
histogram(high_yielders$total_wat_during_v9,  nint=30)
histogram(high_yielders$total_wat_during_v10, nint=30)
histogram(high_yielders$total_wat_during_v11, nint=30)
histogram(high_yielders$total_wat_during_v12, nint=30)
histogram(high_yielders$total_wat_during_v13, nint=30)
histogram(high_yielders$total_wat_during_v14, nint=30)
histogram(high_yielders$total_wat_during_R1,  nint=30)
histogram(high_yielders$total_wat_during_R2,  nint=30)
histogram(high_yielders$total_wat_during_R3,  nint=30)
histogram(high_yielders$total_wat_during_R4,  nint=30)

