Tymed
=====
[![Build Status](https://travis-ci.org/csabasulyok/tymed.svg?branch=master)](https://travis-ci.org/csabasulyok/tymed)
[![PyPI version](https://badge.fury.io/py/tymed.svg)](https://badge.fury.io/py/tymed)


Timer utility for [Python](https://www.python.org/) functions and bound methods. Allows calling functions/methods multiple times and analysing how much time they took.

## Installation ##
```bash
pip install tymed
```

## Examples ##

1. Monitor a function
```python
from tymed import *

@tymed
def tymedFunction():
    # do stuff here...

# ...
# do other stuff here, calling tymedFunction()
# ...

print lastTyme(tymedFunction)  # how long the last iteration of the function took
print allTyme(tymedFunction)   # how long all of them took
resetTyme(tymedFunction)       # reset measurements
print lap(tymedFunction)       # how long all of them took + reset measurements
```

2. Monitor a bound method

```python
from tymed import *

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
    
print allTyme(t1.tymedMethod)  # see the times
print allTyme(t2.tymedMethod)  # per instance
```
