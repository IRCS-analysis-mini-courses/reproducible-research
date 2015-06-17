
library(lme4)


# scaling variables -------------------------------------------------------


# scale attempts for easier fitting

multivariate.exp.data$AttemptsScale <- scale(multivariate.exp.data$Attempts)

# treat each token, trial, phase as a discrete entity

multivariate.exp.data$TokenFac <- as.factor(multivariate.exp.data$Token)

multivariate.exp.data$TrialFac <- as.factor(multivariate.exp.data$Trial)

multivariate.exp.data$PhaseFac <- as.factor(multivariate.exp.data$Phase)

# group alone models ------------------------------------------------------

group.rt.lmm <- 
  lmer(RT ~ Group * Age + (1 | Subject), data = multivariate.exp.data,
       subset = RT < 2000, REML = FALSE)

group.correct.glmm <- 
  glmer(Correct ~ Group * Age + (1 | Subject), data = multivariate.exp.data,
       binomial, subset = RT < 2000)

# fit without interactions
group.rt.add.lmm <- 
  lmer(RT ~ Group + Age + (1 | Subject), data = multivariate.exp.data,
       subset = RT < 2000, REML = FALSE)

group.correct.add.glmm <- 
  glmer(Correct ~ Group + Age + (1 | Subject), data = multivariate.exp.data,
        binomial, subset = RT < 2000)



# token alone models ------------------------------------------------------

token.rt.lmm <- 
  lmer(log(RT) ~ TokenFac * Age + (1 | Subject), data = multivariate.exp.data,
       subset = RT < 2000, REML = FALSE)

token.correct.glmm <- 
  glmer(Correct ~ TokenFac * Age + (1 | Subject), data = multivariate.exp.data,
        binomial, subset = RT < 2000)

# fit without interactions
token.rt.add.lmm <- 
  lmer(log(RT) ~ TokenFac + Age + (1 | Subject), data = multivariate.exp.data,
       subset = RT < 2000, REML = FALSE)

token.correct.add.glmm <- 
  glmer(Correct ~ TokenFac + Age + (1 | Subject), data = multivariate.exp.data,
        binomial, subset = RT < 2000)



# ‘proper’ models ---------------------------------------------------------

omnibus.rt.lmm <- 
  lmer(log(RT) ~ Group + TokenFac + Attempts + TrialFac + PhaseFac +
         (Token + Trial | Subject),
       data = multivariate.exp.data, subset = RT < 2000, REML = FALSE)

omnibus.correct.lmm <- 
  lmer(Correct ~ Group + TokenFac + Attempts + TrialFac + PhaseFac +
         (Token + Trial  | Subject),
       data = multivariate.exp.data, binomial, subset = RT < 2000)
