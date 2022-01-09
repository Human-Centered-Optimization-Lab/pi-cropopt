library(ggplot2)
library(magrittr)
library(boot)
library(dplyr)

samplemean <- function(x, d) {
  return(mean(x[d]))
}

INPUT_DATA_ROOT <- 'Z:/Gilgamesh/kroppian/agovization_results/validation/'
INPUT_DATA_ROOT <- '/Volumes/data/Gilgamesh/kroppian/agovization_results/validation/'

SUMMARY_INPUT_PATH <- paste(INPUT_DATA_ROOT, "validation_summary.feather", sep="")
CUMUL_NET_CHANGE_OUTPUT_PATH <- paste(INPUT_DATA_ROOT, "cumul_net_change.feather", sep="")

PLOT_OUTPUT_PATH <- 'C:/Users/Ian Kropp/OneDrive/OneDrive - Michigan State University/Documents/Shared/todo/paper1Innovization/figures/'
PLOT_OUTPUT_PATH <- "/Users/iankropp/OneDrive - Michigan State University/Documents/Shared/todo/paper1Innovization/figures/"



run_summary <- arrow::read_feather(SUMMARY_INPUT_PATH)    
cumul_net_changes <- arrow::read_feather(CUMUL_NET_CHANGE_OUTPUT_PATH)

min_year <- min(cumul_net_changes$year)
max_year <- max(cumul_net_changes$year)

# Clear old plots
if(! is.null(dev.list())){
  dev.off(dev.list()["RStudioGD"]) # Clears plots
}

## Plot average loss/gains

run_summary_bar_plot <- run_summary %>% 
                        dplyr::group_by(run_type) %>% 
                        dplyr::summarize_at(vars(avg_yield_losses,avg_yield_gains),funs(mean))

# Massage data for chart
plot_run_summary_1 <- run_summary_bar_plot %>% 
                      dplyr::select(run_type, avg_yield_gains) %>% 
                      dplyr::rename(change = avg_yield_gains) %>% 
                      dplyr::mutate(type = "gains")

plot_run_summary_2 <- run_summary_bar_plot %>% 
                      dplyr::select(run_type, avg_yield_losses) %>% 
                      dplyr::rename(change = avg_yield_losses) %>% 
                      dplyr::mutate(change = change*-1) %>% 
                      dplyr::mutate(type = "losses")

plot_run_summary <- rbind(plot_run_summary_1, plot_run_summary_2)

p1 <- ggplot(data=plot_run_summary, aes(x=run_type, y=change, fill=type)) + 
    geom_bar(stat="identity", position=position_dodge()) + 
    labs(x = "", fill = "Change type") + 
    ylab("Average change in yield (2010-2018) (kg/ha)") 

plot(p1)

ggsave(
  paste(PLOT_OUTPUT_PATH, "/averageChangeYield.png", sep=""),
  p1,
  width = 5,
  height = 4,
  dpi = 1200
)

## Plot cumulative net gain in yield 

# Summarize the results by year
cumul_net_changes_by_year <- cumul_net_changes %>% 
                      group_by(year) %>%
                      summarize_at(
                        vars(
                          cumul_net_yield_changes_irr,
                          cumul_net_yield_changes_nitro,
                          cumul_net_yield_changes_all_recs,
                          cumul_net_leach_changes_irr,
                          cumul_net_leach_changes_nitro,
                          cumul_net_leach_changes_all_recs
                          ), funs(mean))

# TODO create confidence intervals 

# TODO Create empty dataframes

ci_upper <- c()
ci_lower <- c()
ci_years <- c()
ci_type <- c()

for(current_year in min_year:max_year){
 
  # Calculate confidence intervals
  # ---- Irrigation only yield ----
  vals <- cumul_net_changes %>% filter(year == current_year) %>% pull(irr_only_net_yield) 
  
  reps <- boot(vals, statistic=samplemean, R=1000)
  boot_res <- boot.ci(reps, type="basic")

  ci_upper <- append(ci_upper, boot_res$basic[1,5])
  ci_lower <- append(ci_lower, boot_res$basic[1,4])
  ci_years <- append(ci_years, current_year)
  ci_type  <- append(ci_type, "Irrigation only")
  
  
  # ---- Nitrogen only yield ----
  vals <- cumul_net_changes %>% filter(year == current_year) %>% pull(nitro_only_net_yield) 
  reps <- boot(vals, statistic=samplemean, R=1000)
  boot_res <- boot.ci(reps, type="basic")
  
  ci_upper <- append(ci_upper, boot_res$basic[1,5])
  ci_lower <- append(ci_lower, boot_res$basic[1,4])
  ci_years <- append(ci_years, current_year)
  ci_type  <- append(ci_type, "Nitro only")
  
  
  # ---- All recs yield ----
  vals <- cumul_net_changes %>% filter(year == current_year) %>% pull(all_rec_net_yield) 
  reps <- boot(vals, statistic=samplemean, R=1000)
  boot_res <- boot.ci(reps, type="basic")
  
  ci_upper <- append(ci_upper, boot_res$basic[1,5])
  ci_lower <- append(ci_lower, boot_res$basic[1,4])
  ci_years <- append(ci_years, current_year)
  ci_type  <- append(ci_type, "All reccomendations")
 
  
   
  cumul_net_leach_ci_irr <- 1
  cumul_net_leach_ci_nitro <- 1
  cumul_net_leach_ci_all_recs <- 1
  
}

cis <- data.frame(
  upper=ci_upper,
  lower=ci_lower,
  year=ci_years,
  type=ci_type
)




# stack them on top of each other for ggplot
df1 <- cumul_net_changes_by_year %>% 
        dplyr::select(year, cumul_net_yield_changes_irr) %>%
        rename(net_change=cumul_net_yield_changes_irr) %>%
        mutate(type="Irrigation only")

df2 <- cumul_net_changes_by_year %>% 
        dplyr::select(year, cumul_net_yield_changes_nitro) %>%
        rename(net_change=cumul_net_yield_changes_nitro) %>%
        mutate(type="Nitro only")

df3 <- cumul_net_changes_by_year %>% 
        dplyr::select(year, cumul_net_yield_changes_all_recs) %>%
        rename(net_change=cumul_net_yield_changes_all_recs) %>%
        mutate(type="All reccomendations")


cumul_net_yield_changes_plot <- rbind(df1, df2, df3)

p2 <- ggplot(data=cumul_net_yield_changes_plot, aes(x=year, y=net_change, group=type)) + 
      geom_line(aes(color=type)) +
      geom_point(aes(shape=type)) + 
      geom_polygon(data=ci_polys, aes(x = x, y = y), group = id) +
      ylab("Cumulative net yield increase (kg/ha)") 
     
 
 
plot(p2)

ggsave(
  paste(PLOT_OUTPUT_PATH, "/cumulYieldChange.png", sep=""),
  p2,
  width = 6,
  height = 4,
  dpi = 1200
)

## Plot cumulative net change in leaching 

# stack them on top of each other for ggplot
df1 <- cumul_net_changes_by_year %>% 
        dplyr::select(year, cumul_net_leach_changes_irr) %>%
        rename(net_change=cumul_net_leach_changes_irr) %>%
        mutate(type="Irrigation only")


df2 <- cumul_net_changes_by_year %>% 
        dplyr::select(year, cumul_net_leach_changes_nitro) %>%
        rename(net_change=cumul_net_leach_changes_nitro) %>%
        mutate(type="Nitro only")

df3 <- cumul_net_changes_by_year %>% 
        dplyr::select(year, cumul_net_leach_changes_all_recs) %>%
        rename(net_change=cumul_net_leach_changes_all_recs) %>%
        mutate(type="All reccomendations")

avg_leach <- 16.783

df4 <- cumul_net_changes_by_year %>% 
        mutate(net_change=avg_leach) %>%
        mutate(type="Average leaching in common practices") %>%
        dplyr::select(year, net_change, type)

cumul_net_leach_changes_plot <- rbind(df1, df2, df3, df4)

p3 <- ggplot(data=cumul_net_leach_changes_plot, aes(x=year, y=net_change, group=type)) + 
      geom_line(aes(color=type)) +
      geom_point(aes(shape=type)) + 
      ylab("Cumulative net leaching increase (kg/ha)") 
      
plot(p3)

ggsave(
  paste(PLOT_OUTPUT_PATH, "/cumulLeachChange.png", sep=""),
  p3,
  width = 6,
  height = 4,
  dpi = 1200
)