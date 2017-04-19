'''
Test data for tymed unit tests.
@author: Csaba Sulyok <csaba.sulyok@gmail.com>
'''
from tymed import tymed, tymedCls
from time import sleep


def notTymedFunction():
    print 'notTymedFunction()'
    sleep(0.1)
    
    
@tymed
def tymedFunction():
    print 'tymedFunction()'
    sleep(0.1)


@tymed
def tymedFunctionWithArgsAndRetVal(arg1, arg2 = 42):
    print 'tymedFunctionWithArgsAndRetVal(arg1=%d,arg2=%d)' %(arg1, arg2)
    sleep(0.1)
    return arg1+arg2


@tymed
def tymedFunctionWithException():
    print 'tymedFunctionWithException()'
    sleep(0.1)
    raise Exception("I am an exception")


class NotTymedClass(object):
    @tymed
    def tymedMethod(self):
        print '%s.tymedMethod()' %(self)
        sleep(0.1)



@tymedCls
class TymedClass(object):
    
    def __init__(self):
        self.otherProp = 42
        
    @tymed
    def tymedMethod(self):
        print '%s.tymedMethod()' %(self)
        sleep(0.1)
        
    @tymed
    def tymedMethodWithArgAndOtherPropAndRetVal(self, arg):
        print 'tymedFunctionWithArgsAndRetVal(self.otherProp=%d,arg=%d)' %(self.otherProp, arg)
        sleep(0.1)
        return self.otherProp+arg
