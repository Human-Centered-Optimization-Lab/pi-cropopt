library(ggplot2)
library(magrittr)

SUMMARY_INPUT_PATH <- "/Volumes/data/Gilgamesh/kroppian/agovization_results/validation/validation_summary.feather"
CUMUL_NET_CHANGE_OUTPUT_PATH <- "/Volumes/data/Gilgamesh/kroppian/agovization_results/validation/cumul_net_change.feather"

run_summary <- arrow::read_feather(SUMMARY_INPUT_PATH)    
cumul_net_changes <- arrow::read_feather(CUMUL_NET_CHANGE_OUTPUT_PATH)

# Clear old plots
if(! is.null(dev.list())){
  dev.off(dev.list()["RStudioGD"]) # Clears plots
}

## Plot percentage of years improvement
p1 <- ggplot(data=run_summary, aes(x=run, y=percent_yield_impr*100))  +
   geom_bar(stat="identity") + 
   ylim(0, 100  ) + 
   ylab("Percentage of years improved (%)") + 
   xlab("Strategy") 

plot(p1)


## Plot average loss/gains

# Massage data for chart
plot_run_summary_1 <- run_summary %>% 
                      dplyr::select(run, avg_yield_gain) %>% 
                      dplyr::rename(change = avg_yield_gain) %>% 
                      dplyr::mutate(type = "gain")

plot_run_summary_2 <- run_summary %>% 
                      dplyr::select(run, avg_yield_loss) %>% 
                      dplyr::rename(change = avg_yield_loss) %>% 
                      dplyr::mutate(type = "loss")

plot_run_summary <- rbind(plot_run_summary_1, plot_run_summary_2)

p2 <- ggplot(data=plot_run_summary, aes(x=run, y=change, fill=type)) + 
    geom_bar(stat="identity", position=position_dodge()) + 
    labs(x = "", fill = "Chagne type") + 
    ylab("Magnitude of change in yield (kg/ha)") 

plot(p2)


## Plot cumulative net gain in yield 

# stack them on top of each other for ggplot
df1 <- cumul_net_changes %>% 
        dplyr::select(year, cumul_net_changes_irr) %>%
        rename(net_change=cumul_net_changes_irr) %>%
        mutate(type="Irrigation only")


df2 <- cumul_net_changes %>% 
        dplyr::select(year, cumul_net_changes_nitro) %>%
        rename(net_change=cumul_net_changes_nitro) %>%
        mutate(type="Nitro only")

df3 <- cumul_net_changes %>% 
        dplyr::select(year, cumul_net_changes_all_recs) %>%
        rename(net_change=cumul_net_changes_all_recs) %>%
        mutate(type="All reccomendations")


cumul_net_changes_plot <- rbind(df1, df2, df3)

p3 <- ggplot(data=cumul_net_changes_plot, aes(x=year, y=net_change, group=type)) + 
      geom_line(aes(color=type)) +
      geom_point(aes(shape=type)) + 
      ylab("Cumulative net yield increase (kg/ha)") 
      

plot(p3)
