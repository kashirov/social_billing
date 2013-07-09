# -*- coding: utf-8 -*-
from social_billing.base_order import BaseOrder
from social_billing.vk.engine.errors import CallbackError
from social_billing.vk.engine.handler.billing import BillingHandler


CHARGEABLE = 'chargeable'


class VKOrder(BaseOrder, BillingHandler):

    def ischargeable(self, status):
        return status == CHARGEABLE

    def __call__(self, order_id, receiver_id, item_count, status):
        if not self.has_order(order_id) and self.ischargeable(status):
            name, count = self.split_item_count(item_count)
            self.process(order_id, receiver_id, name, count)
        return self.response({'order_id': order_id})
