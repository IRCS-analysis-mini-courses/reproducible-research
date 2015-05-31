#!/usr/bin/env Rscript

# implement statistical modeling examples in R

target.dir <- '~/GitHub/reproducible-research/Day-3/datasets'
target.file <- 'statistical-modeling-r-examples.txt'
sink(file = file.path(target.dir, target.file))


# published dataset -------------------------------------------------------

data.dir <- '~/GitHub/reproducible-research/Day-2/datasets'
data.file <- 'published-data-complete.csv'

# use base R to import
child.study.data <- read.csv(file.path(data.dir, data.file), header = TRUE)

# remove model fit values already included in the file
child.study.data$Fitted <- NULL
child.study.data$Resid <- NULL
child.study.data$ScaledResid <- NULL
child.study.data$Predicted <- NULL

head(child.study.data)

str(child.study.data)
summary(child.study.data)
dplyr::glimpse(child.study.data)

# density estimate for each Case

library(ggplot2)

# color-blind friendly palette
cbPalette <-
  c("#999999", "#E69F00", "#56B4E9", 
    "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7")

ggplot(child.study.data, aes(x = M100LatCorr)) +
  geom_density(aes(colour = Case, fill = Case, linetype = Case),
               size = 1.3, alpha = 0.3) +
  theme_bw() + 
  labs(x = 'Latency (ms)', y = 'Density', 
       title = 'Latency distribution for each Case') +
  scale_x_continuous(breaks = seq(90, 170, 20))+
  scale_y_continuous(breaks = seq(0, 0.1, 0.02))+
  theme(legend.position = 'bottom',
        legend.text = element_text(face = 'bold', size = 16),
        legend.title = element_blank(),
        axis.text.x = element_text(size = 15, face = 'bold'),
        axis.text.y = element_text(size = 15, face = 'bold'),
        axis.ticks = element_blank(),
        axis.title.x = element_text(size = 20, face = 'bold'),
        axis.title.y = element_text(size = 20, face = 'bold'),
        panel.grid.minor.x = element_blank(),
        panel.grid.major.x = element_blank(),
        panel.grid.minor.y = element_blank(),
        panel.grid.major.y = element_blank(),
        plot.title = element_text(size = 20, face = 'bold')) + 
  scale_fill_manual(values = cbPalette) + 
  scale_colour_manual(values = cbPalette) + 
  scale_linetype_manual(values = c('solid', 'dashed', 'dotted'))

# plot latency against age for each case

ggplot(child.study.data, aes(x = Age_Calc, y = M100LatCorr)) +
  geom_point(aes(colour = Case, shape = Case), size = 1.3) +
  geom_smooth(aes(colour = Case, fill = Case), method = 'lm', size = 1.3) + 
  theme_bw() + 
  scale_x_continuous(breaks = seq(5, 17, 2))+
  scale_y_continuous(breaks = seq(90, 215, 20))+
  coord_cartesian(ylim = c(90, 190)) + 
  labs(x = 'Age (years)', y = 'Latency (ms)', 
       title = 'Regression of latency against age') +
  theme(legend.position = 'bottom',
        legend.text = element_text(face = 'bold', size = 16),
        legend.title = element_blank(),
        axis.text.x = element_text(size = 15, face = 'bold'),
        axis.text.y = element_text(size = 15, face = 'bold'),
        axis.ticks = element_blank(),
        axis.title.x = element_text(size = 20, face = 'bold'),
        axis.title.y = element_text(size = 20, face = 'bold'),
        plot.title = element_text(size = 20, face = 'bold')) + 
  scale_fill_manual(values = cbPalette) + 
  scale_colour_manual(values = cbPalette) + 
  scale_linetype_manual(values = c('solid', 'dashed', 'dotted'))

# regression of latency against age

lat.age.model <- lm(M100LatCorr ~ Age_Calc, data = child.study.data)

summary(lat.age.model)

# ANOVA-table style summary
summary.aov(lat.age.model)

# treatment contrast summary
summary.lm(lat.age.model)

# plot model

# default plots
par(mfrow = c(2, 2))
plot(lat.age.model)

# all six diagnostic plots
par(mfrow = c(3, 2))
plot(lat.age.model, which = c(1:6))

# added functionality with ggplot2: append model fit values to the data.frame

# fortify model with data
lat.age.model.fortify <- fortify(lat.age.model)

# fortify parent data frame with model fit parameters
# refit without dropping NA; rows must match with fortifying
# data with model fit parameters

lat.age.model.2 <- 
  lm(M100LatCorr ~ Age_Calc, data = child.study.data, na.action = na.exclude)

lat.age.model.data.fortify <- fortify(lat.age.model.2, child.study.data)

# for class lm(), glm() and anything that inherits from them
# you get yhat, sigma, cook's distance, fitted, residuals
# and standardized residuals

head(lat.age.model.fortify)

summary(lat.age.model.fortify)

str(lat.age.model.fortify)

dplyr::glimpse(lat.age.model.fortify)

# plot distribution of residuals

ggplot(lat.age.model.fortify, aes(.resid)) + geom_density(fill = 'gray')

# additional diagnostics and plots with car package
library(car)

durbinWatsonTest(lat.age.model.fortify$.resid)

outlierTest(lat.age.model)

sigmaHat(lat.age.model)

par(mfrow = c(1, 1))

influencePlot(lat.age.model)

infIndexPlot(lat.age.model)

qqPlot(lat.age.model)

residualPlots(lat.age.model)


# linear mixed effects models ---------------------------------------------

library(lme4)
library(multcomp)


# internal numeric representation of the categorical predictors

unique(as.numeric(child.study.data$Hem))
unique(as.numeric(child.study.data$Cond))
unique(as.numeric(child.study.data$Case))
unique(as.numeric(child.study.data$Site))

levels(child.study.data$Hem)
levels(child.study.data$Cond)
levels(child.study.data$Case)
levels(child.study.data$Site)

# since missing values are removed be default, no need to drop
# but we can include them if we want to impute missing values
# or fortify the data.frame with model fit values

m100.lmm <- 
  lmer(M100LatCorr ~ Hem + Cond + Case + Site + Age_Calc + 
         (Hem + Cond | Subject), data = child.study.data,
       REML = FALSE)

# include rows with missing values in the dependent variable
m100.lmm.2 <- 
  lmer(M100LatCorr ~ Hem + Cond + Case + Site + Age_Calc + 
         (Hem + Cond | Subject), data = child.study.data,
       na.action = na.exclude, REML = FALSE)

# note: can only use summary() directly if NA values have been dropped

summary(m100.lmm)

Anova(m100.lmm)

summary(glht(m100.lmm, linfct = mcp(Hem = 'Tukey', covariate_average = TRUE)))

summary(glht(m100.lmm, linfct = mcp(Case = 'Tukey', covariate_average = TRUE)))

summary(glht(m100.lmm, linfct = mcp(Cond = 'Tukey', covariate_average = TRUE)))

# plot with languageR

library(languageR)

par(mfrow = c(1, 1))

plotLMER.fnc(m100.lmm, withList = TRUE)

# fortify with model fit parameters
# using model with NA rows included since rows must match

m100.lmm.2.fortify <- fortify(m100.lmm.2, child.study.data)

head(m100.lmm.2.fortify)

# predict new values and allowing for levels/rows not present in fit

m100.lmm.2.fortify$Predicted <- 
  predict(m100.lmm.2, newdata = m100.lmm.2.fortify, 
          na.action = na.pass, allow.new.levels = TRUE)

head(m100.lmm.2.fortify)


# refit latency-age relationship and plot the resulting model

library(dplyr)

m100.lmm.2.fortify.summarize <- 
  m100.lmm.2.fortify %>% 
  group_by(Subject, Case, Age_Calc) %>% 
  summarize(meanFitted = mean(.fitted), meanPredicted = mean(Predicted))

ggplot(m100.lmm.2.fortify.summarize,
       aes(y = meanPredicted, x = Age_Calc, shape = Case))+
  geom_point(size = 3, aes(colour = Case)) + theme_bw() +
  labs(y = 'Latency (ms)', x = 'Age (years)',
       title = 'Mean predicted M100 vs. age',
       shape = 'Case', linetype = 'Case')+
  geom_smooth(aes(linetype = Case, colour = Case, fill = Case),
              size = 1.3, method = 'lm', se = TRUE)+
  scale_x_continuous(breaks = seq(5, 17, 2))+
  scale_y_continuous(breaks = seq(90, 215, 20))+
  coord_cartesian(ylim = c(90, 190))+
  theme(legend.position = 'bottom',
        legend.text = element_text(face = 'bold', size = 16),
        legend.title = element_blank(),
        axis.text.x = element_text(size = 15, face = 'bold'),
        axis.text.y = element_text(size = 15, face = 'bold'),
        axis.ticks = element_blank(),
        axis.title.x = element_text(size = 20, face = 'bold'),
        axis.title.y = element_text(size = 20, face = 'bold'),
        plot.title = element_text(size = 20, face = 'bold')) + 
  scale_fill_manual(values = cbPalette) + 
  scale_colour_manual(values = cbPalette) +
  scale_linetype_manual(values = c('solid', 'dashed', 'dotted'))

# overall model between latency and age
m100.age.dist.case.aov <- 
  aov(meanPredicted ~ Age_Calc * Case, data = m100.lmm.2.fortify.summarize)

summary.lm(m100.age.dist.case.aov)

summary.aov(m100.age.dist.case.aov)


# slope for each case level
by(m100.lmm.2.fortify.summarize,
   m100.lmm.2.fortify.summarize[, 'Case'],
   function(x) summary(lm(meanPredicted ~ Age_Calc, data = x)))

par(mfrow = c(3, 2))

plot(m100.age.dist.case.aov, which = c(1:6))


# analysis of deviance ----------------------------------------------------

m100.complete <- glm(M100compCase ~ Case, binomial, data = child.study.data)

summary(m100.complete)

# summary and observed proportions

m100.complete.summary <- 
  child.study.data %>% 
  group_by(Case) %>% 
  summarize(counts = sum(M100compCase), 
            total = sum(complete.cases(M100compCase)), pct = counts / total)

m100.complete.summary


# psychophysical discrimination -------------------------------------------


source.dir <- '~/GitHub/reproducible-research/Day-2/datasets'
exact.path = 'psycho-data-april-2015.csv'

vowel.data <- read.csv(file.path(source.dir, exact.path), header = TRUE)

head(vowel.data)

# see help(family) for more options
vowel.glm <- glm(RespNum ~ Vowel, binomial, data = vowel.data)
vowel.probit.glm <- glm(RespNum ~ Vowel, binomial(probit), data = vowel.data)
vowel.cauchit.glm <- glm(RespNum ~ Vowel, binomial(cauchit), data = vowel.data)

summary(vowel.glm)

summary(vowel.probit.glm)

summary(vowel.cauchit.glm)

# plot GLM; notice what is different between GLM and least-squares
par(mfrow = c(3, 2))

plot(vowel.glm, which = c(1:6))

# significance
Anova(vowel.glm)

summary(glht(vowel.glm, linfct = mcp(Vowel = 'Tukey')))

# repeat with GLMM
vowel.glmm <- 
  glmer(RespNum ~ Vowel + (Vowel  | SubjectAssgn), binomial, data = vowel.data)

# notice that what works in the GLM case may not work in the GLMM case;
# random effects terms may have to be adjusted (hint: try (1 | SubjectAssgn))

vowel.probit.glmm <- 
  glmer(RespNum ~ Vowel + (Vowel  | SubjectAssgn), 
        binomial(probit), data = vowel.data)

vowel.cauchit.glmm <- 
  glmer(RespNum ~ Vowel + (Vowel  | SubjectAssgn), 
        binomial(cauchit), data = vowel.data)

summary(vowel.glmm)

# reaction time analysis

# remove timed-out responses
vowel.data.late.removed <- subset(vowel.data, absRT < 2000)
vowel.data.late.removed <- droplevels(vowel.data.late.removed)

# implement least-squares model for log RT
# three ways to do this
vowel.lm <- lm(logAbsRT ~ Vowel, data = vowel.data.late.removed)

vowel.lm.2 <- 
  lm(logAbsRT ~ Vowel, data = vowel.data, subset = absRT < 2000)

vowel.lm.3 <- 
  lm(log10(absRT) ~ Vowel, data = vowel.data, subset = absRT < 2000)

# linear mixed effects model for log RT

vowel.lmm <- 
  lmer(logAbsRT ~ Vowel + (Vowel | SubjectAssgn), 
       data = vowel.data.late.removed, REML = FALSE)

vowel.lmm.2 <- 
  lmer(logAbsRT ~ Vowel + (Vowel | SubjectAssgn), 
       data = vowel.data, subset = absRT < 2000, REML = FALSE)

vowel.lmm.3 <- 
  lmer(log10(absRT) ~ Vowel + (Vowel | SubjectAssgn), 
       data = vowel.data, subset = absRT < 2000, REML = FALSE)

# making more complicated models:

# no random slopes to avoid convergence issues
vowel.item.lmm <- 
  lmer(log10(absRT) ~ Vowel * ItemPair + (1 | SubjectAssgn),
       data = vowel.data, subset = absRT < 2000, REML = FALSE)

vowel.item.glmm <- 
  glmer(RespNum ~ ItemPair + (1 | SubjectAssgn),
       binomial, data = vowel.data, subset = absRT < 2000)

# significance
Anova(vowel.item.lmm)
Anova(vowel.item.glmm)

summary(glht(vowel.item.lmm, 
             linfct = mcp(Vowel = 'Tukey', interaction_average = TRUE)))

summary(glht(vowel.item.lmm, 
             linfct = mcp(ItemPair = 'Tukey', interaction_average = TRUE)))

summary(glht(vowel.item.glmm, 
             linfct = mcp(ItemPair = 'Tukey', interaction_average = TRUE)))

# output from languageR

par(mfrow = c(1, 1))
plotLMER.fnc(vowel.item.lmm, withList = TRUE)

# notice that plogis() is set automatically
plotLMER.fnc(vowel.item.glmm, withList = TRUE)


# construction of design matrices -----------------------------------------

subj.case.data <- 
  m100.lmm.2.fortify %>% 
  group_by(Subject, Case, Age_Calc) %>% 
  summarize(meanPredicted = mean(Predicted))

design.mtx <- model.matrix(~ Case * Age_Calc, data = subj.case.data)

# notice the similarities to the Python example
design.mtx

sink()
