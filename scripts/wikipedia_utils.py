#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'Wattik'


import redis


class AbstractWikipedia(object):

    def __init__(self, lang = "cs"):
        self.lang = lang

    def get_page_categories(self, name):
        raise NotImplementedError("Abstract method.")

    def change_language(self, lang):
        self.lang = lang

    def _is_disambiguation_page(self, name):

        __DISAMBIGUATION_CATEGORIES = {'cs': u'wikipedie:rozcestníky',
                                       'en': u'Disambiguation_pages'} #TODO check for EN

        if name is unicode or name is str:
            if name == __DISAMBIGUATION_CATEGORIES[self.lang]:
                return True

        if isinstance(name, list):
            for i in name:
                if i == __DISAMBIGUATION_CATEGORIES[self.lang]:
                    return True

        return False

    def _unicode(self, items):
        temp = []
        for item in items:
            if item is not unicode: item = unicode(item, "utf-8")
            temp.append(item)
        return temp



class WikipediaRedis(AbstractWikipedia):

    def __init__(self, lang = "cs"):
        # just up until multiple langs are supported
        if lang != "cs":
            self.change_language(lang)

        AbstractWikipedia.__init__(self,lang)
        self.r = redis.StrictRedis()

        self.prep = {"page":"p:", "category":"c:", "redirect":"r:", "pagelinks":"l:"}

    def get_page_categories(self, name):
        # Initialize.
        categories = []
        gen_by = "redis"

        # Check if there is any page of this name.
        list_of_page_proposals = self.r.lrange(self.prep["page"] + name, 0, -1)

        # In case of an empty list = page not found.
        if not list_of_page_proposals:
            return categories, gen_by

        # The list is not empty, we've got proposals. Let's find redirects.
        checked_page_proposals = []
        for page_id in list_of_page_proposals:
            # If it leads to a redirect, get the redirect's page id.
            redirect_name = self.r.get(self.prep["redirect"] + page_id)
            # if page_is is a redirect:
            if redirect_name is not None:
                proposals = self.r.lrange(self.prep["page"] + redirect_name, 0, -1)
                checked_page_proposals = checked_page_proposals + proposals
            # if it's not:
            else:
                checked_page_proposals.append(page_id)

        # unigness of items check, loop 'em again > fetch categories of all ids
        for page_id in list(set(checked_page_proposals)):
            categories = categories + self._single_page_id_to_categories(page_id)

        return categories, gen_by


    def _single_page_id_to_categories(self, page_id):
        # Get the page's categories
        proposed_categories = self.r.lrange(self.prep["category"] + page_id, 0, -1)

        # convert string items (categories) into unicode
        proposed_categories = self._unicode(proposed_categories)

        # Check whether this page is not a disambiguation page.
        if self._is_disambiguation_page(proposed_categories):
            # If so, get its links
            """
            links = self.r.lrange(self.prep["pagelinks"] + page_id, 0, -1)
            links = self._unicode(links)
            links = self._filter_links(links)
            proposed_categories = links"""

        return proposed_categories


    def _filter_links(self, links):
        temp = []
        black_list = [u'název_článku', u'odkaz_na_rozcestník', u'rozcestník', u'rozcestníky', u'článek'] # TODO add more, probably needed
        for link in links:
            if link not in black_list:
                temp.append(link)
        return temp

    def change_language(self, lang):
        raise NotImplementedError("When using REDIS, so far only INITIAL (depending on redis instance's data) language is available.")
