# Basic template testing class i am testing

import unittest

class DatabaseTestCase(unittest.TestCase):
    def testAdd(self):
        self.assertEqual((1 + 2), 3) 
        self.assertEqual(0 + 1, 1)

    def testMultiply(self):
        self.assertEqual((0 * 10), 0) 
        self.assertEqual((5 * 8), 40)

    def testDivision(self):
        self.assertEqual((5/2),2.52)

if __name__ == '__main__':
    unittest.main()