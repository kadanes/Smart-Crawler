from bs4 import BeautifulSoup
import re
from bs4.element import Comment
from utils import create_driver

def get_text(html_code):
    """Get text from webpage content
    This function will parse the webpage and return a cleaned text content.
    """

    text_string = text_from_html(html_code)
    text_string = clean_text(text_string)
    return text_string

def text_from_html(body):
    """Get needed text content from web page content
    This function will return only text that matter in a webpage. 
    """

    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)  
    return u" ".join(t.strip() for t in visible_texts)

def tag_visible(element):
    """Filter unneeded tags
    This function will filter out tags that are not needed and reutrn true only if tag 
    matters. 
    """

    if element.parent.name in ['style', 'script', 'head', 'title', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def clean_text(string):
    """Clean text
    This function will clean text and remove escape characters and spaces. 
    """

    string=remove_emoji(string)
    string=string.replace('\n', ' ').replace('\r', '')
    string=string.replace(',', '')
    string =' '.join(string.split())
    return string

def remove_emoji(string):
    """Clean text
    This function will clean text and remove emoji characters. 
    """

    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)

if __name__ == "__main__":
    url = 'https://defenders.org/butterflies/basic-facts' 
    driver = create_driver()
    driver.get(url)
    print(get_text(driver.page_source)) #demo run
    driver.close()