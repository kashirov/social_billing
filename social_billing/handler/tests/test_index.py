# -*- coding: utf-8 -*-
from social_billing.base_test import BaseTest
from social_billing.handler.index_handler import IndexHandler, GET_ITEM, \
    ORDER, CHARGEABLE


class IndexTest(BaseTest):

    def callback(self, *args):
        pass

    def setUp(self):
        super(IndexTest, self).setUp()
        self.handler = self.fake(IndexHandler)
        self.handler.init({'gems': {10: 1, 20: 2}}, self.callback)
        self.handler.set_args(self.get_item('gems_20'))

    def get_item(self, item='gems_20', ntype=GET_ITEM):
        return {'notification_type': ntype, 'item': item}

    def order_status_change(self):
        return {'notification_type': ORDER, 'status': CHARGEABLE,
                'item': 'gems_20', 'price': '10', 'order_id': '100500',
                'receiver_id': 'uidhere'}

    def test_title(self):
        self.eq(self.handler.title('gems', 20), u'20 алмазов')
        self.eq(self.handler.title('gems', 10), u'10 алмазов')

    def test_post_get_info(self):
        self.eq(self.handler.post(self.get_item()),
                {'response': {'title': u'20 алмазов', 'price': 2}})

    def test_post_order(self):
        self.eq(self.handler.post(self.order_status_change()),
                {'response': {'order_id': '100500'}})
