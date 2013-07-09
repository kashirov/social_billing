# -*- coding: utf-8 -*-
import re

from social_billing.vk.engine.errors import ItemFormatError


class BillingHandler(object):

    item_regexp = re.compile('^([a-z]+)_([0-9]+)$')

    def split_item_count(self, arg):
        match = self.item_regexp.match(arg)
        if match:
            name, count = match.groups()
            return name, int(count)
        else:
            raise ItemFormatError()

    def response(self, msg):
        return {'response': msg}
    