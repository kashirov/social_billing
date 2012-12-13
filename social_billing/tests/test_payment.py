# -*- coding: utf-8 -*-
from social_billing.base_test import BaseTest
from social_billing.errors import ItemFormatError, UnknownItemError,\
    InvalidCountError
from social_billing.payment import Payment, CHARGEABLE


class Engine(object):

    def __init__(self):
        self.log = []

    def callback(self, receiver_id, name, count):
        self.log.append((receiver_id, name, count))


class PaymentTest(BaseTest):

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

    def test_title(self):
        self.eq(self.payment.title('gems', 20), u'20 алмазов')
        self.eq(self.payment.title('gems', 10), u'10 алмазов')

    def test_info(self):
        self.eq(self.payment.info('gems_10'),
                self.payment.response({'title': self.payment.title('gems', 10),
                'price': 1}))

    def test_info_error(self):
        for error, item in [(ItemFormatError(), 'gems_no'),
                            (UnknownItemError(), 'coins_10'),
                            (InvalidCountError(), 'gems_11')]:

            self.eq(self.payment.info(item),
                    {'error': {'error_code': error.code,
                               'error_msg': error.msg,
                               'critical': 1}})

    def test_order(self):
        self.eq(self.payment.order(1, 'uid', 'gems_10', CHARGEABLE),
                self.payment.response({'order_id': 1}))

    def test_order_db(self):
        self.payment.order(1, 'uid', 'gems_10', CHARGEABLE)
        self.eq(list(self.payment.collection.find({'order_id': 1},
                                                  {'_id': False})),
                [{'order_id': 1}])

    def test_order_callback(self):
        for _ in xrange(3):
            self.payment.order(1, 'uid', 'gems_10', CHARGEABLE)

        self.eq(self.engine.log, [('uid', 'gems', 10)])

    def test_order_callback_not_chargeable(self):
        self.payment.order(1, 'uid', 'gems_10', False)

        self.eq(self.engine.log, [])

    def test_payment_error(self):
        for error, item in [(ItemFormatError(), 'gems_no'),]:

            self.eq(self.payment.order(1, 'uid', item, CHARGEABLE),
                    {'error': {'error_code': error.code,
                               'error_msg': error.msg,
                               'critical': 1}})

    def test_item_format_error(self):
        self.raises(ItemFormatError, self.payment.item, 'item_no')
        self.raises(ItemFormatError, self.payment.item, 'item10')

    def test_unknown_item(self):
        self.raises(UnknownItemError, self.payment.price, 'item', 10)

    def test_invalid_count(self):
        self.raises(InvalidCountError, self.payment.price, 'gems', 11)
