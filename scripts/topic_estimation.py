# -*- coding: utf-8 -*-
#!/usr/bin/python

__author__ = 'Wattik'

import sys
from nltk.tokenize import word_tokenize
from nltk.util import ngrams
from categories_utils import Token2Topic, Topic
from wikipedia_utils import *

"""
The script estimates topics of a short text based on Wikipedia categories.

It's expected that first argument is the text. For example:

    python topic-estimation "First documented in the 13th century, Berlin was the capital of the Kingdom of Prussia (1701–1918), the German Empire (1871–1918), the Weimar Republic (1919–33) and the Third Reich (1933–45)."


The output is a set of topics. (TBD...)

"""

class TopicEstimator(object):

    DEBUG = True

    def __init__(self, wiki, n = 3, level = 2):
        self.level = level
        self.n = n
        self.wiki = wiki


    def estimate_topic(self, text):

        if len(text) == 0:
            raise Exception("Text is not long enough.")

        # Basic preprocessing such as: utf-8 encoding, lowercasing
        text = self._preprocess(text)

        # Breaking apart into n-grams, so far n=3
        tokens = self._tokenize(text)

        # TODO: additional filtering of words
        # additional layers and filters here
        # Synonyms etc
        # Stemmatization, lemmatization, stopwords, etc.


        # Given tokens find categories in wiki's net. Go 2 levels deep.
        proposed_topics, list_of_parents = self._find_topics(tokens)

        # Choose the best proposals of all proposed topics.
        frequencies = self._filter_topics(proposed_topics)

        return frequencies, list_of_parents


    def _preprocess(self, text):
        if not isinstance(text, unicode):
            text = unicode(text, 'utf-8')
        text = text.lower()
        return text


    def _tokenize(self, text):
        if self.n < 1:
            raise Exception("N-grams require n >= 1.")

        # Create tokens from the text.
        unigrams = word_tokenize(text)

        # Get rid of '.', ',' and etc.
        blacklist = [u'.', u',']
        unigrams = [unigram for unigram in unigrams if unigram not in blacklist]

        # Create n-grams
        tokens = unigrams
        for i in xrange(2, self.n+1):
            new_tokens = ngrams(unigrams, i)

            # Change 'new_tokens' that is a list() type into a string type
            new_tokens = ['_'.join(ngram) for ngram in new_tokens]
            tokens = tokens + new_tokens

        return tokens


    def _find_topics(self, tokens):

        helper = Token2Topic(self.wiki, self.level)

        proposed_topics = []
        list_of_parents = []

        step = float(100)/float(len(tokens))
        progress = float(0)

        for token in tokens:
            progress += step
            if TopicEstimator.DEBUG: print "%0.1f %%" % progress

            new_incomers, parent = helper.get_topics(token)
            proposed_topics = proposed_topics + new_incomers
            list_of_parents.append(parent)

        del helper
        if TopicEstimator.DEBUG: print "\n=======================================\n"

        return proposed_topics, list_of_parents


    def _get_frequencies(self, list):
        # Frequency of elements
        fr = {}

        for topic in list:
            if topic in fr:
                fr[topic] += 1
            else:
                fr.update({topic: 1})

        return fr

    def _get_topics_with_fr(self, dictionary, fr):

        filter_out = dict()
        for topic, value in dictionary.iteritems():
            if value >= fr:
                filter_out.update({topic: value})

        return  filter_out

    def _filter_topics(self, proposed_topics):
        frequency = self._get_frequencies(proposed_topics)

        filtered = self._get_topics_with_fr(frequency, 3)

        return filtered



