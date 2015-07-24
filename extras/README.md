# Extras

This folder contains a dataset (and the Python script used to generate it) that can be used to compare functionality between `dplyr` and `pandas` as well as any other concerns and fucntionality that are brought up. The notebooks and scripts for the comparison are also included. Also contains other data notebooks, and code that are requested or solve problems that come up during the course.

## Contents
- comparison of functionality between `dplyr` and `pandas`  
- introduction to `NumPy` (Jupyter/IPython notebook) [Notebook on GitHub](https://github.com/IRCS-analysis-mini-courses/reproducible-research/blob/master/extras/NumPy-basics.ipynb)  || [Notebook on nbviewer](http://nbviewer.ipython.org/github/IRCS-analysis-mini-courses/reproducible-research/blob/master/extras/NumPy-basics.ipynb)  

## Running a Python script in RStudio
You may run a Python script in RStudio in two ways:  
    1. Use the `Run Script` button at the top of the editor window 
    2. From command line: `system("python path/to/script.py")`
        a. if the above does not work (R may look at the system isntall of Python instead of the output of `which python`) do this: `system("path/to/python/beingused Documents/R_info/python-test-run.py")` where `path/to/python/beingused` is the output of `which python`
