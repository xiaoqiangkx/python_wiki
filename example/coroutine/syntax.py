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
@time: 2016/1/10 15:02
@change_time: 
    1.2016/1/10 15:02
"""


def coroutine_test():
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

    def coroutine(func):
        def gen_func(*args, **kwargs):
            c = func(*args, **kwargs)
            c.next()
            return c

        return gen_func

    @coroutine
    def printer():
        try:
            while True:
                line = (yield)
                print line
        except GeneratorExit:
            print "exit"

    @coroutine
    def co_filter(target):
        try:
            while True:
                line = (yield)
                if line.get('status', -1) == 200:
                    target.send(line)
        except GeneratorExit:
            print "exit"

    def producer(log, c):
        for l in log:
            c.send(l)

    producer(apache_log(follow(data_directory)), co_filter(printer()))


if __name__ == '__main__':
    coroutine_test()