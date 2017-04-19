'''
@author: Csaba Sulyok <csaba.sulyok@gmail.com>
'''

import unittest
from tymedtest.testtymeddata import tymedFunction,\
    tymedFunctionWithArgsAndRetVal, tymedFunctionWithException, notTymedFunction,\
    TymedClass, NotTymedClass
from tymed import lastTyme, allTyme, resetTyme, FunctionNotTymedException,\
    BoundMethodNotInTymedClassException, lap


class TestTymed(unittest.TestCase):

    def setUp(self):
        print ''
        resetTyme()
    
    def test_tymedFunctionCalledNonce(self):
        # then
        self.assertEqual(lastTyme(tymedFunction), 0.0)
        self.assertEqual(allTyme(tymedFunction), 0.0)
        
    def test_tymedFunctionCalledOnce(self):
        # when
        tymedFunction()
        # then
        self.assertAlmostEqual(lastTyme(tymedFunction), 0.1, delta = 0.01)
        self.assertAlmostEqual(allTyme(tymedFunction), 0.1, delta = 0.01)
    
    def test_tymedFunctionReset(self):
        # given
        tymedFunction()
        # when
        resetTyme(tymedFunction)
        # then
        self.assertEqual(lastTyme(tymedFunction), 0.0)
        self.assertEqual(allTyme(tymedFunction), 0.0)
    
    def test_tymedFunctionLap(self):
        # given
        tymedFunction()
        # when
        lapTime = lap(tymedFunction)
        # then
        self.assertAlmostEqual(lapTime, 0.1, delta = 0.01)
        self.assertEqual(lastTyme(tymedFunction), 0.0)
        self.assertEqual(allTyme(tymedFunction), 0.0)
    
    def test_tymedFunctionCalledNnce(self):
        # given
        N = 5
        # when
        for _ in range(N):
            tymedFunction()
        # then
        self.assertAlmostEqual(lastTyme(tymedFunction), 0.1, delta = 0.01)
        self.assertAlmostEqual(allTyme(tymedFunction), N * 0.1, delta = N * 0.01)
    
    def test_tymedFunctionWithArgsAndRetValPropagated(self):
        # when
        retVal1 = tymedFunctionWithArgsAndRetVal(20)
        retVal2 = tymedFunctionWithArgsAndRetVal(arg1 = 20)
        retVal3 = tymedFunctionWithArgsAndRetVal(arg1 = 20, arg2 = 20)
        # then
        self.assertAlmostEqual(lastTyme(tymedFunctionWithArgsAndRetVal), 0.1, delta = 0.01)
        self.assertAlmostEqual(allTyme(tymedFunctionWithArgsAndRetVal), 3 * 0.1, delta = 3 * 0.01)
        self.assertEqual(retVal1, 62) # 20 + 42
        self.assertEqual(retVal2, 62) # 20 + 42
        self.assertEqual(retVal3, 40) # 20 + 20
    
    def test_tymedFunctionWithExceptionIsPropagated(self):
        # when
        try:
            tymedFunctionWithException()
            self.fail("Exception not raised")
        except Exception, e:
            # then
            self.assertEqual(e.message, "I am an exception")
            self.assertIsInstance(e, Exception)
            self.assertAlmostEqual(lastTyme(tymedFunctionWithException), 0.1, delta = 0.01)
            self.assertAlmostEqual(allTyme(tymedFunctionWithException), 0.1, delta = 0.01)
            
    def test_notTymedFunction_raisesException(self):
        # when
        try:
            lastTyme(notTymedFunction)
            self.fail("Exception not raised")
        except Exception, e:
            # then
            self.assertTrue(e.message.startswith("Following item not tymed:"))
            self.assertIsInstance(e, FunctionNotTymedException)
    
    def test_tymedMethodInNotTymedClass(self):
        # given
        notTymedInstance = NotTymedClass()
        # when
        notTymedInstance.tymedMethod()
        try:
            lastTyme(notTymedInstance.tymedMethod)
            self.fail("Exception not raised")
        except Exception, e:
            # then
            self.assertTrue(e.message.startswith("Following bound method part of non-tymed class:"))
            self.assertIsInstance(e, BoundMethodNotInTymedClassException)
    
    def test_tymedMethodCalledOnce(self):
        # given
        tymedInstance = TymedClass()
        # when
        tymedInstance.tymedMethod()
        # then
        self.assertAlmostEqual(lastTyme(tymedInstance.tymedMethod), 0.1, delta = 0.01)
        self.assertAlmostEqual(allTyme(tymedInstance.tymedMethod), 0.1, delta = 0.01)
    
    def test_tymedMethodCalledNnce(self):
        # given
        tymedInstance = TymedClass()
        N = 5
        # when
        for _ in range(N):
            tymedInstance.tymedMethod()
        # then
        self.assertAlmostEqual(lastTyme(tymedInstance.tymedMethod), 0.1, delta = 0.01)
        self.assertAlmostEqual(allTyme(tymedInstance.tymedMethod), N * 0.1, delta = N * 0.01)
    
    def test_tymedMethodWithArgAndOtherPropAndRetVal(self):
        # given
        tymedInstance = TymedClass()
        # when
        retVal1 = tymedInstance.tymedMethodWithArgAndOtherPropAndRetVal(20)
        retVal2 = tymedInstance.tymedMethodWithArgAndOtherPropAndRetVal(arg = 20)
        # then
        self.assertAlmostEqual(lastTyme(tymedInstance.tymedMethodWithArgAndOtherPropAndRetVal), 0.1, delta = 0.01)
        self.assertAlmostEqual(allTyme(tymedInstance.tymedMethodWithArgAndOtherPropAndRetVal), 2 * 0.1, delta = 2 * 0.01)
        self.assertEqual(retVal1, 62) # 20 + 42
        self.assertEqual(retVal2, 62) # 20 + 42
        
    def test_tymedMethodOnMultipleInstances(self):
        # given
        tymedInstance1 = TymedClass()
        tymedInstance2 = TymedClass()
        tymedInstance3 = TymedClass()
        N = 3
        # when
        for _ in range(N):
            tymedInstance1.tymedMethod()
            tymedInstance1.tymedMethod()
            tymedInstance1.tymedMethod()
            
            tymedInstance2.tymedMethod()
            tymedInstance2.tymedMethod()
            
            tymedInstance3.tymedMethod()
            
        # then
        self.assertAlmostEqual(lastTyme(tymedInstance1.tymedMethod), 0.1, delta = 0.01)
        self.assertAlmostEqual(lastTyme(tymedInstance2.tymedMethod), 0.1, delta = 0.01)
        self.assertAlmostEqual(lastTyme(tymedInstance3.tymedMethod), 0.1, delta = 0.01)
        self.assertAlmostEqual(allTyme(tymedInstance1.tymedMethod), 3 * N * 0.1, delta = 3 * N * 0.01)
        self.assertAlmostEqual(allTyme(tymedInstance2.tymedMethod), 2 * N * 0.1, delta = 2 * N * 0.01)
        self.assertAlmostEqual(allTyme(tymedInstance3.tymedMethod), N * 0.1, delta = N * 0.01)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
