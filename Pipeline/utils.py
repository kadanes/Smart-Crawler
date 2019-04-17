from selenium.webdriver.chrome.options import Options
import sys
from selenium import webdriver

ignore_terms = [
"quora",
"linkedin",
"pinterest",
"twitter",
"youtube",
"profile",
"plus.google",
"facebook",
"privacy",
"careers",
"duckduckgo",
"about",
"profile",
"indiamart",
"amazon",
"flipkart",
"shopclues",
"shutterstock",
"pepperfry",
"paperlanternstore",
"mshop.rediff"
]

def check_ignore_terms(link):
    """Ignore domains that generate spammy irrelevant content
    This function will check the url for presence of particular terms that are indicative of 
    spam website.
    """

    for i in range(len(ignore_terms)):
        if not link is None and ignore_terms[i] in link:
            print("Found term: ",ignore_terms[i]," in link")
            return True
    return False

def create_driver():
    """Create driver for web crawling
    This function will create an operating system specific instance of chrome driver to help 
    in crawling.
    """

    chromeOptions = Options()
    chromeOptions.add_argument("--headless")
    chromeOptions.add_argument("--window-size=1920x1080")
    os = get_platform()
    if  os == "OS X":
        chromedriver = r"./chromedriver"
    elif os == "Windows":
        chromedriver = r"./chromedriver.exe"
    driver = webdriver.Chrome(chrome_options=chromeOptions, executable_path=chromedriver)
    return driver

def get_platform():
    """Find the operating system
    This function will return the current os name.
    """

    platforms = {
        'linux1' : 'Linux',
        'linux2' : 'Linux',
        'darwin' : 'OS X',
        'win32' : 'Windows'
    }
    
    if sys.platform not in platforms:
        return sys.platform
    
    return platforms[sys.platform]