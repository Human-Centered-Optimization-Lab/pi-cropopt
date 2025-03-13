
# install.packages("readr")
# install.packages("arrow")
# install.packages("magrittr")
# install.packages("emoa")

library("eaf");
library(readr);
library(magrittr)
library(ggplot2)
library(dplyr)

# Read the CSV file


# Define the years and algorithms
years <- 1988:2017
#years <- c(1988)
#years <- c(1990)


algorithms <- c("pinsga2", "nsga2")


# Loop through each year
for (year in years) {
  # Loop through each algorithm
  
  # NSGA-II 
  # Construct the filename
  filename <- paste0(year, "-nsga2.csv")
  
  # Read the CSV file
  # Use tryCatch to handle any errors in case the file does not exist
  nsga2 <- tryCatch({
    read.csv(filename)
  }, error = function(e) {
    message(paste("Error reading file:", filename, " - ", e$message))
    return(NULL)  # Return NULL if there's an error
  })
 
  # PI-NSGA-II 
  # Construct the filename
  filename <- paste0(year, "-pinsga2.csv")
  
  # Read the CSV file
  # Use tryCatch to handle any errors in case the file does not exist
  pinsga2 <- tryCatch({
    read.csv(filename)
  }, error = function(e) {
    message(paste("Error reading file:", filename, " - ", e$message))
    return(NULL)  # Return NULL if there's an error
  })
  
  # Determine bounds of the plot 
  xmin <- pinsga2 %>% pull(V1) %>% min()
  xmax <- pinsga2 %>% pull(V1) %>% max()
  ymin <- pinsga2 %>% pull(V2) %>% min()
  ymax <- pinsga2 %>% pull(V2) %>% max()
  
  # Pull the different ranges of the interactive results 
  pinsga2_10to20 <- pinsga2 %>% filter(DM_range=="10to20") %>% select(V1, V2)
  pinsga2_20to30 <- pinsga2 %>% filter(DM_range=="20to30") %>% select(V1, V2)
  pinsga2_30to40 <- pinsga2 %>% filter(DM_range=="30to40") %>% select(V1, V2)
  interactive_methods = list(pinsga2_10to20, pinsga2_20to30, pinsga2_30to40)
  
  # Make the plot 
  surface_res = eafplot(nsga2, 
          xlim = c(xmin, xmax),
          ylim = c(ymin, ymax),
          percentiles = c(0, 50, 100), 
          maximise=c(FALSE, TRUE), 
          extra.points = interactive_methods, 
          extra.col = c("orange", "red", "blue"),
          extra.pch = c(15, 16, 17),
          legend.pos="bottomright") 
  
 
  title(paste("Results for ", year)) 
 
  # Determine how many results went out of the bounds 
  max_surface = surface_res[1][[1]]
  med_surface = surface_res[2][[1]]
  min_surface = surface_res[3][[1]]

  interactive_runs = list(pinsga2_10to20=pinsga2_10to20, 
                          pinsga2_20to30=pinsga2_20to30, 
                          pinsga2_30to40=pinsga2_30to40) 
     
  for (run_name in names(interactive_runs)) {
    
    curr_inter_run = interactive_runs[[run_name]] 
     
    total_inbounds = 0
    total_inter = nrow(curr_inter_run)
    for (r in 1:total_inter) {
   
      current_interactive_runs =  interactive_runs[i]
         
      inter_irr_amount = curr_inter_run[r,1]
      inter_yield = curr_inter_run[r,2]
       
      nsga2_min_yield = min_surface[min_surface[,1] == inter_irr_amount, 2]
      nsga2_max_yield = max_surface[max_surface[,1] == inter_irr_amount, 2]
     
      # Check if there's no lower bound
      if (length(nsga2_min_yield) == 0 && length(nsga2_max_yield) != 0){
        if(nsga2_max_yield == inter_yield){
          total_inbounds = total_inbounds + 1
        }  
      }

      # Check if there's no lower bound
      else if (length(nsga2_min_yield) != 0 && length(nsga2_max_yield) == 0){
        if(nsga2_min_yield == inter_yield){
          total_inbounds = total_inbounds + 1
        }  
      }else if (length(nsga2_min_yield) == 0 && length(nsga2_max_yield) == 0){
        print(paste(year, " is an unbounded year at irr amount: ", inter_irr_amount)) 
      }
      # otherwise, check if its in bounds       
      else if (inter_yield >= nsga2_min_yield && inter_yield <= nsga2_max_yield)
        total_inbounds = total_inbounds + 1
      
    }
   
    percentage_in = total_inbounds / total_inter
     
    print(paste("Year: ", year, ", dm_range: ", run_name,  ", perc_in:",  percentage_in)) 
    
  }
  
   
}

