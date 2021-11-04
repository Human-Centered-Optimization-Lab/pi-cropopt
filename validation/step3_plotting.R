library(ggplot2)
library(magrittr)

SUMMARY_INPUT_PATH <- "/Volumes/data/Gilgamesh/kroppian/agovization_results/validation/validation_summary.feather"
CUMUL_NET_CHANGE_INPUT_PATH <- "/Volumes/data/Gilgamesh/kroppian/agovization_results/validation/validation_summary.feather"

run_summary <- arrow::read_feather(SUMMARY_INPUT_PATH)    
cumul_net_changes <- arrow::read_feather(CUMUL_NET_CHANGE_INPUT_PATH)

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
    geom_bar(stat="identity", position=position_dodge()) 

plot(p2)


## Plot cumulative net gain in yield 

p3 <- ggplot(data=cumul_net_changes)

