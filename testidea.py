#encoding=utf-8
import threading
import types
import sys
import testideapackage.AAA

t=threading.enumerate()[0]
#print type(t)
class A(list):
    pass

class B(A):
    pass

class C(B):
    pass
#print sys.modules['__main__'].__dict__