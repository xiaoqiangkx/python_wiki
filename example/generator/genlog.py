#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: xiaoqiangkx
@license: xx
@contact: xiaoqiangkx@163.com
@site: http://www.xx.com
@software: PyCharm Community Edition
@file: genlog.py
@time: 2016/1/9 15:11
@change_time: 
    1.2016/1/9 15:11
"""


def generate_log():
    """
    不生成中间变量，而且代码结构更加的清晰
    :return:
    """
    try:
        with open('data/server.log') as fp:
            line_op = (line for line in fp)

            rec_cnt_op = (line.rsplit(None, 1)[1] for line in line_op)
            int_op = (int(x) for x in rec_cnt_op if x != '-')
            result = sum(int_op)
            print "result:", result
    except Exception:
        import traceback
        traceback.print_exc()
        print "encout error"

if __name__ == '__main__':
    generate_log()