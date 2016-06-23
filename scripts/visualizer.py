#!/usr/bin/python

__author__ = 'Wattik'

class Visualizer(object):

    def __init__(self, list_of_topics, list_of_parents):
        self.list_of_topics = list_of_topics
        self.list_of_parents = list_of_parents
        self.dict_by_levels = None
        self.list_of_frequencies = None

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


    def get_frequencies(self, cut_frequency=5):
        if self.list_of_frequencies is None:
            self.list_of_frequencies = self._get_frequencies(self.list_of_topics)

        return self._get_topics_with_fr(self.list_of_frequencies, cut_frequency)


    def print_frequencies(self, cut_frequency=5):
        for f, v in self.get_frequencies(cut_frequency=cut_frequency).iteritems():
            print f.topic + " " + unicode(v)


    def print_all_topics(self):
        for t in self.list_of_topics:
            print unicode(t)


    def get_dict_by_levels(self):
        if self.dict_by_levels is None:
            self.dict_by_levels = dict()

            d = self.dict_by_levels

            for topic in self.list_of_topics:
                level = topic.hierarchy_level
                if d.has_key(level):
                    d[level].append(topic)
                else:
                    d.update({level:[topic]})


        return self.dict_by_levels

    def print_frequencies_by_levels(self, cut_frequency = 2):
        d = self.get_dict_by_levels()

        for level in d.iterkeys():
            fr = self._get_frequencies(d[level])
            print "\n Level " + str(level) + ":"
            topics = self._get_topics_with_fr(fr, cut_frequency)

            for k, v in topics.iteritems():
                print unicode(k) + " " + unicode(v)

    def print_tree(self):
        self._print_tree(self.list_of_parents, u'- ')

    def _print_tree(self, stack, pre):
        if stack is not None:
            next_pre = u'   ' + pre
            for node in stack:
                print pre + unicode(node)
                self._print_tree(node.parents, next_pre)



