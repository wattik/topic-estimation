# -*- coding: utf-8 -*-
#!/usr/bin/python

__author__ = 'Wattik'

import sys
from nltk.tokenize import word_tokenize
from nltk.util import ngrams

"""
The script estimates topics of a short text based on Wikipedia categories.

It's expected that first argument is the text. For example:

    python topic-estimation "First documented in the 13th century, Berlin was the capital of the Kingdom of Prussia (1701–1918), the German Empire (1871–1918), the Weimar Republic (1919–33) and the Third Reich (1933–45)."


The output is a set of topics. (TBD...)

"""


# Functions ##################################

def estimate_topics(text):

    if len(text) == 0:
        raise Exception("Text is not long enough.")

    # Basic preprocessing such as: utf-8 encoding, lowercasing
    text = preprocess(text)

    # Breaking apart into n-grams, so far n=3
    tokens = tokenize(text, 3)

    # TODO: ?????
    # additional layers and filters here
    # Synonyms etc
    # Stemmatization, lemmatization, stopwords, etc.

    # Given tokens find categories in wiki's net. Go 2 levels deep.
    proposed_topics = find_topics(tokens, 2)

    # Choose the best proposals of all proposed topics.
    topics = filter_topics(proposed_topics)

    return topics


def preprocess(text):
    text = unicode(text, 'utf-8')
    text = text.lower()
    return text


def tokenize(text, n):
    if n < 1:
        raise Exception("N-grams require n >= 1.")

    # Create tokens from the text.
    unigrams = word_tokenize(text)

    # Get rid of '.', ',' and etc.
    blacklist = [u'.', u',']
    unigrams = [unigram for unigram in unigrams if unigram not in blacklist]

    # Create n-grams
    tokens = unigrams
    for i in xrange(2, n+1):
        tokens = tokens + list(ngrams(unigrams, i))

    return tokens


def find_topics(tokens, order):
    topics = dict()
    for token in tokens:


    proposed_topics = tokens
    return proposed_topics


def filter_topics(proposed_topics):
    # TODO
    topics = proposed_topics
    return topics


# Main: ##################################

if __name__ == "__main__":
    #topics = estimate_topics(sys.argv[1])

    # TODO: Return the topic. Could be just a set? Maybe dictionary of key and confidence.


    print estimate_topics("The world isn't fair")