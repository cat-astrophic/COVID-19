# This script converts raw date-like metadata into a usable datetime format

# Importing required modules

from datetime import datetime
import pandas as pd

# Reading in the raw data

raw_data = pd.read_csv('C:/Users/User/Documents/Data/COVID-19/MDPI_papers_all.csv', encoding = 'utf-8-sig')

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
ref_list = []
ref_lista = []
ref_listb = []

for i in range(len(submitted)):
    
    print('Cleaning datetime data for entry ' + str(i+1) + ' of ' + str(len(submitted)))
    
    try:
        
        d = datetime.strptime(submitted[i], '%d %B %Y')
        submitted_clean.append(d.strftime('%Y-%m-%d'))
        
        d = datetime.strptime(revised[i], '%d %B %Y')
        revised_clean.append(d.strftime('%Y-%m-%d'))
        
        d = datetime.strptime(accepted[i], '%d %B %Y')
        accepted_clean.append(d.strftime('%Y-%m-%d'))
        
        d = datetime.strptime(published[i], '%d %B %Y')
        published_clean.append(d.strftime('%Y-%m-%d'))
        
        ref_lista.append(i)
        
    except:
        
        continue

# Computing times between status changes for papers

stage1 = []
stage2 = []
stage3 = []
totals = []
edit = []

for i in range(len(submitted_clean)):
    
    print('Calculating results for entry ' + str(i+1) + ' of ' + str(len(submitted_clean)))
    
    try:
        
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
        
        stage1.append(sub_to_rev.days)
        stage2.append(rev_to_acc.days)
        stage3.append(acc_to_pub.days)
        totals.append(total_time.days)
        edit.append(ed_time.days)
        
        ref_list.append(i)
        ref_listb.append(ref_lista[i])
    
    except:
        
        continue

# Subsetting journals and affiliations based on what data we successfully cleaned

submitted2 = [submitted_clean[i] for i in ref_list]
revised2 = [revised_clean[i] for i in ref_list]
accepted2 = [accepted_clean[i] for i in ref_list]
published2 = [published_clean[i] for i in ref_list]
journals2 = [journals[i] for i in ref_list]
affiliations2 = [affiliations[i] for i in ref_list]

# Saving to file

MDPI_df = pd.DataFrame({'Stage1': stage1, 'Stage2': stage2, 'Stage3': stage3, 'Total': totals, 'Editor': edit,
                        'Submitted': submitted2, 'Revised': revised2, 'Accepted': accepted2,
                        'Published': published2, 'Journal': journals2, 'Affiliations': affiliations2})

MDPI_df.to_csv('C:/Users/User/Documents/Data/COVID-19/MDPI_papers.csv', index = False, encoding = 'utf-8-sig')

