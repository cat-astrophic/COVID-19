# This script converts raw date-like metadata into a usable datetime format

# Importing required modules

from datetime import datetime
import pandas as pd

# Reading in the raw data

raw_data = pd.read_csv('C:/Users/User/Documents/Data/COVID-19/MDPI_papers_all.csv', encoding = 'utf-8')

submitted = raw_data.Submitted.to_list()
revised = raw_data.Revised.to_list()
accepted = raw_data.Accepted.to_list()
published = raw_data.Published.to_list()
journals = raw_data.Journal.to_list()
affiliations = raw_data.Affiliations.to_list()

del(raw_data) # save RAM

# Creating lists of clean datetime data

submitted_clean = []
revised_clean = []
accepted_clean = []
published_clean = []

for i in range(len(submitted)):
    
    d = datetime.strptime(submitted[i], '%d %B %Y')
    submitted_clean.append(d.strftime('%Y-%m-%d'))
    
    d = datetime.strptime(revised[i], '%d %B %Y')
    revised_clean.append(d.strftime('%Y-%m-%d'))
    
    d = datetime.strptime(accepted[i], '%d %B %Y')
    accepted_clean.append(d.strftime('%Y-%m-%d'))
    
    d = datetime.strptime(published[i], '%d %B %Y')
    published_clean.append(d.strftime('%Y-%m-%d'))

# Computing times between status changes for papers

stage1 = []
stage2 = []
stage3 = []
totals = []
edit = []

for i in range(len(submitted)):
    
    # a measure of time taken by both reviewers + authors
    sub_to_rev = datetime.strptime(revised_clean[i], '%Y-%m-%d') - datetime.strptime(submitted_clean[i], '%Y-%m-%d')
    # a measure of time taken by editors
    rev_to_acc = datetime.strptime(accepted_clean[i], '%Y-%m-%d') - datetime.strptime(revised_clean[i], '%Y-%m-%d')
    # a measure of time taken by editorial staff
    acc_to_pub = datetime.strptime(published_clean[i], '%Y-%m-%d') - datetime.strptime(accepted_clean[i], '%Y-%m-%d')
    # a measure of the total time taken by the publishing process
    total_time = datetime.strptime(published_clean[i], '%Y-%m-%d') - datetime.strptime(submitted_clean[i], '%Y-%m-%d')
    # a measure of the total time taken by the journal to get an ultimately accepted article into press
    ed_time = datetime.strptime(published_clean[i], '%Y-%m-%d') - datetime.strptime(revised_clean[i], '%Y-%m-%d')
    
    stage1.append(sub_to_rev)
    stage2.append(rev_to_acc)
    stage3.append(acc_to_pub)
    totals.append(total_time)
    edit.append(ed_time)

# Converting timedeltas to integer values

stage1 = pd.Series(stage1).dt.days.to_list()
stage2 = pd.Series(stage2).dt.days.to_list()
stage3 = pd.Series(stage3).dt.days.to_list()
totals = pd.Series(totals).dt.days.to_list()
edit = pd.Series(edit).dt.days.to_list()

# Saving to file

MDPI_df = pd.DataFrame({'Stage1': stage1, 'Stage2': stage2, 'Stage3': stage3, 'Total': totals, 'Editor': edit,
                        'Submitted': submitted_clean, 'Revised': revised_clean, 'Accepted': accepted_clean,
                        'Published': published_clean, 'Journal': journals, 'Affiliations': affiliations})

MDPI_df.to_csv('C:/Users/User/Documents/Data/COVID-19/MDPI_papers.csv', index = False, encoding = 'utf-8-sig')

