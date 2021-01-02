# This script gathers paper metadata from papers accepted at MDPI journals

# Importing required modules

import urllib
from bs4 import BeautifulSoup as bs

# Defining results pages from an empty search query (there are 18326 pages)
# The selected options include page count (15 results per page), year from (2019), and year to (2020)
# Do not increase the results per page or you will not get data!

start = 'https://www.mdpi.com/search?sort=pubdate&page_no='
end = '&page_count=15&year_from=2019&year_to=2020&view=default'

# Scraping the metadata from all submissions

links = []

for i in range(18326):
   
    # Declaring which results page from the empty search query we want to scrape
   
    url = start + str(i+1) + end
    print('Retrieving data from query page ' + str(i+1) + ' of 18326.')
   
    # Getting the raw data
    
    if i == 18326:
        
        length = len(links) + 4
        
    else:
        
        length = len(links) + 15
   
    while len(links) < length:
   
        try:
           
            page = urllib.request.Request(url, headers = {'User-Agent': 'Mozilla/5.0'})
            response = urllib.request.urlopen(page)
            soup = bs(response, 'html.parser')
           
            # Making a list of the paper links from that results page
           
            data = soup.find_all('a')
            articles = []
           
            for dat in data:
               
                if str(dat)[0:21] == '<a class="title-link"':
                   
                    articles.append(dat)
           
            for art in articles:
               
                c1 = str(art).find('href="')
                c2 = str(art)[c1+6:].find('"')
                links.append('https://www.mdpi.com' + str(art)[c1+6:c1+6+c2])
                   
        except:
           
            continue
        
# Get rid of duplicate links

links = list(set(links))
       
with open('C:/Users/User/Documents/Data/COVID-19/mdpi_links.txt', 'w') as file:
   
    for link in links:
       
        file.write(str(link)+'\n')
   
    file.close()

