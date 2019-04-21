import firebase_admin
from firebase_admin import db
from firebase_admin import credentials
import datetime
import json
from nltk.stem.wordnet import WordNetLemmatizer

def fetchKeywords():
    """Fetch list of keywords 
    This function will fetch list of keywords for a relevent event based on 
    the current date.
    """

    current_ts = datetime.datetime.now().timestamp()
    events_ts = db.reference("eventCalendar").get()

    for ts in sorted(events_ts.keys()):
        if current_ts > float(ts):
            val = events_ts[ts]
            keywords = db.reference("keywords/"+val).get()

            for i in range(len(keywords)):
                keywords[i] = val +" "+ keywords[i]
            
            return keywords

def fetchKeyTerms():
    """Get a list of key terms  
    This function will fetch list of keyterms from the keywords defined for a 
    relevent event based on the current date.
    """

    tabooWords = ["make","to","creative","your","fun"]

    key_terms = fetchKeywords()
    temp = []
    lem = WordNetLemmatizer()

    for term in key_terms:
        split_terms = term.split()
        for split_term in split_terms:
            if not split_term in tabooWords and not lem.lemmatize(split_term) in temp:
                temp.append(lem.lemmatize(split_term))

    key_terms = temp
    return key_terms

if __name__ == "__main__":
    cred = credentials.Certificate('config.json')
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://smartcrawler-75efe.firebaseio.com'
    })
    fetchKeywords()
    
    
