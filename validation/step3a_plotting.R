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

# Calculate confidence intervals
ci_upper_yield <- c()
ci_lower_yield <- c()
ci_years_yield <- c()
ci_type_yield <- c()

ci_upper_leach <- c()
ci_lower_leach <- c()
ci_years_leach <- c()
ci_type_leach <- c()



for(current_year in min_year:max_year){
 
  # ---- Irrigation only yield ----
  vals <- cumul_net_changes %>% filter(year == current_year) %>% pull(cumul_net_yield_changes_irr) 
  
  reps <- boot(vals, statistic=samplemean, R=1000)
  boot_res <- boot.ci(reps, type="basic")

  ci_upper_yield <- append(ci_upper_yield, boot_res$basic[1,5])
  ci_lower_yield <- append(ci_lower_yield, boot_res$basic[1,4])
  ci_years_yield <- append(ci_years_yield, current_year)
  ci_type_yield  <- append(ci_type_yield, "Irrigation recommendations")
  
  
  # ---- Nitrogen only yield ----
  vals <- cumul_net_changes %>% filter(year == current_year) %>% pull(cumul_net_yield_changes_nitro) 
  reps <- boot(vals, statistic=samplemean, R=1000)
  boot_res <- boot.ci(reps, type="basic")
  
  ci_upper_yield <- append(ci_upper_yield, boot_res$basic[1,5])
  ci_lower_yield <- append(ci_lower_yield, boot_res$basic[1,4])
  ci_years_yield <- append(ci_years_yield, current_year)
  ci_type_yield  <- append(ci_type_yield, "Nitrogen recommendations")
  
  
  # ---- All recs yield ----
  vals <- cumul_net_changes %>% filter(year == current_year) %>% pull(cumul_net_yield_changes_all_recs) 
  reps <- boot(vals, statistic=samplemean, R=1000)
  boot_res <- boot.ci(reps, type="basic")
  
  ci_upper_yield <- append(ci_upper_yield, boot_res$basic[1,5])
  ci_lower_yield <- append(ci_lower_yield, boot_res$basic[1,4])
  ci_years_yield <- append(ci_years_yield, current_year)
  ci_type_yield  <- append(ci_type_yield, "All reccomendations")
 
  
  # ---- Irrigation only leaching ----
  vals <- cumul_net_changes %>% filter(year == current_year) %>% pull(cumul_net_leach_changes_irr) 
  
  reps <- boot(vals, statistic=samplemean, R=1000)
  boot_res <- boot.ci(reps, type="basic")

  ci_upper_leach <- append(ci_upper_leach, boot_res$basic[1,5])
  ci_lower_leach <- append(ci_lower_leach, boot_res$basic[1,4])
  ci_years_leach <- append(ci_years_leach, current_year)
  ci_type_leach  <- append( ci_type_leach, "Irrigation recommendations")
  
  
  # ---- Nitrogen only yield ----
  vals <- cumul_net_changes %>% filter(year == current_year) %>% pull(cumul_net_leach_changes_nitro) 
  reps <- boot(vals, statistic=samplemean, R=1000)
  boot_res <- boot.ci(reps, type="basic")
  
  ci_upper_leach <- append(ci_upper_leach, boot_res$basic[1,5])
  ci_lower_leach <- append(ci_lower_leach, boot_res$basic[1,4])
  ci_years_leach <- append(ci_years_leach, current_year)
  ci_type_leach  <- append( ci_type_leach, "Nitrogen recommendations")
  
  
  # ---- All recs yield ----
  vals <- cumul_net_changes %>% filter(year == current_year) %>% pull(cumul_net_leach_changes_all_recs) 
  reps <- boot(vals, statistic=samplemean, R=1000)
  boot_res <- boot.ci(reps, type="basic")
  
  ci_upper_leach <- append(ci_upper_leach, boot_res$basic[1,5])
  ci_lower_leach <- append(ci_lower_leach, boot_res$basic[1,4])
  ci_years_leach <- append(ci_years_leach, current_year)
  ci_type_leach  <- append( ci_type_leach, "All reccomendations")
  
}

cis_yield <- data.frame(
  upper=ci_upper_yield,
  lower=ci_lower_yield,
  year=ci_years_yield,
  type=ci_type_yield
)

cis_leach <- data.frame(
  upper=ci_upper_leach,
  lower=ci_lower_leach,
  year= ci_years_leach,
  type= ci_type_leach
)


# stack them on top of each other for ggplot
df1 <- cumul_net_changes_by_year %>% 
        dplyr::select(year, cumul_net_yield_changes_irr) %>%
        rename(net_change=cumul_net_yield_changes_irr) %>%
        mutate(type="Irrigation recommendations")

df2 <- cumul_net_changes_by_year %>% 
        dplyr::select(year, cumul_net_yield_changes_nitro) %>%
        rename(net_change=cumul_net_yield_changes_nitro) %>%
        mutate(type="Nitrogen recommendations")

df3 <- cumul_net_changes_by_year %>% 
        dplyr::select(year, cumul_net_yield_changes_all_recs) %>%
        rename(net_change=cumul_net_yield_changes_all_recs) %>%
        mutate(type="All reccomendations")


cumul_net_yield_changes_plot <- rbind(df1, df2, df3)

# Add confidence intervals
cumul_net_yield_changes_plot <- cumul_net_yield_changes_plot %>% 
                                full_join(cis_yield)


p2 <- ggplot(data=cumul_net_yield_changes_plot, aes(x=year, y=net_change, group=type)) + 
      geom_line(aes(color=type)) +
      geom_point(aes(shape=type)) + 
      geom_ribbon(aes(ymin = lower, ymax = upper, fill=type), alpha = 0.25) + 
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
        mutate(type="Irrigation recommendations")


df2 <- cumul_net_changes_by_year %>% 
        dplyr::select(year, cumul_net_leach_changes_nitro) %>%
        rename(net_change=cumul_net_leach_changes_nitro) %>%
        mutate(type="Nitrogen recommendations")

df3 <- cumul_net_changes_by_year %>% 
        dplyr::select(year, cumul_net_leach_changes_all_recs) %>%
        rename(net_change=cumul_net_leach_changes_all_recs) %>%
        mutate(type="All reccomendations")

#avg_leach <- 16.783
#
#df4 <- cumul_net_changes_by_year %>% 
#        mutate(net_change=avg_leach) %>%
#        mutate(type="Average leaching in common practices") %>%
#        dplyr::select(year, net_change, type)
#
#cumul_net_leach_changes_plot <- rbind(df1, df2, df3, df4)
cumul_net_leach_changes_plot <- rbind(df1, df2, df3)

cumul_net_leach_changes_plot <- cumul_net_leach_changes_plot %>% full_join(cis_leach)

p3 <- ggplot(data=cumul_net_leach_changes_plot, aes(x=year, y=net_change, group=type)) + 
      geom_line(aes(color=type)) +
      geom_point(aes(shape=type)) + 
      geom_ribbon(aes(ymin = lower, ymax = upper, fill=type), alpha = 0.25) + 
      ylab("Cumulative net leaching increase (kg/ha)") 
      
plot(p3)

ggsave(
  paste(PLOT_OUTPUT_PATH, "/cumulLeachChange.png", sep=""),
  p3,
  width = 6,
  height = 4,
  dpi = 1200
)