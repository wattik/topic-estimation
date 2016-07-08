#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'Wattik'


class Topic(object):

    def __init__(self, topic, hierarchy_level, generating_ngram):
        self.generating_ngram = generating_ngram
        self.hierarchy_level = hierarchy_level
        self.topic = topic
        self.parents = None
        self.gen_by = u'N/A'

    def __repr__(self):
        return self.topic + u' by ' + self.generating_ngram

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        return other.topic == self.topic

    def __cmp__(self, other):
        return self.__cmp__(other)

    def __hash__(self):
        return self.topic.__hash__()

class Token2Topic(object):


    def __init__(self, wiki, level):
        self.level = level
        self.wiki = wiki

    """
    Returns a list of Topics()
    """
    def get_topics(self, token):

        parent_topic = Topic(token, 0, u'-')

        topics = self._dfs_over_categories(parent_topic)

        return topics, parent_topic

    """
    Depth-first search throughout categories.
    """
    def _dfs_over_categories(self, topic):

        output = [topic]

        level = topic.hierarchy_level + 1

        # If we reached the deepest level, then exit.
        if level > self.level:
            topic.gen_by  = "end_node"
            return output

        supercategories, gen_by = self.wiki.get_page_categories(topic.topic)
        supercategories = self._process_proposals(topic, supercategories)
        list_of_topics = self._categories2topics(supercategories, topic.topic, level)

        topic.parents = list_of_topics
        topic.gen_by = gen_by

        for supertopic in list_of_topics:
                output = output + self._dfs_over_categories(supertopic)

        return output


    """
    Processes the proposed categories so that the final list:
        - includes unique items only,
        - with lowered text,
        - and doesn't include the parent node again (no simple backloops)

    Although some of those shall not happen because this is secured already on lower levels by wikipedia walkers, it's
    good practise to test it for sure.
    """
    def _process_proposals(self, topic, list_of_categories):
        list_of_categories = list(set(list_of_categories))
        output = []
        for i in list_of_categories:
            i = i.lower()
            if i != topic.topic:
                output.append(i.lower())
        return output


    def _categories2topics(self, subcategories, ngram, level):
        topics = list()
        for subcategory in subcategories:
            topics.append(Topic(subcategory, level, ngram))

        return topics

