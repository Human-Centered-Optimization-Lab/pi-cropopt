
## Get data 

ROOT_PATH <- "Z:/Gilgamesh/kroppian/agovization_results/validation/"
ROOT_PATH <- "/Volumes/data/Gilgamesh/kroppian/agovization_results/validation/"

COMM_PRACT_PATH           <- paste(ROOT_PATH,  "comm_pract_full.feather", sep = "")
IRR_ONLY_RESULT_PATH      <- paste(ROOT_PATH,  "nitro_full.feather", sep = "")
NITRO_ONLY_RESULT_PATH    <- paste(ROOT_PATH,  "all_recs_full.feather", sep = "")
ALL_RECS_RESULT_PATH      <- paste(ROOT_PATH,  "irr_full.feather", sep = "")

SUMMARY_OUTPUT_PATH <- paste(ROOT_PATH, "validation_summary.feather", sep = "")
CUMUL_NET_CHANGE_OUTPUT_PATH <- paste(ROOT_PATH, "cumul_net_change.feather", sep = "")
PRETTY_TAB_OUTPUT_PATH <- paste(ROOT_PATH, "pretty_tab.csv", sep="")

comm_pract_full    <- arrow::read_feather(COMM_PRACT_PATH)     
irr_only_full      <- arrow::read_feather(IRR_ONLY_RESULT_PATH)  
nitro_only_full    <- arrow::read_feather(NITRO_ONLY_RESULT_PATH)
all_recs_full      <- arrow::read_feather(ALL_RECS_RESULT_PATH)


## Year-by-year plotting
if(! is.null(dev.list())){
  dev.off(dev.list()["RStudioGD"]) # Clears plots
}

hist(comm_pract_full$yield, 20, main="Common practices year-by-year")
hist(irr_only_full$yield  , 20, main="Irr only year-by-year")
hist(nitro_only_full$yield, 20, main="Nitro only year-by-year")
hist(all_recs_full$yield  , 20, main="All recs year-by-year")

## Cumulative plotting 

# Clear old plots

comm_pract_tyield <- comm_pract_full %>% group_by(run) %>% summarize(total_yield = sum(yield)) %>% pull(total_yield)
irr_only_tyield <- irr_only_full %>% group_by(run) %>% summarize(total_yield = sum(yield)) %>% pull(total_yield)
nitro_only_tyield <- nitro_only_full %>% group_by(run) %>% summarize(total_yield = sum(yield)) %>% pull(total_yield)
all_recs_tyield <- all_recs_full %>% group_by(run) %>% summarize(total_yield = sum(yield)) %>% pull(total_yield)

# individual plots
hist(comm_pract_tyield, 20)
hist(nitro_only_tyield, 20)
hist(all_recs_tyield, 20)
hist(irr_only_tyield, 20)


# comm vs irr
max_l <- max(max(comm_pract_tyield), max(irr_only_tyield))*1.05
min_l <- min(min(comm_pract_tyield), min(irr_only_tyield))*0.95
hist(comm_pract_tyield, 20, col=rgb(0,0,1,1/4), xlim=c(min_l, max_l), main="Irrigation only recommendations")  # first histogram
hist(irr_only_tyield, 20, col=rgb(1,0,0,1/4), xlim=c(min_l, max_l), add=T, main="Irrigation only recommendations")  # second
#legend(x = "topleft", legend = c("Common Practices", "Irrigation recommendations"), fill= c(rgb(0,0,1,1/4), rgb(1,0,0,1/4)))

# comm vs nitro
max_l <- max(max(comm_pract_tyield), max(nitro_only_tyield))*1.05
min_l <- min(min(comm_pract_tyield), min(nitro_only_tyield))*0.95
hist( comm_pract_tyield, 20, col=rgb(0,0,1,1/4), xlim=c(min_l, max_l), main="Nitrogen only recommendations")  # first histogram
hist( nitro_only_tyield, 20, col=rgb(1,0,0,1/4), xlim=c(min_l, max_l), add=T, main="Nitrogen only recommendations")  # second
#legend(x = "topleft", legend = c("Common Practices", "Nitrogen recommendations"), fill= c(rgb(0,0,1,1/4), rgb(1,0,0,1/4)))

# comm vs all recs  
max_l <- max(max(comm_pract_tyield), max(all_recs_tyield))*1.05
min_l <- min(min(comm_pract_tyield), min(all_recs_tyield))*0.95
hist( comm_pract_tyield, 20, col=rgb(0,0,1,1/4), xlim=c(min_l, max_l))  # first histogram
hist( all_recs_tyield, 20, col=rgb(1,0,0,1/4),   xlim=c(min_l, max_l), add=T)  # second
#legend(x = "topleft", legend = c("Common Practices", "All recommendations"), fill= c(rgb(0,0,1,1/4), rgb(1,0,0,1/4)))



## Year-by-year tests
print("year-by-year change in yield")
print("t.test")
p_irr_t   <- t.test(comm_pract_full$yield, irr_only_full$yield  )
p_nitro_t <- t.test(comm_pract_full$yield, nitro_only_full$yield)
p_all_t   <- t.test(comm_pract_full$yield, all_recs_full$yield  )
print(p_irr_t$p.value    )
print(p_nitro_t$p.value  )
print(p_all_t$p.value    )

print("Wilcoxon")
p_irr_w   <- wilcox.test(comm_pract_full$yield, irr_only_full$yield)
p_nitro_w <- wilcox.test(comm_pract_full$yield, nitro_only_full$yield)
p_all_w   <- wilcox.test(comm_pract_full$yield, all_recs_full$yield)
print(p_irr_w$p.value    )
print(p_nitro_w$p.value  )
print(p_all_w$p.value    )


## Cumulative tests

print("Cumulative change in yield")
print("t.test")
p_irr_t   <- t.test(comm_pract_tyield, irr_only_tyield)
p_nitro_t <- t.test(comm_pract_tyield, nitro_only_tyield)
p_all_t   <- t.test(comm_pract_tyield, all_recs_tyield)
print(p_irr_t$p.value    )
print(p_nitro_t$p.value  )
print(p_all_t$p.value    )

print("Wilcoxon")
p_irr_w   <- wilcox.test(comm_pract_tyield, irr_only_tyield)
p_nitro_w <- wilcox.test(comm_pract_tyield, nitro_only_tyield)
p_all_w   <- wilcox.test(comm_pract_tyield, all_recs_tyield)
print(p_irr_w$p.value    )
print(p_nitro_w$p.value  )
print(p_all_w$p.value    )






