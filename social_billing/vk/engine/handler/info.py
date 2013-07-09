# -*- coding: utf-8 -*-
import tornado

from social_billing.vk.engine.errors import UnknownItemError, InvalidCountError
from social_billing.vk.engine.handler.billing import BillingHandler


class Info(BillingHandler):

    def __init__(self, prices):
        self.items = prices
        self.locale = tornado.locale.get('ru_RU')

    def get_item(self, name):
        item = self.items.get(name)
        if item is None:
            raise UnknownItemError()
        return item

    def price(self, item, count):
        price = item['prices'].get(count)

        if price is None:
            raise InvalidCountError()
        else:
            return price

    def title(self, name, count):
        return ' '.join((str(count), self.locale.translate(name)))

    def image(self, item):
        return item.get('image', '')

    def __call__(self, item_count):
        name, count = self.split_item_count(item_count)
        item = self.get_item(name)
        return self.response({'title': self.title(name, count),
                              'price': self.price(item, count),
                              'photo_url': self.image(item)})
