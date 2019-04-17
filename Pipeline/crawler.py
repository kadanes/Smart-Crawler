import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import collections
import logging
import scraper
import classifier
import keywordFetcher
from nltk.stem.wordnet import WordNetLemmatizer
from utils import check_ignore_terms,create_driver

found_links = []
linkTree = []

def get_all_links(url):
    """Get all child URLs of a parent
    This function will fetch all urls that are present on a parent webpage
    It will ignore already crawled urls, urls that refer to self, 
    or those within the list of ignored domains.
    """

    driver = create_driver()
    links=[]

    try:
        driver.get(url)
    except Exception as e:
            logging.exception(e)
            return

    for a in driver.find_elements_by_xpath('.//a'):
        
        link = a.get_attribute('href')

        if check_ignore_terms(link):
            print(">",link,"< contains ignore term")

        elif not link is None and "#" in link: 
            parts = link.split("#")
            if parts[0] not in found_links:
                links.append(parts[0])
            else:
                print(">",link,"< dropping repeat url containing #")

        elif link not in found_links:
            links.append(link)

        else:
            print(">",link,"< exists.")

    return links

def recursive_crawl(url, maxdepth):
    """Recursively crawl a url till you reach a maximum depth
    This function will crawl all the child urls of a parent level by level
    using BFS searching. The max depth value will be used to limit the levels
    crawled.
    """

    global found_links
    global linkTree

    visited_links=[]
    queue_links=collections.deque()

    if is_url_relevant(url):
        queue_links.extend([url, 'null'])

    depth=0

    while queue_links: 
        current_link = queue_links.popleft()
        if(current_link=='null'):
            depth+=1
            if depth>=maxdepth:
                break
            if queue_links:
                queue_links.append('null')
            continue
    
        visited_links.append(current_link)
        
        received_links = get_all_links(current_link)
        for link in received_links:
            
            if not link is None and link not in visited_links and link not in queue_links and is_url_relevant(link):
                print("Appended: "+link)
                queue_links.append(link)
                found_links.append(link)

                urlObj = {"parent":current_link,"keywords":getParentKeywords(current_link),"url":link,"abstract":"To be filled","likes":[],"dislikes":[]}
                linkTree.append(urlObj)

                db.reference("linkTree").set(linkTree)
                db.reference("links").set(found_links)



def is_url_relevant(url):
    """Check if a url is relevant
    This function will check if a url is classified as relevant and 
    if it has relevent keyword.
    """

    driver = create_driver()
    driver.get(url)
    
    print("Checking:",url)
    urltext = scraper.get_text(driver.page_source)
    value = classifier.predict([urltext]) 
    keyword_relevance=isKeywordPresent(urltext)
    relevant = value and keyword_relevance
    print("Relavent: ",relevant)

    return relevant

def isKeywordPresent(text):
    """Check if keywords are present in passed text
    This function will check if the passed text has keywords for a perticular event
    """
    lem = WordNetLemmatizer()

    keywords=set(keywordFetcher.fetchKeyTerms())

    text_set = text.split()
    text_set = [lem.lemmatize(plural) for plural in text_set] 
    text_set = set(text_set)

    if len(keywords.intersection(text_set))>1:
        return True
    else:
        return False

def getParentKeywords(link):
    """Fetch keyword object assigned to parent
    This function will find the parent of a child link and return keywords
    assigned to it.
    """

    for linkObj in linkTree:
        if(linkObj['url'] == link):
            if 'keywords' in linkObj:
                return linkObj['keywords']
            else:
                print('no keywords')
                return []

def seedCrawler():
    """Start the crawling from seed urls
    This function will fetch seed urls from list of all urls and start 
    crawling them.
    """

    global found_links
    global linkTree

    found_links = db.reference("links").get()
    linkTree = db.reference("linkTree").get()
    seedurls = []

    for obj in linkTree:
        link = obj['url']
        parent = obj['parent']
        if parent == "none":
            seedurls.append(link)

    if found_links is None:
        found_links = []

    if linkTree is None:
        linkTree = []

    for seedurl in seedurls:
        print("Seed: "+seedurl)
        recursive_crawl(seedurl, 1)


if __name__ == "__main__":
    cred = credentials.Certificate('config.json')
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://web-quickstart-e65e8.firebaseio.com/'
    })
    seedCrawler()    