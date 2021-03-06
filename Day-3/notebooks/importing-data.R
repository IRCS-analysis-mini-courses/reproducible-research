#!/usr/bin/env Rscript

sink(file = '~/GitHub/reproducible-research/Day-3/datasets/import-data-output.txt')

library(readr)

# importing 2010 US Census data with base R -------------------------------

census.url <- 'http://www.census.gov/2010census/csv/pop_density.csv'

file.dir <- '~/GitHub/reproducible-research/Day-3/datasets'

census.file <- 'census-data-from-r.csv'

census.data  <- 
  download.file(url = census.url, destfile = file.path(file.dir, census.file))

census.data.base <- 
  read.csv(file.path(file.dir, census.file), 
           stringsAsFactors = FALSE, header = TRUE)

head(census.data.base)

# importing 2010 US Census data with readr --------------------------------

census.data.readr <- read_csv(census.url, col_names = TRUE)

head(census.data.readr)


# import 2010 US Census data with base R; skip 1st 3 lines ----------------

census.data.base <- 
  read.csv(file.path(file.dir, census.file), stringsAsFactors = FALSE, 
           header = TRUE, skip = 3)


# import 2010 US Census data with reader; skip 1st 3 lines ----------------

census.data.readr <- read_csv(census.url, col_names = TRUE, skip = 3)


# import program effort data using base R ---------------------------------

# notice that R parses the DAT file irregular spacing properly
# on the first try but we need to supply correct column names

program.effort.url <- 'http://data.princeton.edu/wws509/datasets/effort.dat'
file.dir <- '~/GitHub/reproducible-research/Day-3/datasets'
program.effort.file <- 'program-effort-from-r.dat'

program.effort.data  <- 
  download.file(url = program.effort.url, 
                destfile = file.path(file.dir, program.effort.file))

program.effort.base <- 
read.table(file.path(file.dir, program.effort.file),
         stringsAsFactors = FALSE, header = TRUE)

head(program.effort.base)

# change column names

program.columns <- c('Country', 'Setting', 'Effort', 'Change')

program.effort.base <- 
  read.table(file.path(file.dir, program.effort.file),
             stringsAsFactors = FALSE, header = TRUE, 
             col.names = program.columns, row.names = NULL)

head(program.effort.base)


# import program effort data using readr ----------------------------------

# notice that readr does not properly read the variable spacing

program.effort.readr  <- read_table(program.effort.url)

head(program.effort.readr)

# import data again with variable whitespace

program.effort.readr  <- 
  read_delim(program.effort.url, delim = '/s+', skip = 1, col_names = FALSE)

# remove empty bottom rows
program.effort.readr <- dplyr::slice(program.effort.readr, 1:20)

# separate single column into multiple
program.effort.readr.separate <- 
  tidyr::separate(program.effort.readr, col = X1, into = program.columns,
                  extra = 'merge')

program.effort.readr.separate <- 
  tidyr::separate(program.effort.readr.separate, col = Change, 
                  into = c('Effort', 'Change'), extra = 'merge')

# drop and rename columns
program.effort.readr.separate$Country <- NULL
colnames(program.effort.readr.separate) <- program.columns

head(program.effort.readr)


# importing FEC dataset (unzipped already) using readr --------------------

# using version of dataset with different attributes appended to each row
# total file is ~2GB

fec.file <- '~/Documents/ircs-mini-course-data/fec-data-complete-formatted.csv'

fec.data <- read_csv(fec.file, col_names = TRUE)

dplyr::glimpse(fec.data)

pryr::object_size(fec.data)

sink()
