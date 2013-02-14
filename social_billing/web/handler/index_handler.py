# -*- coding: utf-8 -*-
from urlparse import parse_qs, parse_qsl
from social_billing.engine.errors import ItemFormatError, UnknownItemError,\
    InvalidCountError
from social_billing.web.handler.base_handler import BaseHandler


ORDER = 'order_status_change'
GET_ITEM = 'get_item'


class IndexHandler(BaseHandler):

    def isget_item(self, ntype):
        return ntype.startswith(GET_ITEM)

    def isorder(self, ntype):
        return ntype.startswith(ORDER)

    def gen_args(self):
        for name, value in parse_qsl(self.request.query, True):
            yield name, value

    def args(self):
        return dict(self.gen_args())

    def post(self):
        return self.finish(self.payment.request(self.args()))

    get = post
