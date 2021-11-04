library(dplyr)
library(fitdistrplus)
library(R.utils)
library(stringr)

#ATTRIB_TAB <- "/Volumes/data/Gilgamesh/kroppian/agovization_results/mlearning/attrib_tab.feather"
#RECD_PRACTICES_PATH <- "/Volumes/data/Gilgamesh/kroppian/agovization_results/mlearning/recommended_practices.feather"
#CLIMATE_PATH <- "/Volumes/data/Gilgamesh/kroppian/agovization_results/mlearning/climate.feather"
ATTRIB_TAB <- "Z:/Gilgamesh/kroppian/agovization_results/mlearning/attrib_tab.feather"
RECD_PRACTICES_PATH <- "Z:/Gilgamesh/kroppian/agovization_results/mlearning/recommended_practices.feather"
CLIMATE_PATH <- "Z:/Gilgamesh/kroppian/agovization_results/mlearning/climate.feather"


attrib_tab <- arrow::read_feather(ATTRIB_TAB)
recd_practs <- arrow::read_feather(RECD_PRACTICES_PATH)
climate_tab <- arrow::read_feather(CLIMATE_PATH)

## Join climate info into the attribute table 
#attrib_tab <- attrib_tab %>% 
#              left_join(climate_tab, by = "year")


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

# Normalized yield with PO
high_yielders <- filter(attrib_tab, norm_yield > 0.75) %>%
                 filter(front == 0)
# End - Normalized yield 

# Just PO
#high_yielders <- filter(attrib_tab, front == 0)
# End - Just PO

# Normalized yield
#high_yielders <- filter(attrib_tab, norm_yield > 0.75) 
# End Normaliezd yiedl


growth_stages <- c('total_wat_during_v6', 
                   'total_wat_during_v7', 
                   'total_wat_during_v8', 
                   'total_wat_during_v9',
                   'total_wat_during_v10', 
                   'total_wat_during_v11',
                   'total_wat_during_v12',
                   'total_wat_during_v13',
                   'total_wat_during_v14',
                   'total_wat_during_R1')



if(! is.null(dev.list())){
  dev.off(dev.list()["RStudioGD"]) # Clears plots
}

for(s in 1:length(growth_stages)){
  
  stage_opt <- growth_stages[s]
  stage_rec <- str_replace(stage_opt, "total_wat_during_", "") %>% capitalize()
  
  optimized_irr <- high_yielders[,stage_opt] %>% pull(stage_opt) 
  recommended_irr <- recd_practs %>% filter(stages == stage_rec) %>% pull(irr)

  optimized_irr_dry <- high_yielders %>% 
                        filter(climate == 0) %>%
                        pull(stage_opt) 
  
  optimized_irr_norm <- high_yielders %>% 
                        filter(climate == 1) %>%
                        pull(stage_opt) 
  
  
  optimized_irr_wet <- high_yielders %>% 
                        filter(climate == 2) %>%
                        pull(stage_opt)  

  
  recommended_irr_dry <- recd_practs %>% 
                         filter(stages == stage_rec & climate == 0) %>% 
                         pull(irr)
  
  recommended_irr_norm <- recd_practs %>% 
                         filter(stages == stage_rec & climate == 1) %>% 
                         pull(irr)
  
  recommended_irr_wet <- recd_practs %>% 
                         filter(stages == stage_rec & climate == 2) %>% 
                         pull(irr)
  
  all_obvs <- append(optimized_irr,recommended_irr) 
  b <-  seq(min(all_obvs), max(all_obvs), length.out=15)
  
  opt_p <- hist(optimized_irr, col=rgb(0,0,1,1/4), breaks=b, main=paste("Total water usage during ", stage_rec  ))
  rec_p <- hist(recommended_irr,col=rgb(1,0,0,1/4), breaks=b, add=T) 
  
  for(c in 0:2){
   
    if(c == 0) {
      current_opt_irr = optimized_irr_dry
      current_rec_irr = recommended_irr_dry
    }else if (c == 1){
      current_opt_irr = optimized_irr_norm
      current_rec_irr = recommended_irr_norm
    }else if (c == 2){
      current_opt_irr = optimized_irr_wet
      current_rec_irr = recommended_irr_wet
    }
     
    # Calculate the differenc between optimized and recommended
    opt_med <- median(current_opt_irr)
    rec_med <- median(recommended_irr)
   
    percentage_change = -(rec_med - opt_med)/rec_med
     
    print(str_interp("For ${c} '${stage_rec}': ${percentage_change},")) 
      
  }
   
}

heavy_rain_threshold <- median(attrib_tab$max_p_5_day_prior_N)
moderate_rain_threshold <- median(attrib_tab$max_p_3_day_prior_N)
light_rain_threshold <- median(attrib_tab$max_p_1_day_prior_N)

print(str_interp("Heavy rain threshold: ${heavy_rain_threshold}"))
print(str_interp("Moderate rain threshold: ${moderate_rain_threshold}"))
print(str_interp("Light rain threshold: ${light_rain_threshold}"))


