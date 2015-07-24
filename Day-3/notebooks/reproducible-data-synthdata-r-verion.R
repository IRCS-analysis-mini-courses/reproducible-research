#!/usr/bin/env Rscript

# Data generation
# Set random seed

RNGkind('Mersenne-Twister')
set.seed(2340875)
old.seed <- .Random.seed

# Create `Subject`, `Age`, `Group` vectors
subj.nums <- seq(1, 102, 1)

subj.ids <- character(length(subj.nums))

for (i in 1:length(subj.nums)) {
  subj.ids[i] <- paste('subj-', subj.nums[i], sep = '')
}

subj.rep <- rep(subj.ids, 800)

groups <- list('treatment-1', 'treatment-2', 'control')
age.vec <- runif(min = 18, max = 52, n = length(subj.ids))


# Assign subjects to an age
age.rep <- rep(age.vec, 800)


# Simulating correct responses
correctness <- runif(min = 0, max  = 1, n = length(subj.rep))

correct.vec <- integer()

for (i in 1:length(subj.rep)) {
  correct.vec[i] <- rbinom(n = 1, prob = correctness[i], size = 1)
}


# Generating reaction times
rt.vec <- numeric(length(subj.rep))

for (i in 1:length(subj.rep)) {
  rt.vec[i] <- 
    rlnorm(n = 1, meanlog = 6.0, sdlog = 0.5) + 5 +
    runif(n = 1, min = 10, max = 100) +
    rnorm(n = 1, mean = 70, sd = 15)
}


# Replacing values selectively with real data
data.dir <- '~/GitHub/reproducible-research/Day-2/datasets'
data.file <- 'psycho-data-april-2015.csv'

real.data <- read.csv(file.path(data.dir, data.file), header = TRUE)

real.rt <- real.data$absRT

for (i in 1:length(subj.rep)) {
  if (rt.vec[i] > 600) {
    rt.vec[i] <- sample(real.rt, replace = TRUE, size = 1)
  } else {
    next # R's version of a continue statement
  }
}


# Creating timed out values

for (i in 1:length(subj.rep)) {
  if (rt.vec[i] > 2200) {
    rt.vec[i] = 200
  } else {
    next
  }
}


# Creating attempts vector
attempt.vec <- round(runif(n = length(subj.rep), min = 1, max = 15))


# Create token vector
token.rep <- rep(seq(1, 20, 1), each = 20)
token.vec <- rep(token.rep, 800)



# Create experimental `data.frame`
library(data.table)

sample.data$Subject <- subj.rep

sample.data <- 
  data.table(Subject = subj.rep, Age = age.rep, Attempts = attempt.vec, 
             Correct = correct.vec, RT = rt.vec)


library(dplyr)
sample.data <- arrange(sample.data, Subject)


# Generate tokens
sample.data$Token <- gl(n = 20, k = 40, labels = seq(1, 20, 1))


# Generate trials
sample.data$Trial <- gl(n = 20, k = 1, length = 20 * length(subj.ids))


# Generate phases
sample.data$Phase <- gl(n = 2, k = 400, labels = c(1, 2))

# Generate groups

treat.1 <- rep(c('treatmet-1'), 34 * 800)
treat.2 <- rep(c('treatment-2'), 34 * 800)
control <- rep(c('control'), 34 * 800)

group.vec <- c(treat.1, treat.2, control)

sample.data$Group <- group.vec

# Changing data types

sample.data$Subject <- as.factor(sample.data$Subject)

sample.data$Group <- as.factor(sample.data$Group)

# write to CSV

output.path <- 
  '~/GitHub/reproducible-research/Day-3/notebooks/multivariate-data-creation-in-r'

output.file <- 'multivariate-dataset-in-r.csv'

write.csv(sample.data, file.path(output.path, output.file),
          na = '', row.names = FALSE)
