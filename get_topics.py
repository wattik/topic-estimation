# -*- coding: utf-8 -*-
#!/usr/bin/python

__author__ = 'Wattik'

from scripts.topic_estimation import TopicEstimator
from scripts.wikipedia_utils import *
import sys
from scripts.visualizer import Visualizer

if __name__ == "__main__":

    # text = u'java ruby programovací jazyky'
    text = sys.argv[1]

    print "Looking for topics in: " + text

    # wiki = WikipediaMySQL("socialbakers", "tajneheslo")
    wiki = WikipediaRedis()
    estimator = TopicEstimator(wiki, level=6)

    proposed_topics, list_of_parents =  estimator.estimate_topic(text)

    #####################

    vis = Visualizer(proposed_topics, list_of_parents)
    vis.print_frequencies()
    print
    vis.print_frequencies_by_levels()
    print "\n"
    vis.print_tree()


