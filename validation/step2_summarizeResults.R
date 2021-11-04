library(dplyr)
library(magrittr)

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



## Reading data

COMM_PRACT_PATH           <- "/Volumes/data/Gilgamesh/kroppian/agovization_results/comm_pract.feather"
IRR_ONLY_RESULT_PATH      <- "/Volumes/data/Gilgamesh/kroppian/agovization_results/irr_only_result.feather"
NITRO_ONLY_RESULT_PATH    <- "/Volumes/data/Gilgamesh/kroppian/agovization_results/nitro_only_result.feather"
ALL_RECS_RESULT_PATH      <- "/Volumes/data/Gilgamesh/kroppian/agovization_results/all_recs_full_result.feather"

comm_pract           <- arrow::read_feather(COMM_PRACT_PATH)     
irr_only_result      <- arrow::read_feather(IRR_ONLY_RESULT_PATH)  
nitro_only_result    <- arrow::read_feather(NITRO_ONLY_RESULT_PATH)
all_recs_result      <- arrow::read_feather(ALL_RECS_RESULT_PATH)


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

irr_only_summary <- summarize(irr_only_result)

nitro_only_summary <- summarize(nitro_only_result)

all_recs_summary <- summarize(all_recs_result)




