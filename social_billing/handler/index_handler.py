# -*- coding: utf-8 -*-
from social_billing.handler.base_handler import BaseHandler

ORDER = 'order_status_change'
GET_ITEM = 'get_item'
CHARGEABLE = 'chargeable'


class IndexHandler(BaseHandler):

    def title(self, name, count):
        return '%s %s' % (count, self.locale.translate(name))

    def price(self, name, count):
        return self.store[name][count]

    def post(self):
        notification_type = self.get_argument('notification_type')
        name, count = self.payment.item(self.get_argument('item'))

        if notification_type == GET_ITEM:
            return self.response({'title': self.title(name, count),
                                  'price': self.payment.price(name, count)})
        elif notification_type == ORDER:
            order_id = self.get_argument('order_id')
            receiver_id = self.get_argument('receiver_id')
            return self.response(self.payment.order(order_id, receiver_id,
                                                    name, count))
