# -*- coding: utf-8 -*-
from tornado.web import Application, url

from social_billing.handler.index_handler import IndexHandler


application = Application([
    url(r'/', IndexHandler),
])
