# -*- coding: utf-8 -*-
from social_billing.xsolla.engine.payment import CHECK, PAY
from social_billing.xsolla.engine.errors import CallbackError, \
    SignatureError
from tests.xsolla.xsolla_base_test import XsollaBaseTest


class PaymentTest(XsollaBaseTest):

    def setUp(self):
        super(PaymentTest, self).setUp()

    def test_request_check(self):
        self.eq(self.payment.request(self.check_args(command=CHECK, v1='user')),
                self.payment.check('user_id'))

    def test_request_order(self):
        self.eq(self.payment.request(self.order_args(command=PAY, id=1,
                                                     v1='user', sum=1)),
                self.payment.order(1, 'user', 'gems', 10, 1))

    def test_request_error_callback(self):
        self.payment.order.callback = self.error_callback
        self.eq(self.payment.request(self.order_args(command=PAY, id=1,
                                                     v1='user', sum=1)),
                CallbackError().response())

    def test_request_error_sig(self):
        args = self.order_args(command=PAY, id=1, v1='user', sum=1)
        args['md5'] = 'error'
        self.eq(self.payment.request(args),
                SignatureError().response())
