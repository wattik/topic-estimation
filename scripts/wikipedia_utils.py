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

    def get_page_categories(self, name):
        raise NotImplementedError("Abstract method.")

    def change_language(self, lang):
        self.lang = lang


class WikipediaBrowser(AbstractWikipedia):
    """
    Using this API: https://en.wikipedia.org/w/api.php
    """

    def __init__(self, lang = "cs"):
        AbstractWikipedia.__init__(self, lang)
        wiki.set_lang(lang)
        self.set_rate_limiting(False)
        pass

    def get_page_categories(self, name, page_id=None):
        categories = []
        gen_by = "empty"
        try:
            categories = self.get_page_categories_unprotected(name, page_id)
            gen_by = u'wiki_api'
        except DisambiguationError as err:
            categories = self._afterprocess_categories(err.options)
            gen_by = u'wiki_api'
        except PageError:
            gen_by = u'empty-wiki_api'
        except HTTPTimeoutError:
            print "Wikipedia has kicked us out. :("

        return categories, gen_by

    def get_page_categories_unprotected(self, name, page_id=None):

        try:
            page = wiki.page(pageid=page_id)

        except (PageError, ValueError):
            page = wiki.page(name)
            if u'a' in page.categories:
                print page.title

        return self._afterprocess_categories(page.categories)

    def _afterprocess_categories(self, cats):
        filtered_cats = []
        for cat in cats:
            parts = cat.split(u':', 1)
            final = cat
            # This removes the first word before ':'
            if len(parts) == 2:
                final = parts[1]

            final = final.replace(' ', '_')
            filtered_cats.append(final)


        return filtered_cats


    def change_language(self, lang):
        AbstractWikipedia.change_language(lang)
        wiki.set_lang(lang)

    def set_rate_limiting(self, rate):
        wiki.set_rate_limiting(rate)


class WikipediaMySQL(AbstractWikipedia):

    """
    help : if True, then queries not found in the local DB are requested from wikipedia data services via the module

    It's expected that there exists a database called accordingly to the chosen language, eg. "cs_wikipedia"
    """
    def __init__(self, username, password, host = "localhost", lang = "cs", help = False):
        AbstractWikipedia.__init__(self, lang)
        self.db = records.Database('mysql://' + username + ':' + password + '@' + host + '/' + lang + '_wikipedia?charset=utf8')
        self.help = help
        self.helper = WikipediaBrowser(lang=lang)

        # TODO #3: the db entries shall be RESTRUCTURED according to text-preprocessing we will agree on
        # TODO  |  now, the equivalence uses only simplified characters lowercased – very loose.


    def _gen(self, gen_by, newer):
        if gen_by is None:
            return newer
        elif gen_by == u'local_db':
            return gen_by
        else:
            return u'combined'


    def get_page_categories(self, name):
        gen_by = "empty-local_db"
        categories = []

        # Start with MySQL DB query that delivers dictionary of results.
        try:
            # The query itself.
            pages = self.db.query('SELECT categorylinks.cl_to, page.page_title, page.page_id '
                                   'FROM page, categorylinks '
                                   'WHERE LOWER(CONVERT(page.page_title USING utf8)) = \'' + name + '\' '
                                        'AND page.page_id = categorylinks.cl_from '
                                        'AND page_namespace != 10')
            # Get the names of categories from the response.
            for page in pages:
                category = unicode(page["cl_to"], "utf-8")

                # A category of a page is considered all of listed:
                #   - a category
                #   - links from a disambiguation page (but NOT the categories of those links' pages)
                #
                #   Note: Disambiguation pages shall not have other then the specific disambi category. If this is met,
                #   then a mixture of both cases shall be observed if and only if 'name' leads to more than one page.

                if self._is_disambiguation_page(category):
                    self._gen(gen_by, 'wiki_api')
                    categories = categories + self._get_links_from_disambiguation_page(page["page_title"], page_id=page["page_id"])
                # Assuming that if a page is redirect than page_id is only once in the list.
                elif self._is_redirect(page["page_id"]):
                    pass
                else:
                    gen_by = u'local_db'
                    categories.append(category)

        # Dirty trick: if an error is raised due to encodings, the helper class is utilized. This shall be eliminated in future versions.
        except UnicodeEncodeError as err:
            # TODO solve encoding issue
            print("UnicodeEncodeError while DB connection: If this exception was raised, change 'help=True' handler when constructing "
                  "'WikiepdiaMySQL() object. Then, in cases similar to this one, the Wikipedia API will be used to look for categories.")
            if self.help:
                categories, gen_by = self.helper.get_page_categories(name)

        return categories, gen_by


    def _is_redirect(self, page_id):
        return False


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
        links = []

        # At this stage, instead of parsing html and looking for links in it, the WikipediaBroweser class providing this tool
        # via requests is utilized. In the future, this will be implemented as well via the local mysql db.

        try:
            self.helper.get_page_categories_unprotected(name, page_id=page_id)
        except DisambiguationError as err:
            # Dirty borrowing of private method
            links = self.helper._afterprocess_categories(err.options)

        return links



    def change_language(self, lang):
        AbstractWikipedia.change_language(self, lang)
        if self.help: self.helper.change_language(lang)
        # TODO change db to prefix

