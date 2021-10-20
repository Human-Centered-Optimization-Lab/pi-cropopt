library(dplyr)
library(fitdistrplus)
library(R.utils)
library(stringr)

#ATTRIB_TAB <- "/Volumes/data/Gilgamesh/kroppian/agovization_results/mlearning/attrib_tab.feather"
ATTRIB_TAB <- "Z:/Gilgamesh/kroppian/agovization_results/mlearning/attrib_tab.feather"
RECD_PRACTICES_PATH <- "Z:/Gilgamesh/kroppian/agovization_results/mlearning/recommended_practices.feather"

attrib_tab <- arrow::read_feather(ATTRIB_TAB)
recd_practs <- arrow::read_feather(RECD_PRACTICES_PATH)

## Normalize yield across all years
max_yields <- attrib_tab %>%
              group_by(year) %>%
              summarize(year_max_yield = max(yield_)) 

norm_yield <- attrib_tab %>%
              inner_join(max_yields) %>%
              dplyr::select(yield_, year_max_yield) %>%
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
  stage_opt <- growth_stages[s]
  stage_rec <- str_replace(stage_opt, "total_wat_during_", "") %>% capitalize()
  
  optimized_irr <- high_yielders[,stage_opt] %>% pull(stage_opt) 
  
  recommended_irr <- recd_practs %>% filter(stages == stage_rec) %>% pull(irr)

  all_obvs <- append(optimized_irr,recommended_irr) 
   
  b <-  seq(min(all_obvs), max(all_obvs), length.out=15)
  
  
  opt_p <- hist(optimized_irr, col=rgb(0,0,1,1/4), breaks=b, main=paste("Total water usage during ", stage_rec  ))
  rec_p <- hist(recommended_irr,col=rgb(1,0,0,1/4), breaks=b, add=T) 
   
}

