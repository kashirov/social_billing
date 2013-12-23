# -*- coding: utf8 -*-
import os

import tornado


class BillingCore(object):

    @staticmethod
    def get_payment(social):
        from social_billing.mm.engine.payment import MMPayment
        from social_billing.vk.engine.payment import VKPayment
        from social_billing.od.engine.payment import ODPayment
        from social_billing.xsolla.engine.payment import XsollaPayment

        return {'vk': VKPayment, 'mm': MMPayment, 'od': ODPayment,
                                            'xsolla': XsollaPayment}[social]

    @classmethod
    def init(cls, social_name, default_item, *args):
        tornado.locale.load_translations(
            os.path.join(os.path.dirname(__file__), "vk/translations")
        )
        cls.default_item = default_item
        cls.payment = cls.get_payment(social_name)(*args)