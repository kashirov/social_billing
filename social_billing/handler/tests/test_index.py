# -*- coding: utf-8 -*-
from social_billing.base_test import BaseTest
from social_billing.errors import InvalidCountError, UnknownItemError,\
    ItemFormatError
from social_billing.handler.index_handler import IndexHandler, GET_ITEM, \
    ORDER
from social_billing.payment import CHARGEABLE


class IndexTest(BaseTest):

    def setUp(self):
        super(IndexTest, self).setUp()
        self.handler = self.fake(IndexHandler)
        self.handler.set_args(self.get_item('gems_20'))
        self.payment = self.handler.payment

    def get_item(self, item='gems_20', ntype=GET_ITEM):
        return {'notification_type': ntype, 'item': item}

    def order_status_change(self):
        return {'notification_type': ORDER, 'status': CHARGEABLE,
                'item': 'gems_20', 'price': '10', 'order_id': '100500',
                'receiver_id': 'uidhere'}

    def test_post_get_info(self):
        self.eq(self.handler.post(self.get_item()),
                {'response': {'title': u'20 алмазов', 'price': 2}})

    def test_post_order(self):
        self.eq(self.handler.post(self.order_status_change()),
                {'response': self.payment.order('100500', 'uid', 'gems', 10,
                                                True)})

    def test_errors(self):
        for error, item in [(ItemFormatError(), 'gems_no'),
                            (UnknownItemError(), 'coins_10'),
                            (InvalidCountError(), 'gems_11')]:

            self.eq(self.handler.post(self.get_item(item=item)),
                    {'error': {'error_code': error.code,
                               'error_msg': error.msg,
                               'critical': 1}})
