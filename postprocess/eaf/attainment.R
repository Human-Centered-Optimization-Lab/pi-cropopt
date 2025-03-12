
# install.packages("readr")
# install.packages("arrow")
# install.packages("feather")
# install.packages("magrittr")


library("eaf");
library(readr);
library(magrittr)
library(ggplot2)
library(dplyr)

# Read the CSV file


# Define the years and algorithms
#years <- 1988:2017
years <- c(1988)


algorithms <- c("pinsga2", "nsga2")

i = 1

min_surfaces = c()
med_surfaces = c()
max_surfaces = c()

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
  
 
  # Combine tables  
  df1 <- nsga2 %>% 
  #  rename(V1=irr_total, V2=yield) %>% 
    mutate(alg = "nsga2")  # Add nsga2 column
  
  df2 <- pinsga2 %>% 
  #  rename(V1=preferred_irr_total, V2=preferred_yield) %>% 
    mutate(alg = "pinsga2")  # Add source column
 
  results <- bind_rows(df1, df2) 
  
  #print(ggplot() +
  #  # Add points for nsga2
  #  geom_point(data = nsga2, aes(x = V1, y = V2), color = "blue", alpha = 0.6) +
  #  # Add points for pinsga2
  #  geom_point(data = pinsga2, aes(x = V1, y = V2), color = "red", alpha = 0.6) +
  #  # Add labels and title
  #  labs(x = "Irrigation Total", y = "Yield", 
  #       title = "Scatter Plot of NSGA2 and PINSGA2") +
  #  # Optional: Add a theme
  #  theme_minimal())

  xmin <- pinsga2 %>% pull(V1) %>% min()
  xmax <- pinsga2 %>% pull(V1) %>% max()
  ymin <- pinsga2 %>% pull(V2) %>% min()
  ymax <- pinsga2 %>% pull(V2) %>% max()
  
     
  pinsga2_10to20 <- pinsga2 %>% filter(DM_range=="10to20") %>% select(V1, V2)
  pinsga2_20to30 <- pinsga2 %>% filter(DM_range=="20to30") %>% select(V1, V2)
  pinsga2_30to40 <- pinsga2 %>% filter(DM_range=="30to40") %>% select(V1, V2)
  interactive_methods = list(pinsga2_10to20, pinsga2_20to30, pinsga2_30to40)
  
  
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
  
  min_surfaces[i] = surface_res[1]
  med_surfaces[i] = surface_res[2]
  max_surfaces[i] = surface_res[3]
  
  i <- i + 1
   
}

