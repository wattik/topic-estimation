# -*- coding: utf-8 -*-
#!/usr/bin/python

__author__ = 'Wattik'

from scripts.topic_estimation import TopicEstimator
from scripts.wikipedia_utils import *
import sys
from scripts.analyzer import Analyzer

if __name__ == "__main__":

    #text = u'Java je lepší programovací jazyk než Python. Ruby jim nesahá ani po kotníky.'
    #text = u'Meteorologové rozšířili současnou výstrahu před vysokými teplotami o varování před velmi silnými bouřkami. Ojediněle je mohou doprovázet i přívalové srážky a krupobití. V pondělí o tom informoval Český hydrometeorologický ústav (ČHMÚ).'
    text = u'Chystáte se na filmový festival do Varů? Stáhněte si naši appku Vodafone KVIFF. Najdete v ní kompletní program filmů, seznam akcí na naší pláži, denní updaty, live feed ze social kanálu a mnoho dalšího. Buďte v obraze :) Android ➡ http://tam.je/avary  iPhone ➡ http://tam.je/ivary  Windows ➡ http://tam.je/wvary'
    # text = sys.argv[1]

    print "Looking for topics in: " + text

    # wiki = WikipediaMySQL("socialbakers", "tajneheslo")
    wiki = WikipediaRedis()
    estimator = TopicEstimator(wiki, level=3)

    proposed_topics, list_of_parents =  estimator.estimate_topic(text)

    #####################

    vis = Analyzer(proposed_topics, list_of_parents)
    print
    print "Frekvence kategorií celkem:"
    print
    vis.print_frequencies(cut_frequency=3)
    print
    print "Frekvence kategorií podle úrovně zanoření"
    vis.print_frequencies_by_levels()
    print
    print "Strom všech nalezených kategorií"
    print
    vis.print_tree()


