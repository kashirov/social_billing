# -*- coding: utf-8 -*-
from social_billing.engine.errors import CallbackError
from social_billing.engine.handler.billing import BillingHandler


CHARGEABLE = 'chargeable'


class Order(BillingHandler):

    def __init__(self, collection, callback):
        self.collection = collection
        self.callback = callback

    def has_order(self, order_id):
        return self.collection.find_one({'order_id': order_id}) is not None

    def ischargeable(self, status):
        return status == CHARGEABLE

    def process(self, order_id, receiver_id, item_count):
        name, count = self.item(item_count)
        if self.callback(receiver_id, name, count):
            self.collection.insert({'order_id': order_id})
        else:
            raise CallbackError()

    def __call__(self, order_id, receiver_id, item_count, status):
        if not self.has_order(order_id) and self.ischargeable(status):
            self.process(order_id, receiver_id, item_count)
        return self.response({'order_id': order_id})
