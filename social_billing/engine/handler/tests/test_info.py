# -*- coding: utf-8 -*-
from social_billing.base_test import BaseTest
from social_billing.engine.errors import InvalidCountError, UnknownItemError,\
    ItemFormatError
from social_billing.engine.handler.info import Info


class InfoTest(BaseTest):

    def setUp(self):
        super(InfoTest, self).setUp()
        self.info = Info(self.items)
        self.gems = self.info.get_item('gems')

    def test_item(self):
        self.eq(self.info.split_item_count('gems_20'), ('gems', 20))
        self.eq(self.info.split_item_count('gems_10'), ('gems', 10))

    def test_price(self):
        self.eq(self.info.price(self.gems, 10), 1)
        self.eq(self.info.price(self.gems, 20), 2)

    def test_title(self):
        self.eq(self.info.title('gems', 20), u'20 алмазов')
        self.eq(self.info.title('gems', 10), u'10 алмазов')

    def test_info(self):
        self.eq(
            self.info('gems_10'),
            self.info.response(
                {'title': self.info.title('gems', 10), 'price': 1,
                 'photo_url': self.items['gems']['image']}
            )
        )

    def test_info_error(self):
        for error, item in [(ItemFormatError, 'gems_no'),
                            (UnknownItemError, 'coins_10'),
                            (InvalidCountError, 'gems_11')]:

            self.raises(error, self.info, item)

    def test_item_format_error(self):
        self.raises(ItemFormatError, self.info.split_item_count, 'item_no')
        self.raises(ItemFormatError, self.info.split_item_count, 'item10')

    def test_unknown_item(self):
        self.raises(UnknownItemError, self.info.get_item, 'item')

    def test_invalid_count(self):
        self.raises(InvalidCountError, self.info.price, self.gems, 11)
    