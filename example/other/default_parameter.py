# -*- coding: utf-8 -*-


def foo(item, items = [], added = True):
    if added:
        items.append(item)

    print items

foo(1)
foo(2)
foo(3, added=False)

