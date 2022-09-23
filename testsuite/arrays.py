import unittest
from math import sin, exp, sqrt, log

from QuantLib import *

from utilities import *


class ArrayTest(unittest.TestCase):

    def testConstruction(self):
        TEST_MESSAGE(
            "Testing array construction...")
        a1 = Array()
        self.assertFalse(
            not a1.empty(),
            "default-initialized array is not empty ")

        size = 5
        a2 = Array(size)
        self.assertFalse(
            len(a2) != size,
            "array not of the required size")

        value = 42.0
        a3 = Array(size, value)
        self.assertFalse(
            len(a3) != size,
            "array not of the required size")

        for i in range(size):
            self.assertFalse(
                a3[i] != value,
                " element not with required value")

        increment = 3.0
        a4 = Array(size, value, increment)
        self.assertFalse(
            len(a4) != size,
            "array not of the required size")

        for i in range(size):
            self.assertFalse(
                a4[i] != value + i * increment,
                " element not with required value")

        a5 = Array(a1)
        self.assertFalse(
            len(a5) != len(a1),
            "array not of the required size")

        a6 = Array(a3)
        self.assertFalse(
            len(a6) != len(a3),
            "array not of the required size")
        for i in range(len(a6)):
            self.assertFalse(
                a6[i] != a3[i],
                " element of copy not with same value as original")

    def testArrayFunctions(self):
        TEST_MESSAGE(
            "Testing array functions...")
        a = Array(5)
        for i in range(len(a)):
            a[i] = sin(i) + 1.1

        exponential = -2.3
        p = Pow(a, exponential)
        e = Exp(a)
        l = Log(a)
        s = Sqrt(a)

        tol = 10 * QL_EPSILON

        for i in range(len(a)):
            self.assertFalse(abs(p[i] - pow(a[i], exponential)) > tol)
            self.assertFalse(abs(e[i] - exp(a[i])) > tol)
            self.assertFalse(abs(l[i] - log(a[i])) > tol)
            self.assertFalse(abs(s[i] - sqrt(a[i])) > tol)

    def testArrayResize(self):
        TEST_MESSAGE(
            "Testing array resize...")
        a = Array(10, 1.0, 1.0)
        tol = 10 * QL_EPSILON

        for i in range(10):
            self.assertFalse(
                abs(a[i] - float(1 + i)) > tol)

        a.resize(5)
        self.assertTrue(len(a) == 5)
        for i in range(5):
            self.assertFalse(
                abs(a[i] - float(1 + i)) > tol)

        a.resize(15)
        self.assertTrue(len(a) == 15)
        for i in range(5):
            self.assertFalse(
                abs(a[i] - float(1 + i)) > tol)
