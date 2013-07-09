# -*- coding: utf-8 -*-
import tornado
from tornado.web import RequestHandler

from social_billing.core import BillingCore


class BaseHandler(RequestHandler):

    @property
    def payment(self):
        return BillingCore.payment

    def get_user_locale(self):
        return tornado.locale.get('ru_RU')
