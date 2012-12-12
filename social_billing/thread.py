# -*- coding: utf-8 -*-
from threading import Thread

from tornado.ioloop import IOLoop

from social_billing.app import application
from social_billing.handler.base_handler import BaseHandler


class BillingThread(Thread):

    def __init__(self, prices, callback, port=8888):
        super(BillingThread, self).__init__()
        BaseHandler.init(prices, callback)
        self.app = application
        self.port = port
        self.loop = IOLoop.instance()

    def run(self):
        self.app.listen(self.port)
        self.loop.start()

    def stop(self):
        self.loop.stop()


if __name__ == '__main__':
    def callback(self, *a):
        print a

    import signal
    import sys

    service = BillingThread({'gems': {10: 1, 20: 2}}, callback)

    def signal_handler(signal, frame):
        service.stop()

    signal.signal(signal.SIGINT, signal_handler)

    service.run()
    print 'started'
