import firebase_admin
from firebase_admin import db
from firebase_admin import credentials
import requests
import urllib
import json
from bs4 import BeautifulSoup
import furl
from utils import check_ignore_terms

def get_seed_urls(inQueries):
    """Generate seed urls
    This function will generate seed urls from set of keywords.
    """

    for i in range(len(inQueries)):

        #Query terms will be dynamically imported from query database
        query = inQueries[i]
        query = urllib.parse.quote_plus(query)

        #A google search url will be formed out of it
        url = "https://www.google.com/search?q="+query

        #The response will be parsed using beautiful soup
        response = requests.get(url)
        soup = BeautifulSoup(response.text,"html.parser")

        # List of search results
        found_links = db.reference("links").get()
        linkTree = db.reference("linkTree").get()

        if found_links is None:
            found_links = []

        if linkTree is None:
            linkTree = []

        #Div with class g contains relevent links
        for item in soup.find_all('div', attrs={'class':'g'}):
            for links in item.find_all('a'):
                #[7:] skips first 7 characters. These characters are '/url?q='
                query_result = links['href'][7:]
                #Filter links that point to default google urls
                #check for well formed urls
                if "google" not in query_result.lower():
                    #Clean results
                    cleanUrl = furl.furl(query_result).remove(args=True, fragment=True).url
                    cleanUrl = cleanUrl.split('&')[0]
                    if (not cleanUrl in found_links and cleanUrl != "" and not check_ignore_terms(cleanUrl)):
                        found_links.append(cleanUrl)
                        print(cleanUrl)
                        urlObj = {"parent":"none","keywords":query.split("+"),"url":cleanUrl,"abstract":"To be filled","likes":[],"dislikes":[]}
                        linkTree.append(urlObj)

        db.reference("linkTree").set(linkTree)
        db.reference("links").set(found_links)

    return found_links

if __name__ == "__main__":
    cred = credentials.Certificate('config.json')
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://smartcrawler-75efe.firebaseio.com'
    })
    get_seed_urls(["diwali make your decoration"])