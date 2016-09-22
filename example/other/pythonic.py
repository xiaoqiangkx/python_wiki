# -*- coding: utf-8 -*-
"""
记录一些pythonic的写法
"""

# 0. 工具
# 0.1 help：例如help(islice)

# 1. 迭代器使用
data = [1, 2, 3, 4]
for i in data:
    print i

print list(reversed(data))  # reversed返回一个反转的迭代器

for index, value in enumerate(data):
    print "index:{index}, value:{value}.".format(index=index, value=value)      # index从0开始计数


def do_enumerate(sequence):
    index = len(sequence) - 1
    for elem in reversed(sequence):
        yield index, elem
        index -= 1

for index, value in do_enumerate(data):
     print "index:{index}, value:{value}.".format(index=index, value=value)

data_dict = {1: "hello", 2: "world"}
for key, value in data_dict.iteritems():
    print "key:{key}, value:{value}".format(key=key, value=value)


# 2. 简胜繁
a = 1
b = 2
a, b = b, a
c = a if a < b else b
print 'a={a}, b={b}, the minimum={c}'.format(a=a, b=b, c=c)

print '{greet} from {language}.'.format(greet='Hello World', language="Python")
print '{0} < {1}'.format(1, 2)


# 3. 命名。不适用i、j以及内置名字list等
def find_num(search_list, num):
    for list_value in search_list:
        if num == list_value:
            return True
        else:
            pass
    return None


# 4. switch_case的替代：跳转表
def get_case(x):
    return {
        0: "0",
        1: "1",
        2: "2"
    }.get(x, "Only single-digit from 0~2 are allowed\n")    # 第二个参数是KeyError的参数

print get_case(0)
print get_case(3)


# 5. 函数注释
def quick_sort(num_list):
    """对字符串数组或者整型数组进行排序
    Args:
        num_list: 字符串数组或者整型数组

    Return：
        没有返回值，in_place_sort
    """
    if num_list is None:
        raise Exception("None is not expected in quick_sort")
    if len(num_list) <= 1:
        return

    smaller_part = []
    larger_part = []
    for num in num_list:
        if num <= num_list[0]:
            smaller_part.append(num)
        else:
            larger_part.append(num)

    num_list = smaller_part + larger_part

test_list = [3, 1, 2, 4]

try:
    quick_sort(test_list)
    print test_list
    quick_sort(None)
except Exception, e:
    print e

# 6. 常量:建议在constant中直接定义。
constant.COMPANY = "IBM"
try:
    constant.abc = "AAA"   # 一旦此句抛出异常，后面则不再执行
    constant.COMPANY = "dd"
except constant.ConstError as e:
    print e
except constant.ConstCaseError as e:
    print e

print "my name:", constant.MY_NAME


# 7. lazy evaluation
a = ["ab.", "cd.", "ef.", "eg.", "ab.", "dd.", "dd2.", "dd1.", "dd5.", "dd8.", "dd18.", "dd28."]
import time
time_start = time.time()
for x in xrange(100000):
    for w in ("ab.", "cd.", "ef.", "gh", "dd"):
        if w in a:
            pass

time_passed = time.time() - time_start
print "time_passed:", time_passed

time_start = time.time()
for x in xrange(100000):
    for w in ("ab.", "cd.", "ef.", "gh", "dd"):
        if w[-1] != '.' or w in a:      # 随着数组a长度的增长，w in a的计算成果会逐渐增长。
            pass

time_passed = time.time() - time_start
print "time_passed:", time_passed


# 8. 类型检查，使用isinstance
class UserInt(int):
    def __init__(self, val):
        self.m_val = val

    def __add__(self, other):
        if isinstance(other, UserInt):
            return UserInt(self.m_val + other.m_val)
        return self.m_val + other       # 尝试去+，有错系统会报出异常

    def _iadd(self, other):
        raise NotImplementedError("not supported operation")

    def __repr__(self):
        return "Integer(%s): " % self.m_val

    def __str__(self):
        return str(self.m_val)

print "type:", type(UserInt)
print UserInt(1) + UserInt(2)
print UserInt(1) + 2
print "instance int:", isinstance(UserInt(2), int)


# 9. 除法操作使用浮点数来计算
gpa = (3 * 4 + 4 * 4) / float(4 + 4)
print "gpa:", gpa

i = 0.1
eps = 0.000001
while abs(i - 1.5) > eps:   #   浮点数比较需要精度
    i += 0.1
    print "i=", i

# 10. is vs ==: True\False\None\


# 11. unicode默认作为中转编码：decode将其它编码转换为unicode；encode将unicode转换为其它编码；
# 系统默认使用ASCII存储py文件，所以需要使用 # -*- coding: utf-8 -*-
with open("test.txt", 'r') as file_handle:
    print (file_handle.read())

s = "中文测试".decode("utf-8") + u"Chinese"
print s


# 12. 查看命名空间，import和from import区别。
import sys
print u"当前命名空间:" + str(dir()).decode("utf-8")

from example.other import iteration, constant

print u"import后命名空间:" + str(dir()).decode("utf-8")  # 引入iter
print "module:" + str(sys.modules["iteration"] == iteration)      # 引入了iter module变量，同时sys.modules加入了module，两者指向同一个module

print u"import后命名空间:" + str(dir()).decode("utf-8")  # 引入IterTest
print "module:" + str(sys.modules["iteration"] == iteration)      # sys.modules中乜有IterTest变量，sys.modules中有iter


# 13. 重要：循环import，在模块中不要直接对变量和函数赋值和修改，包括使用from import。


# 14. 使用absolute import。即从根目录开始写路径。

# 15. 文件关闭问题：使用with替代try: finally, 见11


# 16. 使用else以及异常：异常except包含代码少，使用单独Exception或者Error
for i in xrange(10):
    for j in xrange(5):
        if i % 2 == 0:
            break
    else:
        print "not break:", i

try:
    print "test"
    #   raise Exception()
except Exception:
    print "exception"
else:
    print "no exception"
finally:
    print "test over"


# 17. finally级别比return要高。
def test_finally(a):
    try:
        if a <= 2:
            return 1
        else:
            return 2
    except Exception as except_e:
        print except_e
    finally:
        return -1

print test_finally(1)
print test_finally(3)

# 18. 对象的__nonzero__()被调用用来判断是否为空，然后调用__len__()来判断，否则if判断都为True


class TestZero(object):
    def __nonzero__(self):
        return True

    def __len__(self):
        return False

    def __init__(self):
        pass

if TestZero():
    print "True"
else:
    print "False"


# 19. 字符串操作, 使用join方法

# 20. format使用，%r使用repr进行转换
print "your score is {num:06.1f}, {num:05.1f}".format(num=9.5)      # 5和6表示宽度
itemname = ("mouse", "mobilephone", "cup")
print "itemlist are %s" % (itemname, )      # 一定要有","，否则理解为 % ("mouse", "mobilephone", "cup")


# 21. 可变对象和不可变对象, 每个对象都有id、type和值


# 22. 计算代码的性能, 代码时压栈的形式
from timeit import Timer
Timer('x, y = y, x', 'x = 2; y = 3').timeit()


# 23. lazy evaluation
def fib():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

from itertools import islice
print list(islice(fib(), 5))    # islice返回iteration


# 24 枚举类型
# def enum(*posarg, **keysarg):
#     return type("Enum", (object,), dict(zip(posarg, range(len(posarg))), **keysarg))
#
# Seasons = enum("Spring", "Summer", "Autumn", Winter=3)
#
# print "Seasons.Spring:", Seasons.Spring, ",Seasons.Winter:", Seasons.Winter

# 创建枚举类型的数据 [比全部列出来要好]
from collections import namedtuple
Seasons = namedtuple('Seasons', 'Spring Summer Autumn Winter')._make(range(4))

print Seasons.Spring

# 缺陷：无法保证唯一性; 支持无意义的加减乘除操作
r = Seasons._replace(Spring=1)
print r.Spring

# 使用flufl.enum

try:
    from flufl.enum import Enum
    Seasons = Enum("Seasons", "Spring Summer Autumn Winter")
    print "flufl.enum:", Seasons.Spring.value
    for member in Seasons._enums:
        print member
except:
    import traceback
    print traceback.print_exc()
    print "no flufl"

# 25： type：type()即调用types模块中的名称来比较
# 1. 由于所有原始的类都是type 'instance'类型，不能比较
# 2. 继承基本类型时需要修改默认的type，不是很方便

isinstance(2, float)
isinstance((2, 3), (str, list, tuple))


# 26. 浮点数问题：主动转换浮点数，浮点数不适合比较。

# 27. 序列索引的迭代
li = ['a', 'b', 'c', 'd', 'e']
for i, e in enumerate(li):
    print "index:", i, "element:", e


def my_enumerate(sequence):
    n = -1
    for elem in reversed(sequence):
        yield len(sequence) + n, elem
        n -= 1


# 28. Unicode的编码是固定的，在实际传输过程中，不同系统实现方式不同，例如UTF-8，不同范围的字符使用不同长度的编码

# 1. Unicode可以作为不同语言的中间编码格式
s = "中文测试".decode('utf-8') + u"Chinese"     # 系统默认使用ASCII码转换为Unicode中间码，转换失败
print s


# 29. Package目录下有Module1和__init__.py文件
# 1. 在__init__.py文件中添加from Module1 import Test就可以直接from Package import Test了
# 2. 在__init__.py中添加__all__ = ['Module1', ...]可以控制from Package import *导入的模块类别
# 3. 使用import Package.Module1可以通过Package.Module1来区别Module1


# 30. modules说明
# 1. import的作用：Python初始化环境时预先加载一批内建模块到内存中，放在sys.modules中。
# 2. 加载过程，查看sys.modules是否有，确认加载的文件是否需要编译，编译后放到模块对应的字典中。这个过程是可以自己模拟的。
# 3. 通过__package__ = str('app.sub1')来使用form . import string 和 form .. xx import string; 由于问题较多，推荐使用absolute import好


# 31: 重点with的

class ContextTest(object):
    def __enter__(self):
        print "enter"

    def __exit__(self, exception_type, exception_value, traceback):
        print "exit"
        if exception_type is None:
            print "no exception"
            return False
        elif exception_type is ValueError:
            print "Value error"
            return True
        else:
            print "other error"
            return True

with ContextTest():
    print "test"
    raise (ValueError)


# 32. else用于判断正常退出的情况，无需通过变量来判断。
def print_prime2(n):
    for i in xrange(2, n):
        for j in xrange(2, i):
            if i % j == 0:
                break
        else:
            print "{number} is a primer number".format(number=i)

print_prime2(15)

try:
    print "test"
    raise ValueError
except ValueError:
    print "error"
else:
    print "success"


# 33. classmethod:

class Date(object):

    day = 0
    month = 0
    year = 0

    def __init__(self, day=0, month=0, year=0):
        self.day = day
        self.month = month
        self.year = year

    @classmethod
    def from_string(cls, date_as_string):
        day, month, year = map(int, date_as_string.split('-'))
        date1 = cls(day, month, year)
        return date1

date2 = Date.from_string('11-09-2012')
print date2


# 34. reduce, map, filter


# 35. iter

with open('test.txt', 'r') as fp:
    for line in iter(fp.readline, ''):
        print(line)