# -*- coding: utf8 -*-
import os

import tornado


class BillingCore(object):

    @staticmethod
    def get_payment(social):
        from social_billing.mm.engine.payment import MMPayment
        from social_billing.vk.engine.payment import VKPayment

        return {'vk': VKPayment, 'mm': MMPayment}[social]

    @classmethod
    def init(cls, social_name, default_item, *args):
        tornado.locale.load_translations(
            os.path.join(os.path.dirname(__file__), "vk/translations")
        )
        cls.default_item = default_item
        cls.payment = cls.get_payment(social_name)(*args)