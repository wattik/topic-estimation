# -*- coding: utf-8 -*-
#!/usr/bin/python

__author__ = 'Wattik'

from scripts.topic_estimation import TopicEstimator
from scripts.wikipedia_utils import *
from scripts.analyzer import Analyzer
import sys
import csv
from collections import Counter

def estimate(estimator, word):
    proposed_topics, list_of_parents = estimator.estimate_topic(word)

    vis = Analyzer(proposed_topics, list_of_parents)
    best_topics = vis.get_most_frequent(n=2)
    string_topics = [i.topic for i in best_topics]
    keyword_topic = vis.get_generators(string_topics)

    return string_topics, keyword_topic

def compute_csv_file(name):
    source_file = name

    wiki = WikipediaRedis()
    estimator_level2 = TopicEstimator(wiki, level=2)
    estimator_level3 = TopicEstimator(wiki, level=3)

    stack_of_all_proposals_level2 = []
    stack_of_all_proposals_level3 = []

    with open(source_file) as source:
        with open('out.csv', 'a+') as output:
            reader = csv.reader(source)
            headers = reader.next()
            writer = csv.writer(output)
            writer.writerow(headers + ['topics_l2', 'topics_l3', 'keyword:topic_l2', 'keyword:topic_l3'])

            count = 0

            for row in reader:
                cells = dict(zip(headers, row))

                count += 1

                joined = ""

                if len(cells['message']) > 0:
                    best_topics_level2, keyword_topic_level2 = estimate(estimator_level2, cells['message'])
                    best_topics_level3, keyword_topic_level3 = estimate(estimator_level3, cells['message'])

                    stack_of_all_proposals_level2 += best_topics_level2
                    stack_of_all_proposals_level3 += best_topics_level3

                    string_keywords_topic_level2 = [k.topic + u':' + u','.join(v) for k, v in
                                                    keyword_topic_level2.iteritems()]
                    string_keywords_topic_level3 = [k.topic + u':' + u','.join(v) for k, v in
                                                    keyword_topic_level3.iteritems()]

                    row += [(u'|'.join(best_topics_level2)).encode("utf-8")]
                    row += [(u'|'.join(best_topics_level3)).encode("utf-8")]
                    row += [(u'|'.join(string_keywords_topic_level2)).encode("utf-8")]
                    row += [(u'|'.join(string_keywords_topic_level3)).encode("utf-8")]

                writer.writerow(row)

                print str(count) + " finished."

                # print all per frequency
                # counter = Counter(stack_of_all_proposals_level2)
                # for k,v in counter.most_common():
                #     print k + u' : ' + unicode(v)
                #
                # counter = Counter(stack_of_all_proposals_level3)
                # for k, v in counter.most_common():
                #     print k + u' : ' + unicode(v)


if __name__ == "__main__":
    compute_csv_file("../176688316811_posts.csv")
    compute_csv_file("../286483085526_posts.csv")
    compute_csv_file("../120461304659141_posts.csv")
    compute_csv_file("../170261873008353_posts.csv")
    compute_csv_file("../194690260556051_posts.csv")






