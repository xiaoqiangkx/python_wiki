#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: xiaoqiangkx
@license: xx
@contact: xiaoqiangkx@163.com
@site: http://www.xx.com
@software: PyCharm Community Edition
@file: genreceive.py
@time: 2016/1/9 16:06
@change_time: 
    1.2016/1/9 16:06
"""


def generate_receiver():
    def receive_connections(addr):
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)     # TODO: TCP不记得了
        s.bind(addr)
        s.listen(5)

        while True:
            client = s.accept()
            yield client

    def gen_events(socks):
        import select
        while True:
            if not socks:
                import time
                time.sleep(0.1)
                continue

            read_events, write_events, err_events = select.select(socks, socks, socks, 0.1)
            for r in read_events:
                yield "read", r

            for w in write_events:
                yield "write", w

            for e in err_events:
                yield "error", e

    # print "server is on..."
    # for c, a in receive_connections(("", 9000)):
    #     c.send("Hello World\n")
    client_set = []

    def accepter(socket_set, addr):
        for c, a in receive_connections(addr):
            socket_set.append(c)

    import threading
    accept_thread = threading.Thread(target=accepter, args=(client_set, ("", 9000)))
    accept_thread.setDaemon(True)
    accept_thread.start()

    for evt, s in gen_events(client_set):
        if evt == "read":
            data = s.recv(1024)
            if not data:
                print "Closing", s
                s.close()
                client_set.remove(s)
            else:
                print s, data
                s.send("Hello World\n")

if __name__ == '__main__':
    generate_receiver()