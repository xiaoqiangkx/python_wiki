# -*- coding: utf-8 -*-

print __name__
class IterTest(object):
    """
    只能一层循环的迭代类
    """
    def __init__(self):
        self._list = [1, 2, 3, 4, 5]    # '_'并不是强制性的私有变量
        self._cur_idx = 0

    def next(self):
        if self._cur_idx < len(self._list):
            res = self._list[self._cur_idx]
            self._cur_idx += 1
            return res
        else:
            raise StopIteration

    def __iter__(self):
        self._cur_idx = 0
        return self


class FooIterator(object):
    def __init__(self, csv):
        self._csv = csv
        self._cur_idx = 0

    def next(self):
        if self._cur_idx >= len(self._csv):
            raise StopIteration
        else:
            res = self._csv[self._cur_idx]
            self._cur_idx += 1
            return res


class Foo(object):
    """
    使用独立的迭代类
    """
    def __init__(self):
        self._list = [1, 2, 3, 4, 5]

    def __iter__(self):
        return FooIterator(self)

    def __len__(self):
        return len(self._list)

    def __getitem__(self, item):
        return self._list[item]


class YieldFoo(object):
    def __init__(self):
        self._list = [1, 2, 3, 4, 5]

    def __iter__(self):
        for v in self._list:
            yield v


class BorrowingFoo(object):
    def __init__(self):
        self._list = [1, 2, 3, 4, 5]

    def __iter__(self):
        return iter(self._list)


class ClosureFoo(object):
    def __init__(self):
        self._list = [1, 2, 3, 4, 5]

    def __iter__(self):
        encounter = [0]

        def get():
            if encounter[0] >= len(self._list):
                raise StopIteration
            else:
                res = self._list[encounter[0]]
                encounter[0] += 1
                return res
        return iter(get, None)

if __name__ == '__main__':
    iter_instance = IterTest()
    print "------------first kind---------------"
    for i in iter_instance:
        for j in iter_instance:
            print i, j

    print "------------second kind--------------"
    foo_instance = Foo()
    for i in foo_instance:
        for j in foo_instance:
            print i, j

    print "------------third kind---------------"
    yield_foo_instance = YieldFoo()
    for i in yield_foo_instance:
        for j in yield_foo_instance:
            print i, j

    print "------------forth kind----------------"
    borrowing_foo_instance = BorrowingFoo()
    for i in borrowing_foo_instance:
        for j in borrowing_foo_instance:
            print i, j

    print "------------fifth kind-----------------"
    closure_foo_instance = ClosureFoo()
    for i in closure_foo_instance:
        for j in closure_foo_instance:
            print i, j


