'''
Timer utility for functions and bound methods.
Annotate a function to activate timing for it.
The execution will be incrementally timed for every iteration, until consumed using the lap method.

@author: Csaba Sulyok <csaba.sulyok@gmail.com>
'''


from time import time


class TymedMethods(object):
    '''
    Annotate a method to activate timing for it.
    The function's execution will be incrementally timed for every iteration,
    until consumed using the lap method.
    '''
        
    def __init__(self):
        self.mtds = {}
        
    def onMtdStart(self, mtdId):
        if not self.mtds.has_key(mtdId):
            self.mtds[mtdId] = {'lastStarted': 0.0, 'allTime': 0.0}
        self.mtds[mtdId]['lastStarted'] = time()
    
    def onMtdFinish(self, mtdId):
        self.mtds[mtdId]['allTime'] += time() - self.mtds[mtdId]['lastStarted']
    
    def lap(self, mtdId):
        ret = self.mtds[mtdId]['allTime']
        self.mtds[mtdId]['allTime'] = 0.0
        return ret


# default instance & methods
tymedMtds = TymedMethods()



def tymedCls(cls):
    for _, val in cls.__dict__.iteritems():
        if callable(val) and hasattr(val, '__tymed__'):
            val.__boundtymed__ = True
               
    return cls

    
def tymed(mtd):
    def wrappedMtd(*args, **kwargs):
        if hasattr(wrappedMtd, '__boundtymed__'):
            mtdId = "%s.%s" %(id(args[0]), id(mtd))
        else:
            mtdId = id(mtd)
            
        tymedMtds.onMtdStart(mtdId)
        ret = mtd(*args, **kwargs)
        tymedMtds.onMtdFinish(mtdId)
        
        return ret
    
    wrappedMtd.__tymed__ = True
    wrappedMtd.__origMtd__ = mtd
    return wrappedMtd


def lap(mtd):
    if hasattr(mtd, '__self__'):
        mtdId = "%s.%s" %(id(mtd.__self__), id(mtd.__origMtd__))
    else:
        mtdId = id(mtd.__origMtd__)
    return tymedMtds.lap(mtdId)

