library(dplyr)
library(magrittr)
library(stringr)

## ------- Start - functions -------

summarize <- function(input_tab) {
 
  output_tab <- input_tab %>% 
                mutate(wat_eff = yield/total_wat) %>%
                mutate(wat_eff_rec = yield_rec/total_wat_rec) %>%
                mutate(imprv_yield = yield_rec > yield) %>%
                mutate(worse_yield = yield_rec < yield) %>% 
                mutate(good_leaching = leaching_rec >= leaching) %>%
                mutate(imprv_leaching = leaching_rec < leaching) %>%
                mutate(worse_leaching = leaching_rec > leaching) %>%
                mutate(imprv_wat_eff = wat_eff_rec > wat_eff) %>%
                mutate(worse_wat_eff = wat_eff_rec < wat_eff) %>%
                mutate(loss_yield = ifelse(worse_yield, yield - yield_rec, 0)) %>%
                mutate(gain_yield = ifelse(imprv_yield, yield_rec - yield, 0)) %>% 
                mutate(loss_leaching = ifelse(worse_leaching, leaching_rec - leaching, 0 )) %>%
                mutate(gain_leaching = ifelse(imprv_leaching, leaching - leaching_rec, 0)) %>%
                mutate(loss_wat_eff = ifelse(worse_wat_eff, wat_eff - wat_eff_rec, 0)) %>%
                mutate(gain_wat_eff = ifelse(imprv_wat_eff, wat_eff_rec - wat_eff, 0)) 
  
   
  return(output_tab)  
}

calc_avg_yield_loss <- function(summ_tab){
  avg_loss <- sum(summ_tab$loss_yield)/sum(summ_tab$worse_yield)
  return(avg_loss)  
}

calc_avg_yield_gain <- function(summ_tab){
  avg_gain <- sum(summ_tab$gain_yield)/sum(summ_tab$imprv_yield)
  return(avg_gain)  
}

calc_med_wat_eff_loss <- function(summ_tab){
  med_loss <- summ_tab %>% 
                filter(worse_wat_eff) %>% 
                summarise(a = median(loss_wat_eff)) %>% 
                pull(a)
  
  return(med_loss)
}

calc_med_wat_eff_gain <- function(summ_tab){
  med_gain <- summ_tab %>% 
                filter(imprv_wat_eff) %>% 
                summarise(a = median(gain_wat_eff)) %>% 
                pull(a)
  
  return(med_gain)
}

calc_avg_leaching_imprv <- function(summ_tab){
  avg_loss <- sum(summ_tab$loss_leaching)/sum(summ_tab$imprv_leaching)
  return(avg_loss)  
  
}

calc_avg_leaching_worsening <- function(summ_tab){
  avg_gain <- sum(summ_tab$gain_leaching)/sum(summ_tab$worse_leaching)
  return(avg_gain)  
}


## ------- End - functions -------

## ------- Start - Reading data -------

ROOT_PATH <- "Z:/Gilgamesh/kroppian/agovization_results/validation/"
ROOT_PATH <- "/Volumes/data/Gilgamesh/kroppian/agovization_results/validation/"

COMM_PRACT_PATH           <- paste(ROOT_PATH,  "comm_pract_full.feather", sep = "")
IRR_ONLY_RESULT_PATH      <- paste(ROOT_PATH,  "irr_full.feather", sep = "")
NITRO_ONLY_RESULT_PATH    <- paste(ROOT_PATH,  "nitro_full.feather", sep = "")
ALL_RECS_RESULT_PATH      <- paste(ROOT_PATH,  "all_recs_full.feather", sep = "")

SUMMARY_OUTPUT_PATH <- paste(ROOT_PATH, "validation_summary.feather", sep = "")
CUMUL_NET_CHANGE_OUTPUT_PATH <- paste(ROOT_PATH, "cumul_net_change.feather", sep = "")
PRETTY_TAB_OUTPUT_PATH <- paste(ROOT_PATH, "pretty_tab.csv", sep="")

comm_pract_full           <- arrow::read_feather(COMM_PRACT_PATH)     
irr_only_result_full      <- arrow::read_feather(IRR_ONLY_RESULT_PATH)  
nitro_only_result_full    <- arrow::read_feather(NITRO_ONLY_RESULT_PATH)
all_recs_result_full      <- arrow::read_feather(ALL_RECS_RESULT_PATH)


run_ids     <- unique(comm_pract_full %>% pull(run))
year_count  <- length(unique(comm_pract_full %>% pull(year)))


## ------- End - Reading data -------


for (run_id in run_ids){
  
  ## ------- Start - Join rec practices with com practices -------
 
  print(paste("Processing run", run_id)) 
  
  comm_pract        <- comm_pract_full        %>% filter(run == run_id)
  irr_only_result   <- irr_only_result_full   %>% filter(run == run_id)
  nitro_only_result <- nitro_only_result_full %>% filter(run == run_id)
  all_recs_result   <- all_recs_result_full   %>% filter(run == run_id)
  
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
  
  
  ## ------- End - Join rec practices with com practices -------
  
  ## ------- Start - Calculate innovization performance  -------
  
  # Create supporting columns 
  irr_only_summary <- summarize(irr_only_result)
  nitro_only_summary <- summarize(nitro_only_result)
  all_recs_summary <- summarize(all_recs_result)
  
  # Create summarized results table
  run_type <- c("Irr recs only", "Nitro recs only", "Irr and Nitro recs")
  
  # Start - Yearly yield summaries
  percent_yield_impr <- c(
                          sum(irr_only_summary$imprv_yield)/year_count,
                          sum(nitro_only_summary$imprv_yield)/year_count,
                          sum(all_recs_summary$imprv_yield)/year_count
                          )
  
  avg_yield_losses <- c(
                        calc_avg_yield_loss(irr_only_summary)  ,
                        calc_avg_yield_loss(nitro_only_summary),
                        calc_avg_yield_loss(all_recs_summary)
                      )
  
  max_yield_loss <- c(
                      irr_only_summary %>% 
                        filter(worse_yield) %>% 
                        mutate(diff=yield-yield_rec) %>% 
                        summarise(m = max(diff)) %>% pull(m),
                      nitro_only_summary %>% 
                        filter(worse_yield) %>% 
                        mutate(diff=yield-yield_rec) %>% 
                        summarise(m = max(diff)) %>% pull(m),
                      all_recs_summary %>% 
                        filter(worse_yield) %>% 
                        mutate(diff=yield-yield_rec) %>% 
                        summarise(m = max(diff)) %>% pull(m)
  )
  
  min_yield_loss <- c(
                      irr_only_summary %>% 
                        filter(worse_yield) %>% 
                        mutate(diff=yield-yield_rec) %>% 
                        summarise(m = min(diff)) %>% pull(m),
                      nitro_only_summary %>% 
                        filter(worse_yield) %>% 
                        mutate(diff=yield-yield_rec) %>% 
                        summarise(m = min(diff)) %>% pull(m),
                      all_recs_summary %>% 
                        filter(worse_yield) %>% 
                        mutate(diff=yield-yield_rec) %>% 
                        summarise(m = min(diff)) %>% pull(m)
  )
  
  max_yield_gain <- c(
                      irr_only_summary %>% 
                        filter(imprv_yield) %>% 
                        mutate(diff=yield_rec-yield) %>% 
                        summarise(m = max(diff)) %>% pull(m),
                      nitro_only_summary %>% 
                        filter(imprv_yield) %>% 
                        mutate(diff=yield_rec-yield) %>% 
                        summarise(m = max(diff)) %>% pull(m),
                      all_recs_summary %>% 
                        filter(imprv_yield) %>% 
                        mutate(diff=yield_rec-yield) %>% 
                        summarise(m = max(diff)) %>% pull(m)
  )
  
  min_yield_gain <- c(
                      irr_only_summary %>% 
                        filter(imprv_yield) %>% 
                        mutate(diff=yield_rec-yield) %>% 
                        summarise(m = min(diff)) %>% pull(m),
                      nitro_only_summary %>% 
                        filter(imprv_yield) %>% 
                        mutate(diff=yield_rec-yield) %>% 
                        summarise(m = min(diff)) %>% pull(m),
                      all_recs_summary %>% 
                        filter(imprv_yield) %>% 
                        mutate(diff=yield_rec-yield) %>% 
                        summarise(m = min(diff)) %>% pull(m)
  )
  
  avg_yield_gains <- c(
                        calc_avg_yield_gain(irr_only_summary),
                        calc_avg_yield_gain(nitro_only_summary),
                        calc_avg_yield_gain(all_recs_summary)
                      )
  
  # End - Yearly yield summaries
  
  # Start - Yearly water use  summaries
  percent_wat_eff_impr <- c(
                          sum(irr_only_summary$imprv_wat_eff)/year_count,
                          sum(nitro_only_summary$imprv_wat_eff)/year_count,
                          sum(all_recs_summary$imprv_wat_eff)/year_count
                          )
  
  max_wat_eff_gain <- c(
                      irr_only_summary %>% 
                        filter(imprv_wat_eff) %>% 
                        mutate(diff=wat_eff_rec-wat_eff) %>% 
                        summarise(m = max(diff)) %>% pull(m),
                      nitro_only_summary %>% 
                        filter(imprv_wat_eff) %>% 
                        mutate(diff=wat_eff_rec-wat_eff) %>% 
                        summarise(m = max(diff)) %>% pull(m),
                      all_recs_summary %>% 
                        filter(imprv_wat_eff) %>% 
                        mutate(diff=wat_eff_rec-wat_eff) %>% 
                        summarise(m = max(diff)) %>% pull(m)
  )
  
  min_wat_eff_gain <- c(
                      irr_only_summary %>% 
                        filter(imprv_wat_eff) %>% 
                        mutate(diff=wat_eff_rec-wat_eff) %>% 
                        summarise(m = min(diff)) %>% pull(m),
                      nitro_only_summary %>% 
                        filter(imprv_wat_eff) %>% 
                        mutate(diff=wat_eff_rec-wat_eff) %>% 
                        summarise(m = min(diff)) %>% pull(m),
                      all_recs_summary %>% 
                        filter(imprv_wat_eff) %>% 
                        mutate(diff=wat_eff_rec-wat_eff) %>% 
                        summarise(m = min(diff)) %>% pull(m)
  )
  
  max_wat_eff_loss <- c(
                      irr_only_summary %>% 
                        filter(worse_wat_eff) %>% 
                        mutate(diff=wat_eff-wat_eff_rec) %>% 
                        summarise(m = max(diff)) %>% pull(m),
                      nitro_only_summary %>% 
                        filter(worse_wat_eff) %>% 
                        mutate(diff=wat_eff-wat_eff_rec) %>% 
                        summarise(m = max(diff)) %>% pull(m),
                      all_recs_summary %>% 
                        filter(worse_wat_eff) %>% 
                        mutate(diff=wat_eff-wat_eff_rec) %>% 
                        summarise(m = max(diff)) %>% pull(m)
  )
  
  min_wat_eff_loss <- c(
                      irr_only_summary %>% 
                        filter(worse_wat_eff) %>% 
                        mutate(diff=wat_eff-wat_eff_rec) %>% 
                        summarise(m = min(diff)) %>% pull(m),
                      nitro_only_summary %>% 
                        filter(worse_wat_eff) %>% 
                        mutate(diff=wat_eff-wat_eff_rec) %>% 
                        summarise(m = min(diff)) %>% pull(m),
                      all_recs_summary %>% 
                        filter(worse_wat_eff) %>% 
                        mutate(diff=wat_eff-wat_eff_rec) %>% 
                        summarise(m = min(diff)) %>% pull(m)
  )
  
  
  med_wat_eff_losses <- c(
                        calc_med_wat_eff_loss(irr_only_summary),
                        calc_med_wat_eff_loss(nitro_only_summary),
                        calc_med_wat_eff_loss(all_recs_summary)
  )
  
  med_wat_eff_gain <- c(
                        calc_med_wat_eff_gain(irr_only_summary),
                        calc_med_wat_eff_gain(nitro_only_summary),
                        calc_med_wat_eff_gain(all_recs_summary)
  )
  
  # End - Yearly water use  summaries
  
  # Start - Yearly leaching summaries 
  percent_leaching_impr <- c(
                          sum(irr_only_summary$imprv_leaching)/year_count,
                          sum(nitro_only_summary$imprv_leaching)/year_count,
                          sum(all_recs_summary$imprv_leaching)/year_count
                          )
  
  max_leaching_imprv <- c(
                      irr_only_summary %>% 
                        filter(imprv_leaching) %>% 
                        mutate(diff=leaching-leaching_rec) %>% 
                        summarise(m = ifelse(length(diff) == 0, 0, max(diff))) %>% 
                        pull(m),
                      nitro_only_summary %>% 
                        filter(imprv_leaching) %>% 
                        mutate(diff=leaching-leaching_rec) %>% 
                        summarise(m = ifelse(length(diff) == 0, 0, max(diff))) %>% 
                        pull(m),
                      all_recs_summary %>% 
                        filter(imprv_leaching) %>% 
                        mutate(diff=leaching-leaching_rec) %>% 
                        summarise(m = ifelse(length(diff) == 0, 0, max(diff))) %>% 
                        pull(m)
  )
  
  min_leaching_imprv <- c(
                      irr_only_summary %>% 
                        filter(imprv_leaching) %>% 
                        mutate(diff=leaching-leaching_rec) %>% 
                        summarise(m = ifelse(length(diff) == 0, 0, max(diff))) %>% pull(m),
                      nitro_only_summary %>% 
                        filter(imprv_leaching) %>% 
                        mutate(diff=leaching-leaching_rec) %>% 
                        summarise(m = ifelse(length(diff) == 0, 0, max(diff))) %>% pull(m),
                      all_recs_summary %>% 
                        filter(imprv_leaching) %>% 
                        mutate(diff=leaching-leaching_rec) %>% 
                        summarise(m = ifelse(length(diff) == 0, 0, max(diff))) %>% pull(m)
  )
  
  max_leaching_worsening <- c(
                      irr_only_summary %>% 
                        filter(worse_leaching) %>% 
                        mutate(diff=leaching_rec-leaching) %>% 
                        summarise(m = ifelse(length(diff) == 0, 0, max(diff))) %>% pull(m),
                      nitro_only_summary %>% 
                        filter(worse_leaching) %>% 
                        mutate(diff=leaching_rec-leaching) %>% 
                        summarise(m = ifelse(length(diff) == 0, 0, max(diff))) %>% pull(m),
                      all_recs_summary %>% 
                        filter(worse_leaching) %>% 
                        mutate(diff=leaching_rec-leaching) %>% 
                        summarise(m = ifelse(length(diff) == 0, 0, max(diff))) %>% pull(m)
  )
  
  min_leaching_worsening <- c(
                      irr_only_summary %>% 
                        filter(worse_leaching) %>% 
                        mutate(diff=leaching_rec-leaching) %>% 
                        summarise(m = ifelse(length(diff) == 0, 0, max(diff))) %>% pull(m),
                      nitro_only_summary %>% 
                        filter(worse_leaching) %>% 
                        mutate(diff=leaching_rec-leaching) %>% 
                        summarise(m = ifelse(length(diff) == 0, 0, max(diff))) %>% pull(m),
                      all_recs_summary %>% 
                        filter(worse_leaching) %>% 
                        mutate(diff=leaching_rec-leaching) %>% 
                        summarise(m = ifelse(length(diff) == 0, 0, max(diff))) %>% pull(m)
  )
  
  
  avg_leaching_imprv <- c(
                        calc_avg_leaching_imprv(irr_only_summary),
                        calc_avg_leaching_imprv(nitro_only_summary),
                        calc_avg_leaching_imprv(all_recs_summary)
  )
  
  avg_leaching_worsening <- c(
                        calc_avg_leaching_worsening(irr_only_summary),
                        calc_avg_leaching_worsening(nitro_only_summary),
                        calc_avg_leaching_worsening(all_recs_summary)
  )
  # End - Yearly leaching summaries 
  
  run_summary <- data.frame(run_type, percent_yield_impr, avg_yield_losses, 
                            avg_yield_gains, max_yield_loss, min_yield_loss, 
                            max_yield_gain, min_yield_gain, percent_wat_eff_impr,
                            med_wat_eff_losses, med_wat_eff_gain, min_wat_eff_gain, 
                            max_wat_eff_gain, max_wat_eff_loss, min_wat_eff_loss,
                            percent_leaching_impr, max_leaching_imprv, 
                            min_leaching_imprv, max_leaching_worsening, 
                            min_leaching_worsening, avg_leaching_imprv, 
                            avg_leaching_worsening)
  
  ## ------- End - Calculate innovization performance -------
  
  ## ------- Start - Year-by-year analysis -------
  
  # Calculate the net yield gain from the recommended practices
  net_yield_changes_irr_only <- irr_only_result %>% 
                          mutate(irr_only_net_yield = yield_rec - yield) %>%
                          dplyr::select(year, irr_only_net_yield)
  
  net_yield_changes_nitro_only <- nitro_only_result %>% 
                            mutate(nitro_only_net_yield = yield_rec - yield) %>%
                            dplyr::select(year, nitro_only_net_yield)
  
  net_yield_changes_all_recs <- all_recs_result %>% 
                          mutate(all_rec_net_yield = yield_rec - yield) %>%
                          dplyr::select(year, all_rec_net_yield)
  
  
  # Calculate the net leach change from the recommended practices
  net_leach_changes_irr_only <- irr_only_result %>% 
                          mutate(irr_only_net_leach = leaching_rec - leaching) %>%
                          dplyr::select(year, irr_only_net_leach)
  
  net_leach_changes_nitro_only <- nitro_only_result %>% 
                            mutate(nitro_only_net_leach = leaching_rec - leaching) %>%
                            dplyr::select(year, nitro_only_net_leach)
  
  net_leach_changes_all_recs <- all_recs_result %>% 
                          mutate(all_rec_net_leach = leaching_rec - leaching) %>%
                          dplyr::select(year, all_rec_net_leach)
  
  
  
  
  
  net_changes <- net_yield_changes_irr_only %>%
                 full_join(net_yield_changes_nitro_only) %>%
                 full_join(net_yield_changes_all_recs) %>%
                 full_join(net_leach_changes_irr_only) %>%
                 full_join(net_leach_changes_nitro_only) %>%
                 full_join(net_leach_changes_all_recs) 
                 
  
  # Calculate the cumulative net gain from the recommended practices
  cumul_net_change <- net_changes %>% 
                       arrange(year) %>%
                       mutate(cumul_net_yield_changes_irr = cumsum(irr_only_net_yield)) %>%
                       mutate(cumul_net_yield_changes_nitro = cumsum(nitro_only_net_yield)) %>%
                       mutate(cumul_net_yield_changes_all_recs = cumsum(all_rec_net_yield)) %>%
                       mutate(cumul_net_leach_changes_irr = cumsum(irr_only_net_leach)) %>%
                       mutate(cumul_net_leach_changes_nitro = cumsum(nitro_only_net_leach)) %>%
                       mutate(cumul_net_leach_changes_all_recs = cumsum(all_rec_net_leach)) 
    
  
  
  print(str_interp("Average leaching: ${mean(comm_pract$leaching)}"))
  
  ## ------- End - Year-by-year analysis -------
  
  ## ------- Start - Create pretty table -------
  
  # Rename recommended columns to delineate them in the final column 
  df1 <- irr_only_summary %>% 
                     rename(irr_only_yield     = yield_rec) %>%
                     rename(irr_only_leaching  = leaching_rec) %>%
                     rename(irr_only_total_wat = total_wat_rec)  %>%
                     rename(irr_only_wat_eff   = wat_eff_rec) %>% 
                     dplyr::select(year, climate, yield, leaching, total_wat, wat_eff,
                                   irr_only_yield, irr_only_leaching, 
                                   irr_only_total_wat, irr_only_wat_eff)
    
  
  
  df2 <- nitro_only_summary %>% 
                       rename(nitr_only_yield     = yield_rec) %>%
                       rename(nitr_only_leaching  = leaching_rec) %>%
                       rename(nitr_only_total_wat = total_wat_rec) %>%
                       rename(nitr_only_wat_eff   = wat_eff_rec) %>%
                       dplyr::select(year, climate, yield, leaching, total_wat, wat_eff,
                                   nitr_only_yield, nitr_only_leaching, 
                                   nitr_only_total_wat, nitr_only_wat_eff)
    
  
  df3 <- all_recs_summary %>%
                          rename(all_rec_yield = yield_rec) %>%
                          rename(all_rec_leaching = leaching_rec) %>%
                          rename(all_rec_total_wat = total_wat_rec) %>%
                          rename(all_rec_wat_eff   = wat_eff_rec) %>%
                          dplyr::select(year, climate, yield, leaching, total_wat, wat_eff,
                                   all_rec_yield, all_rec_leaching,
                                   all_rec_total_wat, all_rec_wat_eff )
  
  
  
  pretty_tab <- df1 %>%
                full_join(df2) %>%
                full_join(df3) %>%
                arrange(year)

  
 
  if(!exists("run_summaries")){
    run_summaries     <- run_summary      %>% mutate(run_id = run_id)
    cumul_net_changes <- cumul_net_change %>% mutate(run_id = run_id)
    pretty_tabs       <- pretty_tab       %>% mutate(run_id = run_id)
  }else{
    run_summaries     <- rbind(run_summaries,     run_summary %>% mutate(run_id = run_id)) 
    cumul_net_changes <- rbind(cumul_net_changes, cumul_net_change %>% mutate(run_id = run_id))
    pretty_tabs       <- rbind(pretty_tabs,       pretty_tab %>% mutate(run_id = run_id))
  }
  
  
  
  ## ------- End - Create pretty table -------
 
}


## ------- End - Output results -------

arrow::write_feather(run_summaries, SUMMARY_OUTPUT_PATH)
arrow::write_feather(cumul_net_changes, CUMUL_NET_CHANGE_OUTPUT_PATH)
#write.csv(pretty_tab, PRETTY_TAB_OUTPUT_PATH)



