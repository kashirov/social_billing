# -*- coding: utf-8 -*-


class Response(object):

    code = 0
    id = 0
    sum = 0
    comment = ''

    def response(self):
        return '''<?xml version="1.0" encoding="windows-1251"?>
            <response>
                <id>%s</id>
                <id_shop>%s</id_shop>
                <sum>%s</sum>
                <result>%s</result>
                <comment>%s</comment>
            </response>
        ''' % (self.id, self.id, self.sum, self.code, self.comment)