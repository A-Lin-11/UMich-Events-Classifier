## IMPORT STATEMENTS
import nltk
import re
import csv
import pandas as pd
import string
import numpy as np
from nltk.corpus import stopwords
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split

with open("taglist.csv", mode='r', encoding = 'utf-8') as csv_tags:
    reader=csv.reader(csv_tags)
    tagdict = dict()
    for row in reader:
        k,v = row
        tagdict[k] = v

csv_train = pd.read_csv('michigan_events - Copy.csv')
des = csv_train.description.tolist()
ttl = csv_train.title.tolist()
tag = csv_train.tags.tolist()
tags = [tagdict[i] if i in tagdict else 'Other' for i in tag]

train = ['{} {}'.format(des[i], ttl[i]) for i in range(len(des))]
train_data = pd.DataFrame(list(zip(train,tags)),columns = ['text','tag'])
train_data['text'] = train_data['text'].apply(lambda x:''.join([i.lower() for i in x
                                                  if i not in string.punctuation])).str.replace('\d+', '')
# CLASSIFIER  # 1
train, test = train_test_split(train_data, test_size = 0.2)
pipeline = Pipeline([('tfidf', TfidfVectorizer(ngram_range=(1,2),max_df = 0.92,stop_words='english')),
                  ('clf', LinearSVC(C=1.03))])
pipeline.fit(train.text, train.tag)
predicted = pipeline.predict(test.text)
print(np.mean(predicted == test.tag))
