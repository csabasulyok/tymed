'''
Test data for tymed unit tests.
@author: Csaba Sulyok <csaba.sulyok@gmail.com>
'''
from tymed import tymed
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