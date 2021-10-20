library(dplyr)

list_growth_periods <- function(gdd_tab){
  stages <- colnames(gdd_tab)
  stages <- stages[stages != "Year"]
  return(stages) 
}

get_growth_period <- function(gdd_tab, given_year, doy) {
  
  gdd_ranges <- gdd_tab %>% filter(Year == given_year) 
  col_names <- c('growth_stage', 'doy') 
  
  stages <- list_growth_periods(gdd_tab)
   
  doys <- as.numeric(gdd_ranges[stages]) 
  gdd_stages <- data.frame(stages, doys)
  
  period_doy <- as.numeric(gdd_stages %>% filter(doys <= doy) %>% summarize(max(doys))) 
 
  stage <- gdd_stages %>% filter(doys == period_doy) %>% pull(stages) 
   
  return(stage)
}

## Load management data

GDD_TAB_PATH <- 'C:/Users/Ian Kropp/Projects/agovization/management_dates.csv'
#GDD_TAB_PATH <- '/Users/iankropp/Projects/agovization/management_dates.csv'
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


stages <- list_growth_periods(gdd_tab)

stages_col <- c()
year_col <- c()
irr_col <- c()

for(y in 1:length(years)){
  stages_col <- append(stages_col, stages)
  year_col <- append(year_col, as.vector(matrix(years[y], length(stages))))
  irr_col <- append(irr_col, as.vector(matrix(0, length(stages))))
}

result <- data.frame(stages_col, year_col, irr_col)

result <- result %>% 
          rename(stages = stages_col) %>%
          rename(year = year_col) %>%
          rename(irr = irr_col) 
          

for(y in 1:length(years)){
  
  current_year <- years[y]

  mangt_info <-  gdd_tab %>% 
                 filter(Year == current_year)
  
  # Determine planting doy 
  current_day <- mangt_info %>%
                 pull(V6)
  
  # Determine end of vegetative stage
  repro_stag_start <- mangt_info %>%
                      pull(R1)
 
  # Determine end of vegetative stage
  blistering <- mangt_info %>%
                      pull(R2)
   
   
  # Determine the applications during the vegetative stages  
  while(current_day < repro_stag_start){
    
    # Determine which vegetative period we're looking at
    period <-  get_growth_period(gdd_tab, current_year, current_day)
    print(paste("Year: ", current_year,", Veg: On day ", current_day, " irrigate ", veg_stage_amount, " during ", period)) 
   
    # Add the current irrigation application
    current_irr <- result %>% filter(stages == period & year == current_year) %>% pull(irr) 
    new_irr <- current_irr + veg_stage_amount 
    result <- result %>% mutate(irr = ifelse(stages == period & year == current_year, new_irr, irr)) 
    
    # Go to the next irrigation period 
    current_day = current_day + veg_stage_period
  } 
  
   
  # Determine the applications during the vegetative stages  
  while(current_day < blistering){
    
    # Determine which vegetative period we're looking at
    period <-  get_growth_period(gdd_tab, current_year, current_day)
    print(paste("Rep: On day ", current_day, " irrigate ", rep_stage_amount, " during ", period)) 
    
    # Add the current irrigation application
    current_irr <- result %>% filter(stages == period & year == current_year) %>% pull(irr) 
    new_irr <- current_irr + veg_stage_amount 
    result <- result %>% mutate(irr = ifelse(stages == period & year == current_year, new_irr, irr)) 
    
    # Go to the next irrigation period 
    current_day = current_day + rep_stage_period
  } 
   
  
}



