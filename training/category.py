import numpy as np # linear algebra
import pandas as pd 
import pickle
from nltk.corpus import stopwords
import nltk
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split


count_vectorizer = pickle.load(open("./models/countvectorizer.pickle", "rb"))
transformer = pickle.load(open("./models/tfidf.pickle", "rb"))

news = pd.read_json('../datasets/News-Category/News_Category_Dataset_v2.json', lines=True)
news['information'] = news[['headline', 'short_description']].apply(lambda x: ' '.join(x), axis=1)
news.drop(news[(news['authors'] == '') & (news['short_description'] == '' )].index, inplace=True)

counts = count_vectorizer.fit_transform(news['information'].values)
tfidf = transformer.fit_transform(counts)
model = MultinomialNB()
X_train, X_test, Y_train, Y_test = train_test_split(tfidf, news['category'], test_size=0.33)
print("Training ")
model.fit(X_train, Y_train)
from sklearn.metrics import accuracy_score

y_pred = model.predict(X_test)
result = accuracy_score(Y_test, y_pred)

print("Accuracy : "+str(result))
pickle.dump(count_vectorizer, open("./models/countvectorizer.pickle", "wb"))
pickle.dump(transformer, open("./models/tfidf.pickle", "wb"))
pickle.dump(model, open("./models/model-category.pickle", "wb"))

