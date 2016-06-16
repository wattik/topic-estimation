#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'Wattik'

import redis


class Topic(object):

    topic = None
    hierarchy_level = None
    generating_ngram = None

    # etc. Type=(category, article) ...... TODO: is needed?

    def __init__(self, topic, hierarchy_level, generating_ngram):
        self.generating_ngram = generating_ngram
        self.hierarchy_level = hierarchy_level
        self.topic = topic

    def __repr__(self):
        return self.generating_ngram + '->' + self.topic + ' at level ' + unicode(self.hierarchy_level)

    def __eq__(self, other):
        return other.topic == self.topic


class Category2Topic(object):

    _level = None
    _wiki = None

    def __init__(self, level):
        self._level = level
        self._wiki = WikipediaBrowser()

    """
    Returns a list of Topics()
    """
    def get_topics(self, token):
        topics = list()

        # Find out whether it's a wiki page ..
        if self._wiki.is_page(token):
            # ... and if so, go '_level'-times deeper to find categories.
            topics = topics + self._iterate_over_supercategories(Topic(token, 0, None), 1)

        return topics

    """
    Depth-first search in categories.

    This goes until level = 0, then it stops.
    """
    def _iterate_over_supercategories(self, topic, level):
        if level > self._level:
            return []

        supercategories = self._wiki.get_page_categories(topic.topic)
        list_of_topics = self._categories2topics(supercategories, topic.topic, level)

        output = list_of_topics[:]

        for supertopic in list_of_topics:
                output = output + self._iterate_over_supercategories(supertopic, level+1)

        return output

    def _categories2topics(self, subcategories, ngram, level):
        topics = list()
        for subcategory in subcategories:
            topics.append(Topic(subcategory, level, ngram))

        return topics


class WikipediaBrowser(object):

    _redis = None

    def __init__(self):
        self._redis = RedisHelper()

    def is_page(self, name):
        return True

    def get_page_categories(self, name):
        return [u'Car' , u'Plane']



class RedisHelper(object):

    _redis = None

    def __init__(self):
        if RedisHelper._redis is None:
            RedisHelper._redis = redis.StrictRedis()

        # TODO: Check whether db is online and if it contains data



"""
Wikipedia parser might be used for parsing lot of files into REDIS db.
"""
class WikipediaParser(object):

    _redis = None

    def __init__(self):
        if self._redis is None:
            self._redis = RedisHelper()


    # TODO: establish how to read the files, i.e. which form the dump is
    def parse(self, directory):
        return True