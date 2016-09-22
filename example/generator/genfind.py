#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: xiaoqiangkx
@license: xx
@contact: xiaoqiangkx@163.com
@site: http://www.xx.com
@software: PyCharm Community Edition
@file: genfind.py.py
@time: 2016/1/9 15:37
@change_time: 
    1.2016/1/9 15:37
"""


def generate_find():
    import os
    import fnmatch
    data_directory = "data\www"

    def gen_find(filepat, top):
        for path, dirlist, filelist in os.walk(top):
            for name in fnmatch.filter(filelist, filepat):
                yield os.path.join(path, name)

    def gen_open(filenames):
        import gzip
        import bz2
        for name in filenames:
            if name.endswith(".gz"):
                yield gzip.open(name)
            elif name.endswith(".bz2"):
                yield bz2.BZ2File(name)
            else:
                yield open(name)

    def gen_cat(sources):
        for s in sources:
            for item in s:
                yield item

    def gen_grep(pat, lines):
        import re
        patc = re.compile(pat)
        for line in lines:
            if patc.search(line):
                yield line

    def gen_groups(pat, lines):
        import re
        patc = re.compile(pat)
        for line in lines:
            g = patc.match(line)
            if g:
                yield g.groups()

    def field_map(dictseq, name, func):
        for d in dictseq:
            d[name] = func(d[name])
            yield d

    def follow(data_directory):
        lognames = gen_find("access-log*", data_directory)
        logfiles = gen_open(lognames)
        loglines = gen_cat(logfiles)
        return loglines

    def apache_log(loglines):
        logpats = r'(\S+) (\S+) (\S+) \[(.*?)\] 'r'"(\S+) (\S+) (\S+)" (\S+) (\S+)'
        groups = gen_groups(logpats, loglines)
        colnames = ('host', 'referrer', 'user', 'datetime', 'method', 'request', 'proto', 'status', 'bytes')
        log = (dict(zip(colnames, t)) for t in groups)
        log = field_map(log, "status", int)
        log = field_map(log, "bytes", lambda s: int(s) if s != '-' else 0)
        return log

    def gen_pickle(source):
        import pickle
        for item in source:
            yield pickle.dumps(item)

    def send_to(source, addr):
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(addr)
        for pitem in gen_pickle(source):
            s.sendall(pitem)
        s.close()

    lines = follow(data_directory)
    log = apache_log(lines)
    # send_to(log, ("127.0.0.1", 9000))

    import Queue
    import threading
    class ConsumerThread(threading.Thread):
        def __init__(self, target):
            self.target = target
            threading.Thread.__init__(self)
            self.setDaemon(True)
            self.in_queue = Queue.Queue()

        def generate(self):
            while True:
                item = self.in_queue.get()
                yield item

        def run(self):
            self.target(self.generate())

        def send(self, item):
            self.in_queue.put(item)

    def find_404(log):
        for r in (r for r in log if r['status'] == 404):
            print r['status'], r['datetime'], r['request']

    def broadcast(source, consumer):
        for item in source:
            for c in consumer:
                c.send(item)

    c1 = ConsumerThread(find_404)
    c1.start()
    broadcast(log, [c1])

if __name__ == '__main__':
    generate_find()