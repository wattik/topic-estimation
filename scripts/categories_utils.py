#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'Wattik'


import redis


class CategoriesBrowser(object):

    _level = None

    #Singleton
    redis = None

    def __init__(self, level):
        self._level = level
        if CategoriesBrowser.redis is None:
            CategoriesBrowser.redis = redis.StrictRedis()



    """
    Returns a dictionary of tuples: a topic and its level of inheritance
    """
    # TODO: Not detecting re-visits yet
    def get_topics(self, token):

        return dict()


class RedisHelper(object):

    _redis = None

    def __init__(self):
        pass

class WikipediaParser(object):
    pass
