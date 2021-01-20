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

# Create a list of journals which will be included in the study - those with pubs prior to 2019

print('Removing papers from journals first published post 2019-01-01.......')

journals = []

for journal in papers.Journal.unique():
    
    j = papers[papers.Journal == journal].reset_index()
    
    if datetime.datetime.strptime(min(j.Accepted), '%Y-%m-%d') < datetime.datetime.strptime('2020-01-01', '%Y-%m-%d') and datetime.datetime.strptime(max(j.Accepted), '%Y-%m-%d') > datetime.datetime.strptime('2019-01-01', '%Y-%m-%d'):
        
        journals.append(j.Journal[0])

# Subset data based on journals

df = papers[papers.Journal.isin(journals)].reset_index(drop = True)

# Subset data based on submission date

print('Removing papers from outside of the study time frame.......')

post1911 = [int(datetime.datetime.strptime(df.Submitted[i], '%Y-%m-%d') > datetime.datetime.strptime('2019-11-30', '%Y-%m-%d')) for i in range(len(df))]
pre2007 = [int(datetime.datetime.strptime(df.Submitted[i], '%Y-%m-%d') < datetime.datetime.strptime('2020-07-01', '%Y-%m-%d')) for i in range(len(df))]
study = pd.Series([post1911[i] * pre2007[i] for i in range(len(post1911))], name = 'Study')
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
        
        print('Working on records ' + str(nu+1) + ' through ' + str(nu+101) + ' of 77,595.......')
    
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
        
        print('Working on records ' + str(nu+1) + ' through ' + str(nu+101) + ' of 77,595.......')
    
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

# 602 of 77,595 had no discernable Nationality and are dropped here

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
XX = pd.Series(XX, name = 'X')
df = pd.concat([df, XX], axis = 1)

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

XX01 = pd.Series(XX01, name = 'X-1')
XX02 = pd.Series(XX02, name = 'X-2')
XX03 = pd.Series(XX03, name = 'X-3')
XX04 = pd.Series(XX04, name = 'X-4')
XX05 = pd.Series(XX05, name = 'X-5')
XX06 = pd.Series(XX06, name = 'X-6')
XX07 = pd.Series(XX07, name = 'X-7')

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

XX11 = pd.Series(XX11, name = 'X+1')
XX12 = pd.Series(XX12, name = 'X+2')
XX13 = pd.Series(XX13, name = 'X+3')
XX14 = pd.Series(XX14, name = 'X+4')
XX15 = pd.Series(XX15, name = 'X+5')
XX16 = pd.Series(XX16, name = 'X+6')
XX17 = pd.Series(XX17, name = 'X+7')

df = pd.concat([df, XX11, XX12, XX13, XX14, XX15, XX16, XX17], axis = 1)

# Adding the post-effect variables for the main regression

D = [1 if df.X[i] >= 0 else 0 for i in range(len(df))]
D = pd.Series(D, name = 'D')
DXc = D*df.X
DXc = pd.Series(DXc, name = 'D(X-c)')
df = pd.concat([df, D, DXc], axis = 1)

# Adding the post-effect variables for the robustness checks

D01 = [1 if df['X-1'][i] >= 0 else 0 for i in range(len(df))]
D02 = [1 if df['X-2'][i] >= 0 else 0 for i in range(len(df))]
D03 = [1 if df['X-3'][i] >= 0 else 0 for i in range(len(df))]
D04 = [1 if df['X-4'][i] >= 0 else 0 for i in range(len(df))]
D05 = [1 if df['X-5'][i] >= 0 else 0 for i in range(len(df))]
D06 = [1 if df['X-6'][i] >= 0 else 0 for i in range(len(df))]
D07 = [1 if df['X-7'][i] >= 0 else 0 for i in range(len(df))]

D01 = pd.Series(D01, name = 'D-1')
D02 = pd.Series(D02, name = 'D-2')
D03 = pd.Series(D03, name = 'D-3')
D04 = pd.Series(D04, name = 'D-4')
D05 = pd.Series(D05, name = 'D-5')
D06 = pd.Series(D06, name = 'D-6')
D07 = pd.Series(D07, name = 'D-7')

D11 = [1 if df['X+1'][i] >= 0 else 0 for i in range(len(df))]
D12 = [1 if df['X+2'][i] >= 0 else 0 for i in range(len(df))]
D13 = [1 if df['X-3'][i] >= 0 else 0 for i in range(len(df))]
D14 = [1 if df['X+4'][i] >= 0 else 0 for i in range(len(df))]
D15 = [1 if df['X+5'][i] >= 0 else 0 for i in range(len(df))]
D16 = [1 if df['X+6'][i] >= 0 else 0 for i in range(len(df))]
D17 = [1 if df['X+7'][i] >= 0 else 0 for i in range(len(df))]

D11 = pd.Series(D11, name = 'D+1')
D12 = pd.Series(D12, name = 'D+2')
D13 = pd.Series(D13, name = 'D+3')
D14 = pd.Series(D14, name = 'D+4')
D15 = pd.Series(D15, name = 'D+5')
D16 = pd.Series(D16, name = 'D+6')
D17 = pd.Series(D17, name = 'D+7')

df = pd.concat([df, D01, D02, D03, D04, D05, D06, D07, D11, D12, D13, D14, D15, D16, D17], axis = 1)

DXc01 = D01*df['X-1']
DXc02 = D02*df['X-2']
DXc03 = D03*df['X-3']
DXc04 = D04*df['X-4']
DXc05 = D05*df['X-5']
DXc06 = D06*df['X-6']
DXc07 = D07*df['X-7']

DXc11 = D11*df['X+1']
DXc12 = D12*df['X+2']
DXc13 = D13*df['X+3']
DXc14 = D14*df['X+4']
DXc15 = D15*df['X+5']
DXc16 = D16*df['X+6']
DXc17 = D17*df['X+7']

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

# Prepping the data for the regressions

Stage1 = np.log(df.Stage1.values)
Stage2 = np.log(df.Stage2.values)
Stage3 = np.log(df.Stage3.values)
Total = np.log(df.Total.values)
Editor = np.log(df.Editor.values)
Author = np.log(df.Author.values)

XX = stats.add_constant(df[['D', 'X', 'D(X-c)', 'COVID', 'Double_Blind', 'Author_Count', 'ln_arXiv30']])

dG = pd.get_dummies(df['Gender'])
dF = pd.get_dummies(df['Frascati'])
dQ = pd.get_dummies(df['First_Quartile'])
dN = pd.get_dummies(df['Nationality'])
dJ = pd.get_dummies(df['Journal'])

XX = XX.join(dG).drop('unknown', axis = 1)
XX = XX.join(dF).drop(6, axis = 1)
XX = XX.join(dQ).drop('q4', axis = 1)
XX = XX.join(dN).drop('USA', axis = 1)
XX = XX.join(dJ).drop('Animals', axis = 1)

# Running the fuzzy regression discontinuity models models

res = stats.OLS(Stage1,XX).fit(cov_type = 'HC1')
print(res.summary())
#file = open('C:/Users/User/Documents/Data/COVID-19/results_Stage1.txt', 'w')
#file.write(res.summary().as_text())
#file.close()














Y = a + bZ + eD + f(X-c) + gD(X-c) + u

Y :: 'Stage1', 'Stage2', 'Stage3', 'Total', 'Editor','Author'

Z2 :: 'Title', 'Abstract', 'Keywords'

Z :: 'Journal', 'Frascati', 'arXiv7', 'arXiv14', 'arXiv30', 'new7', 'new14', 'new30','COVID',
'Author_Count', 'Gender', 'Nationality', 'First_Quartile', 'Top_Quartile', 'Q1', 'Double_Blind'

X :: 'X', 'X-1', 'X-2', 'X-3', 'X-4', 'X-5', 'X-6', 'X-7', 'X+1', 'X+2',
'X+3', 'X+4', 'X+5', 'X+6', 'X+7', 



"""
INTERACT GENDER VARIABLES WITH PEER REVIEW TYPE VARIABLE!!!!!!!
"""

















# cutoffs could include distance from march, distance from march 16 (mid march), ...

# how much time around cutoff and should it be symmetric in time?
# need to remove papers from journals that did not have publications prior to COVID
# this could be done by only considering journals that published papers in 2019


# Data visualization

viz = [datetime.datetime.strptime(df.Submitted[i], '%Y-%m-%d') for i in range(len(df))]
viz = pd.Series(viz, name = 'viz')
df2 = pd.concat([df, viz], axis = 1)
df3 = df2[df2.COVID == 0]


d0 = datetime.datetime.strptime('2018-12-31', '%Y-%m-%d')
days = [d0 + datetime.timedelta(days = d) for d in range(548)]
plotdata = []
plotdata2 = []

for day in days:
    
    temp = df2[df2.viz == day]
    temp2 = df3[df3.viz == day]
    plotdata.append(np.mean(temp.Total))
    plotdata2.append(np.mean(temp2.Total))

plt.figure(figsize = (8,5))
plt.plot(plotdata, color = 'black')
plt.plot(plotdata2, color = 'red')
"""
ADD VERTICAL LINES FOR MARCH 1 AND MARCH 31 AND MAYBE THE IDES OF MARCH?
"""
"""
ALSO, FORMAT X LABELS AS DATES
"""
"""
ALSO, DE-TREND THIS DATA OR NO?!?!? -- JUST FOR THE SAKE OF THE PLOT.... DO BOTH!!!!
"""








# find visual evidence justifying FRDD
# create plots to include in the paper - mean(papers.Total) conditional on papers.Submitted == day
# subset data by journals
# subset data by dates (around the cut-off)
# subset data for each set of models (Xs, Ys)
# run models
# create output tex tables





