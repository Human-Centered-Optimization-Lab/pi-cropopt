library(dplyr)


## Load management data

GDD_TAB_PATH <- 'C:/Users/Ian Kropp/Projects/agovization/management_dates.csv'
gdd_tab <- read.csv(GDD_TAB_PATH)


## Set up standard management practice params

# Days after planting
veg_stage_start <- 50
veg_stage_period <- 5
veg_stage_amount <- 10


rep_stage_period <- 5
rep_stage_amount <- 20

years <- gdd_tab %>%
         dplyr::select(Year) %>%
         distinct() %>%
         pull(Year)


for(y in 1:length(years)){
  
  current_year <- years[y]

  # Start at planting  
  current_day <- gdd_tab %>% 
                 filter(Year == current_year) %>%
                 pull(P)
  
  # end of vegetative stage
  repro_stag_start <- gdd_tab %>% 
                      filter(Year == current_year) %>%
                      pull(R2)
  
  # Determine the applications during the vegetative stages  
  while(current_day){} 
   
   
  
   
}
