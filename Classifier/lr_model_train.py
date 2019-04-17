from sklearn import model_selection, preprocessing, linear_model, naive_bayes, metrics, svm
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn import decomposition, ensemble

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
train_x, valid_x, train_y, valid_y = model_selection.train_test_split(trainDF['text'], trainDF['label'])

# label encode the target variable 
encoder = preprocessing.LabelEncoder()
train_y = encoder.fit_transform(train_y)
valid_y = encoder.fit_transform(valid_y)

# create a count vectorizer object 
count_vect = CountVectorizer(analyzer='word', token_pattern=r'\w{1,}')
count_vect.fit(trainDF['text'])

# transform the training and validation data using count vectorizer object
xtrain_count =  count_vect.transform(train_x)
xvalid_count =  count_vect.transform(valid_x)

classifier=linear_model.LogisticRegression()

# fit the training dataset on the classifier
classifier.fit(xtrain_count, train_y)

#pickle
pickle.dump(count_vect, open("vectorizer.pickel", "wb"))
pickle.dump(classifier, open("classifier.pickel", "wb"))