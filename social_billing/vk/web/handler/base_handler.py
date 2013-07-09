# -*- coding: utf-8 -*-
import os

import tornado
from tornado.web import RequestHandler

from social_billing.vk.engine.payment import Payment


class BaseHandler(RequestHandler):

    @classmethod
    def init(cls, name, prices, secret, callback):
        tornado.locale.load_translations(
            os.path.join(os.path.dirname(__file__), "../../translations")
        )
        BaseHandler.payment = Payment(name, prices, secret, callback)

    def get_user_locale(self):
        return tornado.locale.get('ru_RU')
