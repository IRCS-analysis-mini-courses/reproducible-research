#!/usr/bin/env Rscript

target.dir <- '~/GitHub/reproducible-research/Day-3/notebooks'
target.file <- 'basic-data-frame-unctionality.txt'
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

