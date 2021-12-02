library("ggplot2")
## Get data 

ROOT_PATH <- "Z:/Gilgamesh/kroppian/agovization_results/validation/"
ROOT_PATH <- "/Volumes/data/Gilgamesh/kroppian/agovization_results/validation/"

COMM_PRACT_PATH           <- paste(ROOT_PATH,  "comm_pract_full.feather", sep = "")
IRR_ONLY_RESULT_PATH      <- paste(ROOT_PATH,  "irr_full.feather", sep = "")
NITRO_ONLY_RESULT_PATH    <- paste(ROOT_PATH,  "nitro_full.feather", sep = "")
ALL_RECS_RESULT_PATH      <- paste(ROOT_PATH,  "all_recs_full.feather", sep = "")

SUMMARY_OUTPUT_PATH <- paste(ROOT_PATH, "validation_summary.feather", sep = "")
CUMUL_NET_CHANGE_OUTPUT_PATH <- paste(ROOT_PATH, "cumul_net_change.feather", sep = "")
PRETTY_TAB_OUTPUT_PATH <- paste(ROOT_PATH, "pretty_tab.csv", sep="")

comm_pract_full    <- arrow::read_feather(COMM_PRACT_PATH)     
irr_only_full      <- arrow::read_feather(IRR_ONLY_RESULT_PATH)  
nitro_only_full    <- arrow::read_feather(NITRO_ONLY_RESULT_PATH)
all_recs_full      <- arrow::read_feather(ALL_RECS_RESULT_PATH)

## Preprocessing

comm_pract_full <- comm_pract_full %>% mutate(wat_eff = yield/total_wat)
irr_only_full   <- irr_only_full   %>% mutate(wat_eff = yield/total_wat)
nitro_only_full <- nitro_only_full %>% mutate(wat_eff = yield/total_wat)
all_recs_full   <- all_recs_full   %>% mutate(wat_eff = yield/total_wat)



## Year-by-year plotting
if(! is.null(dev.list())){
  dev.off(dev.list()["RStudioGD"]) # Clears plots
}

# Yield single histogram
hist(comm_pract_full$yield, 20, main="Common practices year-by-year yield")
hist(irr_only_full$yield  , 20, main="Irr only year-by-year yield")
hist(nitro_only_full$yield, 20, main="Nitro only year-by-year yield")
hist(all_recs_full$yield  , 20, main="All recs year-by-year yield")

# Nitrogen leaching single histogram
hist(comm_pract_full$leaching, 20, main="Common practices year-by-year leaching")
hist(irr_only_full$leaching  , 20, main="Irr only year-by-year leaching")
hist(nitro_only_full$leaching, 20, main="Nitro only year-by-year leaching")
hist(all_recs_full$leaching  , 20, main="All recs year-by-year leaching")

# Water efficiency single histogram
hist(comm_pract_full$wat_eff, 20, main="Common practices year-by-year water efficiency")
hist(irr_only_full$wat_eff  , 20, main="Irr only year-by-year water efficiency")
hist(nitro_only_full$wat_eff, 20, main="Nitro only year-by-year water efficiency")
hist(all_recs_full$wat_eff  , 20, main="All recs year-by-year water efficiency")

# Yield comparative histogram
cat1 <- array(data="Common practices", dim = length(comm_pract_full$yield))
cat2 <- array(data="Irrigation recommendations", dim = length(comm_pract_full$yield))
dat <- data.frame(Yield=c(comm_pract_full$yield, irr_only_full$yield), Practices = c(cat1, cat2) )
ggplot(dat, aes(x=Yield, fill=Practices)) + 
        geom_histogram(alpha=0.2, position="identity") + 
        ggtitle("Distribution of yearly yields for irrigation recommendations")

cat1 <- array(data="Common practices", dim = length(comm_pract_full$yield))
cat2 <- array(data="Nitrogen recommendations", dim = length(comm_pract_full$yield))
dat <- data.frame(Yield=c(comm_pract_full$yield, nitro_only_full$yield), Practices = c(cat1, cat2) )
ggplot(dat, aes(x=Yield, fill=Practices)) + 
        geom_histogram(alpha=0.2, position="identity") + 
        ggtitle("Distribution of yearly yields for irrigation recommendations")

cat1 <- array(data="Common practices", dim = length(comm_pract_full$yield))
cat2 <- array(data="All recommendations", dim = length(comm_pract_full$yield))
dat <- data.frame(Yield=c(comm_pract_full$yield, all_recs_full$yield), Practices = c(cat1, cat2) )
ggplot(dat, aes(x=Yield, fill=Practices)) + 
        geom_histogram(alpha=0.2, position="identity") + 
        ggtitle("Distribution of yearly yields for irrigation recommendations")

# Nitrogen comparative histograms
cat1 <- array(data="Common practices", dim = length(comm_pract_full$leaching))
cat2 <- array(data="Irrigation recommendations", dim = length(comm_pract_full$leaching))
dat <- data.frame(Leaching=c(comm_pract_full$leaching, irr_only_full$leaching), Practices = c(cat1, cat2) )
ggplot(dat, aes(x=Leaching, fill=Practices)) + 
        geom_histogram(alpha=0.2, position="identity") + 
        ggtitle("Distribution of yearly nitrogen leaching for irrigation recommendations")

cat1 <- array(data="Common practices", dim = length(comm_pract_full$leaching))
cat2 <- array(data="Nitrogen recommendations", dim = length(comm_pract_full$leaching))
dat <- data.frame(Leaching=c(comm_pract_full$leaching, nitro_only_full$leaching), Practices = c(cat1, cat2) )
ggplot(dat, aes(x=Leaching, fill=Practices)) + 
        geom_histogram(alpha=0.2, position="identity") + 
        ggtitle("Distribution of yearly nitrogen leaching for irrigation recommendations")

cat1 <- array(data="Common practices", dim = length(comm_pract_full$leaching))
cat2 <- array(data="All recommendations", dim = length(comm_pract_full$leaching))
dat <- data.frame(Leaching=c(comm_pract_full$leaching, all_recs_full$leaching), Practices = c(cat1, cat2) )
ggplot(dat, aes(x=Leaching, fill=Practices)) + 
        geom_histogram(alpha=0.2, position="identity") + 
        ggtitle("Distribution of yearly nitrogen leaching for irrigation recommendations")




## Cumulative plotting 

comm_pract_tyield <- comm_pract_full %>% group_by(run) %>% summarize(total_yield = sum(yield)) %>% pull(total_yield)
irr_only_tyield <- irr_only_full %>% group_by(run) %>% summarize(total_yield = sum(yield)) %>% pull(total_yield)
nitro_only_tyield <- nitro_only_full %>% group_by(run) %>% summarize(total_yield = sum(yield)) %>% pull(total_yield)
all_recs_tyield <- all_recs_full %>% group_by(run) %>% summarize(total_yield = sum(yield)) %>% pull(total_yield)

# individual plots
hist(comm_pract_tyield, 10, main="Total 30-year yields for common practices")
hist(nitro_only_tyield, 10, main="Total 30-year yields for nitrogen recommendations")
hist(all_recs_tyield, 10, main="Total 30-year yields for all recommendations")
hist(irr_only_tyield, 10, main="Total 30-year yields irrigation recommendations")


# comm vs irr
max_l <- max(max(comm_pract_tyield), max(irr_only_tyield))*1.05
min_l <- min(min(comm_pract_tyield), min(irr_only_tyield))*0.95
hist(comm_pract_tyield, 10, col=rgb(0,0,1,1/4), xlim=c(min_l, max_l), main="Total 30-year yields for irrigation only recommendations")  # first histogram
hist(irr_only_tyield, 10, col=rgb(1,0,0,1/4), xlim=c(min_l, max_l), add=T, main="Total 30-year yields for irrigation only recommendations")  # second
#legend(x = "topleft", legend = c("Common Practices", "Irrigation recommendations"), fill= c(rgb(0,0,1,1/4), rgb(1,0,0,1/4)))

# comm vs nitro
max_l <- max(max(comm_pract_tyield), max(nitro_only_tyield))*1.05
min_l <- min(min(comm_pract_tyield), min(nitro_only_tyield))*0.95
hist( comm_pract_tyield, 10, col=rgb(0,0,1,1/4), xlim=c(min_l, max_l), main="Total 30-year yields for nitrogen only recommendations")  # first histogram
hist( nitro_only_tyield, 10, col=rgb(1,0,0,1/4), xlim=c(min_l, max_l), add=T, main="Total 30-year yields for nitrogen only recommendations")  # second
#legend(x = "topleft", legend = c("Common Practices", "Nitrogen recommendations"), fill= c(rgb(0,0,1,1/4), rgb(1,0,0,1/4)))

# comm vs all recs  
max_l <- max(max(comm_pract_tyield), max(all_recs_tyield))*1.05
min_l <- min(min(comm_pract_tyield), min(all_recs_tyield))*0.95
hist( comm_pract_tyield, 10, col=rgb(0,0,1,1/4), xlim=c(min_l, max_l), main="Total 30-year yields for all recommendations")  # first histogram
hist( all_recs_tyield, 10, col=rgb(1,0,0,1/4),   xlim=c(min_l, max_l), add=T, main="Total 30-year yields for all recommendations")  # second
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

print("year-by-year change in leaching")

print("t.test")
p_irr_t   <- t.test(comm_pract_full$leaching, irr_only_full$leaching  )
p_nitro_t <- t.test(comm_pract_full$leaching, nitro_only_full$leaching)
p_all_t   <- t.test(comm_pract_full$leaching, all_recs_full$leaching  )
print(p_irr_t$p.value    )
print(p_nitro_t$p.value  )
print(p_all_t$p.value    )

print("Wilcoxon")
p_irr_w   <- wilcox.test(comm_pract_full$leaching, irr_only_full$leaching)
p_nitro_w <- wilcox.test(comm_pract_full$leaching, nitro_only_full$leaching)
p_all_w   <- wilcox.test(comm_pract_full$leaching, all_recs_full$leaching)
print(p_irr_w$p.value    )
print(p_nitro_w$p.value  )
print(p_all_w$p.value    )

print("year-by-year change in water efficiency")

print("t.test")
p_irr_t   <- t.test(comm_pract_full$wat_eff, irr_only_full$wat_eff  )
p_nitro_t <- t.test(comm_pract_full$wat_eff, nitro_only_full$wat_eff)
p_all_t   <- t.test(comm_pract_full$wat_eff, all_recs_full$wat_eff  )
print(p_irr_t$p.value    )
print(p_nitro_t$p.value  )
print(p_all_t$p.value    )

print("Wilcoxon")
p_irr_w   <- wilcox.test(comm_pract_full$wat_eff, irr_only_full$wat_eff)
p_nitro_w <- wilcox.test(comm_pract_full$wat_eff, nitro_only_full$wat_eff)
p_all_w   <- wilcox.test(comm_pract_full$wat_eff, all_recs_full$wat_eff)
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






