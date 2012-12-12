# -*- coding: utf-8 -*-
import os

import tornado
from tornado.web import RequestHandler

from social_billing.payment import Payment


class BaseHandler(RequestHandler):

    @classmethod
    def init(self, prices, callback):
        BaseHandler.payment = Payment(prices, callback)
        tornado.locale.load_translations(
            os.path.join(os.path.dirname(__file__), "../translations")
        )

    def get_user_locale(self):
        return tornado.locale.get('ru_RU')

    def response(self, resp):
        return self.finish({'response': resp})

    def error(self, code, msg, critical=1):
        return self.finish({'error': {'error_code': code, 'error_msg': msg,
                            'critical': critical}})
