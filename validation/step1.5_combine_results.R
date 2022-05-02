library(dplyr)

ROOT_PATH <- "Z:/Gilgamesh/kroppian/agovization_results/validation/"
ROOT_PATH <- "/Volumes/data/Gilgamesh/kroppian/agovization_results/validation/"

COMM_TABS_OUTPUT    <- paste(ROOT_PATH, "comm_pract_full.feather", sep="")
NITRO_TABS_OUTPUT   <- paste(ROOT_PATH, "nitro_full.feather", sep="")
ALL_RECS_TABS_OUTPUT<- paste(ROOT_PATH, "all_recs_full.feather", sep="")
IRR_TABS_OUTPUT     <- paste(ROOT_PATH, "irr_full.feather", sep="")

comm_tabs <- bind_rows(list(
    arrow::read_feather(paste(ROOT_PATH, "comm_pract_run000.feather", sep="")), 
    arrow::read_feather(paste(ROOT_PATH, "comm_pract_run001.feather", sep="")),
    arrow::read_feather(paste(ROOT_PATH, "comm_pract_run002.feather", sep="")),
    arrow::read_feather(paste(ROOT_PATH, "comm_pract_run003.feather", sep="")),
    arrow::read_feather(paste(ROOT_PATH, "comm_pract_run004.feather", sep="")),
    arrow::read_feather(paste(ROOT_PATH, "comm_pract_run005.feather", sep="")),
    arrow::read_feather(paste(ROOT_PATH, "comm_pract_run006.feather", sep="")),
    arrow::read_feather(paste(ROOT_PATH, "comm_pract_run007.feather", sep="")),
    arrow::read_feather(paste(ROOT_PATH, "comm_pract_run008.feather", sep="")),
    arrow::read_feather(paste(ROOT_PATH, "comm_pract_run009.feather", sep="")),
    arrow::read_feather(paste(ROOT_PATH, "comm_pract_run010.feather", sep="")),
    arrow::read_feather(paste(ROOT_PATH, "comm_pract_run011.feather", sep="")),
    arrow::read_feather(paste(ROOT_PATH, "comm_pract_run012.feather", sep="")),
    arrow::read_feather(paste(ROOT_PATH, "comm_pract_run013.feather", sep="")),
    arrow::read_feather(paste(ROOT_PATH, "comm_pract_run014.feather", sep=""))
), .id="run")


nitro_tabs <- bind_rows(list(
    arrow::read_feather(paste(ROOT_PATH, "nitro_only_result_run000.feather", sep="")), 
    arrow::read_feather(paste(ROOT_PATH, "nitro_only_result_run001.feather", sep="")),
    arrow::read_feather(paste(ROOT_PATH, "nitro_only_result_run002.feather", sep="")),
    arrow::read_feather(paste(ROOT_PATH, "nitro_only_result_run003.feather", sep="")),
    arrow::read_feather(paste(ROOT_PATH, "nitro_only_result_run004.feather", sep="")),
    arrow::read_feather(paste(ROOT_PATH, "nitro_only_result_run005.feather", sep="")),
    arrow::read_feather(paste(ROOT_PATH, "nitro_only_result_run006.feather", sep="")),
    arrow::read_feather(paste(ROOT_PATH, "nitro_only_result_run007.feather", sep="")),
    arrow::read_feather(paste(ROOT_PATH, "nitro_only_result_run008.feather", sep="")),
    arrow::read_feather(paste(ROOT_PATH, "nitro_only_result_run009.feather", sep="")),
    arrow::read_feather(paste(ROOT_PATH, "nitro_only_result_run010.feather", sep="")),
    arrow::read_feather(paste(ROOT_PATH, "nitro_only_result_run011.feather", sep="")),
    arrow::read_feather(paste(ROOT_PATH, "nitro_only_result_run012.feather", sep="")),
    arrow::read_feather(paste(ROOT_PATH, "nitro_only_result_run013.feather", sep="")),
    arrow::read_feather(paste(ROOT_PATH, "nitro_only_result_run014.feather", sep=""))
), .id="run")

irr_tabs <- bind_rows(list(
    arrow::read_feather(paste(ROOT_PATH, "irr_only_result_run000.feather", sep="")), 
    arrow::read_feather(paste(ROOT_PATH, "irr_only_result_run001.feather", sep="")),
    arrow::read_feather(paste(ROOT_PATH, "irr_only_result_run002.feather", sep="")),
    arrow::read_feather(paste(ROOT_PATH, "irr_only_result_run003.feather", sep="")),
    arrow::read_feather(paste(ROOT_PATH, "irr_only_result_run004.feather", sep="")),
    arrow::read_feather(paste(ROOT_PATH, "irr_only_result_run005.feather", sep="")),
    arrow::read_feather(paste(ROOT_PATH, "irr_only_result_run006.feather", sep="")),
    arrow::read_feather(paste(ROOT_PATH, "irr_only_result_run007.feather", sep="")),
    arrow::read_feather(paste(ROOT_PATH, "irr_only_result_run008.feather", sep="")),
    arrow::read_feather(paste(ROOT_PATH, "irr_only_result_run009.feather", sep="")),
    arrow::read_feather(paste(ROOT_PATH, "irr_only_result_run010.feather", sep="")),
    arrow::read_feather(paste(ROOT_PATH, "irr_only_result_run011.feather", sep="")),
    arrow::read_feather(paste(ROOT_PATH, "irr_only_result_run012.feather", sep="")),
    arrow::read_feather(paste(ROOT_PATH, "irr_only_result_run013.feather", sep="")),
    arrow::read_feather(paste(ROOT_PATH, "irr_only_result_run014.feather", sep=""))
), .id="run")


all_recs_tabs <- bind_rows(list(
    arrow::read_feather(paste(ROOT_PATH, "all_recs_full_result_run000.feather", sep="")), 
    arrow::read_feather(paste(ROOT_PATH, "all_recs_full_result_run001.feather", sep="")),
    arrow::read_feather(paste(ROOT_PATH, "all_recs_full_result_run002.feather", sep="")),
    arrow::read_feather(paste(ROOT_PATH, "all_recs_full_result_run003.feather", sep="")),
    arrow::read_feather(paste(ROOT_PATH, "all_recs_full_result_run004.feather", sep="")),
    arrow::read_feather(paste(ROOT_PATH, "all_recs_full_result_run005.feather", sep="")),
    arrow::read_feather(paste(ROOT_PATH, "all_recs_full_result_run006.feather", sep="")),
    arrow::read_feather(paste(ROOT_PATH, "all_recs_full_result_run007.feather", sep="")),
    arrow::read_feather(paste(ROOT_PATH, "all_recs_full_result_run008.feather", sep="")),
    arrow::read_feather(paste(ROOT_PATH, "all_recs_full_result_run009.feather", sep="")),
    arrow::read_feather(paste(ROOT_PATH, "all_recs_full_result_run010.feather", sep="")),
    arrow::read_feather(paste(ROOT_PATH, "all_recs_full_result_run011.feather", sep="")),
    arrow::read_feather(paste(ROOT_PATH, "all_recs_full_result_run012.feather", sep="")),
    arrow::read_feather(paste(ROOT_PATH, "all_recs_full_result_run013.feather", sep="")),
    arrow::read_feather(paste(ROOT_PATH, "all_recs_full_result_run014.feather", sep=""))
), .id="run")



arrow::write_feather(comm_tabs,COMM_TABS_OUTPUT)
arrow::write_feather(nitro_tabs,NITRO_TABS_OUTPUT)
arrow::write_feather(irr_tabs,ALL_RECS_TABS_OUTPUT)
arrow::write_feather(all_recs_tabs,IRR_TABS_OUTPUT)

