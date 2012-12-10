# -*- coding: utf-8 -*-
from pymongo import Connection


class Payment(object):

    def __init__(self, prices, callback, db_prefix='test'):
        self.prices = prices
        self.callback = callback

        self.db = Connection()['payment_%s' % db_prefix]
        self.collection = self.db['order']

    def item(self, arg):
        name, count = arg.split('_')
        return name, int(count)

    def price(self, name, count):
        return self.prices[name][count]

    def process(self, order_id, receiver_id, item, count):
        self.collection.insert({'order_id': order_id})
        self.callback(receiver_id, item, count)

    def has_order(self, order_id):
        return self.collection.find_one({'order_id': order_id}) is not None

    def order(self, order_id, receiver_id, item, count, chargeable):
        if not self.has_order(order_id) and chargeable:
            self.process(order_id, receiver_id, item, count)
        return {'order_id': order_id}
