# -*- coding: utf-8 -*-
from social_billing.base_test import BaseTest
from social_billing.errors import CallbackError, ItemFormatError
from social_billing.order import Order, CHARGEABLE


class OrderTest(BaseTest):

    def setUp(self):
        super(OrderTest, self).setUp()
        self.order = Order(self.payment.collection, self.engine.callback)

    def test_order(self):
        self.eq(self.order(1, 'uid', 'gems_10', CHARGEABLE),
                self.order.response({'order_id': 1}))

    def test_db(self):
        self.order(1, 'uid', 'gems_10', CHARGEABLE)
        self.eq(list(self.order.collection.find({'order_id': 1},
                                                {'_id': False})),
                [{'order_id': 1}])

    def test_callback(self):
        for _ in xrange(3):
            self.order(1, 'uid', 'gems_10', CHARGEABLE)

        self.eq(self.engine.log, [('uid', 'gems', 10)])

    def test_callback_not_chargeable(self):
        self.order(1, 'uid', 'gems_10', False)
        self.eq(self.engine.log, [])

    def test_order_error(self):
        self.raises(ItemFormatError, self.payment.order, 1,
                    'uid', 'item_no', CHARGEABLE)

    def test_order_callback_error(self):
        self.payment.order.callback = self.error_callback
        self.raises(CallbackError, self.payment.order,
                    1, 'uid', 'gems_10', CHARGEABLE)
