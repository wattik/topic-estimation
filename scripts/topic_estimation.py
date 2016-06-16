# -*- coding: utf-8 -*-
#!/usr/bin/python

__author__ = 'Wattik'

import sys
from nltk.tokenize import word_tokenize
from nltk.util import ngrams
from categories_utils import CategoriesBrowser, Topic

"""
The script estimates topics of a short text based on Wikipedia categories.

It's expected that first argument is the text. For example:

    python topic-estimation "First documented in the 13th century, Berlin was the capital of the Kingdom of Prussia (1701–1918), the German Empire (1871–1918), the Weimar Republic (1919–33) and the Third Reich (1933–45)."


The output is a set of topics. (TBD...)

"""

class TopicEstimator(object):

    _level = 2
    _n = 3

    def __init__(self, n = 3, level = 2):
        self._level = level
        self._n = n

    def estimate(self, text):

        if len(text) == 0:
            raise Exception("Text is not long enough.")

        # Basic preprocessing such as: utf-8 encoding, lowercasing
        text = self._preprocess(text)

        # Breaking apart into n-grams, so far n=3
        tokens = self._tokenize(text, self._n)


        # TODO: additional filtering of words
        # additional layers and filters here
        # Synonyms etc
        # Stemmatization, lemmatization, stopwords, etc.

        # Given tokens find categories in wiki's net. Go 2 levels deep.
        proposed_topics = self._find_topics(tokens, self._level)

        # Choose the best proposals of all proposed topics.
        topics = self._filter_topics(proposed_topics)

        return topics


    def _preprocess(self, text):
        text = unicode(text, 'utf-8')
        text = text.lower()
        return text


    def _tokenize(self, text, n):
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
            new_tokens = ngrams(unigrams, i)

            # Change 'new_tokens' that is a list() type into a string type
            new_tokens = [' '.join(ngram) for ngram in new_tokens]
            tokens = tokens + new_tokens

        return tokens


    def _find_topics(self, tokens, level):

        helper = CategoriesBrowser(level)

        proposed_topics = list()
        for token in tokens:
            proposed_topics = proposed_topics + helper.get_topics(token)

        return proposed_topics


    def _filter_topics(self, proposed_topics):
        # TODO
        topics = proposed_topics

        for topic in proposed_topics:
            # TODO
            pass

        return topics


# Main: ##################################

if __name__ == "__main__":

    # TODO: change here after beta is done.
    text = "Shoot for the stars 'cause if you miss, you might end up on the moon."
    # text = sys.argv[0]

    estimator = TopicEstimator()

    print estimator.estimate(text)