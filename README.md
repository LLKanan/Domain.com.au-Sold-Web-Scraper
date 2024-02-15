# Domain.com.au-Sold-Web-Scraper
Scrapes Domain.com.au Sold listings and exports to CSV

How to use:
1. Go on domain.com.au and filter for "Sold" and "exclude price withheld"
2. Add whatever you want to your search and search for it i.e I'm searching for Dayton 6055
3. Copy and paste the URL in your browser i.e "https://www.domain.com.au/sold-listings/dayton-wa-6055/?excludepricewithheld=1"
4. Run the command "python3 domainWebScraper.py"
5. When prompted enter the URL you copied from your browser earlier

Scrapes the sold data for each listing on Domain.com.au
 - Street Address
 - Suburb
 - Postcode
 - State
 - Number of Bedrooms
 - Number of Bathrooms
 - Number of Parking spots
 - Property Type
 - Land Size
 - Land Unit
 - Sale Date
