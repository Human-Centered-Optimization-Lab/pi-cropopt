rm(list = ls())

library(arrow)
library(dplyr)
library(mvpart)
library(ggplot2)
library(ggplotify)

filename <- "attrib_tab.feather"
data_raw <- arrow::read_feather(filename)

# Select only Pareto-optimal solutions:
data <- data_raw %>% filter(front == 1)

# Set of relevant explanatory variables

resp <- c('norm_yield','norm_leach')
vars <- c('growth_period_of_second_N_app',
          'climate',
          'total_wat_during_v6',
          'total_wat_during_v7',
          'total_wat_during_v8',
          'total_wat_during_v9',
          'total_wat_during_v10',
          'total_wat_during_v11',
          'total_wat_during_v12',
          'total_wat_during_v13',
          'total_wat_during_v14',
          'total_wat_during_R1',
          'total_wat_during_R2',
          'total_wat_during_R3',
          'total_wat_during_R4'
          )

renames <- c('GP_2nd_Napp',
             'Climate',
             'W_total_v6',
             'W_total_v7',
             'W_total_v8',
             'W_total_v9',
             'W_total_v10',
             'W_total_v11',
             'W_total_v12',
             'W_total_v13',
             'W_total_v14',
             'W_total_R1',
             'W_total_R2',
             'W_total_R3',
             'W_total_R4'
)

# Normalize targets by year
max_yields <- data %>%
              group_by(year) %>%
              summarize(year_max_yield = max(yield_))

norm_yield <- data %>%
              inner_join(max_yields) %>%
              select(yield_, year_max_yield) %>%
              mutate(norm_yield = yield_ / year_max_yield) %>%
              pull(norm_yield)

data$norm_yield <- norm_yield
# data$norm_yield <- data$yield_/max(data$yield_)
data$norm_leach <- data$leaching/max(data$leaching)

# Matrix of target variables
Y <- data.matrix(data[c('norm_yield','norm_leach')])

# Data frame with explanatory variables
X <- data[vars]
names(X) <- renames

# Fit multivariate decision tree

fit <-mvpart(
  Y ~ .,
  X,
  # size = 4,
  margin = 0.08,
  xv = "min",
  xval = 10,
  xvmult = 100,
  maxsurrogate = 20,
  legend = FALSE,
  plot.add = FALSE
  )

R2 <- 1 - tail(printcp(fit)[, 'rel error'],1)
p <- as.ggplot(function() {par(xpd= TRUE); mvpart:::plot.rpart(fit, margin = 0 ,compress = TRUE);
  mvpart:::text.rpart(fit, use.n = TRUE, legend = TRUE, digits = 3)}) +
  labs(caption = sprintf('Pareto-Optimal'),
       subtitle = bquote(~R^2 == .(round(R2,2)))) +
  theme(plot.subtitle = element_text(hjust = 0.1),
        plot.caption  = element_text(hjust = 1))
