# -*- coding: utf8 -*-
import os

import tornado

from social_billing.mm.engine.payment import MMPayment
from social_billing.vk.engine.payment import VKPayment


class BillingCore(object):

    mapper = {'vk': VKPayment, 'mm': MMPayment}

    @classmethod
    def init(cls, social_name, *args):
        tornado.locale.load_translations(
            os.path.join(os.path.dirname(__file__), "vk/translations")
        )
        cls.payment = cls.mapper[social_name](*args)