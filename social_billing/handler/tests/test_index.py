# -*- coding: utf-8 -*-
from social_billing.base_test import BaseTest
from social_billing.handler.index_handler import IndexHandler


class IndexTest(BaseTest):

    def setUp(self):
        super(IndexTest, self).setUp()
        self.handler = self.fake(IndexHandler)
        self.handler.set_args(self.request('gems_20'))

    def request(self, item='gems_20'):
        return {'notification_type': 'get_item', 'item': item}

    def test_get_item(self):
        self.eq(self.handler.get_item(), ('gems', 20))
        self.handler.set_args(self.request('gems_10'))
        self.eq(self.handler.get_item(), ('gems', 10))

    def test_title(self):
        self.eq(self.handler.title('gems', 20), u'20 алмазов')
        self.eq(self.handler.title('gems', 10), u'10 алмазов')

    def test_price(self):
        self.eq(self.handler.price('gems', 20), 2)
        self.eq(self.handler.price('gems', 10), 1)

    def test_post(self):
        self.eq(self.handler.post(self.request()),
                {'response': {'title': u'20 алмазов', 'price': 2}})
