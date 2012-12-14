# -*- coding: utf-8 -*-
import re

import tornado.locale
from pymongo import Connection

from social_billing.errors import ItemFormatError, UnknownItemError,\
    InvalidCountError, CallbackError, SignatureError
from social_billing.signature import Signature


CHARGEABLE = 'chargeable'
ORDER = 'order_status_change'
GET_ITEM = 'get_item'


class Payment(object):

    item_regexp = re.compile('^([a-z]+)_([0-9]+)$')

    def __init__(self, prices, secret, callback, db_prefix='test'):
        self.prices = prices
        self.callback = callback

        self.db = Connection()['payment_%s' % db_prefix]
        self.collection = self.db['order']

        self.signature = Signature(secret)
        self.locale = tornado.locale.get('ru_RU')

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

    def title(self, name, count):
        return ' '.join((str(count), self.locale.translate(name)))

    def has_order(self, order_id):
        return self.collection.find_one({'order_id': order_id}) is not None

    def ischargeable(self, status):
        return status == CHARGEABLE

    def response(self, msg):
        return {'response': msg}

    def info(self, item_count):
        name, count = self.item(item_count)
        return self.response({'title': self.title(name, count),
                              'price': self.price(name, count)})

    def order(self, order_id, receiver_id, item_count, status):
        if not self.has_order(order_id) and self.ischargeable(status):
            self.process(order_id, receiver_id, item_count)
        return self.response({'order_id': order_id})

    def process(self, order_id, receiver_id, item_count):
        name, count = self.item(item_count)
        if self.callback(receiver_id, name, count):
            self.collection.insert({'order_id': order_id})
        else:
            raise CallbackError()

    def request(self, args):
        notification_type = args.get('notification_type')

        try:
            if not self.signature.check(args, args.pop('sig')):
                raise SignatureError()
            if notification_type == GET_ITEM:
                return self.info(args['item'])
            if notification_type == ORDER:
                return self.order(args['order_id'], args['receiver_id'],
                                  args['item'], args['status'])
        except (ItemFormatError, UnknownItemError, InvalidCountError,
                CallbackError, SignatureError) as error:
            return error.response()
