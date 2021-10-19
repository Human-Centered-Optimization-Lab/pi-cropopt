library(dplyr)

get_growth_period <- function(gdd_tab, given_year, doy) {
  
  gdd_ranges <- gdd_tab %>% filter(Year == given_year) 
  col_names <- c('growth_stage', 'doy') 
  stages <- colnames(gdd_tab)
  stages <- stages[stages != "Year"]
 
  doys <- as.numeric(gdd_ranges[stages]) 
  gdd_stages <- data.frame(stages, doys)
  
  period_doy <- as.numeric(gdd_stages %>% filter(doys <= doy) %>% summarize(max(doys))) 
 
  stage <- gdd_stages %>% filter(doys == period_doy) %>% pull(stages) 
   
  return(stage)
}

## Load management data

#GDD_TAB_PATH <- 'C:/Users/Ian Kropp/Projects/agovization/management_dates.csv'
GDD_TAB_PATH <- '/Users/iankropp/Projects/agovization/management_dates.csv'
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

  mangt_info <-  gdd_tab %>% 
                 filter(Year == current_year)
  
  # Start at planting  
  current_day <- mangt_info %>%
                 pull(P)
  
  # end of vegetative stage
  repro_stag_start <- mangt_info %>%
                      pull(R1)
 
  # end of vegetative stage
  blistering <- mangt_info %>%
                      pull(R2)
  
   
  # Determine the applications during the vegetative stages  
  while(current_day < repro_stag_start){
    period <-  get_growth_period(gdd_tab, current_year, current_day)
    print(paste("Year: ", current_year,", Veg: On day ", current_day, " irrigate ", veg_stage_amount, " during ", period)) 
    current_day = current_day + veg_stage_period
  } 
  
   
  # Determine the applications during the vegetative stages  
  while(current_day < blistering){
    period <-  get_growth_period(gdd_tab, current_year, current_day)
    print(paste("Rep: On day ", current_day, " irrigate ", rep_stage_amount, " during ", period)) 
    current_day = current_day + rep_stage_period
  } 
   
  
  break 
}



