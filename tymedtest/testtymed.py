'''
@author: Csaba Sulyok <csaba.sulyok@gmail.com>
'''

import unittest
from tymedtest.testtymeddata import tymedFunction,\
    tymedFunctionWithArgsAndRetVal, tymedFunctionWithException
from tymed import lastTyme, allTyme, resetTyme


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
            
    


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
