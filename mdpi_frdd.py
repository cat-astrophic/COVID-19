# This script runs the RDD models for a paper on the impact of COVID-19 on academic publishing

# Importing required modules

import pandas as pd
import datetime
import numpy as np
import statsmodels.api as stats
from matplotlib import pyplot as plt
from ToTeX import restab

# Read in the data

papers = pd.read_csv('C:/Users/User/Documents/Data/COVID-19/MDPI_data.csv')

# Control for COVID-19 related papers

# Helper function

def covid(papers, row):
    
    string = str(papers.Title[row]) + str(papers.Abstract[row]) + str(papers.Keywords[row])
    
    if 'covid' in string.lower():
        
        return 1
    
    else:
        
        return 0
    
# Creating the list

c19 = [covid(papers, row) for row in range(len(papers))]

# Adding COVID data to data set

c19 = pd.Series(c19, name = 'COVID')
papers = pd.concat([papers, c19], axis = 1)

# Create a list of journals which will be included in the study - those with pubs in both 2020 and pre-2020

journals = []

for journal in papers.Journal.unique():
    
    j = papers[papers.Journal == journal].reset_index()
    
    if datetime.datetime.strptime(min(j.Accepted), '%Y-%m-%d') < datetime.datetime.strptime('2020-01-01', '%Y-%m-%d') and datetime.datetime.strptime(max(j.Accepted), '%Y-%m-%d') > datetime.datetime.strptime('2020-01-01', '%Y-%m-%d'):
        
        journals.append(j.Journal[0])

# Subset data based on journals

df = papers[papers.Journal.isin(journals)].reset_index()

# how much time around cutoff and should it be symmetric in time?
# need to remove papers from journals that did not have publications prior to COVID
# this could be done by only considering journals that published papers in 2019


# Data visualization
d0 = datetime.datetime.strptime('2018-12-31', '%Y-%m-%d')
days = [d0 + datetime.timedelta(days = d) for d in range(548)]
check = [1 if datetime.datetime.strptime(x, '%Y-%m-%d') > d0 else 0 for x in df.Submitted]
ddf = pd.concat([df, pd.Series(check, name = 'check')], axis = 1)
ddf = ddf[ddf.check == 1].reset_index()
com = []
for d in days:
    count = 0
    s = 0
    for c in range(len(ddf.Submitted)):
        if datetime.datetime.strptime(str(ddf.Submitted[c]), '%Y-%m-%d') == d:
            count += 1
            s += ddf.Total[c]
    if count > 0:
        val = s/count
        com.append(val)
    else:
        com.append(0)
plt.plot(com) # includes covid papers
ddf = ddf[ddf.COVID == 0].reset_index(drop=True)
com2 = []
for d in days:
    count = 0
    s = 0
    for c in range(len(ddf.Submitted)):
        if datetime.datetime.strptime(str(ddf.Submitted[c]), '%Y-%m-%d') == d:
            count += 1
            s += ddf.Total[c]
    if count > 0:
        val = s/count
        com2.append(val)
    else:
        com2.append(0)
plt.plot(com2) # covid papers removed


plt.figure(figsize = (8,5))
plt.plot(com, color = 'black')
plt.plot(com2, color = 'red')



# find visual evidence justifying FRDD
# create plots to include in the paper - mean(papers.Total) conditional on papers.Submitted == day
# subset data by journals
# subset data by dates (around the cut-off)
# subset data for each set of models (Xs, Ys)
# run models
# create output tex tables





