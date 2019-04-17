import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from sumy.parsers.plaintext import PlaintextParser
from sumy.parsers.html import HtmlParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
from sumy.summarizers.edmundson import EdmundsonSummarizer
from bs4 import BeautifulSoup
import requests
import random 
import keywordFetcher

linkTree = []

LANGUAGE = "english"
SENTENCES_COUNT = 8
MAX_SENTENCES_COUNT = 8

def summarize():
    """Summarize contents of urls
    This function will generate summary for contents of urls from database and extract a random 
    reference image for it and also store its title.
    """

    global linkTree
    global SENTENCES_COUNT

    for i in range(len(linkTree)):

        length_is_appropriate = False
        max_length = 90
        obj = linkTree[i]

        if not obj["abstract"] == "To be filled":
            print("Exists for ",obj["url"])
            continue

        while not length_is_appropriate:
            
            url=obj["url"]
            try:
                parser = HtmlParser.from_url(url, Tokenizer(LANGUAGE))
            
                response = requests.get(url)
                soup = BeautifulSoup(response.text,"html.parser")
                title = str(soup.find('title').text)
                
                rand = 0
                img_link = ""
                images = soup.findAll('img')
                image_count = len(images)

                if image_count < 3:
                    img_link = ""
                else: 
                    if image_count > 15:
                        rand = int(random.random() * 1000) % (image_count - 10)
                        rand = rand + 5
                    elif image_count >= 3:
                        rand = int(int(random.random() * 1000) % (image_count))

                    if "src" in images[rand]:
                        img_link = str(images[rand]['src'])
                    elif "data-src" in images[rand]:
                        img_link = str(images[rand]['data-src'])
                

                summary = ""     
                summarizer = EdmundsonSummarizer() 
                words = keywordFetcher.fetchKeyTerms()
                summarizer.bonus_words = words
                    
                words = ("another", "and", "some", "next")
                summarizer.stigma_words = words
                    
                words = ("another", "and", "some", "next")
                summarizer.null_words = words

                for sentence in summarizer(parser.document, SENTENCES_COUNT):
                    summary+=str(sentence)
                    summary+=" "
                
                if len(summary.split()) <= max_length:
                    length_is_appropriate = True
                    SENTENCES_COUNT = max
                else:
                    print(len(summary.split()))
                    SENTENCES_COUNT = SENTENCES_COUNT - 1
                    continue
                    
                obj["abstract"] = summary
                obj["title"] = title
                obj["img"] = img_link
                
                print(obj)
                linkTree[i] = obj

            except Exception as e:
                print("Error")
                print(e)
                length_is_appropriate = True
                continue

        SENTENCES_COUNT = MAX_SENTENCES_COUNT
        db.reference("linkTree").set(linkTree)

def fetch():
    global linkTree
    linkTree = db.reference("linkTree").get()
    summarize()

if __name__ == "__main__":
    cred = credentials.Certificate('config.json')
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://web-quickstart-e65e8.firebaseio.com/'
    })
    fetch()