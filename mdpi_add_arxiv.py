# This script adds arxiv submissions data to the mdpi data set as an additional control

# Importing required modules

import pandas as pd
import datetime

# Reading in the data

print('Reading in the data.......')

papers = pd.read_csv('C:/Users/User/Documents/Data/COVID-19/MDPI_papers_with_FM.csv')
arxiv_raw =  pd.read_csv('C:/Users/User/Documents/Data/COVID-19/updated_dates.txt', header = None)
arxiv_new_raw =  pd.read_csv('C:/Users/User/Documents/Data/COVID-19/submission_dates.txt', header = None)

# Convert arxiv data to lists

print('Converting raw arxiv data to datetime.......')

arxiv_raw = arxiv_raw[0].to_list()
arxiv_new_raw = arxiv_new_raw[0].to_list()

# Convert list data into datetime format

arxiv = [datetime.datetime.strptime(x, '%Y-%m-%d') for x in arxiv_raw]
arxiv_new = [datetime.datetime.strptime(x, '%Y-%m-%d') for x in arxiv_new_raw]

# Counting the number of arxiv submissions in week prior to each date

d0 = datetime.datetime.strptime('2019-01-01', '%Y-%m-%d')
days = [d0 + datetime.timedelta(days = d) for d in range(731)]
counts7 = []
counts14 = []
counts30 = []
counts_new7 = []
counts_new14 = []
counts_new30 = []

# Creating primary data

print('Creating total arxiv volume data.......')

for day in days:
    
    print(day) # for watching progress
    c7 = 0
    c14 = 0
    c30 = 0
    
    for a in arxiv:
        
        val = day - a
        
        if val.days > -1 and val.days < 7:
            
            c7 += 1
            c14 += 1
            c30 += 1
            
        elif val.days > -1 and val.days < 14:
            
            c14 += 1
            c30 += 1
            
        elif val.days > -1 and val.days < 30:
            
            c30 += 1
        
    counts7.append(c7)
    counts14.append(c14)
    counts30.append(c30)

# Creating data for robustness checks

print('Creating new submissions arxiv volume data.......')

for day in days:
    
    print(day) # for watching progress
    c7 = 0
    c14 = 0
    c30 = 0
    
    for a in arxiv_new:
        
        val = day - a
        
        if val.days > -1 and val.days < 7:
            
            c7 += 1
            c14 += 1
            c30 += 1
            
        elif val.days > -1 and val.days < 14:
            
            c14 += 1
            c30 += 1
            
        elif val.days > -1 and val.days < 30:
            
            c30 += 1
        
    counts_new7.append(c7)
    counts_new14.append(c14)
    counts_new30.append(c30)

# Create final arxiv submission count data (and final count data for robustness checks)

print('Finding the arxiv data for each paper.......')

arxiv7 = [counts7[days.index(datetime.datetime.strptime(papers.Submitted[row], '%Y-%m-%d'))] if datetime.datetime.strptime(papers.Submitted[row], '%Y-%m-%d') >= d0 else '' for row in range(len(papers))]
arxiv14 = [counts14[days.index(datetime.datetime.strptime(papers.Submitted[row], '%Y-%m-%d'))] if datetime.datetime.strptime(papers.Submitted[row], '%Y-%m-%d') >= d0 else '' for row in range(len(papers))]
arxiv30 = [counts30[days.index(datetime.datetime.strptime(papers.Submitted[row], '%Y-%m-%d'))] if datetime.datetime.strptime(papers.Submitted[row], '%Y-%m-%d') >= d0 else '' for row in range(len(papers))]
new7 = [counts_new7[days.index(datetime.datetime.strptime(papers.Submitted[row], '%Y-%m-%d'))] if datetime.datetime.strptime(papers.Submitted[row], '%Y-%m-%d') >= d0 else '' for row in range(len(papers))]
new14 = [counts_new14[days.index(datetime.datetime.strptime(papers.Submitted[row], '%Y-%m-%d'))] if datetime.datetime.strptime(papers.Submitted[row], '%Y-%m-%d') >= d0 else '' for row in range(len(papers))]
new30 = [counts_new30[days.index(datetime.datetime.strptime(papers.Submitted[row], '%Y-%m-%d'))] if datetime.datetime.strptime(papers.Submitted[row], '%Y-%m-%d') >= d0 else '' for row in range(len(papers))]

# Appending arxiv count data to the data set

print('Creating final data set and writing to file.......')

arxiv7 = pd.Series(arxiv7, name = 'arXiv7')
arxiv14 = pd.Series(arxiv14, name = 'arXiv14')
arxiv30 = pd.Series(arxiv30, name = 'arXiv30')
new7 = pd.Series(new7, name = 'new7')
new14 = pd.Series(new14, name = 'new14')
new30 = pd.Series(new30, name = 'new30')
papers = pd.concat([papers, arxiv7, arxiv14, arxiv30, new7, new14, new30], axis = 1)

# Writing updated data set to file

papers.to_csv('C:/Users/User/Documents/Data/COVID-19/MDPI_data.csv', index = False)

