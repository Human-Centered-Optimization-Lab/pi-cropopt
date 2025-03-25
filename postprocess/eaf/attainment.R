
# install.packages("readr")
# install.packages("arrow")
# install.packages("magrittr")
# install.packages("emoa")

library("eaf");
library(readr);
library(magrittr)
library(ggplot2)
library(dplyr)
library(emoa)

# Read the CSV file


# Define the years and algorithms
years <- 1988:2017

legend_pos = c("bottomright", # 1988
               "bottomright", # 1989
               "topleft",     # 1990  
               "bottomright", # 1991
               "bottomright", # 1992
               "topleft",     # 1993 
               "bottomright", # 1994
               "bottomright", # 1995
               "bottomright", # 1996
               "bottomright", # 1997
               "bottomright", # 1998
               "bottomright", # 1999
               "bottomright", # 2000
               "bottomright", # 2001
               "bottomright", # 2002
               "bottomright", # 2003
               "bottomright", # 2004
               "bottomright", # 2005
               "bottomright", # 2006
               "bottomright", # 2007  
               "bottomright", # 2008
               "bottomright", # 2009
               "bottomright", # 2010
               "bottomright", # 2011
               "bottomright", # 2012
               "bottomright", # 2013
               "bottomright", # 2014
               "bottomright", # 2015
               "bottomright", # 2016
               "topleft")     # 2017 





algorithms <- c("pinsga2", "nsga2")

results_table = data.frame()

y <- 1

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
 
  xoff = 0 
  yoff = 0 

  # Some one off code for years that don't fit 
  # the 
  if(year == 1993) {
    xoff = 10   
    yoff = 10
  }
  
  
  # Make the plot 
  surface_res = eafplot(nsga2, 
          xlim = c(xmin - xoff, xmax),
          ylim = c(ymin, ymax + yoff),
          xlab = "Seasonal Irrigation Applied (mm)",
          ylab = "Seasonal Yield (kg/ha)",
          percentiles = c(0, 50, 100), 
          maximise=c(FALSE, TRUE), 
          extra.points = interactive_methods, 
          extra.legend = c("PI-NSGA-II (10-20mm)", "PI-NSGA-II (20-30mm)", "PI-NSGA-II (30-40mm)"),
          extra.col = c("orange", "red", "blue"),
          extra.pch = c(15, 16, 17),
          legend.pos=legend_pos[y],
          legend.txt = c("NSGA-II Best", "NSGA-II Median", "NSGA-II Worst")) 
  
 
  title(paste("PI-NSGA-II vs NSGA-II Trials (", year, ")", sep="")) 
 
  # Determine how many results went out of the bounds 
  max_surface = surface_res[1][[1]]
  med_surface = surface_res[2][[1]]
  min_surface = surface_res[3][[1]]

  interactive_runs = list(pinsga2_10to20=pinsga2_10to20, 
                          pinsga2_20to30=pinsga2_20to30, 
                          pinsga2_30to40=pinsga2_30to40) 
     
   
  
  for (run_name in names(interactive_runs)) {
   
    curr_inter_run = interactive_runs[[run_name]] 
   
    curr_inter_run = unique(curr_inter_run)   
    min_surface = unique(min_surface)
    max_surface = unique(max_surface)
    
     
    inter_run_cutoff = nrow(curr_inter_run)
   
    ## -------- Calculate % that are not dominated by min surface -------------  
    min_surf_len = nrow(min_surface)
   
    all_points = rbind(curr_inter_run, min_surface)
    
    # reversing yield to a minimization problem
    all_points[,2] = all_points[,2]*-1
    
    # Make a dominance matrix of the minimal points and the interactive points
    dom_mat =  dominance_matrix(t(as.matrix(all_points)))
    
    # Examine whether each interactive points are being dominated by the minimum attainment surface 
    inter_dom_by_min = dom_mat[(inter_run_cutoff+1):(inter_run_cutoff+min_surf_len),0:inter_run_cutoff, drop=FALSE] 
   
    # Sum the total dominated points
    dominated_by_min =  colSums(inter_dom_by_min)
    
    # Count the total that are dominated at all 
    total_dominated = length(which(dominated_by_min != 0))
     
    # Invert this figure to determine the number points that are are as good or better than the min   
    better_than_min_rate = 1 - total_dominated/inter_run_cutoff
   
    ## -------- Calculate % that dominate the max surface -------------  
   
    max_surf_len = nrow(max_surface)
    
    all_points = rbind(curr_inter_run, max_surface)
    
    # reversing yield to a minimization problem
    all_points[,2] = all_points[,2]*-1
    
    # Make a dominance matrix of the minimal points and the interactive points
    dom_mat =  dominance_matrix(t(as.matrix(all_points)))
    
    # Examine whether each interactive points are being dominated by the minimum attainment surface 
    max_dom_by_inter = dom_mat[0:inter_run_cutoff,(inter_run_cutoff+1):(inter_run_cutoff+max_surf_len), drop=FALSE] 
    
    # Sum the total dominated points
    dominating_max = rowSums(max_dom_by_inter)
    
    # Count the total that are dominated at all 
    total_dominating = length(which(dominating_max != 0))
    
    # Invert this figure to determine the number points that are are as good or better than the min   
    better_than_max_rate = total_dominating/inter_run_cutoff 
    
     
    ## -------- Record the results in a dataframe -------------  
     
    next_row = data.frame(
      year = year, 
      dm_range = run_name, 
      perc_better_than_min = better_than_min_rate,
      perc_better_than_max = better_than_max_rate
    )
    
    results_table = rbind(results_table, next_row)
    
  }

  y <- y + 1  
   
}


## ---------- Reformat the table for publication  ---------------

runs_10to20 <- results_table %>% 
                filter(dm_range == "pinsga2_10to20") %>% 
                rename(bt_min_10to20 = perc_better_than_min) %>%
                rename(bt_max_10to20 = perc_better_than_max) %>%
                select(-dm_range)


runs_20to30 <- results_table %>% 
                filter(dm_range == "pinsga2_20to30") %>% 
                rename(bt_min_20to30 = perc_better_than_min) %>%
                rename(bt_max_20to30 = perc_better_than_max) %>%
                select(-dm_range)

runs_30to40 <- results_table %>% 
                filter(dm_range == "pinsga2_30to40") %>% 
                rename(bt_min_30to40 = perc_better_than_min) %>%
                rename(bt_max_30to40 = perc_better_than_max) %>%
                select(-dm_range)


pretty_tab <- runs_10to20 %>% 
                full_join(runs_20to30, by=join_by(year)) %>%
                full_join(runs_30to40, by=join_by(year))



