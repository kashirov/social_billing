# -*- coding: utf-8 -*-
from social_billing.base_test import BaseTest
from social_billing.errors import InvalidCountError, UnknownItemError,\
    ItemFormatError


class ErorrsTest(BaseTest):

    def test_item_format(self):
        error = ItemFormatError()
        self.eq(error.code, 10)
        self.eq(error.msg, u'Неверный формат item')

    def test_unknown_item(self):
        error = UnknownItemError()
        self.eq(error.code, 11)
        self.eq(error.msg, u'Неизвестный item')

    def test_invalid_count(self):
        error = InvalidCountError()
        self.eq(error.code, 12)
        self.eq(error.msg, u'Неверное количество')

    