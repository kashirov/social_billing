# -*- coding: utf-8 -*-
from social_billing.web.handler.base_handler import BaseHandler


class IndexHandler(BaseHandler):
    def gen_args(self):
        for name, value in self.request.arguments.iteritems():
            yield name, value[0]

    def args(self):
        return dict(self.gen_args())

    def post(self):
        return self.finish(self.payment.request(self.args()))

    get = post