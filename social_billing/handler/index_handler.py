# -*- coding: utf-8 -*-
from social_billing.handler.base_handler import BaseHandler


class IndexHandler(BaseHandler):

    store = {'gems': {10: 1, 20: 2}}

    def get_item(self):
        item = self.get_argument('item')
        name, count = item.split('_')
        return name, int(count)

    def title(self, name, count):
        return '%s %s' % (count, self.locale.translate(name))

    def price(self, name, count):
        return self.store[name][count]

    def post(self):
        name, count = self.get_item()
        return self.response({'title': self.title(name, count),
                              'price': self.price(name, count)})
