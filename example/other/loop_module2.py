print "load loop module 2"
from example.other import loop_module1
# import loop_module1.g1
# from loop_module1 import g1

print "define g2()"
def g2():
    loop_module1.g1()
