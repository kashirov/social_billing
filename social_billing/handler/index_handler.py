# -*- coding: utf-8 -*-
from social_billing.errors import ItemFormatError, UnknownItemError,\
    InvalidCountError
from social_billing.handler.base_handler import BaseHandler


ORDER = 'order_status_change'
GET_ITEM = 'get_item'


class IndexHandler(BaseHandler):

    def title(self, name, count):
        return '%s %s' % (count, self.locale.translate(name))

    def price(self, name, count):
        return self.store[name][count]

    def isget_item(self, ntype):
        return ntype.startswith(GET_ITEM)

    def isorder(self, ntype):
        return ntype.startswith(ORDER)

    def post(self):
        notification_type = self.get_argument('notification_type')
        try:

            name, count = self.payment.item(self.get_argument('item'))

            if self.isget_item(notification_type):
                return self.response({'title': self.title(name, count),
                                      'price': self.payment.price(name, count)})
            elif self.isorder(notification_type):
                order_id = self.get_argument('order_id')
                receiver_id = self.get_argument('receiver_id')
                status = self.get_argument('status')

                order = self.payment.order(order_id, receiver_id, name,
                                           count, status)
                return self.response(order)
        except (ItemFormatError, UnknownItemError, InvalidCountError) as error:
            return self.error(error.code, error.msg)

    get = post
