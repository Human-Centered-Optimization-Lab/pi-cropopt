library(ggplot2)
library(magrittr)
library(dplyr)

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
dat$Practices = factor(dat$Practices, levels = c("Irrigation recommendations", "Common practices"))
ggplot(dat, aes(x=Yield, fill=Practices)) + 
        geom_histogram(alpha=0.2, position="identity") + 
        ggtitle("Distribution of yearly yields for irrigation recommendations strategy")

cat1 <- array(data="Common practices", dim = length(comm_pract_full$yield))
cat2 <- array(data="Nitrogen recommendations", dim = length(comm_pract_full$yield))
dat <- data.frame(Yield=c(comm_pract_full$yield, nitro_only_full$yield), Practices = c(cat1, cat2) )
dat$Practices = factor(dat$Practices, levels = c("Nitrogen recommendations", "Common practices"))
ggplot(dat, aes(x=Yield, fill=Practices)) + 
        geom_histogram(alpha=0.2, position="identity") + 
        ggtitle("Distribution of yearly yields for nitrogen recommendations strategy")


cat1 <- array(data="Common practices", dim = length(comm_pract_full$yield))
cat2 <- array(data="All recommendations", dim = length(comm_pract_full$yield))
dat <- data.frame(Yield=c(comm_pract_full$yield, all_recs_full$yield), Practices = c(cat1, cat2) )
dat$Practices = factor(dat$Practices, levels = c("All recommendations", "Common practices"))
ggplot(dat, aes(x=Yield, fill=Practices)) + 
        geom_histogram(alpha=0.2, position="identity") + 
        ggtitle("Distribution of yearly yields for all recommendations strategy")

# Nitrogen comparative histograms
cat1 <- array(data="Common practices", dim = length(comm_pract_full$leaching))
cat2 <- array(data="Irrigation recommendations", dim = length(comm_pract_full$leaching))
dat <- data.frame(Leaching=c(comm_pract_full$leaching, irr_only_full$leaching), Practices = c(cat1, cat2) )
dat$Practices = factor(dat$Practices, levels = c("Irrigation recommendations", "Common practices"))
ggplot(dat, aes(x=Leaching, fill=Practices)) + 
        geom_histogram(alpha=0.2, position="identity") + 
        ggtitle("Distribution of yearly nitrogen leaching for irrigation recommendations strategy")

cat1 <- array(data="Common practices", dim = length(comm_pract_full$leaching))
cat2 <- array(data="Nitrogen recommendations", dim = length(comm_pract_full$leaching))
dat <- data.frame(Leaching=c(comm_pract_full$leaching, nitro_only_full$leaching), Practices = c(cat1, cat2) )
dat$Practices = factor(dat$Practices, levels = c("Nitrogen recommendations", "Common practices"))
ggplot(dat, aes(x=Leaching, fill=Practices)) + 
        geom_histogram(alpha=0.2, position="identity") + 
        ggtitle("Distribution of yearly nitrogen leaching for nitrogen recommendations strategy")

cat1 <- array(data="Common practices", dim = length(comm_pract_full$leaching))
cat2 <- array(data="All recommendations", dim = length(comm_pract_full$leaching))
dat <- data.frame(Leaching=c(comm_pract_full$leaching, all_recs_full$leaching), Practices = c(cat1, cat2) )
dat$Practices = factor(dat$Practices, levels = c("All recommendations", "Common practices"))
ggplot(dat, aes(x=Leaching, fill=Practices)) + 
        geom_histogram(alpha=0.2, position="identity") + 
        ggtitle("Distribution of yearly nitrogen leaching for all recommendations strategy")

# Water efficiency comparative histograms
cat1 <- array(data="Common practices", dim = length(comm_pract_full$wat_eff))
cat2 <- array(data="Irrigation recommendations", dim = length(comm_pract_full$wat_eff))
dat <- data.frame(Wat_Eff=c(comm_pract_full$wat_eff, irr_only_full$wat_eff), Practices = c(cat1, cat2) )
ggplot(dat, aes(x=Wat_Eff, fill=Practices)) + 
        geom_histogram(alpha=0.2, position="identity") + 
        xlab("Water use efficiency") +
        ggtitle("Distribution of yearly water efficiency for irrigation recommendations")

cat1 <- array(data="Common practices", dim = length(comm_pract_full$wat_eff))
cat2 <- array(data="Nitrogen recommendations", dim = length(comm_pract_full$wat_eff))
dat <- data.frame(Wat_Eff=c(comm_pract_full$wat_eff, nitro_only_full$wat_eff), Practices = c(cat1, cat2) )
ggplot(dat, aes(x=Wat_Eff, fill=Practices)) + 
        geom_histogram(alpha=0.2, position="identity") + 
        xlab("Water use efficiency") +
        ggtitle("Distribution of yearly water efficiency for irrigation recommendations")

cat1 <- array(data="Common practices", dim = length(comm_pract_full$wat_eff))
cat2 <- array(data="All recommendations", dim = length(comm_pract_full$wat_eff))
dat <- data.frame(Wat_Eff=c(comm_pract_full$wat_eff, all_recs_full$wat_eff), Practices = c(cat1, cat2))
ggplot(dat, aes(x=Wat_Eff, fill=Practices)) + 
        geom_histogram(alpha=0.2, position="identity") + 
        xlab("Water use efficiency") +
        ggtitle("Distribution of yearly water efficiency for irrigation recommendations")







## Cumulative plotting 

comm_pract_tyield <- comm_pract_full %>% group_by(station) %>% summarize(total_yield = sum(yield)) %>% pull(total_yield)
irr_only_tyield <- irr_only_full %>% group_by(station) %>% summarize(total_yield = sum(yield)) %>% pull(total_yield)
nitro_only_tyield <- nitro_only_full %>% group_by(station) %>% summarize(total_yield = sum(yield)) %>% pull(total_yield)
all_recs_tyield <- all_recs_full %>% group_by(station) %>% summarize(total_yield = sum(yield)) %>% pull(total_yield)

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

