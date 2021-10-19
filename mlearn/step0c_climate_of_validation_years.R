library(dplyr)

## Constants
WTH_FILE_PATH <- "../dhome/Weather/CASSREPR.WTH"
MGT_FILE_PATH <- "../management_dates.csv"

COLUMN_NAMES <- c("date", "srad", "tmax", "tmin", "rain")

START_TRAIN <- 1980
END_TRAIN <- 2009

## Read data

weather_tab <- read.fwf(WTH_FILE_PATH, widths=c(5, 6, 6, 6, 6), skip=5, col.names=COLUMN_NAMES)
gdd_tab <- read.csv(MGT_FILE_PATH) %>% rename(year = Year)

## Preprocessing
# Add dummy variables for the years without GDD data (for now)
gdd_2018 <- c(2018,  min(gdd_tab$P),  -99, -99, -99, -99, -99, -99, -99, -99, -99, -99, -99, -99, -99, -99,  max(gdd_tab$R6))
gdd_2019 <- c(2019,  min(gdd_tab$P),  -99, -99, -99, -99, -99, -99, -99, -99, -99, -99, -99, -99, -99, -99,  max(gdd_tab$R6))
gdd_2020 <- c(2020,  min(gdd_tab$P),  -99, -99, -99, -99, -99, -99, -99, -99, -99, -99, -99, -99, -99, -99,  max(gdd_tab$R6))
gdd_2021 <- c(2021,  min(gdd_tab$P),  -99, -99, -99, -99, -99, -99, -99, -99, -99, -99, -99, -99, -99, -99,  max(gdd_tab$R6))
gdd_tab <- rbind(gdd_tab, gdd_2018)
gdd_tab <- rbind(gdd_tab, gdd_2019)
gdd_tab <- rbind(gdd_tab, gdd_2020)
gdd_tab <- rbind(gdd_tab, gdd_2021)


# Clean up the date data
weather_tab <- weather_tab %>% 
               mutate(year_mini = round(date / 1e3)) %>%
               mutate(year = ifelse(year_mini >= 80 & year_mini <= 99, year_mini + 1900, year_mini + 2000)) %>%
               mutate(doy = date %% 1e3) 

## Main processing
# Bring in the gdd data
weather_tab <- weather_tab %>% 
               inner_join(gdd_tab)

# Sum up the rain for each year during the growing season
rain_summary <- weather_tab %>% 
                filter(doy > P & doy < R6) %>%        # Just during the growing season
                group_by(year) %>%  
                summarize(total_rain = sum(rain)) %>%
                select(year, total_rain)

# Calculate the threshold
year_count <- END_TRAIN - START_TRAIN + 1

threshold_ind <- floor(year_count/3)

rain_ts <- rain_summary %>% 
            filter(year >= START_TRAIN & year <= END_TRAIN) %>%
            arrange(total_rain) %>%
            pull(total_rain)

threshold_normal <- mean(c(rain_ts[threshold_ind], rain_ts[threshold_ind+1]))  
threshold_wet <- mean(c(rain_ts[threshold_ind*2], rain_ts[threshold_ind*2+1]))

rain_summary <- rain_summary %>%
                mutate(climate = ifelse(total_rain < threshold_normal, 0, ifelse(total_rain < threshold_wet, 1, 2)))


dry_count     <- rain_summary %>% 
                  filter(year <= END_TRAIN) %>% 
                  mutate( dry_years = climate == 0) %>% 
                  summarize(b = sum(dry_years)) %>% 
                  pull(b)

normal_count  <- rain_summary %>% 
                  filter(year <= END_TRAIN) %>% 
                  mutate(norm_years = climate == 1) %>% 
                  summarize(b = sum(norm_years)) %>% 
                  pull(b)

wet_count     <- rain_summary %>% 
                  filter(year <= END_TRAIN) %>% 
                  mutate( wet_years = climate == 2) %>% 
                  summarize(b = sum(wet_years)) %>% 
                  pull(b)






