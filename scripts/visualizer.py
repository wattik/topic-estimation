#!/usr/bin/python

__author__ = 'Wattik'

class Visualizer(object):

    def __init__(self, list_of_topics, list_of_parents):
        self.list_of_topics = list_of_topics
        self.list_of_parents = list_of_parents

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

        return filter_out

    def get_frequencies(self, cut_frequency):
        fr = self._get_frequencies(self.list_of_topics)
        return self._get_topics_with_fr(fr, cut_frequency)