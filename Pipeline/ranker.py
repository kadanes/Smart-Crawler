import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from selenium import webdriver
import scraper
from utils import check_ignore_terms,create_driver
import keywordFetcher
from nltk.stem.wordnet import WordNetLemmatizer

def calculate_rank():
    """Initiate the rank calculation
    This function will initiate the rank calculation for list of urls in the database.
    """

    set_key_count()
    set_rank()

def set_rank():
    """Set rank for parent urls
    This function will iterate through list of urls and will update the 
    ranks for parernts based on child urls rank.
    """

    linkTree = db.reference("linkTree").get()
    key_count_sum = {}
    child_count = {}

    for obj in linkTree:
        parent = obj["parent"]

        if parent == "none":
            continue
        else:
            key_count = obj["keyCount"]

            if (parent in key_count_sum.keys()):
                count = child_count[parent]
                child_count[parent] = count + 1

                old_key_count = key_count_sum[parent]
                key_count_sum[parent] = old_key_count + key_count

            else:
                child_count[parent] = 1
                key_count_sum[parent] = key_count 
    
    for i in range(len(linkTree)):
        
        obj = linkTree[i]
        url = obj["url"]

        if (url in child_count.keys()):
            count_val = child_count[url]
            key_count_val = key_count_sum[url]
            old_rank = obj["rank"]
            obj["rank"] = 1/2 * old_rank + 1/2 * 1/count_val * key_count_val 

            linkTree[i] = obj

            db.reference("linkTree").set(linkTree)

def set_key_count():
    """Set count of key terms
    This function will set the count of key terms for each url.
    """

    linkTree = db.reference("linkTree").get()

    for i in range(len(linkTree)):
        obj = linkTree[i]
        url = obj["url"]
        
        if "keyCount" in obj or "rank" in obj:
            print("keycount found for >",url,"<")
            continue
        else: 
            
            key_count = calc_key_count(url)

            obj["keyCount"] = key_count
            obj["rank"] = key_count

            linkTree[i] = obj

            db.reference("linkTree").set(linkTree)


def calc_key_count(url):
    """Count key terms in url
    This function will count the number of key terms for each url by analyzing its web page content.
    """
    
    lem = WordNetLemmatizer()
    driver = create_driver()
    
    driver.get(url)
    
    keywords = keywordFetcher.fetchKeyTerms()

    urltext = scraper.get_text(driver.page_source)
    urltext = urltext.split()
    urltext = [lem.lemmatize(plural).lower() for plural in urltext] 

    key_count = 0

    for i in range(len(keywords)):
        key_count += urltext.count(keywords[i])

    print(key_count)
    return key_count

if __name__ == "__main__":
    
    cred = credentials.Certificate('config.json')
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://web-quickstart-e65e8.firebaseio.com/'
    })
    
    calculate_rank()
