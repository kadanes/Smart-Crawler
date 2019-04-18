from sklearn import model_selection, preprocessing, linear_model, naive_bayes, metrics, svm
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, TfidfTransformer
from sklearn import decomposition, ensemble
from nltk.stem.snowball import SnowballStemmer
import pandas, xgboost, numpy, textblob, string
import pickle

# load the dataset
data = open('webpagetraining.csv', encoding="utf-8").read()
labels, texts = [], []
lines=data.split("\n")
for line in lines:
    if line.strip():
        content = line.split(',')
        texts.append(content[0])
        labels.append(content[1])

# create a dataframe using texts and lables
trainDF = pandas.DataFrame()
trainDF['text'] = texts
trainDF['label'] = labels

# split the dataset into training and validation datasets 
train_x, valid_x, train_y, valid_y = model_selection.train_test_split(trainDF['text'], trainDF['label'], test_size=0.3)

# label encode the target variable 
encoder = preprocessing.LabelEncoder()
train_y = encoder.fit_transform(train_y)
valid_y = encoder.fit_transform(valid_y)

# transform the training and validation data using stemmed count vectorizer object
stemmer = SnowballStemmer("english", ignore_stopwords=True)

class StemmedCountVectorizer(CountVectorizer):
    def build_analyzer(self):
        analyzer = super(StemmedCountVectorizer, self).build_analyzer()
        return lambda doc: ([stemmer.stem(w) for w in analyzer(doc)])

stemmed_count_vect = StemmedCountVectorizer(stop_words='english')

xtrain_count =  stemmed_count_vect.fit_transform(train_x)
xvalid_count =  stemmed_count_vect.transform(valid_x)

tfidf_transformer = TfidfTransformer()
xtrain_tfidf = tfidf_transformer.fit_transform(xtrain_count)
xvalid_tfidf = tfidf_transformer.fit_transform(xvalid_count)

# create a classifier model
classifier=naive_bayes.MultinomialNB(fit_prior=False)

# fit the training dataset on the classifier
classifier.fit(xtrain_tfidf, train_y)

# predict the labels on validation dataset
predictions = classifier.predict(xvalid_tfidf)
print("Accuracy: ", metrics.accuracy_score(predictions, valid_y))