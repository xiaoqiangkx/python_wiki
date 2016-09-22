# -*- coding: utf-8 -*-


class A(object):
    def fox(self):
        print "fox"

def cat(self):
        print "cat"

def dog(self):
    print "dog"

def duck(self):
    print "duck"


if __name__ == '__main__':
    a1 = A()
    a2 = A()
    a1.fox()
    a2.fox()
    print '-' * 30

    A.fox = dog
    a1.fox()
    a2.fox()
    print '-' * 30

    import new
    a2.fox = new.instancemethod(cat, a2, A)
    a1.fox()
    a2.fox()
    print '-' * 30

    print dir(a1)
    print dir(a2)

    A.fox = duck
    a1.fox()
    a2.fox()        # 输出cat，由于__dict__中的级别更高
    print '-' * 30

    print a1.__dict__
    print a2.__dict__
    print '-' * 30
