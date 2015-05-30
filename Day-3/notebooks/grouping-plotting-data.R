#!/usr/bin/env Rscript

# describes how to make plots in base R
# introduction to ggplot


# grouping data -----------------------------------------------------------

# will use both plyr and dplyr
# when importing both, load plyr, then dplyr

library(plyr)
library(dplyr)

RNGkind('Mersenne-Twister')
set.seed(86519883)
old.seed <- .Random.seed

col1 = rlnorm(n = 200, meanlog = 4.5, sdlog = 0.08)
col2 = rnorm(n = 200, mean = 2.3, sd = 0.57)
col3 = runif(n = 200, min = 0, max = 2000)
col4 = rgeom(n = 200, prob = 0.34)
col5 = seq(1, 200, 1)

plot.df <- data.frame(col1, col2, col3, col4, col5)

head(plot.df)

# formula notation for a plot;
# uses form y ~ x
# scatter plot by default
plot(col1 ~ col5, data = plot.df)
plot(col1 ~ col5, data = plot.df, type = 'l')


# scatter plot without the default plot shape and size
plot(col3 ~ col2, data = plot.df, pch = 19, 
     xlab = 'Column 2', ylab = 'Column 3',
     main = 'Column 3 vs. Column 2')

# adding subplots and different types
par(mfrow = c(2, 2))

plot(col1 ~ col5, data = plot.df, type = 'l',
     ylab = 'Column 1', xlab = 'Column 5',
     main = 'Column 1 vs. Column 5')

plot(col2 ~ col5, data = plot.df, pch = 19, 
     xlab = 'Column 5', ylab = 'Column 2',
     main = 'Column 2 vs. Column 5')

plot(col3 ~ col5, data = plot.df,
     type = 'l', lty = 6, lwd = 1.3,
     ylab = 'Column 3', xlab = 'Column 5',
     main = 'Column 3 vs. Column 5')

plot(col4 ~ col5, data = plot.df, 
     type = 'l', lty = 4, lwd = 1.3,
     ylab = 'Columns 5', xlab = 'Column 4',
     main = 'Column 4 vs. Column 5')


# histograms and kernel density estimates ---------------------------------

# create categorical variables

random.nums <- runif(n = nrow(plot.df), min = 0, max = 1)

high <- random.nums > 0.85
middling <- random.nums <= 0.85 & random.nums > 0.5
just.ugh <- random.nums <= 0.5

# creates null vector
plot.df$Category <- NA

plot.df[high, 'Category'] <- 'high'
plot.df[middling, 'Category'] <- 'middling'
plot.df[just.ugh, 'Category'] <- 'terrible'

head(plot.df)

summary(plot.df)
str(plot.df)
dplyr::glimpse(plot.df)

# here is a good chance to introduce various additional summaries

min(plot.df$col1)
max(plot.df$col2)
range(plot.df$col4)
fivenum(plot.df$col5)


# basic histograms

hist(plot.df$col1, col = '#000000', main = 'Column 1, 30 bins',
     breaks = 30)

hist(plot.df$col2, col = '#999999', main = 'Column 2, default bin selection')

hist(plot.df$col3, col = '#56B4E9', main = 'Column 3, 15 bins', 
     breaks = 15)

hist(plot.df$col4, col = '#009E73', main = 'Column 4, 10 bins', 
     breaks = 10)


# basic kernel density estimates

plot(density(plot.df$col1))
plot(density(plot.df$col2))
plot(density(plot.df$col3))
plot(density(plot.df$col4))

# binning columns

col3.bins <- seq(1, 2220, 440)
col3.labels = c('one', 'two', 'three', 'four', 'five')

plot.df$col3Cut <- 
  cut(plot.df$col3, breaks = col3.bins, labels = col3.labels, 
      include.lowest = TRUE, right = TRUE)

head(plot.df)


# grouping columns
# two ways to group: use plyr or dplyr

# cross-tabulation is similar to initial Python example (get counts)
# notice that the order of columns and rows is different

plot.df.xtabs <- xtabs( ~ col3Cut + Category, data = plot.df)

par(mfrow = c(1,1))
barplot(plot.df.xtabs, beside = TRUE, main = 'Discretization bar plot',
        legend.text = TRUE, xlab = 'Category',
        args.legend = list(x = 'topleft'))

# grouping with plyr and dplyr

# using plyr
plot.df.plyr <- 
  ddply(plot.df, .(Category), summarize,
        meanCol1 = mean(col1, na.rm = TRUE), 
        meanCol2 = mean(col2, na.rm = TRUE),
        meanCol3 = mean(col3, na.rm = TRUE),
        meanCol4 = mean(col4),
        varCol1 = var(col1, na.rm = TRUE), 
        varCol2 = var(col2, na.rm = TRUE),
        varCol3 = var(col3, na.rm = TRUE),
        varCol4 = var(col4))

plot.df.plyr

# using dplyr
# notice the similarities with pandas
plot.df.dplyr <- 
  group_by(plot.df, Category) %>% 
  summarize(meanCol1 = mean(col1, na.rm = TRUE), 
            meanCol2 = mean(col2, na.rm = TRUE),
            meanCol3 = mean(col3, na.rm = TRUE),
            meanCol4 = mean(col4),
            varCol1 = var(col1, na.rm = TRUE), 
            varCol2 = var(col2, na.rm = TRUE),
            varCol3 = var(col3, na.rm = TRUE),
            varCol4 = var(col4))

plot.df.dplyr


# introduction to ggplot2 -------------------------------------------------

# see also library(help = 'ggplot2') and the RStudio cheatsheet
# for what can be dome with ggplot2

library(ggplot2)

ggplot(plot.df, aes(x = col5, y = col1)) +
  geom_point()

ggplot(plot.df, aes(x = col5, y = col1)) +
  geom_line()

# scatter plot without the default plot shape and size
ggplot(plot.df, aes(x = col5, y = col1)) +
  geom_line()

# note that filled circle (pch = 19) is the default in ggplot
ggplot(plot.df, aes(x = col2, y = col3)) +
  geom_point(shape = 21) +
  xlab('Column 2') + ylab('Column3') + 
  ggtitle('Column 2 vs. Column 3')

# could also do this
ggplot(plot.df, aes(x = col2, y = col3)) +
  geom_point(shape = 21) +
  labs(x = 'Column 2', y = 'Column3', title = 'Column 2 vs. Column 3')

# adding subplots and different types
# to add subplots with ggplot2, need to use the grid package

library(grid)

grid.newpage()
pushViewport(viewport(layout = grid.layout(2,2)))

# can crete objects with ggplot commands
# use these to print to specific part of grid

col1.vs.col5.plot <- 
  ggplot(plot.df, aes(x = col5, y = col1)) +
  geom_line() + 
  labs(title = 'Column 1 vs. Column 5', x = 'Column 5', y = 'Column 1')

col2.vs.col5.plot <- 
  ggplot(plot.df, aes(x = col5, y = col2)) +
  geom_line() + 
  labs(title = 'Column 2 vs. Column 5', x = 'Column 5', y = 'Column 2')

col3.vs.col5.plot <- 
  ggplot(plot.df, aes(x = col5, y = col3)) +
  geom_line(linetype = 6, size = 1.3) + 
  labs(title = 'Column 3 vs. Column 5', x = 'Column 5', y = 'Column 3')

col4.vs.col5.plot <- 
  ggplot(plot.df, aes(x = col5, y = col4)) +
  geom_line(linetype = 'dotdash', size = 1.3) + 
  labs(title = 'Column 4 vs. Column 5', x = 'Column 5', y = 'Column 4')

print(col1.vs.col5.plot, 
      vp = viewport(layout.pos.row = 1, layout.pos.col = 1))

print(col2.vs.col5.plot, 
      vp = viewport(layout.pos.row = 1, layout.pos.col = 2))

print(col3.vs.col5.plot, 
      vp = viewport(layout.pos.row = 2, layout.pos.col = 1))

print(col4.vs.col5.plot, 
      vp = viewport(layout.pos.row = 2, layout.pos.col = 2))

# histograms and kernel density estimates in ggplot2 ----------------------

# histograms

ggplot(plot.df, aes(x = col1)) + 
  geom_histogram(fill = '#000000', binwidth = 1.25) + 
  labs(title = 'Column 1, 30 bins') + 
  theme_bw()

# fill controls inside bins, colour the outside
ggplot(plot.df, aes(x = col2)) + 
  geom_histogram(fill = '#999999', colour = '#000000') + 
  labs(title = 'Column 2, default bin selection') + 
  theme_bw()

ggplot(plot.df, aes(x = col3)) + 
  geom_histogram(fill = '#56B4E9', colour = '#000000',
                 binwidth = 140, alpha = 0.8) + 
  labs(title = 'Column 3, 15 bins') + 
  theme_bw()

ggplot(plot.df, aes(x = col4)) + 
  geom_histogram(fill = '#009E73', colour = '#000000',
                 binwidth = 1.2, alpha = 0.3) + 
  labs(title = 'Column 4, 10 bins')


# kernel density estimates
# not that R/ggplot picks a different rule of thumb to determine bandwidth

ggplot(plot.df, aes(x = col1)) + 
  geom_density(colour = '#000000') + 
  labs(title = 'Column 1') + 
  theme_bw()

# fill controls inside estimate, colour the outside
ggplot(plot.df, aes(x = col2)) + 
  geom_density(fill = '#999999', colour = '#000000') + 
  labs(title = 'Column 2') + 
  theme_bw()

ggplot(plot.df, aes(x = col3)) + 
  geom_density(fill = '#56B4E9', colour = '#56B4E9', alpha = 0.8) + 
  labs(title = 'Column 3') + 
  theme_bw()

# ntice that ggplot2 by defauly ends the KDE at the min and max values
ggplot(plot.df, aes(x = col4)) + 
  geom_density(fill = '#009E73', colour = '#009E73', alpha = 0.3) + 
  labs(title = 'Column 4')


# saving data -------------------------------------------------------------

# reusing data for advanced plotting script

save.path <- '~/GitHub/reproducible-research/Day-3/datasets'
save.image(file.path(save.path, '/basic-grouping-plotting.rda'))
