# -*- coding: utf-8 -*-


class OldStyleClass:
    def __init__(self):
        pass


class NewStyleClass(object):
    def __init__(self):
        pass

if __name__ == '__main__':
    print "new style class: (type,class)", type(NewStyleClass), NewStyleClass.__class__
    print "old style class: (type,class)", type(OldStyleClass), #OldStyleClass.__class__