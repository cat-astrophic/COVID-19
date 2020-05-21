# This script gets data on papers posted to the arXiv

""" NOTE TO USERS:
    
    Specify the directory for storing data - lines 154, 160, 166, 172, 179 """

# Importing required modules

import urllib
from bs4 import BeautifulSoup as bs

# Initializing lists for storing the data

submission_dates = []
updated_dates = []
category_data = []
authorship_data = []
affiliation_data = []

# Creating the components of the query url

base = 'http://export.arxiv.org/api/query?search_query=all:'
mid = '&start='
end = '&max_results=1000&sortBy=submittedDate&sortOrder=descending'

# List of year month combinations for id query

yymm = ['1901', '1902', '1903', '1904', '1905', '1906', '1907', '1908', '1909',
        '1910', '1911', '1912', '2001', '2002', '2003', '2004', '2005']

# Running the outer loop

for ym in yymm:
    
    # Resetting start, flags, and yflag to 0 for each ym in yymm
    
    start = 0 # part of the url
    flags = 0 # indicator that there is no more data to harvest
    yflag = 0 # year indicator for turning off current query
    
    # Outer loop progress checker
    
    print('Harvesting data for ' + ym + '...')
    
    # Running the inner loop
    
    while flags < 10 and yflag < 1:
        
        # Specifying the url
        
        url = base + ym + mid + str(start) + end
        
        # Inner loop progress checker
        
        print('Harvesting data for entries ' + str(start) + ' through ' + str(start+999) + '...')
        
        # Getting the raw data from the url with bs4
        
        page = urllib.request.Request(url, headers = {'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(page)
        soup = bs(response, 'html.parser')
        
        # Separates the metadata for each paper into its own entry in a list
        
        raw_data = soup.find_all('entry')
        
        # Makes sure that the query was successful
        
        if len(raw_data) < 2:
            
            # If the query does not return data, increase the value of flags
            
            flags += 1        
        
        # If the query returned data, parse it
        
        else:
        
            # Checking to make sure all entries are from the correct year (uses the sortOrder parameter)
            
            if str(raw_data[len(raw_data)-1].find_all('published')[0])[13:15] != ym[:2]:

                # Initialize a flag called finished as false
                
                finished = False
                
                # Find the cut-off for correct year
                
                while finished != True:
                    
                    for raw in raw_data:
                        
                        if str(raw.find_all('published')[0])[13:15] != ym[:2]:
                            
                            finished = True
                            ind = raw_data.index(raw) - 1
                            
                raw_data = raw_data[0:ind]
                yflag = 1
            
            # Extracting the desired metadata from each paper and appending it to the appropriate lists
            
            for raw in raw_data:
                
                # Get the submission date and priary arxiv category for the paper
                
                date = raw.find_all('published')
                update = raw.find_all('updated')
                cat = raw.find_all('arxiv:primary_category')
                
                # Isolate each author to extract author level metadata
                
                # Create a list of authors on the paper (includes their affiliation data)
                
                authors = raw.find_all('author')
                
                # Get each author name and affilation for the paper
                
                auths = []
                affils = []
                
                for a in authors:
                    
                    auths.append(a.find_all('name'))
                    affils.append(a.find_all('arxiv:affiliation'))
                
                # Removing tags from the metadata
                
                date2 = str(date)[12:22]
                update2 = str(update)[10:20]
                cat2 = str(cat)[str(cat).find('term="')+6:str(cat).find('" xmlns:arxiv')]
                auths2 = [str(a)[7:len(str(a))-8] for a in auths]
                affils2 = [str(a)[64:len(str(a))-21] for a in affils]
                
                # Appending the metadata from each paper to the appropriate lists
                
                submission_dates.append(date2) # In YYYY-MM-DD format
                updated_dates.append(update2) # In YYYY-MM-DD format
                category_data.append(cat2)
                authorship_data.append(auths2)
                affiliation_data.append(affils2)
            
            # Increase start value for next query
            
            start = start + 1000

# Writing results as .txt files

with open('C:/Users/M535040/Documents/Data/COVID-19/category_data.txt', 'w') as file:
    
    for entry in category_data:
    
        file.write('%s\n' % entry)

with open('C:/Users/M535040/Documents/Data/COVID-19/submission_dates.txt', 'w') as file:
    
    for entry in submission_dates:
    
        file.write('%s\n' % entry)

with open('C:/Users/M535040/Documents/Data/COVID-19/updated_dates.txt', 'w') as file:
    
    for entry in updated_dates:
    
        file.write('%s\n' % entry)

with open('C:/Users/M535040/Documents/Data/COVID-19/affiliation_data.txt', 'w', encoding = 'utf-8') as file:
    
    for row in range(len(affiliation_data)):
        
        entry = str(affiliation_data[row])
        file.write('%s\n' % entry)

with open('C:/Users/M535040/Documents/Data/COVID-19/authorship_data.txt', 'w', encoding = 'utf-8') as file:
    
    for row in range(len(authorship_data)):
        
        entry = str(authorship_data[row])
        file.write('%s\n' % entry)

