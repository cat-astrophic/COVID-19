# This script harvests the metadata from papers published in MDPI journals

# Importing required modules

import pandas as pd
import urllib
from bs4 import BeautifulSoup as bs

# Get links from previous output file

file = open('C:/Users/User/Documents/Data/COVID-19/mdpi_links.txt', 'r')
links = file.readlines()
file.close()

# A function used to help parse strings

def affiliation_finder(string):
    
    return any(s.isdigit() for s in string)

# Run this in blocks because the power keeps flashing three days in :)

for i in range(28):
    
    if i < 27:
        
        links2 = links[10000*i:10000*(i+1)]
        
    else:
        
        links2 = links[270000:]

    # Go to each link and extract the desired data
    
    affiliations = []
    journals = []
    submitted = []
    revised = []
    accepted = []
    published = []
    titles = []
    abstracts = []
    keywords = []
    authors = []
        
    for link in links2:
        
        try:
            
            print('Retrieving data from link #' + str(links.index(link)+1) + ' of ' + str(len(links)))
            page = urllib.request.Request(link[:len(link)-1], headers = {'User-Agent': 'Mozilla/5.0'})
            response = urllib.request.urlopen(page)
            soup = bs(response, 'html.parser')
            data = soup.find_all('div')
            hdata = soup.find_all('h1')
            paper_affiliations = []
            bib_journals = []
            bib_years = []
            bib_keywords = []
            temp_affs = []
            no_keys = True
            
            for hd in hdata:
                
                if str(hd)[0:27] == '<h1 class="title hypothesis':
                    
                    x1 = str(hd).find('\n')
                    x2 = str(hd).find('<\h')
                    title = str(hd)[x1+1:x2]
                    titles.append(title)
            
            for dat in data:
                
                temp_keys = []
                temp_auths = []
    
                if str(dat)[0:28] == '<div class="affiliation-name':
    
                    paper_affiliations.append(dat)
    
                if str(dat)[0:25] == '<div class="bib-identity"':
    
                    bib_journals.append(dat)
    
                if str(dat)[0:23] == '<div class="pubhistory"':
    
                    bib_years.append(dat)
                    
                if str(dat)[0:24] == '<div class="art-abstract':
                    
                    x1 = str(dat).find('>')
                    x2 = str(dat).find('<a')
                    abstract = str(dat)[x1+1:x2]
                    abstracts.append(abstract)
                        
                if str(dat)[0:24] == '<div class="art-keywords':
                    
                    no_keys = False
                    spans = dat.find_all('span')
                    
                    for span in spans:
                        
                        s1 = str(spans[0]).find('>')
                        s2 = str(spans[0]).find('</span')
                        temp_keys.append(str(span)[s1+1:s2])
                    
                    keywords.append(temp_keys[0])
                    
                if str(dat)[0:23] == '<div class="art-authors':
                    
                    spans = dat.find_all('span')
                    
                    for span in spans:
                        
                        s1 = str(span).find('link__name">')
                        s2 = str(span).find('</span')
                        temp_auths.append(str(span)[s1+12:s2])
                        
                    idxset = [i for i in range(len(temp_auths)) if i%3 == 0]
                    temp_auths_clean = [temp_auths[i] for i in idxset]
                    authors.append(temp_auths_clean)
                    
            if no_keys == True:
                
                keywords.append(temp_keys)
            
            for aff in paper_affiliations:
                
                c1 = str(aff).find('>')
                c2 = str(aff)[c1+1:].find('<')
                s = str(aff)[c1+1:c1+c2+1]
                
                if affiliation_finder(str(aff)) is True:
                    
                    temp_affs.append(s)
                    
            if len(temp_affs) > 0:
    
                affiliations.append(temp_affs)
            
            else:
                
                affiliations.append('')
    
            for bib in bib_journals:
    
                yr1 = str(bib).find('<em>')
                yr2 = str(bib)[yr1+4:].find('</em>')
                journals.append(str(bib)[yr1+4:yr1+yr2+4])
    
            for bib in bib_years:
    
                j1 = str(bib).find('Received: ')
                j2 = str(bib)[j1+10:].find('/')
                submitted.append(str(bib)[j1+10:j1+j2+9])
                    
                j1 = str(bib).find('Revised: ')
                j2 = str(bib)[j1+9:].find('/')
                revised.append(str(bib)[j1+9:j1+j2+8])
                    
                j1 = str(bib).find('Accepted: ')
                j2 = str(bib)[j1+10:].find('/')
                accepted.append(str(bib)[j1+10:j1+j2+9])
                    
                j1 = str(bib).find('Published: ')
                j2 = str(bib)[j1+11:].find('<')
                published.append(str(bib)[j1+11:j1+j2+10])
            
        except:
            
            continue
    
    MDPI_df = pd.DataFrame({'Submitted': submitted, 'Revised': revised, 'Accepted': accepted,
                            'Published': published, 'Title':titles, 'Journal': journals,
                            'Affiliations': affiliations, 'Abstract': abstracts,
                            'Keywords': keywords, 'Authors': authors})
    
    MDPI_df.to_csv('C:/Users/User/Documents/Data/COVID-19/MDPI_papers_all_' + str(i+1) + '_of_28.csv', index = False, encoding = 'utf-8-sig')
    
# Combining all 28 batches into a single file

df = pd.DataFrame()

for i in range(28):
    
    temp = pd.read_csv('C:/Users/User/Documents/Data/COVID-19/MDPI_papers_all_' + str(i+1) + '_of_28.csv')
    df = pd.concat([df,temp], axis = 0)

df.to_csv('C:/Users/User/Documents/Data/COVID-19/MDPI_papers_all.csv')

