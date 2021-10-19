library(dplyr)

WTH_FILE_PATH <- "../dhome/Weather/CASSREPR.WTH"

column_names <- c("date", "srad", "tmax", "tmin", "rain")

weather_tab <- read.fwf(WTH_FILE_PATH, widths=c(5, 6, 6, 6, 6), skip=5, col.names=column_names)

normalTheshold <- 452.6
wetThreshold <- 571.5


year <- weather_tab %>% 
    mutate(year = round(date / 1e3)) %>% 
    pull(year)


doy <- weather_tab %>% 
    mutate(doy = date %% 1e3) %>% 
    pull(doy)



weather_tab$year <- year

yearly_rain <- weather_tab %>% 
               group_by(year) %>%
               summarize(total_rain = sum(rain))
