# -*- coding: utf-8 -*-
import tornado
from tornado.web import RequestHandler

from social_billing.payment import Payment


class BaseHandler(RequestHandler):

    def init(self, prices, callback):
        BaseHandler.payment = Payment(prices, callback)

    def get_user_locale(self):
        return tornado.locale.get('ru_RU')

    def response(self, resp):
        return self.finish({'response': resp})
