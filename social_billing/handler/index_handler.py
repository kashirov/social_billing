# -*- coding: utf-8 -*-
from social_billing.errors import ItemFormatError, UnknownItemError,\
    InvalidCountError
from social_billing.handler.base_handler import BaseHandler


ORDER = 'order_status_change'
GET_ITEM = 'get_item'


class IndexHandler(BaseHandler):

    def isget_item(self, ntype):
        return ntype.startswith(GET_ITEM)

    def isorder(self, ntype):
        return ntype.startswith(ORDER)

    def post(self):
        notification_type = self.get_argument('notification_type')
        item = self.get_argument('item')

        if self.isget_item(notification_type):
            return self.finish(self.payment.info(item))
        elif self.isorder(notification_type):
            order_id = self.get_argument('order_id', 'receiver_id')
            receiver_id = self.get_argument('receiver_id')
            status = self.get_argument('status')
            return self.finish(self.payment.order(order_id, receiver_id,
                                                  item, status))

    get = post
