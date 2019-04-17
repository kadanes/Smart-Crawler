from sklearn import model_selection, preprocessing, linear_model, naive_bayes, metrics, svm
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, TfidfTransformer
from sklearn import decomposition, ensemble
from nltk.stem.snowball import SnowballStemmer
import pandas, xgboost, numpy, textblob, string
import pickle

# load the dataset
data = open('webpagetraining1.csv', encoding="utf-8").read()
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

# create a count vectorizer object 
#count_vect = CountVectorizer(analyzer='word', token_pattern=r'\w{1,}')
#count_vect.fit(trainDF['text'])

# transform the training and validation data using count vectorizer object

stemmer = SnowballStemmer("english", ignore_stopwords=True)

class StemmedCountVectorizer(CountVectorizer):
    def build_analyzer(self):
        analyzer = super(StemmedCountVectorizer, self).build_analyzer()
        return lambda doc: ([stemmer.stem(w) for w in analyzer(doc)])

stemmed_count_vect = StemmedCountVectorizer(stop_words='english')

xtrain_count =  stemmed_count_vect.fit_transform(train_x)
xvalid_count =  stemmed_count_vect.transform(valid_x)
#print(stemmed_count_vect.vocabulary)
#print(xtrain_count.shape)

tfidf_transformer = TfidfTransformer()
xtrain_tfidf = tfidf_transformer.fit_transform(xtrain_count)
xvalid_tfidf = tfidf_transformer.fit_transform(xvalid_count)
#print(xtrain_tfidf.shape)

# create a classifier model
classifier=linear_model.SGDClassifier(loss='hinge', penalty='l2',alpha=1e-3, random_state=42, max_iter=5, tol=None)

# fit the training dataset on the classifier
classifier.fit(xtrain_tfidf, train_y)

# predict the labels on validation dataset
predictions = classifier.predict(xvalid_tfidf)
print("Accuracy: ", metrics.accuracy_score(predictions, valid_y))

#pickle
'''pickle.dump(stemmed_count_vect.vocabulary_, open("vectorizer_vocabulary.pickel", "wb"))
pickle.dump(tfidf_transformer, open("tfidf_transformer.pickel", "wb"))
pickle.dump(classifier, open("classifier.pickel", "wb"))'''