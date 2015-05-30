#!/usr/bin/env Rscript

library(plyr)
library(dplyr)
library(readr)

target.dir <- '~/GitHub/reproducible-research/Day-3/notebooks'
target.file <- 'basic-data-frame-functionality.txt'
sink(file = file.path(target.dir, target.file))

# basic functionality with base R data.frame ------------------------------

census.url <- 'http://www.census.gov/2010census/csv/pop_density.csv'

file.dir <- '~/GitHub/reproducible-research/Day-3/datasets'

census.file <- 'census-data-from-r.csv'

census.data  <- 
  download.file(url = census.url, destfile = file.path(file.dir, census.file))

census.data.base <- 
  read.csv(file.path(file.dir, census.file), stringsAsFactors = FALSE, 
           header = TRUE, skip = 3)

attributes(census.data.base)
class(census.data.base)

density.data.dimen <- dim(census.data.base)

density.data.cols <- colnames(census.data.base)

density.data.idx <- row.names(census.data.base)

# remember to always put space before comma to include all rows;
# also makes parsing your code much less confusing

pop.1910 <- census.data.base[ ,'X1910_POPULATION']

sprintf('Data dimensions: %d rows, %d columns',  
        density.data.dimen[1], density.data.dimen[2])

cat('First 10 indices of population density data.frame:',
    row.names(census.data.base)[seq(1,10,1)])

cat('Names of data.frame columns:', density.data.cols, fill = 20)


# using which() to get indices
# this is potentially very slow for very large datasets

which.idx <- which(names(census.data.base) %in% density.data.cols)

print(paste('Name:','Index', sep = ' '))

apply(data.frame(density.data.cols, which.idx), 1, 
      function(row) {cat(row, sep = ': ', fill  = 20) })

# basic functionality with the Hadleyverse --------------------------------

census.data.readr <- read_csv(census.url, col_names = TRUE, skip = 3)

# data.frames in the Hadleyverse have added fuctionality;
# many more options are available to the class 'tbl_df'

attributes(census.data.readr)
class(census.data.readr)

density.data.dimen.readr <- dim(census.data.readr)

density.data.cols.readr <- colnames(census.data.readr)

density.data.idx.readr <- row.names(census.data.readr)

# note that class 'tbl_df' can take columns beginning with a
# numeric argument as valid; this will not work when 
# performing statistical tests

pop.1910.readr <- census.data.readr[ ,'1910_POPULATION']
pop.1910.readr

sprintf('Data dimensions: %d rows, %d columns',  
        density.data.dimen.readr[1], density.data.dimen.readr[2])

cat('First 10 indices of population density data.frame:',
    row.names(census.data.readr)[seq(1,10,1)])

cat('Names of tbl_df columns:', density.data.cols.readr, fill = 15)

# get indices using which()

which.idx.readr <- which(names(census.data.readr) %in% density.data.cols.readr)

print(paste('Name:','Index', sep = ' '))

apply(data.frame(density.data.cols.readr, which.idx.readr), 1, 
      function(row) {cat(row, sep = ': ', fill  = 20) })

# data.frame methods ------------------------------------------------------

# data.frame methods: 
# 1. creation
# 2. indexing
# 3. slicing
# 4. selecting and filtering
# 5. mapping values and functions
# 6. missing data
# 7. summaries and basic stats

# inititate Mersenne_Twister algorithm, set seed, save state

RNGkind('Mersenne-Twister')
set.seed(86519883)
old.seed <- .Random.seed


# creating new data frames

# new data.frame in base R

test.mtx <- rnorm(n = 30)
test.mtx <- matrix(test.mtx, nrow = 10)
test.cols <- c('first', 'second', 'third')

test.data.frame <- data.frame(test.mtx)
colnames(test.data.frame) <- test.cols

test.data.frame

# do the same with dplyr

# cannot make directly yet, so you use this
# in process of being changed with next release
# see https://github.com/hadley/dplyr/issues/876

test.dplyr.frame <- 
  as.data.frame(test.mtx, stringsAsFactors = FALSE) %>%
  as_data_frame()

colnames(test.dplyr.frame) <- test.cols

test.dplyr.frame

## creating new data.frame from vectors in base R

int.col <- round(runif(n = 5, min = 0, max = 255))
char.col <- c('sample1', 'sample2', 'sample3', 'sample4', 'sample5')
binom.col <- rbinom(n = 5, size = 1, p = 0.56)

test.data.frame.2 <- data.frame(int.col, char.col, binom.col)

test.data.frame.2


# creating new data_frame via dplyr

test.dplyr.frame.2 <- data_frame(int.col, char.col, binom.col)
test.dplyr.frame.2

## indexing and slicing

test.data.frame$first

test.data.frame.2['char.col']

log.normal.vec <- rlnorm(meanlog = 2.7, sdlog = 0.2, n = 30)
normal.vec <- rlnorm(mean = -1.6, sd = 2.8, n = 30)
unif.vec <- runif(min = 55, max = 2000, n = 30)

test.dplyr.frame.3 <- data_frame(log.normal.vec, normal.vec, unif.vec)
colnames(test.dplyr.frame.3) <- c('one', '2', 'third')

test.dplyr.frame.3

# notice there is no ':' operator in R to access all columns
test.dplyr.frame.3[1:15, ]


## make row names characters and iterate over them
row.names(census.data.base) <- census.data.base$STATE_OR_REGION

for (name in row.names(census.data.base)) {
  cat(name, census.data.base[name, 'X2010_POPULATION'], fill = 30)
}


## removing data
census.data.base <- census.data.base[-c(1), ]
census.data.base

test.dplyr.frame.3$one <- NULL
test.dplyr.frame.3

test.data.frame.2 <- test.data.frame.2[-c(2, 4)]
head(test.data.frame.2)

## converting between long and wide format
library(reshape2)

child.data.file <- 
  '~/GitHub/reproducible-research/Day-2/datasets/published-data-complete.csv'

# put the data into wide format; there are separate measures
# for each Hemisphere and Condition; these go on the right side of
# the formula specification

child.data <- read.csv(child.data.file, header = TRUE)

child.data.wide <- 
  dcast(data = child.data, formula = Subject + Site + Age_Calc + Gender + 
          Handedness + ASD + NVIQ + VIQ + CELF.4 + SRS_parent + CTOPP + 
          Case + cutAge + breakAge ~ Hem + Cond,
        value.var = "M100LatCorr")

head(child.data.wide)


## mapping values

state.names <- 
  c('Connecticut', 'Maine', 'Massachusetts',
    'New Hampshire', 'Rhode Island', 'Vermont',
    'New Jersey', 'New York', 'Pennsylvania',
    'Illinois', 'Indiana', 'Michigan', 'Ohio',
    'Wisconsin', 'Iowa', 'Kansas', 'Minnesota',
    'Nebraska', 'North Dakota', 'South Dakota', 'Missouri',
    'Delaware', 'Florida', 'Georgia', 'Maryland', 
    'North Carolina', 'South Carolina', 'Virginia',
    'West Virginia', 'Alabama', 'Kentucky', 'Mississippi', 
    'Tennessee', 'Arkansas', 'Louisiana', 'Oklahoma', 
    'Texas', 'Arizona', 'Colorado', 'Idaho', 'Montana', 
    'Nevada', 'New Mexico', 'Utah', 'Wyoming', 'Alaska',
    'California', 'Hawaii', 'Oregon', 'Washington')

state.abbrev <- 
  c('CT', 'ME', 'MA','NH', 'RI', 'VT','NJ', 'NY', 'PA',
    'IL', 'IN', 'MI', 'OH','WI', 'IA', 'KS', 'MN',
    'NE', 'ND', 'SD', 'MO','DE', 'FL', 'GA', 'MD', 
    'NC', 'SC', 'VA','WV', 'AL', 'KY', 'MS', 
    'TN', 'AR', 'LA', 'OK', 'TX', 'AZ', 'CO', 'ID', 'MT', 
    'NV', 'NM', 'UT', 'WY', 'AK', 'CA', 'HI', 'OR', 'WA')

census.data.readr$abbrev <- 
  mapvalues(census.data.readr$STATE_OR_REGION, 
            from  = state.name, to = state.abbrev)

colnames(census.data.readr)

census.data.readr$abbrev

## get summaries of data

# column means of populations

pop.cols <- 
  c('X1910_POPULATION', 'X1920_POPULATION', 'X1930_POPULATION', 'X1940_POPULATION', 
    'X1950_POPULATION', 'X1960_POPULATION', 'X1970_POPULATION', 'X1980_POPULATION',
    'X1990_POPULATION', 'X2000_POPULATION', 'X2010_POPULATION')

rowMeans(census.data.base[ ,pop.cols])
rowSums(census.data.base[ ,pop.cols])

colMeans(census.data.base[ ,pop.cols])
colSums(census.data.base[ ,pop.cols])

# append row means to the data.frame
census.data.base$MeanPop <- rowMeans(census.data.base[ ,pop.cols])

# missing data

# to get elementwise missing, use is.na()
# is.null() tells whether or not the vector is null
is.na(census.data.base[, 'MeanPop'])
is.null(census.data.base[, 'MeanPop'])

# notice that dplyr fills in whatever the original value is
# in a mapping if it is missing
is.na(census.data.readr$abbrev)

# dropping missing values is easy with the subset() command;
# make sure to use droplevels() afterward to fully remove
# as R knows the parent data.frame the data came from

# to remove all NA entries, use na.omit()

census.data.base[c(9, 52), ] <- NA

census.data.base.na.removed <- na.omit(census.data.base)

sprintf('Data dimensions with all entries: %d rows, %d columns',  
        density.data.dimen[1], density.data.dimen[2])

sprintf('Data dimensions with NA removed: %d rows, %d columns',  
        dim(census.data.base.na.removed)[1], 
            dim(census.data.base.na.removed)[2])

# note that while readr will not put an X in front of numers
# you still cannot access the column using '$'

census.data.readr[c(1, 3, 49, 23, 36, 48, 12), 'STATE_OR_REGION'] <- NA

# notice that objects of class tbl_df remove NA in-place
census.data.readr.na.removed <- 
  subset(census.data.readr, STATE_OR_REGION != 'NA')


# modification in-lace is not done for objects of class data.frame
census.data.base[c(1, 3, 49, 23, 36, 48, 12), 'STATE_OR_REGION'] <- NA

census.data.base.na.removed.2 <- 
  subset(census.data.base, STATE_OR_REGION != 'NA')

sprintf('Data dimensions prior to dropping: %d rows, %d columns', 
        dim(census.data.base)[1],
        dim(census.data.base)[2])

census.data.base.na.removed.2 <- 
  droplevels(census.data.base.na.removed.2)

sprintf('Data dimensions after to dropping: %d rows, %d columns', 
        dim(census.data.base.na.removed.2)[1],
        dim(census.data.base.na.removed.2)[2])

## summarizing data
summary(census.data.base)
str(census.data.base)

# extra information using dplyr
summary(census.data.readr)
str(census.data.readr)
glimpse(census.data.readr)



sink()

