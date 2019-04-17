#TextRank summarization

from gensim.summarization import summarize

with open(u'sample_text.txt', 'r', encoding="utf8") as myfile:
    text=myfile.read().replace('\n', '')

print ('Summary:')
print(summarize(text, word_count=90))