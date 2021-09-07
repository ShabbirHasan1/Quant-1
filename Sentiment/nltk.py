# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 18:07:50 2021

@author: User
"""

""" Vectorising documents using NLTL """

import nltk
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

text = 'I am not a sentimental person but I believe in the utility of sentiment analysis'

# Tokenisation
from nltk.tokenize import word_tokenize
tokens = word_tokenize(text)
print(tokens)

# Lemmatisation
from nltk.stem import WordNetLemmatizer
lemmatiser = WordNetLemmatizer()
tokens = [lemmatiser.lemmatize(word) for word in tokens]

# Stemming 
from nltk.stem import PorterStemmer
tokens = word_tokenize(text.lower())
ps = PorterStemmer()
tokens = [ps.stem(word) for word in tokens]
print(tokens)

# Stop Words
stopwords = nltk.corpus.stopwords.words('english')
print(stopwords)

tokens_new = [j for j in tokens if j not in stopwords]
