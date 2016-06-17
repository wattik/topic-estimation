#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'Wattik'

import redis
import wikipedia
from wikipedia.exceptions import *
import records


class Topic(object):

    # etc. Type=(category, article) ...... TODO: is needed?

    def __init__(self, topic, hierarchy_level, generating_ngram):
        self.generating_ngram = generating_ngram
        self.hierarchy_level = hierarchy_level
        self.topic = topic

    def __repr__(self):
        return self.generating_ngram + '->' + self.topic + ' at level ' + unicode(self.hierarchy_level)

    def __eq__(self, other):
        return other.topic == self.topic


class Token2Topic(object):


    def __init__(self, wiki, level):
        self.level = level
        self.wiki = wiki

    """
    Returns a list of Topics()
    """
    def get_topics(self, token):
        topics = []

        # Find out whether it's a wiki page ..
        page = self.wiki.is_page(token)

        # ... and if so, go 'level'-times deeper to find categories.
        if page == True:
            topics = topics + self._dfs_over_categories(Topic(token, 0, None), 1)

        # ... of if it brings in the disambiguation page, then get topics from each of the options
        elif page is list:
            for option in page:
                topics = topics + self.get_topics(option)

        return topics

    """
    Depth-first search throughout categories.
    """
    def _dfs_over_categories(self, topic, level):
        if level > self.level:
            return []

        supercategories = self.wiki.get_page_categories(topic.topic)
        list_of_topics = self._categories2topics(supercategories, topic.topic, level)

        output = list_of_topics[:]

        for supertopic in list_of_topics:
                output = output + self._dfs_over_categories(supertopic, level+1)

        return output

    def _categories2topics(self, subcategories, ngram, level):
        topics = list()
        for subcategory in subcategories:
            topics.append(Topic(subcategory, level, ngram))

        return topics


class WikipediaBrowser(object):


    def __init__(self):
        #self._redis = RedisHelper()
        pass

    def is_page(self, name):
        try:
            wikipedia.page(name)
        except PageError:
            return False
        except DisambiguationError as err:
            print err.options
            return err.options
        except HTTPTimeoutError as err:
            #TODO ???? HUH
            print err
            return False

        return True

    def get_page_categories(self, name):
        page = wikipedia.page(name)
        return page.categories

    def change_language(self, lang):
        wikipedia.set_lang(lang)

    def set_rate_limiting(self, rate):
        wikipedia.set_rate_limiting(rate)


class WikipediaLocalDB(object):


    def __init__(self):
        self.db = records.Database('mysql://socialbakers:tajneheslo@localhost/wikipedia')


    # TODO
    def is_page(self, name):
        try:
            wikipedia.page(name)
        except PageError:
            return False
        except DisambiguationError as err:
            print err.options
            return err.options
        except HTTPTimeoutError as err:
            #TODO ???? HUH
            print err
            return False

        return True

    def get_page_categories(self, name):
        page = wikipedia.page(name)
        return page.categories

    def change_language(self, lang):
        wikipedia.set_lang(lang)

    def set_rate_limiting(self, rate):
        wikipedia.set_rate_limiting(rate)



"""

NOT NEEDED NOW!

"""
class RedisHelper(object):

    def __init__(self):
        if RedisHelper._redis is None:
            RedisHelper._redis = redis.StrictRedis()

        # TODO: Check whether db is online and if it contains data


