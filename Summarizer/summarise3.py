# LSA, Luhn, Edmundson, LexRank summarizers

from sumy.parsers.plaintext import PlaintextParser
from sumy.parsers.html import HtmlParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.summarizers.edmundson import EdmundsonSummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer

LANGUAGE = "english"
SENTENCES_COUNT = 10

url="https://en.wikipedia.org/wiki/Artificial_intelligence"

parser = HtmlParser.from_url(url, Tokenizer(LANGUAGE))

summary1 = ""

print("\n\n")
print ("--LsaSummarizer--")    
summarizer = LsaSummarizer()
summarizer = LsaSummarizer(Stemmer(LANGUAGE))
summarizer.stop_words = get_stop_words(LANGUAGE)

for sentence in summarizer(parser.document, SENTENCES_COUNT):
    summary1+=str(sentence)
    summary1+=" "

with open("summarised_text.txt", "w", encoding="utf8") as myfile:
    myfile.write("\n\nLSA:\n")
    myfile.write(summary1)

summary2 = ""
print("\n\n")
print ("--LuhnSummarizer--")     
summarizer = LuhnSummarizer() 
summarizer = LsaSummarizer(Stemmer(LANGUAGE))
summarizer.stop_words = get_stop_words(LANGUAGE)

for sentence in summarizer(parser.document, SENTENCES_COUNT):
    summary2+=str(sentence)
    summary2+=" "

with open("summarised_text.txt", "a", encoding="utf8") as myfile:
    myfile.write("\n\nLuhn:\n")
    myfile.write(summary2)

summary3 = ""
print("\n\n")
print ("--EdmundsonSummarizer--")     
summarizer = EdmundsonSummarizer() 
words = ("deep", "learning", "neural" )
summarizer.bonus_words = words
    
words = ("another", "and", "some", "next",)
summarizer.stigma_words = words
    
words = ("another", "and", "some", "next",)
summarizer.null_words = words

for sentence in summarizer(parser.document, SENTENCES_COUNT):
    summary3+=str(sentence)
    summary3+=" "

with open("summarised_text.txt", "a", encoding="utf8") as myfile:
    myfile.write("\n\nEdmundson:\n")
    myfile.write(summary3)

summary4 = ""
print("\n\n")
print ("--LexRankSummarizer--")
summarizer = LexRankSummarizer()
summarizer = LexRankSummarizer(Stemmer(LANGUAGE))
summarizer.stop_words = get_stop_words(LANGUAGE)

for sentence in summarizer(parser.document, SENTENCES_COUNT):
    summary4+=str(sentence)
    summary4+=" "

with open("summarised_text.txt", "a", encoding="utf8") as myfile:
    myfile.write("\n\nLexRank:\n")
    myfile.write(summary4)