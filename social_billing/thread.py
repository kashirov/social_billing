# -*- coding: utf-8 -*-
from threading import Thread

from tornado.ioloop import IOLoop
from social_billing.base_test import TEST_PAYMENT_NAME

from social_billing.web.app import application
from social_billing.web.handler.base_handler import BaseHandler


class BillingThread(Thread):

    def __init__(self, name, prices, secret, callback, port=8888):
        super(BillingThread, self).__init__()
        BaseHandler.init(name, prices, secret, callback)
        self.app = application
        self.port = port
        self.loop = IOLoop.instance()

    def run(self):
        self.app.listen(self.port)
        self.loop.start()

    def stop(self):
        self.loop.stop()


def main():
    def callback(self, *a):
        print a

    service = BillingThread(TEST_PAYMENT_NAME,
                            {'gems': {10: 1, 20: 2}}, 'secretkey', callback)
    service.run()
    print 'started'


if __name__ == '__main__':
    main()
