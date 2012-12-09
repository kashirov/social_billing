# -*- coding: utf-8 -*-
import tornado
from tornado.web import RequestHandler


class BaseHandler(RequestHandler):

    def get_user_locale(self):
        return tornado.locale.get('ru_RU')

    def response(self, resp):
        return self.finish({'response': resp})
