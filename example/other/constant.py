# -*- coding: utf-8 -*-


class _const(object):
    class ConstError(TypeError):
        pass

    class ConstCaseError(ConstError):
        pass
    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError, "Can't change const. {p_name}".format(p_name=name)
        if not name.isupper():
            raise self.ConstCaseError,\
                  'const name "{p_name}" is not all uppercase.'.format(p_name=name)

        self.__dict__[name] = value

import sys
sys.modules[__name__] = _const()    # 保证这有一份数据
constant.MY_NAME = "hello"