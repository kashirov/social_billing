# -*- coding: utf8 -*-
from social_billing.base_order import BaseOrder


class MMOrder(BaseOrder):

    def __call__(self, args):
        transaction_id = args['transaction_id']
        if not self.has_order(transaction_id):
            self.process(transaction_id, args['uid'], None, args['service_id'])
        return {'status': 1}