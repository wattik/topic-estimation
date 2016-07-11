#!/usr/bin/python
# -*- coding: utf-8 -*-

import redis

class Lemmatiser(object):

    def __init__(self):
        self.r = redis.StrictRedis()

    def lemmatise(self, word):
        return self.r.get(u'd:' + word)
