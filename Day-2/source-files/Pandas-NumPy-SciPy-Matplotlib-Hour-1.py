
# coding: utf-8

# # Data import and visualization using Python
# The first part of this mini-course will focus on using the Python ecosystem to import and visualize data. We will focus on a few publically-available datasets (more are given in the syllabus) in various formats (CSV, DAT, XML, etc.) and with various data types (continuous, integer, datetime, character, etc.).
# 
# Suggested datasets (some will be used as examples):
# - Princeton stats course by German Rodriguez *(small)*
# - Social Security Baby Names *(small)*
# - USDA food database *(medium)*
# - 2010 US Census *(small; the API can give much larger datasets)*
# - NY MTA *(small)*
# - 2012 Federal Election Commission *(large)*
# - MovieLens *(medium to large)*
# 
# The goal is to get everyone familiar with the nuances and potential issues involved in importing, cleaning, shaping and analyzing data. These datasets are typically used in several data projects or as analytic examples for various statistical tests. We also encourage (implore really) you for the assignments/homeworks to expand what you have learned in order to maniuplate data in both Python and R.  
# 
# Python modules for importing, visualizing and analyzing datasets:
# - `pandas`
# - `lxml`
# - `json`
# - `simplejson` (gives more informative error messages than json; good for troubleshooting)
# - `Matplotlib`
# - `Seaborn`
# - `NumPy`
# - `SciPy`
# - `Statsmodels`
# - `scikit-learn`

# ## Importing data using pandas
# The majority of data you will be using will be in a tabular format, either from a deimited file, URL, database query, or some other method. Ideally, the file will have been formatted in a sensible manner (consistent delimiters and spacing) but that is not guaranteed. The `pandas` module will read in data in a tabular format and store it in a structure called a `DataFrame`; `DataFrame`s have several useful features that will be explored as we go through the data.  
# 
# The main functions you will likely use:
# - `read_csv`: comma is the default delimiter
# - `read_table`: more general function; `\t` is the default delimiter
# - `read_fwf`: read fixed-width files  
# 
# See also the `pandas` IO Tools documentation: http://pandas.pydata.org/pandas-docs/stable/io.html

# ## Example 1: 2010 US Census data (CSV)
# The first example we will look at is from the 2010 US Census, specifically the population density data. You can either download it to a local drive or access the URL directly.

# In[1]:

import pandas as pd


# In[2]:

density_url = 'http://www.census.gov/2010census/csv/pop_density.csv'

density_data_2010 = pd.read_csv(density_url)

density_data_2010.head()


# So what happened here? We (1) specified the URL as a string; (2) called the `read_csv` function to download the data and assign it to the variable `density_data_2010`; (3) examined the first six rows using the `head` function.  
# 
# Do we really want the data in this format? We likely want the row with the index of **`2`** to be the header of our `DataFrame`. Let's reimport the data, using some of `read_csv`'s additional arguments.

# In[3]:

density_url = 'http://www.census.gov/2010census/csv/pop_density.csv'

density_data_2010 = pd.read_csv(density_url, skiprows = [0, 1, 2])

density_data_2010.head()


# That is much better. Let's now explore some of the basic functionality of a `pandas` DataFrame that will aid productivity and inform about the structure of the data.

# In[4]:

density_data_dimen = density_data_2010.shape
density_data_cols = density_data_2010.columns.values.tolist()
density_data_idx = density_data_2010.index
pop_1910 = density_data_2010['1910_POPULATION'].values

print 'Data dimensions: %d rows, %d columns' % (density_data_dimen[0], density_data_dimen[1])
print 'First 10 indices of population density DataFrame: ', density_data_idx[:10]

print 'Names of DataFrame columns:'
print 'Name: index'
for position, name in enumerate(density_data_cols):
    print name, ':', position


# In[5]:

print 'Population values in 1910 (first 10 entries):'
pop_1910[:10]


# So the output of the preceding cells was:
# - the shape of the data using the `shape` function
# - converting the names of the columns to a list and then printing the names and their positions
# - retrieving the values of the indices, in this case row numbers
# - retreiving the first 10 values of the population for the year 1910  
# 
# We will come back to this dataset later in order to do more with indexing.

# ## Example 2: Program effort data (DAT)
# The next dataset we will look at is the program effort dataset by Mauldin and Berelson, which can be downloaded from German Rodriguez's site. We will specficially look at the `DAT` version of the data, since it presents several challenges: we do not want to automatically make an index column from the first column in the file and the delimiters are not consistent.  
# 
# To import the data, we will dictate the column names (hence `header = 0`), set the source URL as a string, and state there is no index column in the dataset.

# In[6]:

col_names = ['Country', 'Setting', 'Effort', 'Change']
effort_url = 'http://data.princeton.edu/wws509/datasets/effort.dat'
effort_data = pd.read_table(effort_url, index_col = False, header = 0, names = col_names)
effort_data.head()


# Well, that was interesting. Seems we cannot read in the data with the tab delimiter. We have multiple spaces present in the file (`CParserError: Too many columns specified: expected 4 and found 1`), so let's use Python syntax for multiple/variable whitespace and see what happens.

# In[7]:

effort_data = pd.read_table(effort_url, index_col = False, header = 0, names = col_names, sep = '\s+')
effort_data.head()


# ##Excel
# A lot of data will be in Excel format...please do not do this. While convenient and many programs can read it, Excel does a lot of weird things under the hood you may not be familiar with. Not to mention formatting issues and how certain values may have been calculated - formula references may not necessarily propagate. And there is the issue of dates - the origin of the calendar differs between platforms and this must be accounted for. If you have data originally in Excel format, I suggest (implore) you to just have the raw data and if you have any calculated columns, try doing those in another program (it will probably be more readily reporducible anyway). In other words take your raw data, export to a different file format (CSV, TSV, TXT) and then perform any data manipulations.  
# 
# As an example, let's parse a file Hadley Wickham uses as a part of the `readxl` R package (foreshadowing!).

# In[8]:

example_xlsx = '/Users/julian/GitHub/reproducible-research/Day-2/datasets/datasets.xlsx'
iris_data = pd.read_excel(example_xlsx, 'iris', index_col = None)
mtcars_data = pd.read_excel(example_xlsx, 'mtcars', index_col = None)
chick_weight_data = pd.read_excel(example_xlsx, 'chickwts', index_col = None)
quake_data = pd.read_excel(example_xlsx, 'quakes', index_col = None)


# In[9]:

iris_data.head()


# In[10]:

mtcars_data.head()


# In[11]:

chick_weight_data.head()


# In[12]:

quake_data.head()


# ## XML and JSON
# XML and JSON files can be tricky to work with, as you will need to know their structure. The NY MTA makes data avaialable in both XML and CSV format; the CSV file is (obviously) easier to work with. If you are working with data from the web, it may be in XML format, where the hierarchical structure makes it ideal for representing nested relationships. Web data may also be in JSON format and may require you to (1) know the structure or (2) have it be arranged in a sensible manner for `pandas` or some other module to read (e.g., the USDA dataset). In any event, reading in data contained in XML or JSON format will be highly context-dependent.  
# 
# If you really need an example of one of these, we can work through it.

# ##DataFrame methods
# There are several methods to access and summarize data for a `DataFrame`. We will cover the basics; if you are interested in more advanced features, such as hierarchical indexing, either check the documentation or ask. Also, Wes McKinney's book goes into much more detail about the features.  
# 
# Topics covered:
# - creating a `DataFrame`
# - indexing
# - selecting and filtering data
# - mapping values and functions
# - missing data
# - summaries and basic statistical descriptions
# - plotting
# - grouping data
# 
# These topics, some of which have been touched on indirectly in the previous examples, will all be tied together and be used for the today's ultimate assignment, analyzing data from the Federal Election Commission.

# ### Creating a `DataFrame` and indexing
# There are several ways to create a `DataFrame`: 
# 1. 2-D data matrix  
# 2. Dict of array, list, or tuple  
# 3. Dict of  pandas Series  
# 4. Dict of dicts  
# 5. List of a dict or Series  
# 6. List of lists or tuples  
# 7. `DataFrame` itself
# 8. NumPy structured or record array
# 9. NumPy MaskedArray  
# 
# Let's go through some of these (since time is limited - you can try buildng the others on your own) and see what the resulting `DataFrame` for each example looks like.

# In[13]:

import numpy as np
np.random.seed(86519883)
test_array = np.random.normal(size = (10, 3))
test_cols = ['first', 'second', 'third']
test_df1 = pd.DataFrame(test_array, columns = test_cols)
test_df1


# The above cell does the following: takes a 2-D array (using `NumPy`), a list containing the column names and then uses them as arguments to create a new `DataFrame` with the desired data and headings.

# In[14]:

test_dict = {'int_column': np.random.random_integers(low = 0, high = 255, size = (5)),
            'binom_column': np.random.binomial(n = 1, p = 0.56, size = (5)),
            'char_col': ['sample1', 'sample2', 'sample3', 'sample4', 'sample5']}
test_df2 = pd.DataFrame(test_dict)
test_df2


# The previous cell used a `dict` to create the `DataFrame`. The keys became the column headings, and the rows are the values. Notice that the columns are sorted in order when the `DataFrame` was created.

# In[15]:

test_col1 = np.random.lognormal(mean = 2.7, sigma = 0.2, size = (30))
test_col2 = np.random.normal(loc = -1.6, scale = 2.8, size = (30))
test_col3 = np.random.uniform(low = 55, high = 2000, size = (30))
test_df3 = pd.DataFrame()

test_df3['one'] = test_col1
test_df3['2'] = test_col2
test_df3['third'] = test_col3
test_df3.head()


# And you can create a new `DataFrame` (or append to an existing one) from arrays and append new ones as well.

# How do we access the data? We use the indices of the `DataFrame` (the leftmost column). The `Index` can either be numeric or text. Indexes are immutable, but they can be set or reset. We can also access the columns in the same way we would access the elements of a `list` or `dict` or via attribute.
# 

# In[16]:

test_df1['first']


# In[17]:

test_df2.char_col


# In[18]:

test_df3.ix[:15, :]


# In[19]:

test_df3.ix[11, ['one', '2']]


# Let's say we do not want integers as our indices, but instead characters. Using the Census data, let's make the state or region the index values.

# In[20]:

density_data_2010.set_index(density_data_2010.STATE_OR_REGION, inplace = True, drop = True)
density_data_2010.head()


# Now instead of iterating over integers, we can iterate over the characters.

# In[21]:

pop_dict = {}
for state in density_data_2010.STATE_OR_REGION:
    pop_dict[state] = density_data_2010.loc[state, '2010_POPULATION']

for k in pop_dict:
    print k, pop_dict[k]


# In[22]:

for state in density_data_2010.STATE_OR_REGION:
    print state, density_data_2010.loc[state, '1930_POPULATION']


# We can also drop data easily:

# In[23]:

density_data_2010 = density_data_2010.drop('United States', axis = 0)


# In[24]:

density_data_2010.head()


# In[25]:

test_df3 = test_df3.drop('one', axis = 1)


# In[26]:

test_df3.head()


# In[27]:

test_df2 = test_df2.drop([2, 4])


# In[28]:

test_df2.head()


# ###Converting between 'long' and 'wide' format
# 
# Occasionally, you will have to convert between having repeated measures in separate columns ('wide' format) versus being in separate rows ('long' format). SAS has a command to do this and Hadley Wickham has authored several packages that can perform this operation. SPSS and JMP cannot, but fortunately you have Python or R if you need to do this. Excel can also perform the same sort of function as a pivot table (but once again, please no Excel except for setting up your data).  
# 
# Let's convert a `DataFrame` from long to wide and vice-versa.

# In[29]:

id_col = ['index_1', 'index_1', 'index_1', 'index_2', 'index_2', 'index_2']
sample_col = ['sample_1', 'sample_2', 'sample_3', 'sample_1', 'sample_2', 'sample_3']

test_df4 = pd.DataFrame(columns = ['one', 'two', 'three'])
test_df4['one'] = id_col
test_df4['two'] = sample_col
test_df4['three'] = np.random.uniform(low = 5, high = 1000, size = 6)

test_df4


# In[30]:

test_df4.pivot(index = 'one',columns = 'two',values = 'three')


# So `pandas` will create a new `DataFrame` with a MultiIndex when pivoting. However, if we run an analysis that requires wide format (almost never done in R; R takes ling format data *almost* exclusively) I would recommened R and either the `dplyr` or `reshape2` package in order to do it.

# ### Mapping values and functions
# You will likely have to create numeric, character, or composite labels for your data at some point. Mapping values is easy using the `map` function. Going back to the Census data, we will map the state or region name to its two-letter abbreviation and its geographic region. We will use several `dicts` to accomplish this.

# In[31]:

state_abbrevs = {'Connecticut':'CT' , 'Maine':'ME', 'Massachusetts':'MA',
                   'New Hampshire':'NH', 'Rhode Island':'RI' , 'Vermont':'VT',
                  'New Jersey':'NJ' , 'New York':'NY' , 'Pennsylvania':'PA',
                  'Illinois':'IL', 'Indiana':'IN', 'Michigan':'MI', 'Ohio':'OH',
                  'Wisconsin':'WI', 'Iowa':'IA', 'Kansas':'KS', 'Minnesota':'MN',
                  'Nebraska':'NE', 'North Dakota':'ND', 'South Dakota':'SD', 'Missouri':'MO',
                  'Delaware':'DE', 'Florida':'FL', 'Georgia':'GA', 'Maryland':'MD', 
                  'North Carolina':'NC', 'South Carolina':'SC','Virginia':'VA',
                  'West Virginia':'WV', 'Alabama':'AL','Kentucky':'KY', 'Mississippi':'MS', 
                  'Tennessee':'TN', 'Arkansas':'AR', 'Louisiana':'LA', 'Oklahoma':'OK', 
                  'Texas':'TX', 'Arizona':'AZ', 'Colorado':'CO', 'Idaho':'ID', 'Montana':'MT', 
                  'Nevada':'NV','New Mexico':'NM', 'Utah':'UT', 'Wyoming':'WY', 'Alaska':'AK',
                  'California':'CA', 'Hawaii':'HI', 'Oregon':'OR', 'Washington':'WA'}
                  

census_regions = {'CT': 'Northeast', 'ME': 'Northeast', 'MA': 'Northeast',
                  'NH': 'Northeast', 'RI': 'Northeast', 'VT': 'Northeast',
                  'NJ': 'Northeast', 'NY': 'Northeast', 'PA': 'Northeast',
                  'IL':'Midwest', 'IN':'Midwest', 'MI':'Midwest', 'OH':'Midwest',
                  'WI':'Midwest', 'IA':'Midwest', 'KS':'Midwest', 'MN':'Midwest',
                  'NE':'Midwest', 'ND':'Midwest', 'SD':'Midwest', 'MO':'Midwest',
                  'DE':'South', 'FL':'South', 'GA':'South', 'MD':'South', 
                  'NC':'South', 'SC':'South', 'VA':'South', 'DC':'South',
                  'WV':'South', 'AL':'South', 'KY':'South', 'MS':'South', 
                  'TN':'South', 'AR':'South', 'LA':'South', 'OK':'South', 
                  'TX':'South','AZ':'West', 'CO':'West', 'ID':'West', 'MT':'West',
                  'NV':'West', 'NM':'West', 'UT':'West', 'WY':'West', 'AK':'West',
                  'CA':'West','HI':'West', 'OR':'West', 'WA':'West'}


# In[32]:

density_data_2010['Abbrev'] = density_data_2010.STATE_OR_REGION.map(state_abbrevs)
density_data_2010['Region'] = density_data_2010.Abbrev.map(census_regions)
density_data_2010.head()


# The next thing we want to do is collect summaries, such as the total population in each year (which we deleted earlier), the mean and median state population in each year, and the mean and median population for each state across each census. Fortunately for us, we can apply functions directly to our `DataFrame` to get the desired values.

# In[33]:

pop_cols = ['1910_POPULATION', '1920_POPULATION', '1930_POPULATION', '1940_POPULATION', '1950_POPULATION',
           '1960_POPULATION', '1970_POPULATION', '1980_POPULATION', '1990_POPULATION', '2000_POPULATION',
           '2010_POPULATION']

density_data_2010['MeanPop'] = density_data_2010[pop_cols].mean(axis = 1)
density_data_2010['MedianPop'] = density_data_2010[pop_cols].median(axis = 1)
density_data_2010.head()


# In[34]:

year_totals = density_data_2010[pop_cols].sum(axis = 0)
year_totals


# Notice something interesting here: the columns become the indices for another `pandas` data type, a `Series`.

# In[35]:

type(year_totals)


# In[36]:

year_totals.index.values.tolist()


# We can convert this to something perhaps more useful, such as a `NumPy` array:

# In[37]:

year_totals_np = np.array(year_totals)
type(year_totals_np)


# In[38]:

year_totals_np


# ###Missing data
# Astute observers will notice that I kind of misled you on the mapping of regions and mean and median populations: Puerto Rico and the District of Columbia were not included for the mapping of regions, but were for the population stats. How do we know which entries are missing? `pandas` has methods to do that.  
# 
# - `dropna`: drop missing data for a given axis label; can adjust how many entries are null are tolerated  
# - `fillna`: fill in missing values with a given value  
# - `isnull`: return Boolean (`True` or `False`) indicating which values are missing  
# - `notnull`: negates `isnull`  
# 
# Since real data will likely contain missing values, these methods are very useful. You may desire to fill in missing values with the series mean or median, but for statistical analysis, this is generally frowned upon. And by frowned upon, I mean you will be told to re-analyze your data by a reviewer.

# In[39]:

density_data_2010.MeanPop.isnull()


# In[40]:

density_data_2010.Abbrev.notnull()


# In[41]:

density_data_2010.Region.isnull()


# Let's say we want to drop all rows with missing values:

# In[42]:

print 'Dimensions of population DataFrame: %d rows, %d columns' %   (density_data_2010.shape[0], density_data_2010.shape[1])


# In[43]:

density_data_2010_na_removed = density_data_2010.dropna()
print 'Dimensions of population DataFrame with NA removed: %d rows, %d columns' % (density_data_2010_na_removed.shape[0], density_data_2010_na_removed.shape[1])


# ###Describing and summarizing data
# So now we are familiar with some common operations of `DataFrame`s we will likely encounter. However, we want a general overview of the data itself, in addition to getting basic statistics (first four moments, quantiles, etc.). To get an overview of the `DataFrame` itself, let's first use the `describe` function.

# In[44]:

density_data_2010.describe()


# You will notice that for the columns with numeric data, it gives basic summary satistics: number of entries, mean, standard deviation, and the Tukey five-number summary (min, 1Q, median, 3Q, max; NOTE: this may be computed differently depending on the program). What about for non-numeric data?

# In[45]:

density_data_2010[['Abbrev', 'Region']].describe()


# And other methods can be called:

# In[46]:

print 'State with greatest population in 1980: ', density_data_2010['1980_POPULATION'].idxmax()
print 'State with smallest population in 1940: ', density_data_2010['1940_POPULATION'].idxmin()


# In[47]:

print 'Variance of the 1980 population: ', density_data_2010['1980_POPULATION'].var()


# In[48]:

print 'Skew of the 1980 population: ', density_data_2010['1980_POPULATION'].skew()


# ## Grouping and plotting data
# Tables are all well and good, but insight and finding patterns really only becomes useful with visualization. We will cover the following types of plots:
# - scatter plots  
# - line plots  
# - bar plots  
# - histograms/density estimates  
#   
# In addition, you will likely have to group your data by some variable. We accomplish this using the `groupby` function/method.

# ### Basic scatter and line plots
# For our first example, we will create a dataset, then plot the various relationships.

# In[49]:

col1 = np.random.lognormal(mean = 4.5, sigma = 0.08, size = (200))
col2 = np.random.normal(loc = 2.3, scale = 0.57, size = (200))
col3 = np.random.uniform(low = 0, high = 2000, size = (200))
col4 = np.random.geometric(p = 0.34, size = (200))
col5 = np.linspace(1, 200, 200)
plot_df = pd.DataFrame()

plot_df['col1'] = col1
plot_df['col2'] = col2
plot_df['col3'] = col3
plot_df['col4'] = col4
plot_df['col5'] = col5
plot_df.head()


# In[50]:

get_ipython().magic(u'matplotlib inline')
#allows for the plots to displayed right in the notebook
import matplotlib.pyplot as plt


# In[51]:

fig = plt.figure()

plt.plot(plot_df.col5, plot_df.col1, 'k-', linewidth = 1.5)
plt.title('Column 1 vs. Column5')
plt.xlabel('Column 5')
plt.ylabel('Column 1')


# In[52]:

fig = plt.figure()

plt.scatter(plot_df.col2, plot_df.col3, color = '#af8dc3', alpha = 0.8, s = 60)
plt.title('Column 2 vs. Column 3')
plt.xlabel('Column 3')
plt.ylabel('Column 2')


# So what did we do? We specified the x and y values we wanted plotted, specified colors and line styles, and some additional things, such as transparencies and labels. Let's take it a step further and specify things like legends on a plot with multiple traces.

# In[53]:

fig = plt.figure(figsize = (11, 8))
ax1 = fig.add_subplot(2, 2, 1)
ax2 = fig.add_subplot(2, 2, 2)
ax3 = fig.add_subplot(2, 2, 3)
ax4 = fig.add_subplot(2, 2, 4)

ax1.plot(plot_df.col5, plot_df.col1, color = '#000000', linestyle = '-', label = '1 vs. 5', linewidth = 1.3)
ax1.legend(loc = 'best')

ax2.scatter(plot_df.col5, plot_df.col2, color = '#999999', label = '2 vs. 5', s = 60)
ax2.legend(loc = 'best')

ax3.plot(plot_df.col5, plot_df.col3, color = '#56B4E9', linestyle = '--', label = '3 vs. 5', linewidth = 1.3)
ax3.legend(loc = 'best')

ax4.plot(plot_df.col5, plot_df.col4, color = '#009E73', linestyle = '-.', label = '4 vs. 5', linewidth = 1.3)
ax4.legend(loc = 'best')


# So in the above, we plotted columns against one another, specified color as a hex string, ad created labels and legends. For multivariate data such as this, you can also make a pairs plot (see the `Seaborn` documentation); due to time this will not be covered but examine the documentation or ask.

# We call also call the `DataFrame` directly:

# In[54]:

plot_df.plot(kind = 'scatter', x = 'col5', y = 'col2', color = '#999999', label = '2 vs. 5', s = 60)


# Next, let's look at various counts and distributions. We will randomly assign labels in a new column; this will also be a good introduction to discretization and grouping.

# In[55]:

np.random.seed(484390)

random_nums = np.random.rand(plot_df.shape[0])

#create categorical variables
high = random_nums > 0.85
middling = (random_nums <= 0.85) & (random_nums > 0.5)
just_ugh = random_nums <= 0.5

# assign values to rows and columns
plot_df['Category'] = pd.Series()
plot_df.loc[high, 'Category'] = 'high'
plot_df.loc[middling, 'Category'] = 'middling'
plot_df.loc[just_ugh, 'Category'] = 'terrible'
plot_df.set_index(plot_df.Category, inplace = True, drop = False)
plot_df.head()


# In[56]:

plot_df.Category.describe()


# Let's first look at how our data are distributed:

# In[57]:

fig = plt.figure(figsize = (16, 8))
ax1 = fig.add_subplot(2, 2, 1)
ax2 = fig.add_subplot(2, 2, 2)
ax3 = fig.add_subplot(2, 2, 3)
ax4 = fig.add_subplot(2, 2, 4)

ax1.hist(plot_df.col1, color = '#000000', label = 'Column 1, 30 bins', bins = 30)
ax1.legend(loc = 'best')

ax2.hist(plot_df.col2, color = '#999999', label = 'Column 2, default bin selection')
ax2.legend(loc = 'best')

ax3.hist(plot_df.col3, color = '#56B4E9', label = 'Column 3, 15 bins', bins = 15, alpha = 0.8)
ax3.legend(loc = 'best')

ax4.hist(plot_df.col4, color = '#009E73', label = 'Column 4, 10 bins', bins = 10, alpha = 0.3)
ax4.legend(loc = 'best')


# Yours truly does not like using histograms since bin selection can give the wrong impression (there are rules of thumb, however). Let's try kernel density estimates instead.

# In[58]:

fig = plt.figure(figsize = (16, 8))

plt.subplot2grid((2, 2), (0, 0))
plot_df.col1.plot(kind = 'kde', color = '#000000')
plt.title('Column 1')

plt.subplot2grid((2, 2), (0, 1))
plot_df.col2.plot(kind = 'kde', color = '#999999')
plt.title('Column 2')

plt.subplot2grid((2, 2), (1, 0))
plot_df.col3.plot(kind = 'kde', color = '#56B4E9')
plt.title('Column 3')

plt.subplot2grid((2, 2), (1, 1))
plot_df.col4.plot(kind = 'kde', color = '#009E73')
plt.title('Column 4')


# Let's now look at binning the columns:

# In[59]:

col3_bins = np.arange(start = 0, stop = 2220, step = 440)
col3_labels = ['one', 'two', 'three', 'four', 'five']
plot_df['col3_cut'] =   pd.cut(plot_df.loc[:, 'col3'], right = True, include_lowest = True,          bins = col3_bins, labels = np.array(col3_labels))

plot_df.head()


# Now let's group by our new binned column and `Category`; we want to see size in each bucket.

# In[60]:

plot_df_grouping = plot_df.groupby(['col3_cut', 'Category']).size().unstack(0)
plot_df_grouping


# And now, let's plot this:

# In[61]:

from matplotlib import rcParams
rcParams['figure.figsize'] = (16, 8)
fig = plt.figure()
plot_df_grouping.plot(kind = 'bar', stacked = False, title = 'Discretization bar plot')


# ## Meta-example: 2012 FEC Presidential Election donation data
# The last example will tie in together the concepts just learned, in addition to introducing new ones. This will also be the basis of the first exercise to work on. Some of this cannot be completed until after your look at some of the Hour 2 info, but what has been covered so should get you started.  
# 
# The FEC dataset is very large: 5,349,937 rows and 18 columns. Thus, it may tax your system reading it into memory. To lessen the memory load, `pandas` has a method to read in chunks that results in a `DataFrame`. Also, you may want to combine datasets, such as population information from the 2010 US Census (there are several files). For that, we will introduce merge operations. Lastly, you will have to deal with dates and times.  
# 
# The ultimate goal of this exercise is to get you to produce figures and analyses similar to those in the assignments. You should also play around with 'prettifying' the figures, something will be covered more in Hour 2 and on Day 3. If you do not want to work on the FEC dataset, please try one of the others and see what analyses and visualizations you can come up with. Basically, we will follow the examples in Wes McKinney's book and expand on it; I found this was really useful in learning `pandas`. We will also revisit this dataset along with the Census data on Day 3.  
# 
# Suggested steps towards maximizing information (some will be redundant):
# - import FEC data  
# - import 2010 US Census data  
# - map values such as candidate parties, geographic regions, state names, electoral college votes  
# - index data by state  
# - create `dict`s to map demographic information  
# - convert dates  
# - reduce to final two candidates  
# - separate donations and expenditures
# - summarize amounts  
# - write to a delimited file of your choice

# ###Reading in chunks
# In order to import in chunks, you must do the following:
# - create an iterator when opening file  
# - create an empty `DataFrame`  
# - iterate over the chunks

# In[62]:

# doing this locally since I already have the dataset
# pandas can also take a zip file and unip it to read it in;
# I have not tried this with chunking or extremely large files

fec_data_head = pd.read_csv('/Users/julian/Documents/R_info/P00000001-ALL.csv', index_col = False, nrows = 10)
fec_data_cols = fec_data_head.columns.values.tolist()

# selected a chunk size of 100000; you can make bigger or smaller depending on amount of free memory
# smaller chunks may take longer, but will also not cause any errors/crashes/melt everything inside
fec_chunker = pd.read_csv('/Users/julian/Documents/R_info/P00000001-ALL.csv', index_col = False, 
                          low_memory = False, chunksize = 100000)

fec_data = pd.DataFrame()

for piece in fec_chunker:
    fec_data = fec_data.append(piece)
fec_data.head()


# In[63]:

fec_data.shape


# ###Merging with other datasets
# Use the `pd.merge` function to merge on indices or columns. Database style merges are very useful and these are the types you will encounter (`pd.merge(left, right, how)`):  
# left: match rows from right to left (i.e., keys in left)  
# right: match rows from left to right (i.e., keys in right)  
# inner: keep rows in both  
# outer: keep all values for all rows, i.e., intersection of keys

# In[64]:

df1 = pd.DataFrame({'x1': ['alpha', 'beta', 'gamma', 'delta'], 'x2': [1, 2, 3, 4]})
df2 = pd.DataFrame({'x3': [False, False, True, False], 'x1': ['alpha', 'beta', 'omicron', 'gamma']})


# In[65]:

df1


# In[66]:

df2


# In[67]:

pd.merge(df1, df2, how = 'left')


# In[68]:

pd.merge(df1, df2, how = 'right')


# In[69]:

pd.merge(df1, df2, how = 'inner')


# In[70]:

pd.merge(df1, df2, how = 'outer')


# In[71]:

pd.merge(df1, df2, on = 'x1')


# ### Converting dates and times
# Use the `pd.datetime` method on the desired column; remember to specify the data format. You may also want to cut off the hours, minutes and seconds from the time; this may be an issue depending on what function(s) you use to import the data into another program.

# In[72]:

date1 = '01-Jun-11'
print(date1)
print 'Time converted to ISO format: ', pd.to_datetime(date1, format = '%d-%b-%y')


# ###Exporting to text
# Use the `DataFrame.to_format` method to output a file:, e.g.,  
# `fec_data_summarized.to_csv(path/to/file/destination.csv)`  where `path/to/file/destination.csv` is a string.
# 
# You will also likely want to make an R-style `data.frame` if you want to do something like time series analysis. To that, use a command such as:  
# 
# `fec_net_money_state = fec_final.groupby(state_data_columns, as_index = False)[['contb_receipt_amt']].sum()`  
# and then export as normal.

# #Assignment
# 
# For practice, try to import the FEC dataset, and map values for each state from different data sources. There are plots in the datasets folder than give an idea of some things that you can do.  
# 
# Possible pipeline:  
# - import 2012 FEC Presidential data  
# - append/map the popular vote totals  
# - append/map the following census data:  
#     - state population data  
#     - elderly population data  
#     - family/househould structure data  
# - append/map parties of the major two candidates  
# - append/map geographic regions (as seen above)  
# - append/map full state names  
# - append/map Electoral College votes for each state  
# 
# For a final summary, try the following:  
# - restrict to 50 state + DC (hint: create a `dict` where the state abbreviations are the keys and use the `isin` function to restrict the data)  
# - restrict the data to the final two candidates  
# - have three separate datasets: all data, donations, expenditures  
# 
# 
# If you do the above, the data restricted to just the 50 states + DC for the Romney and Obama campaigns when written to a CSV file should be about **2 GB**.

# ##References

# McKinney, Wes. *Python for Data Analysis*. Should be able to access through Penn Libraries.  
# Markham, Justin. [Introduction to Linear Regression](http://nbviewer.ipython.org/github/justmarkham/DAT4/blob/master/notebooks/08_linear_regression.ipynb). Used as an example to create categorical values for a variable.

# In[73]:

import IPython
import sys


# In[74]:

print 'Python version: ', sys.version
print 'Platform: ', sys.platform
print 'IPython version: ', IPython.__version__
print 'NumPy version: ', np.__version__
print 'Pandas version: ', pd.__version__

