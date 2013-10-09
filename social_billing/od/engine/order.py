# -*- coding: utf8 -*-
from social_billing.base_order import BaseOrder


class ODOrder(BaseOrder):

    def __call__(self, uid, transaction_id, item, count):
        if not self.has_order(transaction_id):
            self.process(
                transaction_id, uid, item, count
            )
        return {'status': 1}