# This script converts raw date-like metadata into a usable datetime format

# Importing required modules

from datetime import datetime
import pandas as pd

# Reading in the raw data

print('Reading in the data.......')

raw_data = pd.read_csv('C:/Users/User/Documents/Data/COVID-19/MDPI_papers_all.csv', encoding = 'utf-8')

submitted = raw_data.Submitted.to_list()
revised = raw_data.Revised.to_list()
accepted = raw_data.Accepted.to_list()
published = raw_data.Published.to_list()
titles = raw_data.Title.to_list()
journals = raw_data.Journal.to_list()
affiliations = raw_data.Affiliations.to_list()
abstracts = raw_data.Abstract.to_list()
keywords = raw_data.Keywords.to_list()
authors = raw_data.Authors.to_list()

del(raw_data) # save RAM

# Creating lists of clean datetime data

print('Cleaning the datetime data.......')

submitted_clean = []
revised_clean = []
accepted_clean = []
published_clean = []
blanks = []

for i in range(len(submitted)):
    
    try:

        d = datetime.strptime(submitted[i], '%d %B %Y')
        submitted_clean.append(d.strftime('%Y-%m-%d'))
        
    except:
        
        submitted_clean.append('')
        blanks.append(i)
        
    try:
        
        d = datetime.strptime(revised[i], '%d %B %Y')
        revised_clean.append(d.strftime('%Y-%m-%d'))
        
    except:
        
        revised_clean.append('')
        blanks.append(i)
        
    try:
        
        d = datetime.strptime(accepted[i], '%d %B %Y')
        accepted_clean.append(d.strftime('%Y-%m-%d'))
        
    except:
        
        accepted_clean.append('')
        blanks.append(i)
        
    try:
        
        d = datetime.strptime(published[i], '%d %B %Y')
        published_clean.append(d.strftime('%Y-%m-%d'))
        
    except:
        
        published_clean.append('')
        blanks.append(i)

# Computing times between status changes for papers

print('Computing the datetime data.......')

stage1 = []
stage2 = []
stage3 = []
totals = []
edit = []

for i in range(len(submitted)):
    
    try: # a measure of time taken by both reviewers + authors
        
        sub_to_rev = datetime.strptime(revised_clean[i], '%Y-%m-%d') - datetime.strptime(submitted_clean[i], '%Y-%m-%d')

    except:
        
        sub_to_rev = ''
        blanks.append(i)

    try: # a measure of time taken by editors
        
        rev_to_acc = datetime.strptime(accepted_clean[i], '%Y-%m-%d') - datetime.strptime(revised_clean[i], '%Y-%m-%d')
        
    except:
        
        rev_to_acc = ''
        blanks.append(i)
        
    try: # a measure of time taken by editorial staff
        
        acc_to_pub = datetime.strptime(published_clean[i], '%Y-%m-%d') - datetime.strptime(accepted_clean[i], '%Y-%m-%d')
        
    except:
        
        acc_to_pub = ''
        blanks.append(i)
        
    try: # a measure of the total time taken by the publishing process
        
        total_time = datetime.strptime(published_clean[i], '%Y-%m-%d') - datetime.strptime(submitted_clean[i], '%Y-%m-%d')
        
    except:
        
        total_time = ''
        blanks.append(i)
        
    try: # a measure of the total time taken by the journal to get an ultimately accepted article into press
        
        ed_time = datetime.strptime(published_clean[i], '%Y-%m-%d') - datetime.strptime(revised_clean[i], '%Y-%m-%d')
    
    except:
        
        ed_time = ''
        blanks.append(i)
        
    stage1.append(sub_to_rev)
    stage2.append(rev_to_acc)
    stage3.append(acc_to_pub)
    totals.append(total_time)
    edit.append(ed_time)

# Removing lines with blank entries in order to use the .dt method

print('Cleaning the remaining data.......')

for i in range(len(stage1)):
    
    if str(stage1[i]) == '0:00:00':
        
        blanks.append(i)
    
    if str(stage2[i]) == '0:00:00':
    
        blanks.append(i)
        
    if str(stage3[i]) == '0:00:00':
        
        blanks.append(i)
        
    if str(totals[i]) == '0:00:00':
        
        blanks.append(i)
        
    if str(edit[i]) == '0:00:00':
        
        blanks.append(i)

blanks = list(sorted(pd.Series(blanks).unique()))[::-1]

for b in blanks:
    
    del(stage1[b])
    del(stage2[b])
    del(stage3[b])
    del(totals[b])
    del(edit[b])
    del(submitted_clean[b])
    del(revised_clean[b])
    del(accepted_clean[b])
    del(published_clean[b])
    del(titles[b])
    del(journals[b])
    del(affiliations[b])
    del(abstracts[b])
    del(keywords[b])
    del(authors[b])

# Converting timedeltas to integer values

print('Coverting datetime data to integer values.......')

stage1 = pd.Series(stage1).dt.days.to_list()
stage2 = pd.Series(stage2).dt.days.to_list()
stage3 = pd.Series(stage3).dt.days.to_list()
totals = pd.Series(totals).dt.days.to_list()
edit = pd.Series(edit).dt.days.to_list()

# Saving to file

print('Creating final dataframe.......')

MDPI_df = pd.DataFrame({'Stage1': stage1, 'Stage2': stage2, 'Stage3': stage3, 'Total': totals, 'Editor': edit,
                        'Submitted': submitted_clean, 'Revised': revised_clean, 'Accepted': accepted_clean,
                        'Published': published_clean, 'Title':titles, 'Journal': journals, 'Affiliations': affiliations,
                        'Abstract': abstracts, 'Keywords':keywords, 'Authors':authors})

print('Saving data to file.......')

MDPI_df.to_csv('C:/Users/User/Documents/Data/COVID-19/MDPI_papers.csv', index = False, encoding = 'utf-8-sig')

