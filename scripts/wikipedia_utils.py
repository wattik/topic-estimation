#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'Wattik'


import redis
import wikipedia as wiki
from wikipedia.exceptions import *
import records


class AbstractWikipedia(object):

    def __init__(self, lang = "cs"):
        self.lang = lang

    """
    Return true, if it's a page.
    If it's a disambiguation page, then returns list of those pages.
    Otherwise, return False.
    """
    def is_page(self, name):
        raise NotImplementedError("Abstract method. Do not do the same mistake of calling this method again, otherwise you'd be punished.")

    def get_page_categories(self, name):
        raise NotImplementedError("Abstract method.")

    def change_language(self, lang):
        self.lang = lang


class WikipediaBrowser(AbstractWikipedia):


    def __init__(self, lang = "cs"):
        AbstractWikipedia.__init__(self, lang)
        wiki.set_lang(lang)
        self.set_rate_limiting(False)
        pass

    def is_page(self, name):
        try:
            wiki.page(name)
        except PageError:
            return False
        except DisambiguationError as err:
            print err.options
            return err.options
        except HTTPTimeoutError as err:
            print "WIKIDATA kicked us out from the server. More info below.\n"
            print err
            return False

        return True

    def get_page_categories(self, name):
        page = wiki.page(name)
        return page.categories

    def change_language(self, lang):
        AbstractWikipedia.change_language(lang)
        wiki.set_lang(lang)

    def set_rate_limiting(self, rate):
        wiki.set_rate_limiting(rate)


class WikipediaMySQL(AbstractWikipedia):


    def __init__(self, username, password, host = "localhost", db = "wikipedia", lang = "cs"):
        AbstractWikipedia.__init__(self, lang)
        self.db = records.Database('mysql://' + username + ':' + password + '@' + host + '/' + db)

        wiki.set_lang(lang)

        # TODO #1: check whether the connection is established and if there is some
        # TODO #2: rename db wikipedia to cs_wikipedia (or tables)
        # TODO #3: the db entries shall be RESTRUCTURED according to text-preprocessing we will agree on
        # TODO  |  now, the equivalence uses only simplified characters lowercased – very loose.

    def is_page(self, name):
        result = self.db.query('SELECT page_title FROM page WHERE LOWER(CONVERT(page_title USING utf8)) = \'' + name + '\' AND page_namespace!=10 ')
        result = [unicode(pages["page_title"], 'utf-8') for pages in result]


        if len(result) == 0:
            # print name + " is not a page."
            return False
        elif len(result) > 1:
            # print name + " leads to more than one page."
            return True
        elif self._is_disambiguation_page(result):
            # print name + " is disambiguous."
            return True
        else:
            return True

    def get_page_categories(self, name):
        try:
            pages = self.db.query('SELECT categorylinks.cl_to, page.page_title, page.page_id '
                                   'FROM page, categorylinks '
                                   'WHERE LOWER(CONVERT(page.page_title USING utf8)) = \'' + name + '\' '
                                        'AND page.page_id = categorylinks.cl_from '
                                        'AND page_namespace != 10')

        except UnicodeEncodeError as err:
            # print ">>>> '" + name + "' contains utf-8 char"
            try:
                return wiki.page(name).categories
            except WikipediaException:
                # Sorry, I tried my best.
                return []


        # NORMAL CASE:
        categories = []

        for page in pages:
            title = unicode(page["cl_to"], "utf-8")

            if self._is_disambiguation_page(title):
                categories = categories + self._get_links_from_disambiguation_page(page["page_title"], page_id=page["page_id"])
            else:
                categories.append(title)

        return categories

    def _is_disambiguation_page(self, name):

        __DISAMBIGUATION_CATEGORIES = {'cs' : u'Wikipedie:Rozcestníky'}

        if type(name) == unicode or type(name) == str:
            if name == __DISAMBIGUATION_CATEGORIES[self.lang]:
                return True

        if type(name) == list:
            for i in name:
                if name == __DISAMBIGUATION_CATEGORIES[self.lang]:
                    return True

        return False

    def _get_links_from_disambiguation_page(self, name, page_id=None):

        if not page_id == None:
            try:
                disambiguation = wiki.page(pageid=page_id)
            except DisambiguationError as err:
                options = err.options
                return options
                # end of dirty trick
            except PageError:
                pass

        try:
            disambiguation = wiki.page(name)
        except DisambiguationError as err:
            options = err.options
            return options
            # end of dirty trick
        except PageError:
            return []

        return disambiguation.categories


    def change_language(self, lang):
        AbstractWikipedia.change_language(self, lang)
        # TODO change db to prefix


"""

NOT NEEDED NOW!

"""
class WikipediaRedis(AbstractWikipedia):

    def __init__(self, lang = "cs"):
        pass
        # TODO: Check whether db is online and if it contains data


