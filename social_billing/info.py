# -*- coding: utf-8 -*-
import tornado

from social_billing.errors import UnknownItemError, InvalidCountError
from social_billing.payment_handler import PaymentHandler


class Info(PaymentHandler):

    def __init__(self, prices):
        self.prices = prices
        self.locale = tornado.locale.get('ru_RU')

    def price(self, name, count):
        item = self.prices.get(name)

        if item is None:
            raise UnknownItemError()
        elif count not in item:
            raise InvalidCountError()
        else:
            return item[count]

    def title(self, name, count):
        return ' '.join((str(count), self.locale.translate(name)))

    def __call__(self, item_count):
        name, count = self.item(item_count)
        return self.response({'title': self.title(name, count),
                              'price': self.price(name, count)})
