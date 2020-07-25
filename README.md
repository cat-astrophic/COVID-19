# COVID-19

This repo contains code to determine if there has been an impact on the academic publishing process due to COVID-19. The data is sourced from a combination of web scraping (MDPI) and API requests (arXiv).

### Setup

* **arxiv_metadata_scraper** scrapes metadata on papers published to the arXiv
* **mdpi_link_finder** gets urls for mdpi papers
* **mdpi_metadata_scraper** scrapes metadata from mpdi papers
* **mdpi_data_cleaner** cleans raw metadata from mdpi papers + datetime calculations
* **mdpi_add_FM** adds Frascati Manual category for each journal to the dataframe
* **mdpi_add_arxiv** creates arXiv count data and adds it to the main dataframe
* **mdpi_frdd** runs main models, etc.
