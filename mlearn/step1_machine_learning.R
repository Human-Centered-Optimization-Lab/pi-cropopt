#install.packages("arrow")

library(feather);

stage2num <- function(stage){ 
  grep(toString(stage), stages) 
}


path = "Z:\\Gilgamesh\\kroppian\\agovization_results\\mlearning\\2021-09-10_13-31_attr_tab.feather"

stages <- c("P","V6",  "V7", "V8", "V9", "V10",  "V11", "V12", "V13", "V14", "R1", "R2", "R3", "R4")

#raw_attribute_tab <- arrow::read_feather(path)
#attribute_tab <- subset(raw_attribute_tab, select=-growth_period_of_second_N_app)
#attribute_tab['growth_period_of_second_N_app'] <- apply(raw_attribute_tab['growth_period_of_second_N_app'], MARGIN=1, stage2num)



attribute_tab <- arrow::read_feather(path)
attribute_tab['growth_period_of_second_N_app'] <- apply(attribute_tab['growth_period_of_second_N_app'], MARGIN=1, stage2num)



