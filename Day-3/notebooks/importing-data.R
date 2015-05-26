#!/usr/bin/env Rscript


# importing 2010 US Census data with base R -------------------------------

census.url <- 'http://www.census.gov/2010census/csv/pop_density.csv'
file.dir <- '~/GitHub/reproducible-research/Day-3'
census.file <- 'census-data-from-r.csv'

census.data  <- 
  download.file(url = census.url, destfile = file.path(file.dir, census.file))

census.data.base <- 
  read.csv(file.path(file.dir, census.file), 
           stringsAsFactors = FALSE, header = TRUE)

View(census.data.base)

# importing 2010 US Census data with readr --------------------------------

census.data.readr <- read_csv(census.url, col_names = TRUE)

View(census.data.readr)


# import 2010 US Census data with base R; skip 1st 3 lines ----------------

census.data.base <- 
  read.csv(file.path(file.dir, census.file), stringsAsFactors = FALSE, 
           header = TRUE, skip = 3)


# import 2010 US Census data with reader; skip 1st 3 lines ----------------

census.data.readr <- read_csv(census.url, col_names = TRUE, skip = 3)


# import program effort data using base R ---------------------------------

program.effort.url <- 'http://data.princeton.edu/wws509/datasets/effort.dat'
file.dir <- '~/GitHub/reproducible-research/Day-3'
program.effort.file <- 'program-effort-from-r.csv'

program.effort.data  <- 
  download.file(url = program.effor.url, 
                destfile = file.path(file.dir, program.effort.file))

program.effort.base <- 
  read.csv(file.path(file.dir, program.effort.file))
           stringsAsFactors = FALSE, header = TRUE)

View(program.effort.base)