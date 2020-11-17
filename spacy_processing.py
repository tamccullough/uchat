#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd

import spacy
import string
from spacy.lang.en import English
from spacy.lang.en.stop_words import STOP_WORDS
from spacy.symbols import nsubj, VERB

'''from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
from sklearn.base import TransformerMixin
from sklearn.pipeline import Pipeline'''

nlp = English()
smdl = spacy.load('en_core_web_sm') # load a model to get subjects
sbd = nlp.create_pipe('sentencizer')
nlp.add_pipe(sbd)

# Load English tokenizer, tagger, parser, NER and word vectors
parser = English()
# Create our list of punctuation marks
punctuations = string.punctuation
# Create our list of stopwords
stop_words = spacy.lang.en.stop_words.STOP_WORDS

# Basic function to clean the text
def clean_text(text):
    # Removing spaces and converting text into lowercase
    return text.strip().lower()

# Creating our tokenizer function
def spacy_tokenizer(sentence):
    # Creating our token object, which is used to create documents with linguistic annotations.
    mytokens = parser(sentence)
    # Lemmatizing each token and converting each token into lowercase
    mytokens = [ word.lemma_.lower().strip() if word.lemma_ != "-PRON-" else word.lower_ for word in mytokens ]
    # Removing stop words
    mytokens = ' '.join([ word for word in mytokens if word not in stop_words and word not in punctuations ])
    # return preprocessed list of tokens
    return mytokens

# Creating our tokenizer function
def remove_punctuation(sentence):
    # Creating our token object, which is used to create documents with linguistic annotations.
    mytokens = parser(sentence)
    # Lemmatizing each token and converting each token into lowercase
    mytokens = [ word.lemma_.lower().strip() if word.lemma_ != "-PRON-" else word.lower_ for word in mytokens ]
    # Removing stop words
    mytokens = ' '.join([ word for word in mytokens if word not in punctuations ])
    # return preprocessed list of tokens
    return mytokens

'''# Custom transformer using spaCy
class predictors(TransformerMixin):
    def transform(self, X, **transform_params):
        # Cleaning Text
        return [clean_text(text) for text in X]

    def fit(self, X, y=None, **fit_params):
        return self

    def get_params(self, deep=True):
        return {}'''

# this function assigns the appropriate questions to the correct tag and intent
def add_subject(word_list,data):
    doc = []
    for i in data.index:
        v = word_list[i]
        w = data[i]
        doc.append((v,w))
    return doc
# clean up function to remove tuples and list the tokens, and then removes doubles of any tokens
def clean_tup(data):
    l = []
    for t in data:
        l.append(t)
    l = list(dict.fromkeys(l))
    return l

# using space model to get the subject of the sentence
def find_subject(sentence):
    doc = smdl(sentence)
    for token in doc:
        if token.dep_ == "nsubj":
            if token.text == 'I':
                if token.dep_ == 'ROOT':
                    return token.text
                else:
                    return 'no subject'
            else:
                return token.text
        else:
            return 'no subject'
