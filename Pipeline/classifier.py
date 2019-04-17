import pickle
import pandas as pd
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import CountVectorizer

def predict(testdata):
    """Predict if relevent
    This function will check if the text passed belongs to a relevant web page.
    """

    classifier_model=pickle.load(open("classifier.pickel", "rb"))
    vect_vocab=pickle.load(open("vectorizer_vocabulary.pickel", "rb"))
    tfidf_transformer=pickle.load(open("tfidf_transformer.pickel", "rb"))

    stemmer = SnowballStemmer("english", ignore_stopwords=True)

    class StemmedCountVectorizer(CountVectorizer):
        def build_analyzer(self):
            analyzer = super(StemmedCountVectorizer, self).build_analyzer()
            return lambda doc: ([stemmer.stem(w) for w in analyzer(doc)])

    stemmed_count_vect = StemmedCountVectorizer(stop_words='english', vocabulary=vect_vocab)

    xtest_count =  stemmed_count_vect.transform(testdata)
    xtest_tfidf = tfidf_transformer.transform(xtest_count)

    predictions = classifier_model.predict(xtest_tfidf)
    return(predictions[0])