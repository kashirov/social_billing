# -*- coding: utf-8 -*-
from pymongo import Connection

from social_billing.vk.engine.errors import ItemFormatError, UnknownItemError,\
    InvalidCountError, CallbackError, SignatureError
from social_billing.vk.engine.handler.info import Info
from social_billing.vk.engine.handler.vk_order import VKOrder
from social_billing.vk.engine.handler.billing import BillingHandler
from social_billing.vk.engine.signature import Signature


ORDER = 'order_status_change'
GET_ITEM = 'get_item'


class VKPayment(BillingHandler):

    def __init__(self, name, prices, secret, callback):
        self.signature = Signature(secret)
        self.info = Info(prices)
        self.order = VKOrder(name, callback)

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
