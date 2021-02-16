# This script runs the RDD models for a paper on the impact of COVID-19 on academic publishing

# Importing required modules

import pandas as pd
import datetime
import numpy as np
import statsmodels.api as stats
from matplotlib import pyplot as plt
import gender_guesser.detector as gender
from ToTeX import restab

# Defining a helper function for identifying COVID-19 related papers

def covid(papers, row):
    
    string = str(papers.Title[row]) + str(papers.Abstract[row]) + str(papers.Keywords[row])
    
    if 'covid' in string.lower():
        
        return 1
    
    else:
        
        return 0

# Defining a helper function for isolating the name of the first author

def first_name(auths):
    
    a = auths.index("'")
    
    try:
        
        b = auths[a+1:].index(' ')
        
    except:
        
        b = auths[a+1:].index("'")
    
    return auths[a+1:b+2]

# Defining a helper function for isolating the national affiliation of the first author

def first_nationality(affils):
    
    if str(affils) == 'nan':
        
        affils = ''
        
    else:
        
        try:
            
            a = affils.index("',")
            
        except:
            
            a = len(affils) - 2
            
        c = affils[:a].count(', ')
        
        for j in range(c):
            
            b = affils[:a].index(', ')
            affils = affils[b+2:a]
     
    return affils

# Reading in the data

print('Reading in the data.......')

papers = pd.read_csv('C:/Users/User/Documents/Data/COVID-19/MDPI_data.csv')

# Control for COVID-19 related papers
    
# Creating the list

print('Creating a flag for COVID-19 related papers.......')

c19 = [covid(papers, row) for row in range(len(papers))]

# Adding COVID data to data set

print('Adding COVID-19 flag to the data set.......')

c19 = pd.Series(c19, name = 'COVID')
papers = pd.concat([papers, c19], axis = 1)

# Checking the number of COVID-19 related papers after the time cut-off as an anecdote:
# Note that this stat does not reflect dropping certain papers due to being publishing in unestablished journals

post_study_papers = ['lol' for i in range(len(papers)) if datetime.datetime.strptime(papers.Submitted[i], '%Y-%m-%d') > datetime.datetime.strptime('2020-06-30', '%Y-%m-%d')]
poststudy_covid = ['lol' for i in range(len(papers)) if datetime.datetime.strptime(papers.Submitted[i], '%Y-%m-%d') > datetime.datetime.strptime('2020-06-30', '%Y-%m-%d') and papers.COVID[i] == 1]

# Create a list of journals which will be included in the study - those with pubs prior to 2020

print('Removing papers from journals first published post 2020-01-01.......')

journals = []

for journal in papers.Journal.unique():
    
    j = papers[papers.Journal == journal].reset_index()
    
    if datetime.datetime.strptime(min(j.Accepted), '%Y-%m-%d') < datetime.datetime.strptime('2020-01-01', '%Y-%m-%d') and datetime.datetime.strptime(max(j.Accepted), '%Y-%m-%d') > datetime.datetime.strptime('2019-01-01', '%Y-%m-%d'):
        
        journals.append(j.Journal[0])

# Subset data based on journals

df = papers[papers.Journal.isin(journals)].reset_index(drop = True)

# Subset data based on submission date

print('Removing papers from outside of the study time frame.......')

post1812 = [int(datetime.datetime.strptime(df.Submitted[i], '%Y-%m-%d') > datetime.datetime.strptime('2018-12-31', '%Y-%m-%d')) for i in range(len(df))]
pre2007 = [int(datetime.datetime.strptime(df.Submitted[i], '%Y-%m-%d') < datetime.datetime.strptime('2020-07-01', '%Y-%m-%d')) for i in range(len(df))]
study = pd.Series([post1812[i] * pre2007[i] for i in range(len(post1812))], name = 'Study')
df = pd.concat([df, study], axis = 1)
df = df[df.Study == 1].reset_index(drop = True)

# Computing the number of authors

print('Computing the number of authors for each paper.......')

numb_authors = [df.Authors[i].count(',') + 1 for i in range(len(df))]
numb_authors = pd.Series(numb_authors, name = 'Author_Count')
df = pd.concat([df, numb_authors], axis = 1)

# Predict perceived gender of the first author only

print('Predicting the perceived gender of first authors for each paper.......')

gd = gender.Detector()
first_author_gender = [gd.get_gender(first_name(df.Authors[i])) for i in range(len(df))]
first_author_gender = pd.Series(first_author_gender, name = 'Gender')
df = pd.concat([df, first_author_gender], axis = 1)

# Finding the nationality of the first author

print('Finding the nationality of the first author for each paper.......')

first_nat = [first_nationality(df.Affiliations[i]) for i in range(len(df))]
first_nat = pd.Series(first_nat, name = 'Nationality')
df = pd.concat([df, first_nat], axis = 1)

# Estimating the percentage of male / female authors for each paper

# Defining a helper function for the main function below

def inp_trimmer(inp):
    
    a = inp.index("'") # mimic first_name
    
    try:
        
        b = inp[a+1:].index(' ') # mimic first_name 
        
    except:
        
        b = inp[a+1:].index("'") # mimic first_name 
        
    inp = inp[b+3:] # shorten inp
    
    try:
        
        c = inp.index("',") # find next name or end of inp
        inp = inp[c+3:]
        
    except:
        
        inp = ']'
    
    return inp

# Defining a function to parse names and run them through the existing function for first author names

def all_auths(inp,nu):
    
    if nu % 100 == 0: # Just a visual queue because this isn't particularly fast
        
        print('Working on records ' + str(nu+1) + ' through ' + str(nu+101) + ' of 167,703.......')
    
    gd = gender.Detector()
    listicle = []
    
    while inp != ']':
        
        listicle.append(gd.get_gender(first_name(inp)))
        inp = inp_trimmer(inp)
        
    return listicle
        
# Applying this function to predict the perceived genders of all authors

# This is currently commented out because it takes quite a long time to run and too many authors are categorized as 'unknown'

#all_genders = [all_auths(df.Authors[i].replace('"',"'"),i) for i in range(len(df))]

# Below are lists of countries categorized by the World Bank Analytical Classification quartiles

high = ['Andorra', 'Antigua and Barbuda', 'Aruba', 'Australia', 'Austria', 'The Bahamas', 'Bahrain',
        'Barbados', 'Belgium', 'Bermuda', 'Brunei', 'Canada', 'The Cayman Islands', 'Channel Islands',
        'Croatia', 'Cyprus', 'Czech Republic', 'Denmark', 'Equatorial Guinea', 'Estonia', 'Faeroe Islands',
        'Finland', 'France', 'French Polynesia', 'Germany', 'Greece', 'Greenland', 'Hong Kong', 'Hungary',
        'Iceland', 'Ireland', 'Isle of Man', 'Israel', 'Italy', 'Japan', 'Korea', 'Kuwait', 'Liechtenstein',
        'Luxembourg', 'Macao', 'Malta', 'Monaco', 'The Netherlands', 'New Caledonia', 'New Zealand',
        'Northern Mariana Islands', 'Norway', 'Oman', 'Portugal', 'Qatar', 'San Marino', 'Saudi Arabia',
        'Singapore', 'Slovakia', 'Slovenia', 'Spain', 'Sweden', 'Switzerland', 'Taiwan', 'Trinidad and Tobago',
        'United Arab Emirates', 'UK', 'USA']

upper_mid = ['Algeria', 'American Samoa', 'Argentina', 'Belarus', 'Bosnia and Herzegovina', 'Botswana', 'Brazil',
             'Bulgaria', 'Chile', 'Colombia', 'Costa Rica', 'Cuba', 'Dominica', 'Dominican Republic', 'Fiji',
             'Gabon', 'Grenada', 'Jamaica', 'Kazakhstan', 'Latvia', 'Lebanon', 'Libya', 'Lithuania', 'Macedonia',
             'Malaysia', 'Mauritius', 'Mexico', 'Montenegro', 'Namibia', 'Palau', 'Panama', 'Peru', 'Poland',
             'Romania', 'Russia', 'Serbia', 'Seychelles', 'South Africa', 'Saint Kitts and Nevis', 'Saint Lucia',
             'Saint Vincent and the Grenadines', 'Suriname', 'Turkey', 'Uruguay', 'Venezuela']

lower_mid = ['Albania', 'Angola', 'Armenia', 'Azerbaijan', 'Belize', 'Bhutan', 'Bolivia', 'Cabo Verde', 'Cameroon',
             'China', 'Republic of the Congo', 'Ivory Coast', 'Djibouti', 'Ecuador', 'Egypt', 'El Salvador', 'Georgia',
             'Guatemala', 'Guyana', 'Honduras', 'India', 'Indonesia', 'Iran', 'Iraq', 'Jordan', 'Kiribati',
             'Kosovo', 'Lesotho', 'Maldives', 'Marshall Islands', 'Micronesia', 'Moldova', 'Mongolia', 'Morocco',
             'Nicaragua', 'Nigeria', 'Pakistan', 'Papua New Guinea', 'Paraguay', 'Philippines', 'Samoa',
             'Sao Tome and Principe', 'Solomon Islands', 'Sri Lanka', 'Sudan', 'Eswatini', 'Syria', 'Palestine',
             'Thailand', 'Timor-Leste', 'Tonga', 'Tunisia', 'Turkmenistan', 'Ukraine', 'Vanuatu', 'West Bank and Gaza']

low = ['Afghanistan', 'Bangladesh', 'Benin', 'Burkina Faso', 'Burundi', 'Cambodia', 'Central African Republic',
       'Chad', 'Comoros', 'Democratic Republic of the Congo', 'Eritrea', 'Ethiopia', 'The Gambia', 'Ghana', 'Guinea',
       'Guinea-Bissau', 'Haiti', 'Kenya', 'Korea, Dem. Rep.', 'Kyrgyzstan', 'Laos', 'Liberia', 'Madagascar', 'Malawi',
       'Mali', 'Mauritania', 'Mozambique', 'Myanmar', 'Nepal', 'Niger', 'Rwanda', 'Senegal', 'Sierra Leone', 'Somalia',
       'Tajikistan', 'Tanzania', 'Togo', 'Uganda', 'Uzbekistan', 'Vietnam', 'Yemen', 'Zambia', 'Zimbabwe']

# Defining a dictionary for determining the WBAC quartile

qh = {h:'q1' for h in high}
qu = {h:'q2' for h in upper_mid}
qm = {h:'q3' for h in lower_mid}
ql = {h:'q4' for h in low}
qd = {**qh, **qu, **qm, **ql}

# Defining a function for determining the quartile of the first author's nationality

def f_quart(inp):
    
    try:
        
        res = qd[inp]
        
    except:
        
        res = ''
    
    return res

# Determining the quartile of the affiliation of the first author

fq = [f_quart(x) for x in df.Nationality]
fq = pd.Series(fq, name = 'First_Quartile')
df = pd.concat([df, fq], axis = 1)

# Defining a function to determine the 'top quartile' for each paper

def quart(inp,nu):
    
    if nu % 100 == 0: # Just a visual queue because this isn't particularly fast
        
        print('Working on records ' + str(nu+1) + ' through ' + str(nu+101) + ' of 167,703.......')
    
    listicle = []
    
    while inp != ']':
        
        try:
            
            listicle.append(f_quart(first_nationality(inp)))
            inp = inp_trimmer(inp)
            
        except:
            
            inp = ']'
    
    if 'q1' in listicle:
        
        res = 'q1'
        
    elif 'q2' in listicle:
        
        res = 'q2'
        
    elif 'q3' in listicle:
        
        res = 'q3'
        
    else:
        
        res = 'q4'
    
    return res

# Determining the 'top quartile' present in each paper

print('Determining the top WBAC quartile present in each paper.......')

quarts = [quart(df.Affiliations[i],i) for i in range(len(df.Affiliations))]

# An indicator variable for whether or not a Q1 (high) nation contributed

q1 = [1 if q == 'q1' else 0 for q in quarts]

# Appending these two lists to the main df

quarts = pd.Series(quarts, name = 'Top_Quartile')
q1 = pd.Series(q1, name = 'Q1')
df = pd.concat([df, quarts, q1], axis = 1)

# 5443 of 167,703 had no discernable Nationality and are dropped here

df = df[df.First_Quartile != ''].reset_index(drop = True)

# Checking the number of COVID-19 related papers after the time cut-off as an anecdote:
# Note that this stat does now reflect dropping certain papers due to being publishing in unestablished journals

post_study_papers2 = ['lol' for i in range(len(papers)) if datetime.datetime.strptime(papers.Submitted[i], '%Y-%m-%d') > datetime.datetime.strptime('2020-06-30', '%Y-%m-%d')]
poststudy_covid2 = ['lol' for i in range(len(papers)) if datetime.datetime.strptime(papers.Submitted[i], '%Y-%m-%d') > datetime.datetime.strptime('2020-06-30', '%Y-%m-%d') and papers.COVID[i] == 1]

# Determining if the journal uses single blind or double blind peer review

print('Determining if the journal uses single blind or double blind peer review.......')

# Lists of journals with a double blind peer review policy

db_journals = ['Adm. Sci.', 'AgriEngineering', 'Arts', 'Buildings',
               'Economies', 'Educ. Sci.', 'Games', 'Genealogy', 'Humanities',
               'J. Intell.', 'J. Open Innov. Technol. Mark. Complex.',
               'Journal. Media.', 'Languages', 'Laws', 'Psych', 'Religions',
               'Soc. Sci.', 'Societies', 'Toxins']

db = [1 if j in db_journals else 0 for j in df.Journal]
db = pd.Series(db, name = 'Double_Blind')
df = pd.concat([df, db], axis = 1)

# Computing the distances

print('Calculating distances from thresholds.......')

# Distance from March 16 (middle of March)

XX = [datetime.datetime.strptime(df.Submitted[i], '%Y-%m-%d') - datetime.datetime.strptime('2020-03-16', '%Y-%m-%d') for i in range(len(df))]
XX = [x.days for x in XX]
XX = pd.Series(XX, name = 'X-c')
df = pd.concat([df, XX], axis = 1)

# Squared distance from March 16 (middle of March)

XX2 = df['X-c']*df['X-c']
XX2 = pd.Series(XX2, name = '(X-c)^2')
df = pd.concat([df, XX2], axis = 1)

# Cubed distance from March 16 (middle of March)

XX3 = df['X-c']*df['X-c']*df['X-c']
XX3 = pd.Series(XX3, name = '(X-c)^3')
df = pd.concat([df, XX3], axis = 1)

# Distance from surrounding days to serve as robustness checks

# One week prior to March 16

XX01 = [datetime.datetime.strptime(df.Submitted[i], '%Y-%m-%d') - datetime.datetime.strptime('2020-03-17', '%Y-%m-%d') for i in range(len(df))]
XX02 = [datetime.datetime.strptime(df.Submitted[i], '%Y-%m-%d') - datetime.datetime.strptime('2020-03-18', '%Y-%m-%d') for i in range(len(df))]
XX03 = [datetime.datetime.strptime(df.Submitted[i], '%Y-%m-%d') - datetime.datetime.strptime('2020-03-19', '%Y-%m-%d') for i in range(len(df))]
XX04 = [datetime.datetime.strptime(df.Submitted[i], '%Y-%m-%d') - datetime.datetime.strptime('2020-03-20', '%Y-%m-%d') for i in range(len(df))]
XX05 = [datetime.datetime.strptime(df.Submitted[i], '%Y-%m-%d') - datetime.datetime.strptime('2020-03-21', '%Y-%m-%d') for i in range(len(df))]
XX06 = [datetime.datetime.strptime(df.Submitted[i], '%Y-%m-%d') - datetime.datetime.strptime('2020-03-22', '%Y-%m-%d') for i in range(len(df))]
XX07 = [datetime.datetime.strptime(df.Submitted[i], '%Y-%m-%d') - datetime.datetime.strptime('2020-03-23', '%Y-%m-%d') for i in range(len(df))]

XX01 = [x.days for x in XX01]
XX02 = [x.days for x in XX02]
XX03 = [x.days for x in XX03]
XX04 = [x.days for x in XX04]
XX05 = [x.days for x in XX05]
XX06 = [x.days for x in XX06]
XX07 = [x.days for x in XX07]

XX01 = pd.Series(XX01, name = 'X-1-c')
XX02 = pd.Series(XX02, name = 'X-2-c')
XX03 = pd.Series(XX03, name = 'X-3-c')
XX04 = pd.Series(XX04, name = 'X-4-c')
XX05 = pd.Series(XX05, name = 'X-5-c')
XX06 = pd.Series(XX06, name = 'X-6-c')
XX07 = pd.Series(XX07, name = 'X-7-c')

df = pd.concat([df, XX01, XX02, XX03, XX04, XX05, XX06, XX07], axis = 1)

# One week post March 16

XX11 = [datetime.datetime.strptime(df.Submitted[i], '%Y-%m-%d') - datetime.datetime.strptime('2020-03-15', '%Y-%m-%d') for i in range(len(df))]
XX12 = [datetime.datetime.strptime(df.Submitted[i], '%Y-%m-%d') - datetime.datetime.strptime('2020-03-14', '%Y-%m-%d') for i in range(len(df))]
XX13 = [datetime.datetime.strptime(df.Submitted[i], '%Y-%m-%d') - datetime.datetime.strptime('2020-03-13', '%Y-%m-%d') for i in range(len(df))]
XX14 = [datetime.datetime.strptime(df.Submitted[i], '%Y-%m-%d') - datetime.datetime.strptime('2020-03-12', '%Y-%m-%d') for i in range(len(df))]
XX15 = [datetime.datetime.strptime(df.Submitted[i], '%Y-%m-%d') - datetime.datetime.strptime('2020-03-11', '%Y-%m-%d') for i in range(len(df))]
XX16 = [datetime.datetime.strptime(df.Submitted[i], '%Y-%m-%d') - datetime.datetime.strptime('2020-03-10', '%Y-%m-%d') for i in range(len(df))]
XX17 = [datetime.datetime.strptime(df.Submitted[i], '%Y-%m-%d') - datetime.datetime.strptime('2020-03-09', '%Y-%m-%d') for i in range(len(df))]

XX11 = [x.days for x in XX11]
XX12 = [x.days for x in XX12]
XX13 = [x.days for x in XX13]
XX14 = [x.days for x in XX14]
XX15 = [x.days for x in XX15]
XX16 = [x.days for x in XX16]
XX17 = [x.days for x in XX17]

XX11 = pd.Series(XX11, name = 'X+1-c')
XX12 = pd.Series(XX12, name = 'X+2-c')
XX13 = pd.Series(XX13, name = 'X+3-c')
XX14 = pd.Series(XX14, name = 'X+4-c')
XX15 = pd.Series(XX15, name = 'X+5-c')
XX16 = pd.Series(XX16, name = 'X+6-c')
XX17 = pd.Series(XX17, name = 'X+7-c')

df = pd.concat([df, XX11, XX12, XX13, XX14, XX15, XX16, XX17], axis = 1)

# Adding the post-effect variables for the main regression

D = [1 if df['X-c'][i] >= 0 else 0 for i in range(len(df))]
D = pd.Series(D, name = 'D')
DXc = D*df['X-c']
DXc2 = D*df['X-c']*df['X-c']
DXc3 = D*df['X-c']*df['X-c']*df['X-c']
DXc = pd.Series(DXc, name = 'D(X-c)')
DXc2 = pd.Series(DXc2, name = 'D(X-c)^2')
DXc3 = pd.Series(DXc3, name = 'D(X-c)^3')
df = pd.concat([df, D, DXc, DXc2, DXc3], axis = 1)

# Adding the post-effect variables for the robustness checks

D01 = [1 if df['X-1-c'][i] >= 0 else 0 for i in range(len(df))]
D02 = [1 if df['X-2-c'][i] >= 0 else 0 for i in range(len(df))]
D03 = [1 if df['X-3-c'][i] >= 0 else 0 for i in range(len(df))]
D04 = [1 if df['X-4-c'][i] >= 0 else 0 for i in range(len(df))]
D05 = [1 if df['X-5-c'][i] >= 0 else 0 for i in range(len(df))]
D06 = [1 if df['X-6-c'][i] >= 0 else 0 for i in range(len(df))]
D07 = [1 if df['X-7-c'][i] >= 0 else 0 for i in range(len(df))]

D01 = pd.Series(D01, name = 'D-1')
D02 = pd.Series(D02, name = 'D-2')
D03 = pd.Series(D03, name = 'D-3')
D04 = pd.Series(D04, name = 'D-4')
D05 = pd.Series(D05, name = 'D-5')
D06 = pd.Series(D06, name = 'D-6')
D07 = pd.Series(D07, name = 'D-7')

D11 = [1 if df['X+1-c'][i] >= 0 else 0 for i in range(len(df))]
D12 = [1 if df['X+2-c'][i] >= 0 else 0 for i in range(len(df))]
D13 = [1 if df['X-3-c'][i] >= 0 else 0 for i in range(len(df))]
D14 = [1 if df['X+4-c'][i] >= 0 else 0 for i in range(len(df))]
D15 = [1 if df['X+5-c'][i] >= 0 else 0 for i in range(len(df))]
D16 = [1 if df['X+6-c'][i] >= 0 else 0 for i in range(len(df))]
D17 = [1 if df['X+7-c'][i] >= 0 else 0 for i in range(len(df))]

D11 = pd.Series(D11, name = 'D+1')
D12 = pd.Series(D12, name = 'D+2')
D13 = pd.Series(D13, name = 'D+3')
D14 = pd.Series(D14, name = 'D+4')
D15 = pd.Series(D15, name = 'D+5')
D16 = pd.Series(D16, name = 'D+6')
D17 = pd.Series(D17, name = 'D+7')

df = pd.concat([df, D01, D02, D03, D04, D05, D06, D07, D11, D12, D13, D14, D15, D16, D17], axis = 1)

DXc01 = D01*df['X-1-c']
DXc02 = D02*df['X-2-c']
DXc03 = D03*df['X-3-c']
DXc04 = D04*df['X-4-c']
DXc05 = D05*df['X-5-c']
DXc06 = D06*df['X-6-c']
DXc07 = D07*df['X-7-c']

DXc11 = D11*df['X+1-c']
DXc12 = D12*df['X+2-c']
DXc13 = D13*df['X+3-c']
DXc14 = D14*df['X+4-c']
DXc15 = D15*df['X+5-c']
DXc16 = D16*df['X+6-c']
DXc17 = D17*df['X+7-c']

DXc01 = pd.Series(DXc01, name = 'D-1(X-c)')
DXc02 = pd.Series(DXc02, name = 'D-2(X-c)')
DXc03 = pd.Series(DXc03, name = 'D-3(X-c)')
DXc04 = pd.Series(DXc04, name = 'D-4(X-c)')
DXc05 = pd.Series(DXc05, name = 'D-5(X-c)')
DXc06 = pd.Series(DXc06, name = 'D-6(X-c)')
DXc07 = pd.Series(DXc07, name = 'D-7(X-c)')

DXc11 = pd.Series(DXc11, name = 'D+1(X-c)')
DXc12 = pd.Series(DXc12, name = 'D+2(X-c)')
DXc13 = pd.Series(DXc13, name = 'D+3(X-c)')
DXc14 = pd.Series(DXc14, name = 'D+4(X-c)')
DXc15 = pd.Series(DXc15, name = 'D+5(X-c)')
DXc16 = pd.Series(DXc16, name = 'D+6(X-c)')
DXc17 = pd.Series(DXc17, name = 'D+7(X-c)')

df = pd.concat([df, DXc01, DXc02, DXc03, DXc04, DXc05, DXc06, DXc07, DXc11, DXc12, DXc13, DXc14, DXc15, DXc16, DXc17], axis = 1)

# Calculating a total author time to add to the data set as a potential dependent variable

A = [df.Total[i] - df.Editor[i] for i in range(len(df))]
A = pd.Series(A, name = 'Author')
df = pd.concat([df, A], axis = 1)

# Adding natural logarithm transformed arXiv data

ln_arXiv7 = pd.Series(np.log(df.arXiv7.values), name = 'ln_arXiv7')
ln_arXiv14 = pd.Series(np.log(df.arXiv14.values), name = 'ln_arXiv14')
ln_arXiv30 = pd.Series(np.log(df.arXiv30.values), name = 'ln_arXiv30')

ln_new7 = pd.Series(np.log(df.new7.values), name = 'ln_new7')
ln_new14 = pd.Series(np.log(df.new14.values), name = 'ln_new14')
ln_new30 = pd.Series(np.log(df.new30.values), name = 'ln_new30')

df = pd.concat([df, ln_arXiv7, ln_arXiv14, ln_arXiv30, ln_new7, ln_new14, ln_new30], axis = 1)

# Two journals had a bad date resulting in an infeasible value for Stage1 so they are dropped here

df = df[df.Stage1 >= 0].reset_index(drop = True)

# Defining a function for adding a month dummy

def month(m):
    
    md = {'01':'JAN', '02':'FEB', '03':'MAR', '04':'APR', '05':'MAY', '06':'JUN', 
          '07':'JUL', '08':'AUG', '09':'SEP', '10':'OCT', '11':'NOV', '12':'DEC', } # a month dictionary    
    s = m[5:7] # the month as a number stored as a string
    mon = md[s]# getting the month from the dictionary
    
    return mon

# Add a month dummy using the function

months = [month(m) for m in df.Submitted]
months = pd.Series(months, name = 'Month')
df = pd.concat([df, months], axis = 1)

# Prepping the data for the regressions

Stage1 = np.log(df.Stage1.values)
Stage2 = np.log(df.Stage2.values)
Stage3 = np.log(df.Stage3.values)
Total = np.log(df.Total.values)
Editor = np.log(df.Editor.values)

XX = stats.add_constant(df[['X-c', '(X-c)^2', '(X-c)^3', 'D', 'D(X-c)', 'D(X-c)^2', 'D(X-c)^3',
                            'COVID', 'Double_Blind', 'Author_Count', 'ln_arXiv14']])

# Creating the fixed effects

dG = pd.get_dummies(df['Gender'])
dF = pd.get_dummies(df['Frascati'])
dQ = pd.get_dummies(df['First_Quartile'])
dN = pd.get_dummies(df['Nationality'])
dJ = pd.get_dummies(df['Journal'])
dM = pd.get_dummies(df['Month'])

XX = XX.join(dG).drop('unknown', axis = 1)
XX = XX.join(dF).drop(6, axis = 1)
XX = XX.join(dQ).drop('q4', axis = 1)
XX = XX.join(dN).drop('USA', axis = 1)
XX = XX.join(dJ).drop('Animals', axis = 1)
XX = XX.join(dM).drop('JAN', axis = 1)

# Interacting gender and peer review type

F1xPR = pd.Series(XX.Double_Blind*XX.female, name = 'female_DB')
F2xPR = pd.Series(XX.Double_Blind*XX.mostly_female, name = 'mostly_female_DB')
M1xPR = pd.Series(XX.Double_Blind*XX.male, name = 'male_DB')
M2xPR = pd.Series(XX.Double_Blind*XX.mostly_male, name = 'mostly_male_DB')
AxPR = pd.Series(XX.Double_Blind*XX.andy, name = 'andy_DB')

XX = XX.join(F1xPR)
XX = XX.join(F2xPR)
XX = XX.join(M1xPR)
XX = XX.join(M2xPR)
XX = XX.join(AxPR)

# Running the fuzzy regression discontinuity models

print('Running the main models.......')

res1 = stats.OLS(Stage1,XX).fit(cov_type = 'HC1')
res2 = stats.OLS(Stage2,XX).fit(cov_type = 'HC1')
res3 = stats.OLS(Stage3,XX).fit(cov_type = 'HC1')
resT = stats.OLS(Total,XX).fit(cov_type = 'HC1')
resE = stats.OLS(Editor,XX).fit(cov_type = 'HC1')

print(res1.summary())
print(res2.summary())
print(res3.summary())
print(resT.summary())
print(resE.summary())

res_list = [res1, res2, res3, resT, resE]
names = ['Stage1', 'Stage2', 'Stage3', 'Total', 'Editor']

for r in range(len(res_list)):
    
    file = open('C:/Users/User/Documents/Data/COVID-19/results_' + names[r] + '.txt', 'w')
    file.write(res_list[r].summary().as_text())
    file.close()

restab(res_list, 'C:/Users/User/Documents/Data/COVID-19/restab_main.txt')

# Before running any more models, the text mining component needs to be done

# Defining a function for extracting the keywords from the dataframe

def clean_keys(key):
    
    key_list = [] # Initialize a list
    idx = 0
    
    # Data preprocessing prior to identifying individual keywords
    
    key = key.lower() # convert to lowercase
    key = key.replace(',', ' ') # replace certain characters with a space
    key = key.replace('.', ' ') # replace certain characters with a space
    key = key.replace('&', ' ') # replace certain characters with a space
    key = key.replace(' and', ' ') # replace certain characters with a space
    key = key.replace("'", '') # remove apostrophes
    key = key.replace('<i>', '') # remove italicized
    key = key.replace('</i>', '') # remove italicized
    key = key.replace('(m amp;o)', '') # manual cleansing
    key = key.replace('(d amp;a)', '') # manual cleansing
    key = key.replace('d amp; p', '') # manual cleansing
    key = key.replace('m 9191t gt; c', '') # manual cleansing
    key = key.replace('zeama;pht1;6', '') # manual cleansing
    key = key.replace(' l ; r', '') # manual cleansing
    key = key.replace('g 7254t gt;c', '') # manual cleansing
    key = key.replace('m 3243a gt;g', '') # manual cleansing
    key = key.replace('t(6;9)', '') # manual cleansing
    key = key.replace('sh amp; e', '') # manual cleansing
    key = key.replace('q amp; a', '') # manual cleansing
    key = key.replace('−2459g  gt; a', '') # manual cleansing
    key = key.replace('r amp;d', 'rd') # manual cleansing
    key = key.replace('r d', 'rd') # manual cleansing
    key = key.replace('(rd amp;d)', '') # manual cleaning
    key = key.replace('c -32-13t amp;gt; g', '') # manual cleansing
    key = key.replace('rs4253778 g  gt; c; rs4253776 a  gt; g', '') # manual cleansing
    key = key.replace('π', '') # manual cleansing
    key = ' '.join(key.split()) # remove duplicate spaces and begining/end spaces
    
    if key[-2:] == ' r': # manual cleansing
        
        key = key[:-2]
        
    if key[-1] == ';': # remove end ; from certain manual cleansing
        
        key = key[:-1]
        
    while idx != -1:
        
        idx = key.find(';') # isolate keyword
        
        if key[idx-1] == 's': # depluralize
            
            word = key[0:idx-1] # depluralize
            #word = ' '.join(w for w in word if w.isalnum()) # remove special characters
            key_list.append(word) # append keyword to list of keywords
            
        else:
            
            word = key[0:idx] # depluralize
            #word = ' '.join(w for w in word if w.isalnum()) # remove special characters
            key_list.append(word) # append keyword to list of keywords
            
        if key[idx+1] == ' ':
            
            key = key[idx+2:] # remove remainder of key
            
        else:
            
            key = key[idx+1:] # remove remainder of key
        
    if key[-1] == 's':
        
        word = key[:-1] # depluralize
        #word = ' '.join(w for w in word if w.isalnum()) # remove special characters
        key_list.append(word) # last keyword
        
    else:
        
        word = key
        #word = ' '.join(w for w in word if w.isalnum()) # remove special characters
        key_list.append(word) # last keyword
            
    return key_list

# Applying the function

print('Extracting and cleaning the keywords.......')

# Generating raw lists of keywords for each paper

keywords = [clean_keys(k) for k in df.Keywords]

# Creating a main list of keywords

all_keys = [k for keyword in keywords for k in keyword]
key_list = list(sorted(set(all_keys)))
counts = [all_keys.count(k) for k in key_list]

# Generating reference indices for keywords appearing in >= n papers

k2 = [i for i in range(len(counts)) if counts[i] >= 2]
k3 = [i for i in range(len(counts)) if counts[i] >= 3]
k5 = [i for i in range(len(counts)) if counts[i] >= 5]
k10 = [i for i in range(len(counts)) if counts[i] >= 10]
k20 = [i for i in range(len(counts)) if counts[i] >= 20]
k50 = [i for i in range(len(counts)) if counts[i] >= 50]
k100  = [i for i in range(len(counts)) if counts[i] >= 100]

# Generating the lists of keywords that appear in >= n papers

keys2 = [key_list[i] for i in k2]
keys3 = [key_list[i] for i in k3]
keys5 = [key_list[i] for i in k5]
keys10 = [key_list[i] for i in k10]
keys20 = [key_list[i] for i in k20]
keys50 = [key_list[i] for i in k50]
keys100 = [key_list[i] for i in k100]

keydf = pd.DataFrame()

for k in keys100:
    
    print('Creating fixed effect for keyword ' + str(keys100.index(k)+1) + ' of 743.......')
    col = [1 if k in keywords[i] else 0 for i in range(len(df))]
    col = pd.Series(col, name = k)
    keydf = pd.concat([keydf, col], axis = 1)
    
# Removing two meaningless keywords ('[' and '[]')

keykeepers = [k for k in list(keydf.columns) if list(keydf.columns).index(k) not in [2,3]]
keydf = keydf[keykeepers]

# Appending keydf to df

df = pd.concat([df, keydf], axis = 1)

# Running regressions with comntrols for common keywords

# Prepping the data for the regressions

XX = XX.join(keydf)

# Running the fuzzy regression discontinuity models

print('Running the main models.......')

res1b = stats.OLS(Stage1,XX).fit(cov_type = 'HC1')
res2b = stats.OLS(Stage2,XX).fit(cov_type = 'HC1')
res3b = stats.OLS(Stage3,XX).fit(cov_type = 'HC1')
resTb = stats.OLS(Total,XX).fit(cov_type = 'HC1')
resEb = stats.OLS(Editor,XX).fit(cov_type = 'HC1')

print(res1b.summary())
print(res2b.summary())
print(res3b.summary())
print(resTb.summary())
print(resEb.summary())

res_listb = [res1b, res2b, res3b, resTb, resEb]
names = ['Stage1', 'Stage2', 'Stage3', 'Total', 'Editor']

for r in range(len(res_listb)):
    
    file = open('C:/Users/User/Documents/Data/COVID-19/results_with_keywords' + names[r] + '.txt', 'w')
    file.write(res_listb[r].summary().as_text())
    file.close()

restab(res_list, 'C:/Users/User/Documents/Data/COVID-19/restab_with_keywords.txt')

# Data visualization

viz = [datetime.datetime.strptime(df.Submitted[i], '%Y-%m-%d') for i in range(len(df))]
viz = pd.Series(viz, name = 'viz')
df2 = pd.concat([df, viz], axis = 1)
df3 = df2[df2.COVID == 0]

d0 = datetime.datetime.strptime('2019-12-01', '%Y-%m-%d')
d20 = datetime.datetime.strptime('2019-01-01', '%Y-%m-%d')
days = [d0 + datetime.timedelta(days = d) for d in range(213)]
days2 = [d20 + datetime.timedelta(days = d) for d in range(547)]

plotdata = []
plotdata2 = []
plot2data = []
plot2data2 = []

for day in days:
    
    temp = df2[df2.viz == day]
    temp2 = df3[df3.viz == day]
    plotdata.append(np.mean(temp.Total))
    plotdata2.append(np.mean(temp2.Total))

for day in days2:
    
    temp = df2[df2.viz == day]
    temp2 = df3[df3.viz == day]
    plot2data.append(np.mean(temp.Total))
    plot2data2.append(np.mean(temp2.Total))
    
days = pd.Series(days, name = 'Date')
days2 = pd.Series(days2, name = 'Date')
plotdata = pd.Series(plotdata, name = 'Days')
plot2data = pd.Series(plot2data, name = 'Days')
plotdata2 = pd.Series(plotdata2, name = 'Days')
plot2data2 = pd.Series(plot2data2, name = 'Days')
plotdf = pd.concat([days, plotdata], axis = 1)
plot2df = pd.concat([days, plotdata2], axis = 1)
plotdf2 = pd.concat([days2, plot2data], axis = 1)
plot2df2 = pd.concat([days2, plot2data2], axis = 1)
plotdf.set_index('Date', inplace = True, drop = True)
plot2df.set_index('Date', inplace = True, drop = True)
plotdf2.set_index('Date', inplace = True, drop = True)
plot2df2.set_index('Date', inplace = True, drop = True)

ax = plotdf.plot(color  = 'black', legend = False)
plot2df.plot(ax = ax, color  = 'red', legend = False)
plt.title('Mean Days from Submission to Publication\nfor Accepted Papers by Submission Date')
plt.xlabel('Date')
plt.ylabel('Days')
plt.axvline(x = days[107])
plt.savefig('C:/Users/User/Documents/Data/COVID-19/Figure_1.eps')

ax = plotdf.plot(color  = 'black', legend = False)
plot2df2.plot(ax = ax, color  = 'red', legend = False)
plt.title('Mean Days from Submission to Publication\nfor Accepted Papers by Submission Date')
plt.xlabel('Date')
plt.ylabel('Days')
plt.axvline(x = days2[440])
plt.savefig('C:/Users/User/Documents/Data/COVID-19/Figure_2.eps')

# Calculating and plotting COVID effects over time from initial regressions

time = [i for i in range(1,107)] # From March 17 through June 30
effects1 = [res1.params['D'] + t*res1.params['D(X-c)'] + t*t*res1.params['D(X-c)^2'] + t*t*t*res1.params['D(X-c)^3'] for t in time]
stderrs1 = [res1.bse['D'] + res1.bse['D(X-c)'] + res1.bse['D(X-c)^2'] + res1.bse['D(X-c)^3'] for t in time]
effects2 = [res2.params['D'] + t*res2.params['D(X-c)'] + t*t*res2.params['D(X-c)^2'] + t*t*t*res2.params['D(X-c)^3'] for t in time]
stderrs2 = [res2.bse['D'] + res2.bse['D(X-c)'] + res2.bse['D(X-c)^2'] + res2.bse['D(X-c)^3'] for t in time]
effects3 = [res3.params['D'] + t*res3.params['D(X-c)'] + t*t*res3.params['D(X-c)^2'] + t*t*t*res3.params['D(X-c)^3'] for t in time]
stderrs3 = [res3.bse['D'] + res3.bse['D(X-c)'] + res3.bse['D(X-c)^2'] + res3.bse['D(X-c)^3'] for t in time]
effectsT = [resT.params['D'] + t*resT.params['D(X-c)'] + t*t*resT.params['D(X-c)^2'] + t*t*t*resT.params['D(X-c)^3'] for t in time]
stderrsT = [resT.bse['D'] + resT.bse['D(X-c)'] + resT.bse['D(X-c)^2'] + resT.bse['D(X-c)^3'] for t in time]
effectsE = [resE.params['D'] + t*resE.params['D(X-c)'] + t*t*resE.params['D(X-c)^2'] + t*t*t*resE.params['D(X-c)^3'] for t in time]
stderrsE = [resE.bse['D'] + resE.bse['D(X-c)'] + resE.bse['D(X-c)^2'] + resE.bse['D(X-c)^3'] for t in time]

eplot1df = 100*pd.Series(effects1, name = 'Stage 1')
eplot2df = 100*pd.Series(effects2, name = 'Stage 2')
eplot3df = 100*pd.Series(effects3, name = 'Stage 3')
eplotTdf = 100*pd.Series(effectsT, name = 'Total')
eplotEdf = 100*pd.Series(effectsE, name = 'Editorial')

splot1df = 100*pd.Series([effects1[i] + 1.96*stderrs1[i] for i in range(len(effects1))], name = 'SE')
splot2df = 100*pd.Series([effects2[i] + 1.96*stderrs2[i] for i in range(len(effects2))], name = 'SE')
splot3df = 100*pd.Series([effects3[i] + 1.96*stderrs3[i] for i in range(len(effects3))], name = 'SE')
splotTdf = 100*pd.Series([effectsT[i] + 1.96*stderrsT[i] for i in range(len(effectsT))], name = 'SE')
splotEdf = 100*pd.Series([effectsE[i] + 1.96*stderrsE[i] for i in range(len(effectsE))], name = 'SE')

splot1dfm = 100*pd.Series([effects1[i] - 1.96*stderrs1[i] for i in range(len(effects1))], name = 'SE')
splot2dfm = 100*pd.Series([effects2[i] - 1.96*stderrs2[i] for i in range(len(effects2))], name = 'SE')
splot3dfm = 100*pd.Series([effects3[i] - 1.96*stderrs3[i] for i in range(len(effects3))], name = 'SE')
splotTdfm = 100*pd.Series([effectsT[i] - 1.96*stderrsT[i] for i in range(len(effectsT))], name = 'SE')
splotEdfm = 100*pd.Series([effectsE[i] - 1.96*stderrsE[i] for i in range(len(effectsE))], name = 'SE')

ax = eplot1df.plot(color  = 'black', legend = False)
splot1df.plot(ax = ax, color  = 'red', legend = False)
splot1dfm.plot(ax = ax, color  = 'red', legend = False)
plt.title('Effect on Publication Times due to COVID-19')
plt.xlabel('Days Post Treatment (March 16)')
plt.ylabel('Effect (% Change in Time)')
plt.axhline(0)
plt.savefig('C:/Users/User/Documents/Data/COVID-19/Effects_Figure_1.eps')

ax = eplot2df.plot(color  = 'black', legend = False)
splot2df.plot(ax = ax, color  = 'red', legend = False)
splot2dfm.plot(ax = ax, color  = 'red', legend = False)
plt.title('Effect on Publication Times due to COVID-19')
plt.xlabel('Days Post Treatment (March 16)')
plt.ylabel('Effect (% Change in Time)')
plt.axhline(0)
plt.savefig('C:/Users/User/Documents/Data/COVID-19/Effects_Figure_2.eps')

ax = eplot3df.plot(color  = 'black', legend = False)
splot3df.plot(ax = ax, color  = 'red', legend = False)
splot3dfm.plot(ax = ax, color  = 'red', legend = False)
plt.title('Effect on Publication Times due to COVID-19')
plt.xlabel('Days Post Treatment (March 16)')
plt.ylabel('Effect (% Change in Time)')
plt.axhline(0)
plt.savefig('C:/Users/User/Documents/Data/COVID-19/Effects_Figure_3.eps')

ax = eplotTdf.plot(color  = 'black', legend = False)
splotTdf.plot(ax = ax, color  = 'red', legend = False)
splotTdfm.plot(ax = ax, color  = 'red', legend = False)
plt.title('Effect on Publication Times due to COVID-19')
plt.xlabel('Days Post Treatment (March 16)')
plt.ylabel('Effect (% Change in Time)')
plt.axhline(0)
plt.savefig('C:/Users/User/Documents/Data/COVID-19/Effects_Figure_T.eps')

ax = eplotEdf.plot(color  = 'black', legend = False)
splotEdf.plot(ax = ax, color  = 'red', legend = False)
splotEdfm.plot(ax = ax, color  = 'red', legend = False)
plt.title('Effect on Publication Times due to COVID-19')
plt.xlabel('Days Post Treatment (March 16)')
plt.ylabel('Effect (% Change in Time)')
plt.axhline(0)
plt.savefig('C:/Users/User/Documents/Data/COVID-19/Effects_Figure_E.eps')

# Calculating and plotting COVID effects over time from regressions with keywords

time = [i for i in range(1,107)] # From March 17 through June 30
effects1b = [res1b.params['D'] + t*res1b.params['D(X-c)'] + t*t*res1b.params['D(X-c)^2'] + t*t*t*res1b.params['D(X-c)^3'] for t in time]
stderrs1b = [res1b.bse['D'] + res1b.bse['D(X-c)'] + res1b.bse['D(X-c)^2'] + res1b.bse['D(X-c)^3'] for t in time]
effects2b = [res2b.params['D'] + t*res2b.params['D(X-c)'] + t*t*res2b.params['D(X-c)^2'] + t*t*t*res2b.params['D(X-c)^3'] for t in time]
stderrs2b = [res2b.bse['D'] + res2b.bse['D(X-c)'] + res2b.bse['D(X-c)^2'] + res2b.bse['D(X-c)^3'] for t in time]
effects3b = [res3b.params['D'] + t*res3b.params['D(X-c)'] + t*t*res3b.params['D(X-c)^2'] + t*t*t*res3b.params['D(X-c)^3'] for t in time]
stderrs3b = [res3b.bse['D'] + res3b.bse['D(X-c)'] + res3b.bse['D(X-c)^2'] + res3b.bse['D(X-c)^3'] for t in time]
effectsTb = [resTb.params['D'] + t*resTb.params['D(X-c)'] + t*t*resTb.params['D(X-c)^2'] + t*t*t*resTb.params['D(X-c)^3'] for t in time]
stderrsTb = [resTb.bse['D'] + resTb.bse['D(X-c)'] + resTb.bse['D(X-c)^2'] + resTb.bse['D(X-c)^3'] for t in time]
effectsEb = [resEb.params['D'] + t*resEb.params['D(X-c)'] + t*t*resEb.params['D(X-c)^2'] + t*t*t*resEb.params['D(X-c)^3'] for t in time]
stderrsEb = [resEb.bse['D'] + resEb.bse['D(X-c)'] + resEb.bse['D(X-c)^2'] + resEb.bse['D(X-c)^3'] for t in time]

eplot1dfb = 100*pd.Series(effects1b, name = 'Stage 1')
eplot2dfb = 100*pd.Series(effects2b, name = 'Stage 2')
eplot3dfb = 100*pd.Series(effects3b, name = 'Stage 3')
eplotTdfb = 100*pd.Series(effectsTb, name = 'Total')
eplotEdfb = 100*pd.Series(effectsEb, name = 'Editorial')

splot1dfb = 100*pd.Series([effects1b[i] + 1.96*stderrs1b[i] for i in range(len(effects1b))], name = 'SE')
splot2dfb = 100*pd.Series([effects2b[i] + 1.96*stderrs2b[i] for i in range(len(effects2b))], name = 'SE')
splot3dfb = 100*pd.Series([effects3b[i] + 1.96*stderrs3b[i] for i in range(len(effects3b))], name = 'SE')
splotTdfb = 100*pd.Series([effectsTb[i] + 1.96*stderrsTb[i] for i in range(len(effectsTb))], name = 'SE')
splotEdfb = 100*pd.Series([effectsEb[i] + 1.96*stderrsEb[i] for i in range(len(effectsEb))], name = 'SE')

splot1dfmb = 100*pd.Series([effects1b[i] - 1.96*stderrs1b[i] for i in range(len(effects1b))], name = 'SE')
splot2dfmb = 100*pd.Series([effects2b[i] - 1.96*stderrs2b[i] for i in range(len(effects2b))], name = 'SE')
splot3dfmb = 100*pd.Series([effects3b[i] - 1.96*stderrs3b[i] for i in range(len(effects3b))], name = 'SE')
splotTdfmb = 100*pd.Series([effectsTb[i] - 1.96*stderrsTb[i] for i in range(len(effectsTb))], name = 'SE')
splotEdfmb = 100*pd.Series([effectsEb[i] - 1.96*stderrsEb[i] for i in range(len(effectsEb))], name = 'SE')

ax = eplot1dfb.plot(color  = 'black', legend = False)
splot1dfb.plot(ax = ax, color  = 'red', legend = False)
splot1dfmb.plot(ax = ax, color  = 'red', legend = False)
plt.title('Effect on Publication Times due to COVID-19')
plt.xlabel('Days Post Treatment (March 16)')
plt.ylabel('Effect (% Change in Time)')
plt.axhline(0)
plt.savefig('C:/Users/User/Documents/Data/COVID-19/Keyword_Effects_Figure_1.eps')

ax = eplot2dfb.plot(color  = 'black', legend = False)
splot2dfb.plot(ax = ax, color  = 'red', legend = False)
splot2dfmb.plot(ax = ax, color  = 'red', legend = False)
plt.title('Effect on Publication Times due to COVID-19')
plt.xlabel('Days Post Treatment (March 16)')
plt.ylabel('Effect (% Change in Time)')
plt.axhline(0)
plt.savefig('C:/Users/User/Documents/Data/COVID-19/Keyword_Effects_Figure_2.eps')

ax = eplot3dfb.plot(color  = 'black', legend = False)
splot3dfb.plot(ax = ax, color  = 'red', legend = False)
splot3dfmb.plot(ax = ax, color  = 'red', legend = False)
plt.title('Effect on Publication Times due to COVID-19')
plt.xlabel('Days Post Treatment (March 16)')
plt.ylabel('Effect (% Change in Time)')
plt.axhline(0)
plt.savefig('C:/Users/User/Documents/Data/COVID-19/Keyword_Effects_Figure_3.eps')

ax = eplotTdfb.plot(color  = 'black', legend = False)
splotTdfb.plot(ax = ax, color  = 'red', legend = False)
splotTdfmb.plot(ax = ax, color  = 'red', legend = False)
plt.title('Effect on Publication Times due to COVID-19')
plt.xlabel('Days Post Treatment (March 16)')
plt.ylabel('Effect (% Change in Time)')
plt.axhline(0)
plt.savefig('C:/Users/User/Documents/Data/COVID-19/Keyword_Effects_Figure_T.eps')

ax = eplotEdfb.plot(color  = 'black', legend = False)
splotEdfb.plot(ax = ax, color  = 'red', legend = False)
splotEdfmb.plot(ax = ax, color  = 'red', legend = False)
plt.title('Effect on Publication Times due to COVID-19')
plt.xlabel('Days Post Treatment (March 16)')
plt.ylabel('Effect (% Change in Time)')
plt.axhline(0)
plt.savefig('C:/Users/User/Documents/Data/COVID-19/Keyword_Effects_Figure_E.eps')





#### TO DO ####
# extract data from titles
# extract data from abstracts
# create dummies with data extracted from keywords, titles, and abstracts
# run full regressions --- only use keywords maybe???
# finish prep for robustness checks including distance from march with all of march == 0
# run robustness checks
# write the paper





