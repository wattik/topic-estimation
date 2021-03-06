# -*- coding: utf-8 -*-
#!/usr/bin/python

__author__ = 'Wattik'


from nltk.tokenize import word_tokenize
from nltk.util import ngrams
from categories_utils import Token2Topic
from collections import deque
from lemmatiser import Lemmatiser

"""
The script estimates topics of a short text based on Wikipedia categories.

    python topic-estimation "First documented in the 13th century, Berlin was the capital of the Kingdom of Prussia (1701–1918), the German Empire (1871–1918), the Weimar Republic (1919–33) and the Third Reich (1933–45)."


"""

class TopicEstimator(object):

    DEBUG = True

    def __init__(self, wiki, n = 3, level = 2, verbosity = 0):
        self.level = level
        self.n = n
        self.wiki = wiki
        self.verbosity = verbosity

        if verbosity > 10:
            TopicEstimator.DEBUG=True
        else:
            TopicEstimator.DEBUG=False


    def estimate_topic(self, text):

        if len(text) == 0:
            raise Exception("Text is not long enough.")

        if TopicEstimator.DEBUG: print "Prepocessing the text."

        # Basic preprocessing such as: utf-8 encoding, lowercasing
        text = self._preprocess(text)

        if TopicEstimator.DEBUG: print "Tokenizing the text."

        # Breaking apart into n-grams, so far n=3
        tokens = self._tokenize(text)

        if TopicEstimator.DEBUG: print "Lemmatising the tokens."

        # Lemmatise
        tokens = self._lemmatise_tokens(tokens)

        if TopicEstimator.DEBUG: print "Filtering tokens."

        tokens = self._filter_tokens(tokens)

        if TopicEstimator.DEBUG: print "Finding topics."

        # Given tokens find categories in wiki's net. Go 2 levels deep.
        list_of_parents = self._find_topics(tokens)

        if TopicEstimator.DEBUG: print "Filtering\n\n"

        # Choose the best proposals of all proposed topics.
        proposed_topics = self._filter_tree(list_of_parents)

        return proposed_topics, list_of_parents


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

    def _lemmatise_tokens(self, tokens):
        temp = []
        lemm = Lemmatiser()

        counter = 0

        for token in tokens:
            proposal = lemm.lemmatise(token)
            if proposal is not None:
                temp.append(unicode(proposal, "utf-8"))
                counter += 1
            else:
                temp.append(token)
        del lemm
        return temp

    def _filter_tokens(self, tokens):
        temp = []

        stop_words = [u'ten', u'http']

        for token in tokens:
            if token not in stop_words and len(token) > 2:
                temp.append(token)
        return temp



    def _find_topics(self, tokens):

        helper = Token2Topic(self.wiki, self.level)

        list_of_parents = []

        step = float(100)/float(len(tokens))
        progress = float(0)
        if TopicEstimator.DEBUG: print "\n%0.1f %%" % progress

        for token in tokens:
            parent = helper.get_topics(token)
            list_of_parents.append(parent)

            progress += step
            if TopicEstimator.DEBUG: print "%0.1f %%" % progress

        del helper

        return list_of_parents



    def _filter_topics(self, proposed_topics):
        temp = []

        for item in proposed_topics:
            topic = item.topic

            if self.__is_filtred(topic):
                continue

            temp.append(item)

        return temp

    def _filter_tree(self, list_of_parents):
        stack = deque()
        stack.extend(list_of_parents)

        list_of_proposals = []

        while len(stack) > 0:
            item = stack.popleft()

            temp = []
            if item.parents is None:
                continue
            for parent in item.parents:
                if not self.__is_filtred(parent.topic):
                  temp.append(parent)

            item.parents = temp

            list_of_proposals.extend(temp)
            stack.extend(temp)

        return list_of_proposals


    def __is_filtred(self, word):
        # exclude those that start with:
        starts_with = [u'údržba:', u'wikipedie:', u'wikipedia:', u'šablony', u'rozcestník', u'písmena', u'monitoring', u'články_s_odkazem', u'přesměrování', u'miniportály', u'portály']
        # exlcude those that include those
        includes = [u'pahýly', u'kategorie_k_zaplnění', u'články_přeložené_z_enwiki', u'pouze_dočasná_použití', u'články_s_autoritní_kontrolou', u'zkratky', u'zkratka', u'etymologie', u'slova_a_výrazy']
        includes += [u'interpunkce', u'latinka', u'znaky_písma', u'větná_stavba', u'symboly', u'značky', u'šablony', u'terminologie', u'články_podle_témat']
        # exclude those ending with:
        ends_with = [u'šablony', u'portály', u'wikipedie']


        # check starts
        positive = False
        for start in starts_with:
            if word.find(start) == 0:
                positive = True
                break

        if positive: return positive

        # check includes
        positive = False
        for include in includes:
            if word.find(include) >= 0:
                positive = True
                break

        if positive: return positive

        # check ends
        positive = False
        for end in ends_with:
            if word.endswith(end) == True:
                positive = True
                break

        if positive: return positive

        # delete those shorter then 3
        if len(word) < 3:
            return True


        return positive

