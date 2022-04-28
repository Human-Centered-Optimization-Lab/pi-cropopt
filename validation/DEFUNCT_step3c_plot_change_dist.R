library(ggplot2)
library(magrittr)


INPUT_DATA_ROOT <- 'Z:/Gilgamesh/kroppian/agovization_results/validation/'

SUMMARY_INPUT_PATH <- paste(INPUT_DATA_ROOT, "validation_summary.feather", sep="")
CUMUL_NET_CHANGE_OUTPUT_PATH <- paste(INPUT_DATA_ROOT, "cumul_net_change.feather", sep="")

#PLOT_OUTPUT_PATH <- "/Users/iankropp/OneDrive - Michigan State University/Documents/Shared/todo/paper1Innovization/figures/"
PLOT_OUTPUT_PATH <- 'C:/Users/Ian Kropp/OneDrive/OneDrive - Michigan State University/Documents/Shared/todo/paper1Innovization/figures/'


run_summary <- arrow::read_feather(SUMMARY_INPUT_PATH)    
cumul_net_changes <- arrow::read_feather(CUMUL_NET_CHANGE_OUTPUT_PATH)

# Clear old plots
if(! is.null(dev.list())){
  dev.off(dev.list()["RStudioGD"]) # Clears plots
}




irr_only <- cumul_net_changes %>% filter(year == 2018) %>% pull(cumul_net_yield_changes_irr)
nitro_only <- cumul_net_changes %>% filter(year == 2018) %>% pull(cumul_net_yield_changes_nitro)
all_recs <- cumul_net_changes %>% filter(year == 2018) %>% pull(cumul_net_yield_changes_all_recs)


hist(irr_only, 10)
hist(nitro_only, 10)
hist(all_recs, 10)

