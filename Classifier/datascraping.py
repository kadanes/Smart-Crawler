import random
import re
import requests
from bs4 import BeautifulSoup
from bs4.element import Comment
import csv

def getData(url):
    proxy=select_proxy()

    try:
        page = requests.get(url[0])        #to extract page from website  proxies={"http": proxy, "https": proxy}
        html_code = page.content        #to extract html code from page

        text_string = text_from_html(html_code)
        text_string = clean_text(text_string)
    
        with open('webpagetraining.csv','a', newline='', encoding="utf-8") as csv_file:
            writer=csv.writer(csv_file)
            writer.writerow([text_string, url[1]])

    except Exception as e:
        print(e)

def select_proxy():
    proxies = ['62.44.16.177:50781', '125.26.99.204:37142', '116.203.1.180:1994', '188.125.40.79:41087', '187.176.123.155:54438']
    return (random.choice(proxies))

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)  
    return u" ".join(t.strip() for t in visible_texts)

def clean_text(string):
    string=remove_emoji(string)
    string=string.replace('\n', ' ').replace('\r', '')
    string=string.replace(',', '')
    string =' '.join(string.split())
    return string

def remove_emoji(string):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)

urls=[['https://sadtohappyproject.com/diy-paper-lanterns-and-lamps/', 'Yes'], ['https://www.livinghours.com/diwali-lanterns/', 'Yes'], ['http://www.artplatter.com/2011/06/how-to-make-a-paper-bag/', 'Yes'], ['https://www.allfreejewelrymaking.com/Recycled-Jewelry/Jewelry-Designs-from-Household-Items', 'Yes'], ['https://www.tasteofhome.com/collection/homemade-food-gift-packaging-ideas/view-all/', 'Yes'], ['https://www.instructables.com/id/Handmade-Decorative-Diya-Oil-Lamps/', 'Yes'], ['https://buggyandbuddy.com/make-kite/', 'Yes'], 
            ['https://www.sbs.com.au/yourlanguage/hindi/en/audiotrack/why-do-we-light-diyas-diwali', 'No'], ['https://medium.com/the-new-york-times/more-startups-have-an-unfamiliar-message-for-venture-capitalists-get-lost-d2bbb86db39b', 'No'], ['https://www.sciencedirect.com/topics/agricultural-and-biological-sciences/rural-development', 'No'], ['https://www.mybeautynaturally.com/femgetsetglow/5-decorative-items.aspx', 'No'], ['https://en.wikipedia.org/wiki/Diya_(lamp)', 'No'], ['https://zeenews.india.com/exclusive/diwali-significance-of-a-diya_5820.html', 'No'], ['https://muktiskitchen.com/happy-breakfast-on-a-diwali-morning-and-a-special-recipe/', 'No'], ['https://kids.nationalgeographic.com/explore/diwali/', 'No']]

for url in urls:
    getData(url)