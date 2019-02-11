# -*- coding: utf-8 -*-
from lxml import etree
from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

import lxml
import requests


class EmbeddedPageView(BrowserView):

    template = ViewPageTemplateFile('embeddedpage.pt')

    def __call__(self):
        response = requests.get(self.context.url)
        # we receive a utf-8 encoded string from requests
        # lxml expect unicode though
        content = safe_unicode(response.content)
        content = lxml.html.fromstring(content)
        subtree = content.find('body')
        if subtree is not None:
            self.embeddedpage = etree.tostring(subtree)
        else:  # No body tag inside
            self.embeddedpage = etree.tostring(content)
        return self.template()
