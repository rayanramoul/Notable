import numpy as np # linear algebra
import pandas as pd 
import pickle

from sklearn.linear_model import LogisticRegression
logreg = LogisticRegression(C=1e5)
count_vectorizer = pickle.load(open("./models/countvectorizer.pickle", "rb"))
transformer = pickle.load(open("./models/tfidf.pickle", "rb"))
#1 =  Fake
#0: Not a Fake
import os
dirpath = os.getcwd()
print("current directory is : " + dirpath)
train=pd.read_csv('../datasets/fake-news/train.csv')
test=pd.read_csv('../datasets/fake-news/test.csv')
test.info()
test['label']='t'
train.info()

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfTransformer

test=test.fillna(' ')
train=train.fillna(' ')
#test['total']=test['text']
#train['total']=train['text']
#print("Shape of input : "+str(train['total'].shape))

counts = count_vectorizer.fit_transform(train['text'].values)
tfidf = transformer.fit_transform(counts)

targets = train['label'].values
test_counts = count_vectorizer.fit_transform(test['text'].values)
test_tfidf = transformer.fit_transform(test_counts)

#split in samples
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(tfidf, targets, random_state=0)
logreg.fit(X_train, y_train)
print('ACCURACY TRAIN :  {:.2f}'.format(logreg.score(X_train, y_train)))
print('ACCURAY TEST : {:.2f}'.format(logreg.score(X_test, y_test)))


pickle.dump(logreg, open("./models/model-fakenews.pickle", "wb"))
pickle.dump(count_vectorizer, open("./models/countvectorizer.pickle", "wb"))
pickle.dump(transformer, open("./models/tfidf.pickle", "wb"))