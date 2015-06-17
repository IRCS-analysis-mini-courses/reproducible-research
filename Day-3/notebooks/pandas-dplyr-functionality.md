

`pandas` and `dplyr` functionality
========================================================
author: Julian
date: 
width: 1440
height: 900
font-family: 'Helvetica'

`pandas` and `dplyr` functionality
========================================================

On Day 2, we saw how to use the `pandas` Python module to import, summarize and manipulate data in a tabular format. The scripts accompanying the first hour of Day 3 demonstrated how to do the same with base R and the 'Hadleyverse' package `dplyr` . This slide set demonstrates similar functionality with each module/package.  

Since importing data has already been covered, the focus will be on data manipulation. Only new code will be executed, try executing the code contained in the scripts on your own.

Dimensionality in `pandas`
========================================================


```python

import pandas as pd
import numpy as np
density_url = \
'http://www.census.gov/2010census/csv/pop_density.csv'

density_data_2010 = pd.read_csv(density_url, skiprows = [0, 1, 2])

density_data_dimen = density_data_2010.shape
density_data_idx = density_data_2010.index

print 'Data dimensions: %d rows, %d columns' % (density_data_dimen[0], density_data_dimen[1])
print 'First 10 indices of population density DataFrame: ', density_data_idx[:10]

```

Dimensionality in `dplyr`
========================================================


```r
library(readr)
census.url <- 'http://www.census.gov/2010census/csv/pop_density.csv'

census.data.readr <- read_csv(census.url, col_names = TRUE, skip = 3)

density.data.dimen.readr <- dim(census.data.readr)

density.data.cols.readr <- colnames(census.data.readr)

density.data.idx.readr <- row.names(census.data.readr)

sprintf('Data dimensions: %d rows, %d columns',  
        density.data.dimen.readr[1], density.data.dimen.readr[2])

cat('First 10 indices of population density data.frame:',
    row.names(census.data.readr)[seq(1,10,1)])
```
