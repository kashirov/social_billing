# -*- coding: utf8 -*-
from pymongo import Connection
from social_billing.vk.engine.errors import CallbackError


class BaseOrder(object):

    def __init__(self, name, callback):
        self.db = Connection()['payment_%s' % name]
        self.collection = self.db['order']
        self.callback = callback

    def has_order(self, order_id):
        return self.collection.find_one({'order_id': order_id}) is not None

    def __call__(self, *args, **kwargs):
        raise Exception('Template Method')

    def process(self, order_id, receiver_id, name, count):
        if self.callback(receiver_id, name, count):
            self.collection.insert({'order_id': order_id})
        else:
            raise CallbackError()