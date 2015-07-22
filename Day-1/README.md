#Day One overview  
For the first day of the course, we will set up all the needed software. If you took the previous mini-course, you will have most or all of the software needed installed.  

##Needed software
###Python
- Python 2.7.x (2.7.10 is included in the Anaconda release being used)  
- IPython 3.1.0 and above (3.2.0 included in Anaconda release being used)  
- Jupyter/IPython notebook  
- Anaconda (will install IPython, Jupyter/IPython notebook and SciPy stack) 


###R
- R 3.1.3 or higher (scripts have been tested on a R 3.2.1 system install, Mac OS X Yosemite)  
- RStudio 0.99.441 and higher (tested on 0.99.467, Mac OS X Yosemite)  

##Other dependencies
- Pandoc  
- LaTeX  
- GitHub account
- various Python and R packages for data munging and visualization (see [syllabus](https://github.com/IRCS-analysis-mini-courses/reproducible-research/blob/master/SYLLABUS.md) and [references](https://github.com/IRCS-analysis-mini-courses/reproducible-research/blob/master/REFERENCES.md))

# Notes about file sizes and installation
Several of these programs are very large in size and will take a while to download:  
- Anaconda: 882 MB  
- XCode: need acces to App Store to download  
- RStudio: 315 MB  
- MacTex (Mac OS x): 2.5 GB (maybe do this overnight)  
- MikTex (Windows): 158 MB + additional packages (maybe do this overnight)

## Mac OS X
To create PDF and LaTeX output, the install process is more involved (see also the installation notes).  Do the following in order:  
- install Mactex  
- install Pandoc  
- install Macports
- install the following from macports:  
    + `texlive-latex-recommended`  
    + `texlive-latex-extra`  
    + `texlive-fonts-recommended`
If you need assistance installing XCode and XCode command line tools and commands for Macports, we can show you how.

###Suggested
[Julia 0.3.8 and higher](http://julialang.org/) (not needed, but integrates with Jupyter/IPython notebook and is young, but good, language for [numeric analysis and statistics](http://juliastats.github.io/))  
