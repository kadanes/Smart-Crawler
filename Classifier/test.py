import pickle
import pandas as pd

classifier=pickle.load(open("classifier.pickel", "rb"))
count_vect=pickle.load(open("vectorizer.pickel", "rb"))

data = pd.read_csv('webpagetesting.csv', encoding="utf-8")

xtest_count =  count_vect.transform(data['Text'])

predictions = classifier.predict(xtest_count)
print(predictions)