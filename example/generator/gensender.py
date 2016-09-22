#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: xiaoqiangkx
@license: xx
@contact: xiaoqiangkx@163.com
@site: http://www.xx.com
@software: PyCharm Community Edition
@file: gensender.py
@time: 2016/1/9 16:14
@change_time: 
    1.2016/1/9 16:14
"""


def generate_sender():
    def gen_sender():
        import socket
        import time
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("127.0.0.1", 9000))

        while True:
            s.sendall("Hello Server\n")
            data = s.recv(1024)
            if len(data) == 0:
                time.sleep(1)
                continue

            yield data

        s.close()

    for message in gen_sender():
        print message


if __name__ == '__main__':
    generate_sender()