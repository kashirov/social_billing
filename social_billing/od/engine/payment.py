# -*- coding: utf8 -*-
from social_billing.core import BillingCore
from social_billing.od.engine.order import ODOrder
from social_billing.vk.engine.errors import SignatureError, InvalidCountError
from social_billing.vk.engine.signature import Signature


class ODPayment(object):
    def __init__(self, name, prices, secret, callback):
        self.signature = Signature(secret)
        self.prices = prices
        self.callback = callback
        self.order = ODOrder(name, callback)
        self.item = BillingCore.default_item

    def get_price(self, count):
        return self.prices[self.item]['prices'].get(count)

    def check_price(self, count, price):
        if self.get_price(count) != price:
            raise InvalidCountError

    def request(self, args):
        try:
            self.signature.try_check(args)
            count = int(args['service_id'])
            price = int(args['mailiki_price'])
            self.check_price(count, price)
            return self.order(args['uid'], args['transaction_id'], self.item,
                              count)
        except SignatureError:
            return {'status': 0, 'error_code': 700}
        except InvalidCountError:
            return {'status': 0, 'error_code': 703}
