import requests
import json
import pandas as pd
from bs4 import BeautifulSoup


#Gets the webpage data for a single URL
def getData(url):
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
}
    print("Scraping data from: " + url)
    try:
        request = requests.get(url,allow_redirects=False, timeout=10,headers=headers)
        print("Successfully received data")
        return request.text
    except requests.exceptions.Timeout as err:
        print("Error getting data from :" + url)
        print(err)
    return None

#Checks if the URL provided is looking at sold & lists the price
def checkValidURL(url):
    if url.find("sold-listings") == -1:
        return False
    if url.find("excludepricewithheld=1") == -1:
        return False
    return True

#Generates a list of all the pages for a specific search
def getAllURLs(url):
    listURLs = []
    i = url.find("&page=")
    if i != - 1:
        url = url[:i]
        print(url)
    #TODO:Change the rage back to 51, leaving at 2 for testing
    for page in range(1,51):
        listURLs.append(url + "&page=" + str(page))
    return listURLs

#Processes the raw data of the url 
#Extracts Price sold, Address, Suburb, Postcode, Numbers of beds,bathroom,parking spaces, land area
def processData(rawData):
    listings = []
    soup = BeautifulSoup(rawData,"html.parser")
    data=json.loads(soup.find("script", {"id": "__NEXT_DATA__"}).get_text())
    listListings = data["props"]["pageProps"]["componentProps"]["listingsMap"]
    for listing in listListings:
        temp={}
        listingModel = listListings[listing]["listingModel"]
        #Extract Address
        address = listingModel["address"]
        temp["StreetAddress"]= address["street"]
        temp["Suburb"] = address["suburb"]
        temp["State"] = address["state"]
        temp["Postcode"] = address["postcode"]
        #Extract Features
        features = listingModel["features"]
        temp["PropertyType"]= features["propertyType"]
        temp["LandSize"]= features["landSize"]
        temp["LandUnit"]= features["landUnit"]
        temp["IsRetirement"]= features["isRetirement"]
        if "beds" in features:
            temp["Bedrooms"] = int(features["beds"])
        if "baths" in features:
            temp["Bathrooms"] = int(features["baths"])
        if "parking" in features:
            temp["Parking"] = int(features["parking"])
        #Extract Price
        temp["price"] = listingModel["price"]
        #Extract Sale Date 
        temp["SaleDate"] = listingModel["tags"]["tagText"]
        listings.append(temp)

    return listings

def main():
    print("Beginning web scraping")
    urlInput = None
    #Ask and validate url input
    while urlInput == None:
        urlInput = input("Please enter Domain.com.au URL with sold listing & Exclude price withheld:\n")
        if checkValidURL(urlInput) == False:
            urlInput = None
    
    #Generate list of URLs for this search
    print("Generating list of URLs to scrape")
    listURLs = getAllURLs(urlInput)
    print("Generated list of URLs to scape")
    
    #Scrape data from each url
    print("Scraping data from each URL")
    listRawData = []
    for webpage in listURLs:
        listRawData.append(getData(webpage))
    print("Raw data scraped from each URL")
    
    #Extract the relevant data from the raw data
    print("Processing raw data")
    processedData = []
    for rawData in listRawData:
        processedData += processData(rawData)
    print("Raw data processed")

    #Export as CSV
    print("Exporting as housingData.csv")
    df = pd.DataFrame(processedData, columns=["StreetAddress","Suburb","Postcode","State","Bedrooms","Bathrooms","Parking","PropertyType","LandSize","LandUnit","SaleDate"])
    df.to_csv("housingData.csv")
    print("Exported as CSV")
    return None

if __name__ == "__main__":
    main()

