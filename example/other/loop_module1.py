print "load loop module 1"
from example.other import loop_module2
# import loop_module2.g2
# from loop_module2 import g2

print "define g1()"
def g1():
    loop_module2.g2()