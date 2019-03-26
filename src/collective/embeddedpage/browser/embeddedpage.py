# coding: utf-8
from bs4 import BeautifulSoup
from plone.registry.interfaces import IRegistry
from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getUtility

import re
import requests


class EmbeddedPageView(BrowserView):

    template = ViewPageTemplateFile('embeddedpage.pt')

    def __call__(self):
        qs = self.request.QUERY_STRING
        url = qs and "?".join([self.context.url, qs]) or self.context.url
        response = requests.get(url)
        # Normalize charset to unicode
        content = safe_unicode(response.content)
        # # # Turn to utf-8
        # content = content.encode('utf-8')
        soup = BeautifulSoup(content, 'html.parser')

        soup = soup.body or soup
        # Remove nasty nodes like script, etc
        registry = getUtility(IRegistry)
        nastyTags = registry.get('collective.embeddedpage.nastyTags', [])
        for nt in nastyTags:
            for tt in soup.find_all(nt):
                tt.extract()
        self.embeddedpage = soup.prettify()
        # remove style
        self.embeddedpage = self.embeddedpage.replace('style=','style_remote=')
        # href
        self.embeddedpage = re.sub('href="(?!mailto)[^"]+?\?', 'href="?', self.embeddedpage)
        return self.template()
