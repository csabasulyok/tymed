from tymed import *
from time import sleep

# 1

@tymed
def tymedFunction():
    # do stuff here
    sleep(0.1)

# ...
# do other stuff here, calling tymedFunction()
# ...
for i in range(10):
    tymedFunction()
    
print lastTyme(tymedFunction)  # how long the last iteration of the function took
print allTyme(tymedFunction)   # how long all of them took
resetTyme(tymedFunction)       # reset measurements
print lap(tymedFunction)       # how long all of them took + reset measurements


# 2

@tymedCls
class TymedClass(object):
    # ...
    @tymed
    def tymedMethod(self):
        # do stuff here
        sleep(0.1)
    # ...    

t1 = TymedClass() # use multiple instances
t2 = TymedClass()

# ...
# do other stuff here, calling t1.tymedMethod() and t2.tymedMethod()
# ...
for i in range(10):
    tymedFunction()
    
print allTyme(t1.tymedMethod)  # see the times
print allTyme(t2.tymedMethod)  # per instance
