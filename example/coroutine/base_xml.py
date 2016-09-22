#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: xiaoqiangkx
@license: xx
@contact: xiaoqiangkx@163.com
@site: http://www.xx.com
@software: PyCharm Community Edition
@file: base_xml.py
@time: 2016/1/10 15:55
@change_time: 
    1.2016/1/10 15:55
"""


def base_xml():
    import xml.sax
    xml_file = "data/allroutes.xml"

    class EventHandler(xml.sax.ContentHandler):
        def __init__(self, target):
            self.target = target

        def startElement(self, name, attrs):
            self.target.send(('start', (name, attrs._attrs)))

        def characters(self, text):
            self.target.send(('text', text))

        def endElement(self, name):
            self.target.send(('end', name))

    def coroutine(func):
        def gen_func(*args, **kwargs):
            c = func(*args, **kwargs)
            c.next()
            return c

        return gen_func

    @coroutine
    def bus_to_dict(target):

        while True:
            event, value = (yield)
            if event == 'start' and value[0] == 'bus':
                bus_dict = {}
                fragment = []
                while True:
                    event, value = (yield)
                    if event == 'start':
                        fragment = []
                    elif event == 'text':
                        fragment.append(value)
                    elif event == 'end':
                        if value != 'bus':
                            bus_dict[value] = "".join(fragment)
                        else:
                            target.send(bus_dict)
                            break

    @coroutine
    def printer():
        while True:
            line = (yield)
            print line


    xml.sax.parse(xml_file, EventHandler(
        bus_to_dict(printer())
    ))

if __name__ == '__main__':
    base_xml()