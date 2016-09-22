# -*- coding: utf-8 -*-


class A(object):
    a = 1

    def __init__(self):
        pass
if __name__ == '__main__':
    a1 = A()
    a2 = A()
    a1.a = 2
    print "a1.a:", a1.a
    print "a2.a:", a2.a