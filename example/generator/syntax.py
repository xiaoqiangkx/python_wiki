#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: xiaoqiangkx
@license: xx
@contact: xiaoqiangkx@163.com
@site: http://www.xx.com
@software: PyCharm Community Edition
@file: syntax.py
@created_time: 2016/1/9 11:52
@change_time: 
    1.2016/1/9 11:52
"""


# 1. iterator协议
def iterator_func():

    class ListIterator(object):
        def __init__(self, data):
            self.data = data
            self.index = 0

        def next(self):
            try:
                result = self.data[self.index]  # TODO: 只能用于List的Iterator
                self.index += 1
                return result
            except IndexError:
                raise StopIteration()

    class BookShelf(object):
        def __init__(self):
            self.books = ["book_{0}".format(x) for x in xrange(1, 10, 1)]

        def __iter__(self):
            return ListIterator(self.books)

    book_shelf = BookShelf()
    for book in book_shelf:
        print book


def generator_func():
    """
    Generator是一个返回序列的函数，更简便实现iterator的方式
    :return:
    """
    class BookShelf(object):
        def __init__(self):
            self.books = ["book_{0}".format(x) for x in xrange(1, 10, 1)]

        def get_iter(self):
            """
            one-time operation: 生成一个物品序列
            :return:
            """
            for book in self.books:
                yield book

    book_iter = BookShelf().get_iter()
    for book in book_iter:
        print book


def generate(func):
    """
    封装任意函数为generator，支持输入iterator
    :param func:
    :return:
    """
    def gen_func(s):
        for item in s:
            yield func(item)
    return gen_func


def trace(sources):
    """
    打印输出流信息
    :param sources:
    :return:
    """
    for item in sources:
        print item
        yield sources


class StoreLast(object):
    """
    修改next的默认规则
    """
    def __init__(self, source):
        self.source = source

    def next(self):
        item = self.source.next()
        self.last = item
        return item

    def __iter__(self):
        return self


if __name__ == '__main__':
    iterator_func()
    generator_func()