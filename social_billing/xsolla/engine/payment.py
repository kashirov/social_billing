# -*- coding: utf8 -*-
from social_billing.xsolla.engine.errors import ItemFormatError, UnknownItemError,\
    InvalidCountError, CallbackError, SignatureError
from social_billing.vk.engine.handler.billing import BillingHandler
from social_billing.xsolla.engine.handler.check import Check
from social_billing.xsolla.engine.handler.xsolla_order import XsollaOrder
from social_billing.xsolla.engine.signature import Signature


CHECK = 'check'
PAY = 'pay'


class XsollaPayment(BillingHandler):

    item_name = 'gems'

    def __init__(self, name, prices, secret, callback):
        prices = prices.get(self.item_name).get('prices')
        self.prices = dict((v, k) for k, v in prices.items())
        self.signature = Signature(secret)
        self.check = Check()
        self.order = XsollaOrder(name, callback)

    def request(self, args):
        command, user_id = args.get('command'), args.get('v1')
        try:
            if command.startswith(CHECK):
                if not self.signature.check(args.get('md5'), command, user_id):
                    raise SignatureError()
                return self.check(user_id)

            if command.startswith(PAY):
                price, order_id = int(args['sum']), int(args['id'])
                count = self.get_count(price)
                if not self.signature.check(args.get('md5'), command, user_id,
                                            order_id):
                    raise SignatureError()

                return self.order(order_id, user_id, self.item_name, count,
                                  price)

        except (ItemFormatError, UnknownItemError, InvalidCountError,
                CallbackError, SignatureError) as error:
            return error.response()

    def get_count(self, price):
        if price in self.prices:
            return self.prices.get(price)
        raise InvalidCountError
