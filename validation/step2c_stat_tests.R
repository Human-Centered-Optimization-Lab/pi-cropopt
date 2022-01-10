library("ggplot2")

## Functions
num2station <- function(numbers){
  
  result <- c() 
 
  for(num in numbers){
    
    if (num == 1 )      { result <- append(result, "ALLE")    } 
    else if (num == 2 ) { result <- append(result, "BAIN")  }
    else if (num == 3 ) { result <- append(result, "BENT") }
    else if (num == 4 ) { result <- append(result, "BERR") }
    else if (num == 5 ) { result <- append(result, "CASS") }
    else if (num == 6 ) { result <- append(result, "DOWA") }
    else if (num == 7 ) { result <- append(result, "FENN") }
    else if (num == 8 ) { result <- append(result, "GRAN") }
    else if (num == 9 ) { result <- append(result, "HART") }
    else if (num == 10) { result <- append(result, "KEEL") }
    else if (num == 11) { result <- append(result, "LAWR")  }
    else if (num == 12) { result <- append(result, "LAWT") }
    else if (num == 13) { result <- append(result, "OSHT") }
    else if (num == 14) { result <- append(result, "SCOT") }
    else if (num == 15) { result <- append(result, "SOUT") }
    else                { result <- append(result, "WHOOPS")  }
    
  } 
  return(result)
}

## Get data 

ROOT_PATH <- "Z:/Gilgamesh/kroppian/agovization_results/validation/"
ROOT_PATH <- "/Volumes/data/Gilgamesh/kroppian/agovization_results/validation/"

COMM_PRACT_PATH           <- paste(ROOT_PATH,  "comm_pract_full.feather", sep = "")
IRR_ONLY_RESULT_PATH      <- paste(ROOT_PATH,  "irr_full.feather", sep = "")
NITRO_ONLY_RESULT_PATH    <- paste(ROOT_PATH,  "nitro_full.feather", sep = "")
ALL_RECS_RESULT_PATH      <- paste(ROOT_PATH,  "all_recs_full.feather", sep = "")
CLIM_PATH                 <- paste(ROOT_PATH,  "climate.feather", sep="")

SUMMARY_OUTPUT_PATH <- paste(ROOT_PATH, "validation_summary.feather", sep = "")
CUMUL_NET_CHANGE_OUTPUT_PATH <- paste(ROOT_PATH, "cumul_net_change.feather", sep = "")
PRETTY_TAB_OUTPUT_PATH <- paste(ROOT_PATH, "pretty_tab.csv", sep="")

comm_pract_full    <- arrow::read_feather(COMM_PRACT_PATH)     
irr_only_full      <- arrow::read_feather(IRR_ONLY_RESULT_PATH)  
nitro_only_full    <- arrow::read_feather(NITRO_ONLY_RESULT_PATH)
all_recs_full      <- arrow::read_feather(ALL_RECS_RESULT_PATH)
climate            <- arrow::read_feather(CLIM_PATH)


## Preprocessing

climate <- climate %>% rename(climate = clim)

comm_pract_full <- comm_pract_full %>% mutate(wat_eff = yield/total_wat) %>% mutate(station = num2station(run)) %>% select(-run)    
irr_only_full   <- irr_only_full   %>% mutate(wat_eff = yield/total_wat) %>% mutate(station = num2station(run)) %>% select(-run) 
nitro_only_full <- nitro_only_full %>% mutate(wat_eff = yield/total_wat) %>% mutate(station = num2station(run)) %>% select(-run) 
all_recs_full   <- all_recs_full   %>% mutate(wat_eff = yield/total_wat) %>% mutate(station = num2station(run)) %>% select(-run) 


comm_pract_full <- comm_pract_full %>% select(-climate) %>% full_join(climate)
irr_only_full   <- irr_only_full   %>% select(-climate) %>% full_join(climate)
nitro_only_full <- nitro_only_full %>% select(-climate) %>% full_join(climate)
all_recs_full   <- all_recs_full   %>% select(-climate) %>% full_join(climate)

# Remove Cass, as it was what the innovization is trained off of 
comm_pract_full_nocass <- comm_pract_full %>% filter(station != "CASS")

# Initialize what will be our pvalue table
strategies     <- c("Irrigation recommendations", "Nitrogen recommendations", "All recommendations")


## Year-by-year tests
print("year-by-year change in yield -- all years")
p_irr_w   <- wilcox.test(comm_pract_full_nocass %>% pull(yield), irr_only_full   %>% pull(yield))
p_nitro_w <- wilcox.test(comm_pract_full_nocass %>% pull(yield), nitro_only_full %>% pull(yield))
p_all_w   <- wilcox.test(comm_pract_full_nocass %>% pull(yield), all_recs_full   %>% pull(yield))
print(p_irr_w$p.value    )
print(p_nitro_w$p.value  )
print(p_all_w$p.value    )

pvals_yield <- c(p_irr_w$p.value, p_nitro_w$p.value, p_all_w$p.value)

print("year-by-year change in yield -- dry years")
p_irr_w   <- wilcox.test(comm_pract_full_nocass %>% filter(climate == 0) %>% pull(yield), irr_only_full   %>% filter(climate == 0) %>% pull(yield))
p_nitro_w <- wilcox.test(comm_pract_full_nocass %>% filter(climate == 0) %>% pull(yield), nitro_only_full %>% filter(climate == 0) %>% pull(yield))
p_all_w   <- wilcox.test(comm_pract_full_nocass %>% filter(climate == 0) %>% pull(yield), all_recs_full   %>% filter(climate == 0) %>% pull(yield))
print(p_irr_w$p.value    )
print(p_nitro_w$p.value  )
print(p_all_w$p.value    )

pvals_yield_dry <- c(p_irr_w$p.value, p_nitro_w$p.value, p_all_w$p.value)

print("year-by-year change in yield -- normal years")
p_irr_w   <- wilcox.test(comm_pract_full_nocass %>% filter(climate == 1) %>% pull(yield), irr_only_full   %>% filter(climate == 1) %>% pull(yield))
p_nitro_w <- wilcox.test(comm_pract_full_nocass %>% filter(climate == 1) %>% pull(yield), nitro_only_full %>% filter(climate == 1) %>% pull(yield))
p_all_w   <- wilcox.test(comm_pract_full_nocass %>% filter(climate == 1) %>% pull(yield), all_recs_full   %>% filter(climate == 1) %>% pull(yield))
print(p_irr_w$p.value    )
print(p_nitro_w$p.value  )
print(p_all_w$p.value    )

pvals_yield_norm <- c(p_irr_w$p.value, p_nitro_w$p.value, p_all_w$p.value)

print("year-by-year change in yield -- wet years")
p_irr_w   <- wilcox.test(comm_pract_full_nocass %>% filter(climate == 2) %>% pull(yield), irr_only_full   %>% filter(climate == 2) %>% pull(yield))
p_nitro_w <- wilcox.test(comm_pract_full_nocass %>% filter(climate == 2) %>% pull(yield), nitro_only_full %>% filter(climate == 2) %>% pull(yield))
p_all_w   <- wilcox.test(comm_pract_full_nocass %>% filter(climate == 2) %>% pull(yield), all_recs_full   %>% filter(climate == 2) %>% pull(yield))
print(p_irr_w$p.value    )
print(p_nitro_w$p.value  )
print(p_all_w$p.value    )

pvals_yield_wet <- c(p_irr_w$p.value, p_nitro_w$p.value, p_all_w$p.value)


print("year-by-year change in leaching -- all years")
p_irr_w   <- wilcox.test(comm_pract_full_nocass %>% pull(leaching), irr_only_full   %>% pull(leaching))
p_nitro_w <- wilcox.test(comm_pract_full_nocass %>% pull(leaching), nitro_only_full %>% pull(leaching))
p_all_w   <- wilcox.test(comm_pract_full_nocass %>% pull(leaching), all_recs_full   %>% pull(leaching))
print(p_irr_w$p.value    )
print(p_nitro_w$p.value  )
print(p_all_w$p.value    )

pvals_leaching <- c(p_irr_w$p.value, p_nitro_w$p.value, p_all_w$p.value)

print("year-by-year change in leaching -- dry years")
p_irr_w   <- wilcox.test(comm_pract_full_nocass %>% filter(climate == 0) %>% pull(leaching), irr_only_full   %>% filter(climate == 0)  %>% pull(leaching))
p_nitro_w <- wilcox.test(comm_pract_full_nocass %>% filter(climate == 0) %>% pull(leaching), nitro_only_full %>% filter(climate == 0)  %>% pull(leaching))
p_all_w   <- wilcox.test(comm_pract_full_nocass %>% filter(climate == 0) %>% pull(leaching), all_recs_full   %>% filter(climate == 0)  %>% pull(leaching))
print(p_irr_w$p.value    )
print(p_nitro_w$p.value  )
print(p_all_w$p.value    )

pvals_leaching_dry <- c(p_irr_w$p.value, p_nitro_w$p.value, p_all_w$p.value)

print("year-by-year change in leaching -- norm years")
p_irr_w   <- wilcox.test(comm_pract_full_nocass %>% filter(climate == 1) %>% pull(leaching), irr_only_full   %>% filter(climate == 1) %>% pull(leaching))
p_nitro_w <- wilcox.test(comm_pract_full_nocass %>% filter(climate == 1) %>% pull(leaching), nitro_only_full %>% filter(climate == 1) %>% pull(leaching))
p_all_w   <- wilcox.test(comm_pract_full_nocass %>% filter(climate == 1) %>% pull(leaching), all_recs_full   %>% filter(climate == 1) %>% pull(leaching))
print(p_irr_w$p.value    )
print(p_nitro_w$p.value  )
print(p_all_w$p.value    )

pvals_leaching_norm <- c(p_irr_w$p.value, p_nitro_w$p.value, p_all_w$p.value)

print("year-by-year change in leaching -- wet years")
p_irr_w   <- wilcox.test(comm_pract_full_nocass %>% filter(climate == 2) %>% pull(leaching), irr_only_full   %>% filter(climate == 2) %>% pull(leaching))
p_nitro_w <- wilcox.test(comm_pract_full_nocass %>% filter(climate == 2) %>% pull(leaching), nitro_only_full %>% filter(climate == 2) %>% pull(leaching))
p_all_w   <- wilcox.test(comm_pract_full_nocass %>% filter(climate == 2) %>% pull(leaching), all_recs_full   %>% filter(climate == 2) %>% pull(leaching))
print(p_irr_w$p.value    )
print(p_nitro_w$p.value  )
print(p_all_w$p.value    )

pvals_leaching_wet <- c(p_irr_w$p.value, p_nitro_w$p.value, p_all_w$p.value)

print("year-by-year change in water efficiency -- all years")
p_irr_w   <- wilcox.test(comm_pract_full_nocass %>% pull(wat_eff), irr_only_full   %>% pull(wat_eff))
p_nitro_w <- wilcox.test(comm_pract_full_nocass %>% pull(wat_eff), nitro_only_full %>% pull(wat_eff))
p_all_w   <- wilcox.test(comm_pract_full_nocass %>% pull(wat_eff), all_recs_full   %>% pull(wat_eff))
print(p_irr_w$p.value    )
print(p_nitro_w$p.value  )
print(p_all_w$p.value    )

pvals_wat_eff <- c(p_irr_w$p.value, p_nitro_w$p.value, p_all_w$p.value)

print("year-by-year change in water efficiency -- dry")
p_irr_w   <- wilcox.test(comm_pract_full_nocass %>% filter(climate == 0) %>% pull(wat_eff), irr_only_full   %>% filter(climate == 0) %>% pull(wat_eff) )
p_nitro_w <- wilcox.test(comm_pract_full_nocass %>% filter(climate == 0) %>% pull(wat_eff), nitro_only_full %>% filter(climate == 0) %>% pull(wat_eff) )
p_all_w   <- wilcox.test(comm_pract_full_nocass %>% filter(climate == 0) %>% pull(wat_eff), all_recs_full   %>% filter(climate == 0) %>% pull(wat_eff) )
print(p_irr_w$p.value    )
print(p_nitro_w$p.value  )
print(p_all_w$p.value    )

pvals_wat_eff_dry <- c(p_irr_w$p.value, p_nitro_w$p.value, p_all_w$p.value)

print("year-by-year change in water efficiency -- norm")
p_irr_w   <- wilcox.test(comm_pract_full_nocass %>% filter(climate == 1) %>% pull(wat_eff), irr_only_full   %>% filter(climate == 1) %>% pull(wat_eff))
p_nitro_w <- wilcox.test(comm_pract_full_nocass %>% filter(climate == 1) %>% pull(wat_eff), nitro_only_full %>% filter(climate == 1) %>% pull(wat_eff))
p_all_w   <- wilcox.test(comm_pract_full_nocass %>% filter(climate == 1) %>% pull(wat_eff), all_recs_full   %>% filter(climate == 1) %>% pull(wat_eff))
print(p_irr_w$p.value    )
print(p_nitro_w$p.value  )
print(p_all_w$p.value    )

pvals_wat_eff_norm <- c(p_irr_w$p.value, p_nitro_w$p.value, p_all_w$p.value)

print("year-by-year change in water efficiency -- wet")
p_irr_w   <- wilcox.test(comm_pract_full_nocass %>% filter(climate == 2) %>% pull(wat_eff), irr_only_full   %>% filter(climate == 2) %>% pull(wat_eff))
p_nitro_w <- wilcox.test(comm_pract_full_nocass %>% filter(climate == 2) %>% pull(wat_eff), nitro_only_full %>% filter(climate == 2) %>% pull(wat_eff))
p_all_w   <- wilcox.test(comm_pract_full_nocass %>% filter(climate == 2) %>% pull(wat_eff), all_recs_full   %>% filter(climate == 2) %>% pull(wat_eff))
print(p_irr_w$p.value    )
print(p_nitro_w$p.value  )
print(p_all_w$p.value    )

pvals_wat_eff_wet <- c(p_irr_w$p.value, p_nitro_w$p.value, p_all_w$p.value)
## Cumulative tests

print("Cumulative change in yield")
p_irr_w   <- wilcox.test(comm_pract_full %>% pull(yield), irr_only_full   %>% pull(yield))
p_nitro_w <- wilcox.test(comm_pract_full %>% pull(yield), nitro_only_full %>% pull(yield))
p_all_w   <- wilcox.test(comm_pract_full %>% pull(yield), all_recs_full   %>% pull(yield))
print(p_irr_w$p.value    )
print(p_nitro_w$p.value  )
print(p_all_w$p.value    )





## Build pvalue table

pval_tab      <- data.frame(strategies, pvals_yield, pvals_leaching, pvals_wat_eff)
pval_tab_dry  <- data.frame(strategies, pvals_yield_dry , pvals_leaching_dry , pvals_wat_eff_dry )
pval_tab_norm <- data.frame(strategies, pvals_yield_norm, pvals_leaching_norm, pvals_wat_eff_norm)
pval_tab_wet  <- data.frame(strategies, pvals_yield_wet , pvals_leaching_wet , pvals_wat_eff_wet )


