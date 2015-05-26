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



# data.frame methods ------------------------------------------------------

# data.frame methods: 
# 1. creation
# 2. indexing
# 3. slicing
# 4. selecting and filtering
# 5. mapping values and functions
# 6. missing data
# 7. summaries and basic stats

