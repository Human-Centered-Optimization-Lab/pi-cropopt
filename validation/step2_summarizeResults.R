library(dplyr)
library(magrittr)
library(stringr)

summarize <- function(input_tab) {
 
  output_tab <- input_tab %>% 
                mutate(imprv_yield = yield_rec > yield) %>%
                mutate(worse_yield = yield_rec < yield) %>% 
                mutate(good_leaching = leaching_rec >= leaching) %>%
                mutate(imprv_leaching = leaching_rec < leaching) %>%
                mutate(worse_leaching = leaching_rec > leaching) %>%
                mutate(loss_yield = ifelse(worse_yield, yield - yield_rec, 0)) %>%
                mutate(gain_yield = ifelse(imprv_yield, yield_rec - yield, 0)) %>% 
                mutate(loss_leaching = ifelse(worse_leaching, leaching_rec - leaching, 0 )) %>%
                mutate(gain_leaching = ifelse(imprv_leaching, leaching - leaching_rec, 0))
   
  return(output_tab)  
}

avg_yield_loss <- function(summ_tab){
  avg_loss <- sum(summ_tab$loss_yield)/sum(summ_tab$worse_yield)
  return(avg_loss)  
}

avg_yield_gain <- function(summ_tab){
  avg_gain <- sum(summ_tab$gain_yield)/sum(summ_tab$imprv_yield)
  return(avg_gain)  
}


## Reading data

COMM_PRACT_PATH           <- "/Volumes/data/Gilgamesh/kroppian/agovization_results/validation/comm_pract.feather"
IRR_ONLY_RESULT_PATH      <- "/Volumes/data/Gilgamesh/kroppian/agovization_results/validation/irr_only_result.feather"
NITRO_ONLY_RESULT_PATH    <- "/Volumes/data/Gilgamesh/kroppian/agovization_results/validation/nitro_only_result.feather"
ALL_RECS_RESULT_PATH      <- "/Volumes/data/Gilgamesh/kroppian/agovization_results/validation/all_recs_full_result.feather"

SUMMARY_OUTPUT_PATH <- "/Volumes/data/Gilgamesh/kroppian/agovization_results/validation/validation_summary.feather"
CUMUL_NET_CHANGE_OUTPUT_PATH <- "/Volumes/data/Gilgamesh/kroppian/agovization_results/validation/validation_summary.feather"

comm_pract           <- arrow::read_feather(COMM_PRACT_PATH)     
irr_only_result      <- arrow::read_feather(IRR_ONLY_RESULT_PATH)  
nitro_only_result    <- arrow::read_feather(NITRO_ONLY_RESULT_PATH)
all_recs_result      <- arrow::read_feather(ALL_RECS_RESULT_PATH)

year_count <- nrow(irr_only_result)

## Join the different practice tables with common practice tables

# Rename recommended columns to delineate them in the final column 
irr_only_result <- irr_only_result %>% 
                   rename(yield_rec = yield) %>%
                   rename(leaching_rec = leaching) %>%
                   rename(total_wat_rec = total_wat)

nitro_only_result <- nitro_only_result %>% 
                     rename(yield_rec = yield) %>%
                     rename(leaching_rec = leaching) %>%
                     rename(total_wat_rec = total_wat)

all_recs_result <- all_recs_result %>%
                        rename(yield_rec = yield) %>%
                        rename(leaching_rec = leaching) %>%
                        rename(total_wat_rec = total_wat)


# Join those puppies up
irr_only_result <- comm_pract %>%
                   full_join(irr_only_result)

nitro_only_result <- comm_pract %>% 
                     full_join(nitro_only_result)

all_recs_result <- comm_pract %>%
                   full_join(all_recs_result)

## Performance summary 

# Create supporting columns 
irr_only_summary <- summarize(irr_only_result)
nitro_only_summary <- summarize(nitro_only_result)
all_recs_summary <- summarize(all_recs_result)

# Create results table
run <- c("Irr recs only", "Nitro recs only", "Irr and Nitro recs")

percent_yield_impr <- c(
                        sum(irr_only_summary$imprv_yield)/year_count,
                        sum(nitro_only_summary$imprv_yield)/year_count,
                        sum(all_recs_summary$imprv_yield)/year_count
                        )

avg_yield_loss <- c(
                      avg_yield_loss(irr_only_summary),
                      avg_yield_loss(nitro_only_summary),
                      avg_yield_loss(all_recs_summary)
                    )

avg_yield_gain <- c(
                      avg_yield_gain(irr_only_summary),
                      avg_yield_gain(nitro_only_summary),
                      avg_yield_gain(all_recs_summary)
                    )


run_summary <- data.frame(run, percent_yield_impr, avg_yield_loss, avg_yield_gain)

## Year-by-year analysis

# Calculate the net gain from the recommended practices
net_changes_irr_only <- irr_only_result %>% 
                        mutate(irr_only_net_yield = yield_rec - yield) %>%
                        select(year, irr_only_net_yield)

net_changes_nitro_only <- nitro_only_result %>% 
                          mutate(nitro_only_net_yield = yield_rec - yield) %>%
                          select(year, nitro_only_net_yield)

net_changes_all_recs <- all_recs_result %>% 
                        mutate(all_rec_net_yield = yield_rec - yield) %>%
                        select(year, all_rec_net_yield)

net_changes <- net_changes_irr_only %>%
               full_join(net_changes_nitro_only) %>%
               full_join(net_changes_all_recs)
               

# Calculate the cumulative net gain from the recommended practices
cumul_net_changes <- net_changes %>% 
                     arrange(year) %>%
                     mutate(cumul_net_changes_irr = cumsum(irr_only_net_yield)) %>%
                     mutate(cumul_net_changes_nitro = cumsum(nitro_only_net_yield)) %>%
                     mutate(cumul_net_changes_all_recs = cumsum(all_rec_net_yield)) 
  




## Output results
arrow::write_feather(run_summary, SUMMARY_OUTPUT_PATH)
arrow::write_feather(cumul_net_changes, CUMUL_NET_CHANGE_OUTPUT_PATH)




