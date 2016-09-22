#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: xiaoqiangkx
@license: xx
@contact: xiaoqiangkx@163.com
@site: http://www.xx.com
@software: PyCharm Community Edition
@file: coroutine.py
@time: 2016/1/9 17:25
@change_time: 
    1.2016/1/9 17:25
"""


def coroutine_func():
    """
    generator可以接收数据, co_routine是一种消费者和生产者模型
    :return:
    """
    def consumer(func):
        def start(*args, **kwargs):
            c = func(*args, **kwargs)
            c.next()
            return c
        return start

    @consumer
    def recv_count():
        try:
            while True:
                n = (yield)
                print "T-minus", n
        except GeneratorExit:
            print "exit aha"

    r = recv_count()
    for i in range(5, 0, -1):
        print "i:", i
        r.send(i)
    r.close()


if __name__ == '__main__':
    coroutine_func()