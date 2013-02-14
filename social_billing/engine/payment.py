# -*- coding: utf-8 -*-
from pymongo import Connection

from social_billing.engine.errors import ItemFormatError, UnknownItemError,\
    InvalidCountError, CallbackError, SignatureError
from social_billing.engine.handler.info import Info
from social_billing.engine.handler.order import Order
from social_billing.engine.handler.billing import BillingHandler
from social_billing.engine.signature import Signature


ORDER = 'order_status_change'
GET_ITEM = 'get_item'


class Payment(BillingHandler):

    def __init__(self, prices, secret, callback, db_prefix='test'):
        self.db = Connection()['payment_%s' % db_prefix]
        self.collection = self.db['order']

        self.signature = Signature(secret)
        self.info = Info(prices)
        self.order = Order(self.collection, callback)

    def request(self, args):
        notification_type = args.get('notification_type')

        try:
            if not self.signature.check(args, args.pop('sig')):
                raise SignatureError()
            if notification_type.startswith(GET_ITEM):
                return self.info(args['item'])
            if notification_type.startswith(ORDER):
                return self.order(args['order_id'], args['receiver_id'],
                                  args['item'], args['status'])
        except (ItemFormatError, UnknownItemError, InvalidCountError,
                CallbackError, SignatureError) as error:
            return error.response()
