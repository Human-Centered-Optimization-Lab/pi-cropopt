library(ggplot2)
library(magrittr)



INPUT_DATA_ROOT <- 'Z:/Gilgamesh/kroppian/agovization_results/validation/'
INPUT_DATA_ROOT <- '/Volumes/data/Gilgamesh/kroppian/agovization_results/validation/'

SUMMARY_INPUT_PATH <- paste(INPUT_DATA_ROOT, "validation_summary.feather", sep="")
CUMUL_NET_CHANGE_OUTPUT_PATH <- paste(INPUT_DATA_ROOT, "cumul_net_change.feather", sep="")

PLOT_OUTPUT_PATH <- 'C:/Users/Ian Kropp/OneDrive/OneDrive - Michigan State University/Documents/Shared/todo/paper1Innovization/figures/'
PLOT_OUTPUT_PATH <- "/Users/iankropp/OneDrive - Michigan State University/Documents/Shared/todo/paper1Innovization/figures/"


run_summary <- arrow::read_feather(SUMMARY_INPUT_PATH)    
cumul_net_changes <- arrow::read_feather(CUMUL_NET_CHANGE_OUTPUT_PATH)

# Clear old plots
if(! is.null(dev.list())){
  dev.off(dev.list()["RStudioGD"]) # Clears plots
}

run_summary       <- run_summary       %>% filter(run_id == 2)
cumul_net_changes <- cumul_net_changes %>% filter(run_id == 2)

## Plot average loss/gains

# Massage data for chart
plot_run_summary_1 <- run_summary %>% 
                      dplyr::select(run_type, avg_yield_gains) %>% 
                      dplyr::rename(change = avg_yield_gains) %>% 
                      dplyr::mutate(type = "gains")

plot_run_summary_2 <- run_summary %>% 
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

# stack them on top of each other for ggplot
df1 <- cumul_net_changes %>% 
        dplyr::select(year, cumul_net_yield_changes_irr) %>%
        rename(net_change=cumul_net_yield_changes_irr) %>%
        mutate(type="Irrigation only")


df2 <- cumul_net_changes %>% 
        dplyr::select(year, cumul_net_yield_changes_nitro) %>%
        rename(net_change=cumul_net_yield_changes_nitro) %>%
        mutate(type="Nitro only")

df3 <- cumul_net_changes %>% 
        dplyr::select(year, cumul_net_yield_changes_all_recs) %>%
        rename(net_change=cumul_net_yield_changes_all_recs) %>%
        mutate(type="All reccomendations")


cumul_net_yield_changes_plot <- rbind(df1, df2, df3)

p2 <- ggplot(data=cumul_net_yield_changes_plot, aes(x=year, y=net_change, group=type)) + 
      geom_line(aes(color=type)) +
      geom_point(aes(shape=type)) + 
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
df1 <- cumul_net_changes %>% 
        dplyr::select(year, cumul_net_leach_changes_irr) %>%
        rename(net_change=cumul_net_leach_changes_irr) %>%
        mutate(type="Irrigation only")


df2 <- cumul_net_changes %>% 
        dplyr::select(year, cumul_net_leach_changes_nitro) %>%
        rename(net_change=cumul_net_leach_changes_nitro) %>%
        mutate(type="Nitro only")

df3 <- cumul_net_changes %>% 
        dplyr::select(year, cumul_net_leach_changes_all_recs) %>%
        rename(net_change=cumul_net_leach_changes_all_recs) %>%
        mutate(type="All reccomendations")

avg_leach <- 16.783

df4 <- cumul_net_changes %>% 
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