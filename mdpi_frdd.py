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

# need to remove papers from journals that did not have publications prior to COVID
    # this could be done by only considering journals that published papers in 2019

# Create a list of journals which will be included in the study - those with pubs in both 2020 and pre-2020

journals = []

for journal in papers.Journal.unique():
    
    j = papers[papers.Journal == journal]
    
    if datetime.datetime.strptime(min(j.Submitted), '%Y-%m-%d') < datetime.datetime.strptime('2020-01-01', '%Y-%m-%d') and datetime.datetime.strptime(max(j.Submitted), '%Y-%m-%d') > datetime.datetime.strptime('2020-01-01', '%Y-%m-%d'):
        
        journals.append(j)

# Subset data based on journals

df = papers[papers.Journal.isin(journals)] # SOOOOOOOOOOOOOOOOOO SLOOOOOOOOOOOOOOOOOOOOW.....

# how much time around cutoff and should it be symmetric in time?










# find visual evidence justifying FRDD
# create plots to include in the paper - mean(papers.Total) conditional on papers.Submitted == day
# subset data by journals
# subset data by dates (around the cut-off)
# subset data for each set of models (Xs, Ys)
# run models
# create output tex tables





