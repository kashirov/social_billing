# -*- coding: utf8 -*-
from social_billing.mm.engine.order import MMOrder
from social_billing.vk.engine.errors import SignatureError
from social_billing.vk.engine.signature import Signature


class MMPayment(object):
    def __init__(self, name, prices, secret, callback):
        self.signature = Signature(secret)
        self.callback = callback
        self.order = MMOrder(name, callback)

    def request(self, args):
        try:
            self.signature.try_check(args)
            return self.order(args)
        except SignatureError:
            return {'status': 0, 'error_code': 700}