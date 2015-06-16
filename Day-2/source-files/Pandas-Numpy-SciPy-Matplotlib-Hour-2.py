
# coding: utf-8

# #Basic statistical modeling using Python and the Jupyter/IPython notebook
# In the first hour, we went over how to import and format our data in Python. We now continue with implementing basic statistical models using `Statsmodels`, `NumPy` and `scikit-learn`. If you want to do anything advanced and related to machine learning, it is best to use `scikit-learn`. `Statsmodels` is useful as it provides a formula interface and summary output similar to `R`. `scikit-learn` allows for cross-validation, scoring measures, and other advanced features. We will also examine alternatives to implement when faced with the limitations of Python modules.  
# 
# In the first hour, it was suggested that you examine the FEC and 2010 US Census data, and combine them into something descriptive (I figure you are not done with this yet). Some of the techniques covered (notably linear binomial regression and associated plots) will be applicable to that data, but mostly the technqiues covered will be useful for experimental data.  
# 
# Procedure:
# - perform analysis in Python (`Statsmodels`, `sckikit-learn`)  
# - perform analysis in R (base R, `lme4`)
# - statistical modeling in Julia (separate notebook)  
# 
# For more `Statsmodels` examples see the [GitHub repository](https://github.com/statsmodels/statsmodels) (which you can clone!) with [Jupyter/IPython notebooks](https://github.com/statsmodels/statsmodels/tree/master/examples/notebooks) (which you can download and run locally!) covering how to perform various fits.

# ##Dataset from a published study
# The first dataset we will look at is from a [paper I recently published](http://julian3rd.github.io/chromosomal-mutations-auditory-latency/). The data have already been analyzed and have extra columns related to the model ouput as analyzed in R. Let's first explore some of the relationships present in the data using `Seaborn`.   
# 
# Background details may be found [here](http://cercor.oxfordjournals.org/content/early/2015/02/11/cercor.bhv008.short?rss=1).

# In[1]:

import seaborn as sns
import numpy as np
import pandas as pd


# In[2]:

data_dir = '/Users/julian/GitHub/reproducible-research/Day-2/datasets/'
data_file = 'published-data-complete.csv'
child_study_data = pd.read_csv(data_dir + data_file)
child_study_data.head(n = 16)


# In[3]:

child_study_data.dtypes


# The main variable of interest is a measure of auditory processing, located in the column `M100LatCorr`. There are three groups (`Case`) for the comparison we are interested in. Let's first examine the distribution of values across groups.

# In[4]:

get_ipython().magic(u'matplotlib inline')
import matplotlib.pyplot as plt
from IPython.core.pylabtools import figsize
sns.set_palette("deep", desat = 0.6) # taken from examples on Seaborn documentation page


# In[5]:

control_data = []
deletion_data = []
duplication_data = []

for idx in range(len(child_study_data.Case)):
    if child_study_data.ix[idx, 'Case'] == 'control':
        control_data.append(child_study_data.ix[idx, 'M100LatCorr'])
    elif child_study_data.ix[idx, 'Case'] == 'deletion':
        deletion_data.append(child_study_data.ix[idx, 'M100LatCorr'])
    elif child_study_data.ix[idx, 'Case'] == 'duplication':
        duplication_data.append(child_study_data.ix[idx, 'M100LatCorr'])

control_data = np.array(control_data)
deletion_data = np.array(deletion_data)
duplication_data = np.array(duplication_data)


# In[6]:

plt.figure(figsize = (7, 7))
plt.xlabel('Latency (ms)', size = 20)
plt.ylabel('Density', size = 20)
plt.title('Latency distribution for each Case', size = 20)
sns.kdeplot(control_data, shade = True, label  = 'control', lw = 3)
sns.kdeplot(deletion_data, shade = True, label  = 'deletion', lw = 3)
sns.kdeplot(duplication_data, shade = True, label  = 'duplication', lw = 3)


# We could have also done this by calling plot from the `DataFrame` directly.

# In[7]:

child_study_data_case_group = child_study_data.groupby(['Case'])
figsize(7, 7)
child_study_data_case_group.M100LatCorr.plot(kind = 'kde')


# One covariate in the model is that of `Age`. There is an inverse relationship between latency and age; let's create a scatterplot with regression lines to see if this relationship holds in our dataset.

# In[8]:

plt.figure(figsize = (7,7))
sns.lmplot('Age_Calc', 'M100LatCorr', hue = 'Case', data = child_study_data)


# Maybe there is another way to examine the data. Let's examine the distributions in addition to the regression lines.

# In[9]:

sns.jointplot('Age_Calc', 'M100LatCorr', kind = 'reg', data = child_study_data)


# The linear regression accompaying the plot indicates that the inverse relationship between latency and age is significant. But I actually want to see it in a model that I can diagnose. And I want to see if the regressions broken down by `Case` are also significant. We will also revisit this data after seeing what the LMM output is.
# 
# `Statsmodels` takes either a formula or matrices to specify the model. You can use either, but for ease and comparison to R, we will use the formula interface.

# In[10]:

import statsmodels.api as sm
import statsmodels.formula.api as smf


# In[11]:

lat_age_model = smf.ols('M100LatCorr ~ Age_Calc', data = child_study_data).fit()


# In[12]:

print lat_age_model.summary()


# Let's parse the output (the `summary()` call), or at least the things people most commonly care about:
# - R-squared: squared correlation between the predictors and the dependent variable
# - Df Residuals: degrees of freedom of the residuals
# - Df Model: degreesof freedom of the model
# - F-statistic: *F* ratio
# - Prob(F-statistic): significance of F-statistic (1 - probability density(F-statistic, Df model, Df Residuals) for the overall model
# - No. Observations: observations in the model
# - Log-likelihood: 
# - AIC: Akaike’s Information Criterion; −2 × log -likelihood + 2(p + 1) where p is the number of parameters in the model (lower/smaller is better)
# - BIC: Bayesian Information Criterion
# - coef: model coefficients
# - std err: standard error for the coefficients
# - t: coefficient / standard error (notice this has been truncated)
# - P > |t|: signficiance of t value 
# - 95% Conf Int: lower and upper bounds for 95% CI
# - Bottom table: statistics on the residuals, i.e., are they normally distributed

# So the output is indicating that the inverse relationship between latency and age is significant; for every "unit" decrease in `Age`, there is an associated 5.4 ms decrease in latency. It might be better to examine this relationship are the mean of ***fitted*** values from the ultimate LMM, but that will be done at the end.  
# 
# Let's perform some graphical examinations of this particular model:
# 
# - the influence of various data points  
# - the distribution of residuals      
# - residuals vs. fitted

# In[13]:

sm.graphics.influence_plot(lat_age_model)


# In[14]:

plt.hist(np.array(lat_age_model.resid), bins = 10)
plt.title('Histogram of residuals')


# In[15]:

plt.scatter(x = lat_age_model.fittedvalues, y = lat_age_model.resid, s = 60, alpha = 0.65)
plt.ylabel('Residuals')
plt.xlabel('Fitted values')
plt.title('Residuals vs. Fitted')


# So the distribution of residuals and the residuals vs fitted values look alright-ish. That leverage plot...is something else. The distribution of residuals is OK, but all the points appear to have the same leverage (be interesting when we get to a comparison with R on Day 3). Maybe modeling the *all* measurements of the subject latency ~ age relationship is not that smart and use the mean across conditions after fitting the LMM instead.

# ##Linear Mixed Effects Modeling in `Statsmodels`
# 
# Since we a currently using `Python` and we want to implement a LMM, we are fortunate that `Statsmodels` can implement LMMs. Unfortunately, `Statsmodels` does not currently allow for interaction terms to be specified. Fortunately again, the most parsimonious model for these data is a main-effects model. So we can implement an analysis of these data. Once that is done, we will begin again ad replicate the results in R.  
# 
# We want to see what factors/predictors affect the latency. Breakdown of the model specifications is as follows:  
# - ***Dependent variable***: M100LatCorr  
# - ***Fixed effects***: Hem, Cond, Case, Site  
# - ***Covariate***: Age_Calc  
# - ***Random effect***: Subject
# - ***Random slopes (repeated measures)***: Hem, Cond; not implemented in `Statsmodels` example below  

# `Statsmodels` handles missing values in the dependent variable in a less than ideal manner. In addition, just to be safe, we will introduce numeric versions of categorical labels via mapping.

# In[16]:

# not really necessary at this point; 
# just a good way to demonstrate vectorized functions with pandas
child_study_data['SubjectNum'] = child_study_data.Subject.str.replace('-', '')

child_study_data.head()


# In[17]:

# numeric values for the categorical predictors

hem_dict = {'1-LH': 1, '2-RH': 2}
cond_dict = {'1-200': 1, '2-300': 2, '3-500': 3, '4-1000': 4}
case_dict = {'control': 1, 'deletion': 2, 'duplication': 3}
site_dict = {'UCSF': 2, 'CHOP': 1}

child_study_data['HemNum'] = child_study_data.Hem.map(hem_dict)
child_study_data['CondNum'] = child_study_data.Cond.map(cond_dict)
child_study_data['CaseNum'] = child_study_data.Case.map(case_dict)
child_study_data['SiteNum'] = child_study_data.Site.map(site_dict)

child_study_data.head()


# In[18]:

# removing rows with missing values in the dependent variable

child_study_data_no_na = child_study_data.dropna(subset = ['M100LatCorr'])
child_study_data_no_na = child_study_data_no_na.reindex()
child_study_data_no_na.head()


# In[19]:

print 'Dimensions with missing dependent variable removed: %d rows, %d columns' %  (child_study_data_no_na.shape[0], child_study_data_no_na.shape[1])


# In[20]:

# fitting a model without repeated measures (i.e., no random slopes)
# because I cannot entirely  figure out what Statsmodels is doing
# with the random effects structure

# also notice that Statsmodels does not fit quite as quickly as lme4

m100_lmm = smf.mixedlm('M100LatCorr ~ Hem + Cond + Case + Site + Age_Calc ',                        data = child_study_data_no_na, groups = child_study_data_no_na['Subject'])


m100_lmm_fit = m100_lmm.fit()


# And now to inspect the output:

# In[21]:

print m100_lmm_fit.summary()


# ##Calling R from Python
# The `rpy2` package allows for calling R directly from Python. Let's use it to see if we get similar results for the coefficients and how the summary output differs. The cells below illustrate how to do this directly in Python (with or without a notebook).   
# 
# Unfortunately, using `rpy2` directly in Python involves a lot of aliasing and object calling. For example, let's see what it takes to read in a dataset and convert it to a R `data.frame` in Python.

# In[22]:

import rpy2.robjects as robjects
r = robjects.r
from rpy2.robjects.packages import importr
import pandas.rpy.common as com


# In[23]:

child_study_r = com.convert_to_r_dataframe(child_study_data, strings_as_factors = True)


# In[24]:

# python representation
child_study_r


# That was a bit of a pain. And that is before having to do painful, mistake-prone things such as setting global variables in order to call a model.  
# 
# Fortunately for us there is an easier way: use `R magics` and via the `ipython` extension for the module `rpy2` we can directly use the R engine in a Jupyter/IPython notebook. Time to redo this in R directly via the R engine in Jupyter/IPython.

# In[25]:

get_ipython().magic(u'load_ext rpy2.ipython')


# In[26]:

# use a single '%' in front of 'R' when you have just one line to execute
get_ipython().magic(u'R library(lme4)')


# In[27]:

get_ipython().run_cell_magic(u'R', u'', u"# use two '%' when you have multiple lines to execute in a cell, i.e., a cell magic\n# must go at very beginning of the celll\nlibrary(car)\nlibrary(multcomp)")


# In[28]:

get_ipython().run_cell_magic(u'R', u'', u"data.dir = '/Users/julian/Documents/ircs-mini-course-data'\ndata.file = 'published-data-complete.csv'\nchild.data = read.csv(file.path(data.dir, data.file), header = TRUE)")


# Let's fit two models: one using restricted maximum likelihood and no random slopes (as `Statsmodels`; restricted maximum likelihood is the default for most analysis programs/routines) and another using maximum likelihood with random slopes (which you should do and is the default in `MixedModels` in Julia - maximum likelihood, not including random slopes).

# In[29]:

get_ipython().run_cell_magic(u'R', u'', u'child.addmodel.reml <- lmer(M100LatCorr ~ Hem + Cond + Case + Site + Age_Calc + \n                           (1 | Subject), data = child.data)\n\nchild.addmodel.ml <- lmer(M100LatCorr ~ Hem + Cond + Case + Site + Age_Calc + \n                           (Cond + Hem | Subject), data = child.data, REML = F)')


# In[30]:

get_ipython().magic(u'R print(summary(child.addmodel.reml))')


# Let's compare this to the `Statsmodels` output:

# In[31]:

print m100_lmm_fit.summary()


# Pretty close; and I would argue that due to limits in precision, nothing past the first decimal point (and maybe not even that) is significant.  
# 
# Now let's examine the proper model:

# In[32]:

get_ipython().magic(u'R print(summary(child.addmodel.ml))')


# One R package I used to use a lot of, lost track of, and am using a lot again is `languageR`. It has useful functions for plotting the results of class `lmerMod`. Lets diagnose the fit with some very basic plots.

# In[33]:

get_ipython().magic(u'R library(languageR); # semicolon suppresses memory address output')


# In[34]:

get_ipython().magic(u'R plotLMER.fnc(child.addmodel.ml, withList = TRUE)')


# Now let's check the significance of our models using the `car` package.

# In[35]:

get_ipython().magic(u'R print(Anova(child.addmodel.reml))')
# this is from the car package; notice the capital 'A' at the beginning
# to differentiate from the built-in R functions `anova()`


# In[36]:

get_ipython().magic(u'R print(Anova(child.addmodel.ml))')


# And because we want to do the right thing/are completists, let's implement some multiple comparison procedures.

# In[37]:

get_ipython().magic(u"R print(summary(glht(child.addmodel.ml, linfct = mcp(Hem = 'Tukey', covariate_average = T))))")


# In[38]:

get_ipython().magic(u"R print(summary(glht(child.addmodel.ml, linfct = mcp(Case = 'Tukey', covariate_average = T))))")


# In[39]:

get_ipython().magic(u"R print(summary(glht(child.addmodel.ml, linfct = mcp(Cond = 'Tukey', covariate_average = T))))")


# Last thing to do: revist the age - latency relationship, now that we have accounted for our covariate of age. We will collapse across hemispheres and conditions for each subject, impelement a linear regression and examine R's plots for the linear regression.

# In[40]:

get_ipython().run_cell_magic(u'R', u'', u'library(dplyr)\nlibrary(ggplot2)\n\n# refit model so that rows with missing values are included\n# this is so we can match the model fit values and\n# impute missing observations if we desire\n\n\nchild.addmodel.ml <- lmer(M100LatCorr ~ Hem + Cond + Case + Site + Age_Calc + \n                           (Cond + Hem | Subject), data = child.data, \n                          na.action = na.exclude, REML = F)\n\n# append fitted  and residual values\nchild.addmodel.ml.fortify <- fortify(child.addmodel.ml)\n\nchild.addmodel.ml.fortify$Predicted <- \n  predict(child.addmodel.ml, newdata = child.addmodel.ml.fortify, \n          na.action = na.pass, allow.new.levels = TRUE)\n\nchild.addmodel.ml.fortify.summarize <- child.addmodel.ml.fortify %>% \n     group_by(Subject, Case, Age_Calc) %>% \n       summarize(meanFitted = mean(.fitted), meanPredicted = mean(Predicted))\n\nhead(child.addmodel.ml.fortify.summarize)')


# In[41]:

get_ipython().magic(u'R print(glimpse(child.addmodel.ml.fortify.summarize))')


# In[42]:

get_ipython().run_cell_magic(u'R', u'', u'\n# colorblind friendly palette via Winston Chang\ncbPalette <- c("#999999", "#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7")\n\nggplot(child.addmodel.ml.fortify.summarize,\n         aes(y = meanPredicted, x = Age_Calc, shape = Case))+\n  geom_point(size = 3, aes(colour = Case)) + theme_bw() +\n  labs(y = \'Latency (ms)\', x = \'Age (years)\',\n       title = \'Mean predicted M100 vs. age\',\n       shape = \'Case\', linetype = \'Case\')+\n  geom_smooth(aes(linetype = Case, colour = Case, fill = Case),\n              size = 1.3, method = \'lm\', se = TRUE)+\n  scale_x_continuous(breaks = seq(5, 17, 2))+\n  scale_y_continuous(breaks = seq(90, 215, 20))+\n  coord_cartesian(ylim = c(90, 190))+\n  theme(legend.position = \'bottom\',\n        legend.text = element_text(face = \'bold\', size = 16),\n        legend.title = element_blank(),\n        axis.text.x = element_text(size = 15, face = \'bold\'),\n        axis.text.y = element_text(size = 15, face = \'bold\'),\n        axis.ticks = element_blank(),\n        axis.title.x = element_text(size = 20, face = \'bold\'),\n        axis.title.y = element_text(size = 20, face = \'bold\'),\n        plot.title = element_text(size = 20, face = \'bold\')) + \n  scale_fill_manual(values = cbPalette) + \n  scale_colour_manual(values = cbPalette) +\n  scale_linetype_manual(values = c(\'solid\', \'dashed\', \'dotted\'))')


# In[43]:

get_ipython().magic(u'R m100.age.dist.case.aov <- aov(meanPredicted ~ Age_Calc * Case, data = child.addmodel.ml.fortify.summarize);')
# semicolon suppress the output; Jupyter/IPython gives the memory addresses and nothing useful


# In[44]:

get_ipython().magic(u'R print(summary.aov(m100.age.dist.case.aov)) # ANOVA table style summary')


# In[45]:

get_ipython().magic(u'R print(summary.lm(m100.age.dist.case.aov)) # treatment contrast style summary')


# R (and other programs) allows you to plot the model diagnostics. I know JMP does this by default, I think SPSS does, and I am unsure about others.

# In[46]:

get_ipython().run_cell_magic(u'R', u'-w 800 -h 800 -u px # changes the figure width and height in pixels', u'\npar(mfrow = c(2,2)) # 2 x 2 plot layout: plot in row-dominant fashion\nplot( m100.age.dist.case.aov)')


# Those are the four plots you get by default when plotting a model of class `lm` or `glm` (or something that inherits from it). Let's look at all six possible plots.

# In[47]:

get_ipython().run_cell_magic(u'R', u'-w 900 -h 1000 -u px', u'\npar(mfrow = c(3, 2))\nplot( m100.age.dist.case.aov, which = c(1:6))')


# This is also a nice segue into our next topic: logisitc regression. We can perform this using both `Statsmodels` and R; let's start with `Statsmodels` before moving to R. We will save the full R implementation for Day 3. `scikit-learn` also can perform logistic regression, except geared more towards machine learning applications.

# #Generalized Linear Models
# ##Logistic regression
# 
# Logistic regression is used when the dependent variable is binary (1/0; TRUE/FALSE; yes/no) and depending on the data and discipline, probit, logit, tobit or other types of models are used. For perceptual research, logit type models are usually implemented. In the first example, we will use logistic regression to determine if the number of observed responses are different between `Case` levels for the data just analyzed. The second one will examine correct and incorrect responses in a psychophysical experiment.
# 
# Analysis of deviance - `Statsmodels`  
# Vowel discrimination - `Statsmodels`, R

# #Analysis of deviance
# The column `M100compCase` indicates whether or not a reponse was recorded in an individual; 1 indicates yes, and 0 indicates no. We want to see if for whatever reason, the three different groups (`Case` levels) differed in the number of observed responses. If we had two groups, we would perform a two-sample proportion test (or maybe even a Chi-square test). Since we have three groups, we will perform an analysis of deviance. We will have to specify a binomial error function (the family argument) and a logit link.

# In[48]:

m100_complete = smf.glm(formula = 'M100compCase ~ Case', data = child_study_data,                         family = sm.families.Binomial()).fit();
m100_complete.summary()


# So the model indicates there is likely no statistically significant difference between the controls (intercept) and deletions, but between the duplications and deletions and duplications and controls. We have to back-transform the coefficients in order to get the original proportions.

# In[49]:

from scipy import stats


# In[50]:

# must use the inverse of the link function
# in this case, cumulative probability distribution
# i.e., stats.continuous_distribution.cdf()

# these are treatment contrasts, so include
# the sign to ge the proper value for each coefficient

print 'Proportion of observed responses in controls: ', stats.logistic.cdf(0.8128)
print 'Proportion of observed responses in deletions: ', stats.logistic.cdf(0.8128 + 0.1566)
print 'Proportion of observed responses in duplications: ', stats.logistic.cdf(0.8128 - 0.7816)


# Well, that was easy enough. Let's compute the proportion of complete observations for each `Case` level and see if those calculations match up with the model results.

# In[51]:

case_counts = child_study_data.groupby(['Case']).size()
case_counts


# In[52]:

complete_counts = child_study_data.groupby('Case')['M100compCase'].sum()
complete_counts


# In[53]:

complete_counts.div(case_counts)


# ##Psychophyical discrimination in an AX task
# 
# The analysis of the following data in R and Julia and background information can be found in a [GitHub repo I made](http://julian3rd.github.io/model-comparison-r-julia/).  We are going to use the `Statsmodels` formula interface once again and utilize `patsy` in order to deal with the matrices directly.  
# 
# A quick overview: participants were given a pair of synthetic vowel sounds, each constructed using a different set of waveforms and harmonics. They had to indicate whether or not a given pair sounded the same or different to them. The participants did not know if the signals had the same physical structure; so an answer was incorrect if the signals were physcally different and they answered the were the same (and vice versa).  Those of you who know about psychophyiscs will notice I said nothing about false alarms and such; we just want to know about whether or not the responses were correct or incorrect. Besides, details are in my dissertation and a manuscript that may never be published.

# In[54]:

# going to be fancy and get it directly from GitHub

source_dir = 'https://raw.githubusercontent.com/IRCS-analysis-mini-courses/reproducible-research/'
exact_path = 'master/Day-2/datasets/psycho-data-april-2015.csv'

vowel_data = pd.read_csv(source_dir + exact_path)
vowel_data.head()


# Let's ask a simple question: there were three vowels used (/a/, /i/, /u/). Was participant performance the same for all of the vowels?

# In[55]:

vowel_glm = smf.glm(formula = 'RespNum ~ Vowel', data = vowel_data,                         family = sm.families.Binomial()).fit();
vowel_glm.summary()


# In[56]:

print 'Proportion correct for /a/: ', stats.logistic.cdf(0.0669)
print 'Proportion correct for /i/: ', stats.logistic.cdf(0.0669 + 1.3351)
print 'Proportion correct for /u/: ', stats.logistic.cdf(0.0669 + 0.8498)


# Examining the coefficients, z-values and confidence intervals suggests that there was a performance difference between the vowels.  Let's compare this to R's output.

# In[57]:

get_ipython().run_cell_magic(u'R', u'', u"\nlibrary(readr)\n\nsource.dir = 'https://raw.githubusercontent.com/IRCS-analysis-mini-courses/reproducible-research'\nexact.path = 'master/Day-2/datasets/psycho-data-april-2015.csv'\n\nvowel.data = read_csv(file.path(source.dir, exact.path))\nhead(vowel.data)")


# In[58]:

get_ipython().run_cell_magic(u'R', u'', u'glimpse(vowel.data)')


# And now to use R's `glm()` function to do the same thing.

# In[59]:

get_ipython().run_cell_magic(u'R', u'', u"\nvowel.glm = glm('RespNum ~ Vowel', data = vowel.data, family = binomial)\nsummary(vowel.glm)")


# Get the proportions for each vowel:

# In[60]:

get_ipython().run_cell_magic(u'R', u'', u"\n# in R, the cumulative distribution function is given by\n# pdistribution, e.g., plogis for the logistic equation\n\na.corr <- plogis(0.06690)\ni.corr <- plogis(0.06690 + 1.33509)\nu.corr <- plogis(0.06690 + 0.84983)\n\ncat('Proportion correct for /a/:', a.corr, sep = '\\n')\ncat('Proportion correct for /i/:', i.corr, sep = '\\n')\ncat('Proportion correct for /u/:', u.corr, sep = '\\n')")


# We can see that R is a little bit more explicit about the significances when we look at the output of the table. But the study involved repeated measures and every subject has a different internal representation, dialect, etc. Fortunately, `lme4` allows for Generalized Linear Mixed Effects Models so we can have different error families. Time to refit the data. And do it relatively quickly.

# In[61]:

get_ipython().run_cell_magic(u'R', u'', u"\nvowel.glmm = glmer('RespNum ~ Vowel + (Vowel|SubjectAssgn)', data = vowel.data, family = binomial)\nsummary(vowel.glmm)")


# In[62]:

get_ipython().run_cell_magic(u'R', u'', u"\na.corr <- plogis(0.07378)\ni.corr <- plogis(0.07378 + 1.39440)\nu.corr <- plogis(0.07378 + 0.93826)\n\ncat('Proportion correct for /a/ from GLMM:', a.corr, sep = '\\n')\ncat('Proportion correct for /i/ from GLMM:', i.corr, sep = '\\n')\ncat('Proportion correct for /u/ from GLMM:', u.corr, sep = '\\n')")


# There are other analyses we could look at (and you can look at [the GitHub repo](http://julian3rd.github.io/model-comparison-r-julia/) I made if you really want to) but we will move on from here.

# Next, let's examine the RT data. Data of this type are usually analyzed as an exponentially-modified Gaussian, but since that is beyond the scope of this course, we will avoid that. One thing that was done in the past however, was to transform the data (usually via log-transform) and analyze the data before a back-transformation when reporting the results. Fortunately, I already included the log transform version of the RT in the data. Let's first see what each distribution looks like.

# In[63]:

get_ipython().run_cell_magic(u'R', u'', u"library(ggplot2)\n\nggplot(vowel.data, aes(x = absRT)) + geom_density(fill = 'black') + \n  labs(title = 'Raw RT KDE') + theme_bw()")


# In[64]:

get_ipython().run_cell_magic(u'R', u'', u"ggplot(vowel.data, aes(x = logAbsRT)) + geom_density(fill = 'black') + \n  labs(title = 'log10 RT KDE') + theme_bw()")


# There are some timed out responses above (2000 ms) so let's remove those before proceeding.

# In[65]:

get_ipython().run_cell_magic(u'R', u'', u'vowel.data.late.removed <- subset(vowel.data, absRT < 2000)\nvowel.data.late.removed <- droplevels(vowel.data.late.removed)')


# In[66]:

get_ipython().magic(u"R print(ggplot(vowel.data.late.removed, aes(x = logAbsRT)) + geom_density(fill = 'black') + theme_bw());")


# Now to implement models in the same manner as the response models above.

# Linear model:

# In[67]:

get_ipython().run_cell_magic(u'R', u'', u"vowel.lm <- lm('logAbsRT ~ Vowel', data = vowel.data.late.removed)\nsummary(vowel.lm)")


# Linear Mixed Effects Model:

# In[68]:

get_ipython().run_cell_magic(u'R', u'', u"vowel.lmm <- lmer('logAbsRT ~ Vowel + (Vowel|SubjectAssgn)', data = vowel.data.late.removed, REML = FALSE)\nsummary(vowel.lmm)")


# Notice that we could have also done this:

# In[69]:

get_ipython().run_cell_magic(u'R', u'', u"vowel.lm2 <- lm('log10(absRT) ~ Vowel', data = vowel.data.late.removed)\nsummary(vowel.lm2)")


# In[70]:

get_ipython().run_cell_magic(u'R', u'', u"vowel.lmm2 <- lmer('log10(absRT) ~ Vowel + (Vowel|SubjectAssgn)', data = vowel.data.late.removed, REML = FALSE)\nsummary(vowel.lmm2)")


# And remember, there is nothing that says you must take the base-10 logarithm; this is just the expression of the natural logarithm in a different numeric base (as any of you who have done research with perceptual scales or remember log rules will know).

# ##Linear regression with `scikit-learn`
# `scikit-learn` is a Python module for machine learning. As such, you can implement very basic routines such as linear regression, to more complicated ones such as Support Vector Machines. `scikit-learn` also supports a large number of classification and learning algorithms and transforms.  You can even combine methodologies: for (a very simple and incomplete) example, separate data into training, cross-validation and test sets; apply linear regression to the training set, and see how well the predictions perform in the cross-validation and test sets. [See the documentation for a list of full examples](http://scikit-learn.org/stable/documentation.html).  
# 
# Let's re-implement out age regression in `scikit-learn`.

# For `scikit-learn`, we will have to specify our features as a matrix, and indicate what the dependent variable is. Once we get the model object, there are several methods to access different parts/features of the model. I had to use the version of the data with no missing values in the dependent variable in order for this to work.

# In[71]:

from sklearn.linear_model import LinearRegression


# In[72]:

def prepare_features(data_frame, featureslist, dependent_var):
    """prepare_features(data_frame, featureslist, dependent_var)
    prepare_features prepares the features (predictors)
    in featureslist for a linear regression.
    returns matrices y and X (target, coefficient matrix)""" 
    y = data_frame[dependent_var].values
    X = data_frame[featureslist].values
    if len(X.shape) == 1:
        X = X.reshape(-1, 1)
    return y, X


# In[73]:

dependent_var, predictors = prepare_features(child_study_data_no_na, ['Age_Calc'], ['M100LatCorr'])


# In[74]:

age_scikit_model = LinearRegression().fit(predictors, dependent_var)


# In[75]:

print 'Model intercept: ', age_scikit_model.intercept_
print 'Model coefficients: ', age_scikit_model.coef_
print 'Model R-squared value: ', age_scikit_model.score(predictors, dependent_var)


# And since I want to be a showoff/show my results are consistent no matter what underlying engine I use, do it again in `SciPy`.

# In[76]:

slope, intercept, r_value, p_value, std_err =  stats.linregress(child_study_data_no_na.Age_Calc, child_study_data_no_na.M100LatCorr)


# In[77]:

print 'SciPy model intercept: ', intercept
print 'SciPy model coefficient: ', slope
print 'SciPy model R-squared value: ', r_value ** 2


# What about when I have both numeric and categorical predictors? Let's try this again with the fitted latency values vs. the age like we did in R.  
# 
# First, we group the data by `Subject`, `Case`, and continuous age (`Age_Calc`) and then for the `Predicted` column, aggregate the the data and call the mean function across the values.

# In[78]:

# as_index = False argument prevents the group headings from being part of the indexing
# compare this to the summary from dplyr in R above
subj_case_data = child_study_data.groupby(['Subject', 'Case', 'Age_Calc'], as_index = False).agg({'Predicted': 'mean'})


# In[79]:

subj_case_data.head()


# `scikit-learn` needs all of the variable in numerics form to fit the model (for `Statsmodels` and `R` there is an underlying numeric representation that is used).  
# 
# Then we have to create dummy values for each level of `Case`; otherwise, `sckikit-learn` would assume there is an order and that the numeric values we assign for each `Case` level are multiplicative.

# In[80]:

subj_case_data['CaseNum'] = subj_case_data.Case.map(case_dict)
subj_case_data.head()


# In[81]:

case_dummies = pd.get_dummies(subj_case_data.Case, prefix = 'Case').iloc[:, 1:]
subj_case_data = pd.concat([subj_case_data, case_dummies], axis = 1)
subj_case_data.head()


# In[82]:

predictors = ['Age_Calc', 'Case_deletion', 'Case_duplication']
predicted_lat, predictors = prepare_features(subj_case_data, predictors, ['Predicted'])


# In[83]:

predicted_lat_age_model = LinearRegression().fit(predictors, predicted_lat)


# In[84]:

print 'Model intercept: ', predicted_lat_age_model.intercept_
print 'Model coefficients: ', predicted_lat_age_model.coef_
print 'Model R-squared value: ', predicted_lat_age_model.score(predictors, predicted_lat)


# Hmmmmm. Close, but not quite right. When we did this in R, we specified an interaction term. Since `scikit-learn` does not allow a formula interface, how do we do this? Internally, all programs that use a formula system (in fact, all statistical programs) take the terms and make matrices directly. We will use the `patsy` module in order to create the matrices directly. But first, try this again in `Statsmodels`. In fact, `Statsmodels` is taking the representation from `patsy` in order to create the matrices used in the fit.

# In[85]:

lat_age_model_statsmodels = smf.ols('Predicted ~ Age_Calc * Case', data = subj_case_data).fit()


# In[86]:

print lat_age_model_statsmodels.summary()


# The R output:
aov(formula = meanPredicted ~ Age_Calc * Case, data = child.addmodel.ml.fortify.summarize)

Residuals:
    Min      1Q  Median      3Q     Max 
-51.426 -11.795   2.298  13.478  31.924 

Coefficients:
                         Estimate Std. Error t value Pr(>|t|)    
(Intercept)              175.1262    12.7816  13.701  < 2e-16 ***
Age_Calc                  -3.8589     0.9934  -3.885 0.000192 ***
Casedeletion              41.7952    18.7085   2.234 0.027878 *  
Caseduplication          -22.2545    26.0828  -0.853 0.395726    
Age_Calc:Casedeletion     -1.7530     1.5395  -1.139 0.257754    
Age_Calc:Caseduplication   1.4583     2.1848   0.667 0.506120 
# Now to try this in `patsy`.  
# 
# Steps:  
# 1. See how the model description is derived from the formula  
# 2. Build the design matrix that the formula specifies  
# 3. Use the design matrix in order to create the model in `scikit-learn`

# In[87]:

from patsy import ModelDesc, EvalEnvironment


# In[88]:

env = EvalEnvironment.capture()
predicted_lat_age_mtx = ModelDesc.from_formula('Predicted ~ Age_Calc * Case', env)


# In[89]:

predicted_lat_age_mtx


# In[90]:

from patsy import dmatrix


# In[91]:

design_mtx = dmatrix('Case * Age_Calc', subj_case_data)


# In[92]:

design_mtx


# In[93]:

# notice how the second and third columns ('deletion' and 'duplication')
# match up with the dummy columns created previously

np.asarray(design_mtx)


# In[94]:

y_val = subj_case_data.Predicted

predicted_lat_age_model_2 = LinearRegression().fit(design_mtx, y_val)


# In[95]:

print 'Model intercept: ', predicted_lat_age_model_2.intercept_
print 'Model coefficients: ', predicted_lat_age_model_2.coef_


# Comparison to `Statsmodels`:

# In[96]:

print lat_age_model_statsmodels.summary()


# And R output:
aov(formula = meanPredicted ~ Age_Calc * Case, data = child.addmodel.ml.fortify.summarize)

Residuals:
    Min      1Q  Median      3Q     Max 
-51.426 -11.795   2.298  13.478  31.924 

Coefficients:
                         Estimate Std. Error t value Pr(>|t|)    
(Intercept)              175.1262    12.7816  13.701  < 2e-16 ***
Age_Calc                  -3.8589     0.9934  -3.885 0.000192 ***
Casedeletion              41.7952    18.7085   2.234 0.027878 *  
Caseduplication          -22.2545    26.0828  -0.853 0.395726    
Age_Calc:Casedeletion     -1.7530     1.5395  -1.139 0.257754    
Age_Calc:Caseduplication   1.4583     2.1848   0.667 0.506120 
# You can also use `Seaborn` to see if the parameters from our model graphically match what the table gives us ([examples can be seen here](http://nbviewer.ipython.org/github/mwaskom/seaborn/blob/master/examples/linear_models.ipynb)).

# And of course you could go further: separate out the data into the three different sets, use a predict method to get new values and see how your model performed. The separation into different data sets is easiest done in Python using `scikit-learn`. You can also perform similar machine learning procedures in R [using the caret package](http://topepo.github.io/caret/index.html).

# #Assignment
# For the HW2 dataset, go through and analyze the data as you would your own data. That means examine distributions, plot relationships, and apply the approriate type of model to the data (binomial GLM/GLMM for binary responses; LM/LMM for continuous). And be a good researcher and perform multiple comparison procedures.   
# 
# Personally, I would suggest carrying out any data munging and the basic analyses in Python (regressions, binomial GLM) to get a feel for what is going on and the more stat-heavy analyses in R (mixed models, multiple comparisons) ad any basic analyses (which will also be covered on Day 3).
# 
# Make sure to perform the analysis in a Jupyter/IPython notebook so that you can easily display and share results on Monday. Try doing things such as creating functions to make life easier/make analyses generalizable. Also play around with some of the data contained in the [references](https://github.com/IRCS-analysis-mini-courses/reproducible-research/blob/master/REFERENCES.md) so that you can make stylized plots.

# ##References
# [An Introduction to Linear Regression](http://nbviewer.ipython.org/github/justmarkham/DAT4/blob/master/notebooks/08_linear_regression.ipynb)  
# [Desperately seeking Silver](http://nbviewer.ipython.org/github/cs109/content/blob/master/HW2.ipynb). I used this notebook to learn how to fit models in `scikit-learn` as well as how to perform simulations in Python.  
# [How formulas work in patsy](http://patsy.readthedocs.org/en/latest/formulas.html). Description of formulas and design matrices are create in `patsy` and how their formulas and interpretation can differ from R.  
# [`scikit-learn` stable documentation](http://scikit-learn.org/stable/documentation.html). Documentation for the latest stable release of `scikit-learn`.  
# [Graphical representations of linear models](http://nbviewer.ipython.org/github/mwaskom/seaborn/blob/master/examples/linear_models.ipynb). IPython notebook using the Titanic dataset to illustrate some of `Seaborn`'s capabilities.  
# [GitHub repository on model comparisons in R and Julia](http://scikit-learn.org/stable/documentation.html). GitHub repo of a project of mine that involved implementing GLMs and LMMs in R and Julia and comparing the output.  

# In[97]:

import IPython
import sys


# In[98]:

print 'Python version: ', sys.version
print 'Platform: ', sys.platform
print 'IPython version: ', IPython.__version__
print 'NumPy version: ', np.__version__
print 'Pandas version: ', pd.__version__

