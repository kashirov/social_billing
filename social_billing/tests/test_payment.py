# -*- coding: utf-8 -*-
from ztest import ZTest

from social_billing.payment import Payment


class Engine(object):

    def __init__(self):
        self.log = []

    def callback(self, receiver_id, name, count):
        self.log.append((receiver_id, name, count))


class PaymentTest(ZTest):

    def setUp(self):
        super(PaymentTest, self).setUp()
        self.engine = Engine()
        self.payment = Payment({'gems': {10: 1, 20: 2}},
                               self.engine.callback)
        self.payment.db.drop_collection(self.payment.collection)

    def test_item(self):
        self.eq(self.payment.item('gems_20'), ('gems', 20))
        self.eq(self.payment.item('gems_10'), ('gems', 10))

    def test_price(self):
        self.eq(self.payment.price('gems', 10), 1)
        self.eq(self.payment.price('gems', 20), 2)

    def test_order(self):
        self.eq(self.payment.order(1, 'uid', 'gems', 10, True),
                {'order_id': 1})

    def test_order_db(self):
        self.payment.order(1, 'uid', 'gems', 10, True)
        self.eq(list(self.payment.collection.find({'order_id': 1},
                                                  {'_id': False})),
                [{'order_id': 1}])

    def test_order_callback(self):
        for _ in xrange(3):
            self.payment.order(1, 'uid', 'gems', 10, True)

        self.eq(self.engine.log, [('uid', 'gems', 10)])

    def test_order_callback_not_chargeable(self):
        self.payment.order(1, 'uid', 'gems', 10, False)

        self.eq(self.engine.log, [])
