# -*- coding: utf-8 -*-
#!/usr/bin/python

__author__ = 'Wattik'

from scripts.topic_estimation import TopicEstimator
from scripts.wikipedia_utils import *
from scripts.analyzer import Analyzer

if __name__ == "__main__":

    text = "Václav Havel"

    print "Looking for topics in: " + text

    # wiki = WikipediaMySQL("socialbakers", "tajneheslo")
    wiki = WikipediaRedis()
    estimator = TopicEstimator(wiki, level=2)

    proposed_topics, list_of_parents =  estimator.estimate_topic(text)

    #####################

    vis = Analyzer(proposed_topics, list_of_parents)
    vis.print_frequencies()
    vis.print_tree()

    for i in vis.get_most_frequent():
        print i


