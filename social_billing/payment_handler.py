# -*- coding: utf-8 -*-
import re

from social_billing.errors import ItemFormatError


class PaymentHandler(object):

    item_regexp = re.compile('^([a-z]+)_([0-9]+)$')

    def item(self, arg):
        match = self.item_regexp.match(arg)
        if match:
            name, count = match.groups()
            return name, int(count)
        else:
            raise ItemFormatError()

    def response(self, msg):
        return {'response': msg}
    