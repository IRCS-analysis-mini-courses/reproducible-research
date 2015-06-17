library(RColorBrewer)

data.dir <- '~/GitHub/reproducible-research/Day-3/notebooks'
file.dir <- 'multivariate-data-sweave/modified-538-theme.R'

source(file.path(data.dir, file.dir))

cbbPalette <-
  c("#000000", "#E69F00", "#56B4E9", 
    "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7")

overall.rt.dist <- 
  ggplot(multivariate.exp.data, aes(x = RT)) +
  geom_density(fill = 'black') + 
  labs(title = 'Overall RT distribution',
       x = 'Reaction time (ms)', y = 'Density') + 
  fte_theme()

group.rt.dist <- 
  ggplot(multivariate.exp.data, aes(x = RT)) +
  geom_density(aes(fill = Group, colour = Group), alpha = 0.4) + 
  labs(title = 'RT distribution by Group',
       x = 'Reaction time (ms)', y = 'Density') +
  fte_theme() +
  scale_colour_manual(values = cbbPalette) + 
  scale_fill_manual(values = cbbPalette)
