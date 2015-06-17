#!/usr/bin/env Rscript

# R script for using dplyr to manipulate data

# import dataset ----------------------------------------------------------

target.dir <- '~/GitHub/reproducible-research/extras'
target.file <- 'common-dataset.csv'

library(dplyr)
library(readr)

common.dataset <- read_csv(file.path(target.dir, target.file), col_names = TRUE)

# subsetting observations -------------------------------------------------

a0a.greater.700 <- dplyr::filter(common.dataset, A0A > 700)

common.sample <- sample_n(common.dataset, 100, replace = FALSE)

common.sample.fac <- sample_frac(common.dataset, 0.8, replace = FALSE)


# subsetting columns ------------------------------------------------------

contains.w.miniscule <- select(common.dataset, contains('w'))
contains.w.majuscule <- select(common.dataset, contains('W'))

endswith.rt <- select(common.dataset, ends_with('RT'))
endswith.z <- select(common.dataset, ends_with('z'))

startswith.a <- select(common.dataset, starts_with('A'))
startsth.k <- select(common.dataset, starts_with('K'))

# get column names using regex
select(common.dataset, matches('.w.d.w'))



# grouping data -----------------------------------------------------------

common.dataset %>% group_by(Cat) %>% summarize(meanA0A = mean(A0A))

common.dataset %>% group_by(Cat) %>% 
  summarize(meanA0A = mean(A0A), medianF5F = median(F5F), variL = var(iL))


common.dataset %>% group_by(Cat, Part) %>% summarize(meanA0A = mean(A0A))

common.dataset %>% group_by(Cat, Part) %>% 
  summarize(meanA0A = mean(A0A), medianF5F = median(F5F), variL = var(iL))

# database-style joins ----------------------------------------------------

df1 <- 
  data_frame(x1 = c('alpha', 'beta', 'gamma', 'delta'), 
             x2 = c(1, 2, 3, 4))

df2 <- 
  data_frame(x3 = c(FALSE, FALSE, TRUE, FALSE),
             x1 = c('alpha', 'beta', 'omicron', 'gamma'))

left_join(df1, df2, by = 'x1')

right_join(df1, df2, by = 'x1')

inner_join(df1, df2, by = 'x1')

full_join(df1, df2, by = 'x1')

merge(df1, df2) # this is a base R function
