import seedStorer
import crawler
import firebase_admin
import summarizer
import keywordFetcher
import ranker

from firebase_admin import credentials

if __name__ == '__main__':

    cred = credentials.Certificate('config.json')
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://web-quickstart-e65e8.firebaseio.com/'
    })
    
    print("Keywords")
    keywords = keywordFetcher.fetchKeywords()
    print(keywords)
    
    print("Seed")
    seedStorer.get_seed_urls(keywords)

    print("Crawl")
    crawler.seedCrawler()

    print("Rank")
    ranker.calculate_rank()

    print("Summarise")
    summarizer.fetch()