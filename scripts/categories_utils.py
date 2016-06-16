#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'Wattik'

import redis


class Topic(object):

    topic = None
    hierarchy_level = None
    generating_ngram = None

    # etc. Type (category, article) ...... TODO

    def __init__(self, topic, hierarchy_level, generating_ngram):
        self.generating_ngram = generating_ngram
        self.hierarchy_level = hierarchy_level
        self.generating_ngram = generating_ngram

class CategoriesBrowser(object):

    _level = None
    _redis = None

    def __init__(self, level):
        self._level = level
        self._redis = RedisHelper()


    """
    Returns a list of Topics()
    """
    # TODO: Not detecting re-visits yet
    def get_topics(self, token):

        return list()


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
        # TODO
        return True