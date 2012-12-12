# -*- coding: utf-8 -*-
import re

from pymongo import Connection

from social_billing.errors import ItemFormatError, UnknownItemError,\
    InvalidCountError

CHARGEABLE = 'chargeable'


class Payment(object):

    item_regexp = re.compile('^([a-z]+)_([0-9]+)$')

    def __init__(self, prices, callback, db_prefix='test'):
        self.prices = prices
        self.callback = callback

        self.db = Connection()['payment_%s' % db_prefix]
        self.collection = self.db['order']

    def item(self, arg):
        match = self.item_regexp.match(arg)
        if match:
            name, count = match.groups()
            return name, int(count)
        else:
            raise ItemFormatError()

    def price(self, name, count):
        item = self.prices.get(name)

        if item is None:
            raise UnknownItemError()
        elif count not in item:
            raise InvalidCountError()
        else:
            return item[count]

    def has_order(self, order_id):
        return self.collection.find_one({'order_id': order_id}) is not None

    def ischargeable(self, status):
        return status == CHARGEABLE

    def order(self, order_id, receiver_id, item, count, status):
        if not self.has_order(order_id) and self.ischargeable(status):
            self.process(order_id, receiver_id, item, count)
        return {'order_id': order_id}

    def process(self, order_id, receiver_id, item, count):
        self.collection.insert({'order_id': order_id})
        self.callback(receiver_id, item, count)
