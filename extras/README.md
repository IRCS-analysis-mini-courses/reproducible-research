# Extras

This folder contains a dataset (and the Python script used to generate it) that can be used to compare functionality between `dplyr` and `pandas` as well as any other concerns and fucntionality that are brought up. The notebooks and scripts for the comparison are also included. Also contains other data notebooks, and code that are requested or solve problems that come up during the course.

## Contents
- comparison of functionality between `dplyr` and `pandas`  
- introduction to `NumPy` (Jupyter/IPython notebook) [Notebook on GitHub](https://github.com/IRCS-analysis-mini-courses/reproducible-research/blob/master/extras/NumPy-basics.ipynb)  || [Notebook on nbviewer](http://nbviewer.ipython.org/github/IRCS-analysis-mini-courses/reproducible-research/blob/master/extras/NumPy-basics.ipynb)  

## Running a Python script in R or RStudio
You may run a Python script in R or RStudio in two ways:  
    1. Use the `Run Script` button at the top of the editor window in R Studio  
    2. From R console: `system("python path/to/script.py")`  
        - if the above does not work (R may look at the system isntall of Python instead of the output of `which python`)  
        - do this: `system("path/to/python/beingused path/to/script/python-test-run.py")` where `path/to/python/beingused` is the output of `which python`

## Machine learning resources
At least one person mentioned wanting to learn more about machine learning. The topic is briefly mentioned on Day 2, with the limited use of `scikit-learn` to fit a regression. If you would like to learn more, I can suggest the following which I have used previously:  
- Notebook using the Kaggle Titanic machine learning tutorial in Python. This covers importing data, visualization, and modeling using different techniques (logistic regression, SVM, random forest) and visualziation of results. [You can access it here](nbviewer.ipython.org/github/agconti/kaggle-titanic/blob/master/Titanic.ipynb).  
- Markdown document using the Kaggle Titanic machine learning tutorial in R. This demonstrates some visualzations and model techniques that are not normally covered or implemented, but that can be useful. It also demonstrates how to use the `caret` package for machine learning. [You can access it here.](https://github.com/wehrley/wehrley.github.io/blob/master/SOUPTONUTS.md)
