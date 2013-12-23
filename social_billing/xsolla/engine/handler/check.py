# -*- coding: utf-8 -*-


class Check(object):

    def __init__(self):
        pass

    def __call__(self, user_id):
        return '''<?xml version="1.0" encoding="windows-1251"?>
            <response>
                <result>0</result>
            </response>'''
