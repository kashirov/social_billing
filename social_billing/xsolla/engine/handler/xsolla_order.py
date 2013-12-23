# -*- coding: utf-8 -*-
from social_billing.base_order import BaseOrder
from social_billing.xsolla.engine.errors import CallbackError
from social_billing.xsolla.engine.response import Response


class XsollaOrder(BaseOrder):

    def __call__(self, order_id, receiver_id, name, count, price):
        if not self.has_order(order_id):
            self.process(order_id, receiver_id, name, count)
        return self.response(order_id, price)

    def process(self, order_id, receiver_id, name, count):
        if self.callback(receiver_id, name, count):
            self.collection.insert({'order_id': order_id})
        else:
            raise CallbackError()

    def response(self, order_id, sum):
        response = Response()
        response.id = order_id
        response.sum = sum
        return response.response()
