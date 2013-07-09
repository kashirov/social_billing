# -*- coding: utf8 -*-
from urllib import urlencode

from tornado.testing import AsyncHTTPTestCase

from social_billing.core import BillingCore
from social_billing.web.app import application
from tests.mm.mm_base_test import MMBaseTest
from tests.vk.vk_base_test import TEST_PAYMENT_NAME


class IndexHandlerWithMMPaymentTest(AsyncHTTPTestCase, MMBaseTest):
    def get_app(self):
        return application

    def setUp(self):
        super(IndexHandlerWithMMPaymentTest, self).setUp()
        BillingCore.init('mm', 'gems',
                         TEST_PAYMENT_NAME, self.items, 'secretkey',
                         self.engine.callback)

    def test_buy(self):
        args = urlencode(self.signed_args())
        self.http_client.fetch(self.get_url('/?' + args), self.stop)
        response = self.wait()
        self.eq(response.code, 200)
        self.eq(response.body, '{"status": 1}')