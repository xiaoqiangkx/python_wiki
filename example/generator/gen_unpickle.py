#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: xiaoqiangkx
@license: xx
@contact: xiaoqiangkx@163.com
@site: http://www.xx.com
@software: PyCharm Community Edition
@file: gen_unpickle.py
@time: 2016/1/9 16:53
@change_time: 
    1.2016/1/9 16:53
"""


def generate_unpickle():
    import pickle

    def gen_unpickle(infile):
        while True:
            try:
                item = pickle.load(infile)
                yield item
            except EOFError:
                return

    def receiveform(addr):
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(addr)
        s.listen(5)
        c, a = s.accept()
        for line in gen_unpickle(c.makefile()):
            yield line
        c.close()

    for r in receiveform(("", 9000)):
        print r


if __name__ == '__main__':
    generate_unpickle()