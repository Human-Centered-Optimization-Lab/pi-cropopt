
library(arrow)
library(writexl)

INPUT_FILE = 'Z:\\Gilgamesh\\kroppian\\agovization_results\\mlearning\\targets.feather'
OUTPUT_FILE = 'Z:\\Gilgamesh\\kroppian\\agovization_results\\mlearning\\targets_R_preprocessed.xlsx'


df <- arrow::read_feather(INPUT_FILE)
write_xlsx(df, OUTPUT_FILE)

