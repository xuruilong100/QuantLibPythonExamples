import unittest
from utilities import *
from QuantLib import *
from math import atan


class F1(object):
    def __init__(self):
        pass

    def __call__(self, x):
        return x * x - 1.0

    def derivative(self, x):
        return 2.0 * x


class F2(object):
    def __init__(self):
        pass

    def __call__(self, x):
        return 1.0 - x * x

    def derivative(self, x):
        return -2.0 * x


class F3(object):
    def __init__(self):
        pass

    def __call__(self, x):
        return atan(x - 1)

    def derivative(self, x):
        return 1.0 / (1.0 + (x - 1.0) * (x - 1.0))


class Probe(object):
    def __init__(self, result, offset):
        self.result_ = result
        self.previous_ = result
        self.offset_ = offset

    def __call__(self, x):
        self.result_ = x
        return self.previous_ + self.offset_ - x * x

    def derivative(self, x):
        return 2.0 * x


class Solver1DTest(unittest.TestCase):

    def testBrent(self):
        TEST_MESSAGE("Testing Brent solver...")
        self._test_solver(Brent(), "Brent", 1.0e-6)

    def testBisection(self):
        TEST_MESSAGE("Testing bisection solver...")
        self._test_solver(Bisection(), "Bisection", 1.0e-6)

    def testFalsePosition(self):
        TEST_MESSAGE("Testing false-position solver...")
        self._test_solver(FalsePosition(), "FalsePosition", 1.0e-6)

    def testNewton(self):
        TEST_MESSAGE("Testing Newton solver...")
        self._test_solver(Newton(), "Newton", 1.0e-12)

    def testNewtonSafe(self):
        TEST_MESSAGE("Testing Newton-safe solver...")
        self._test_solver(NewtonSafe(), "NewtonSafe", 1.0e-9)

    def testFiniteDifferenceNewtonSafe(self):
        TEST_MESSAGE("Testing finite-difference Newton-safe solver...")
        self._test_solver(FiniteDifferenceNewtonSafe(), "FiniteDifferenceNewtonSafe", NullReal())

    def testRidder(self):
        TEST_MESSAGE("Testing Ridder solver...")
        self._test_solver(Ridder(), "Ridder", 1.0e-6)

    def testSecant(self):
        TEST_MESSAGE("Testing secant solver...")
        self._test_solver(Secant(), "Secant", 1.0e-6)

    def _test_not_bracketed(self,
                            solver,
                            name,
                            f,
                            guess):
        accuracy = [1.0e-4, 1.0e-6, 1.0e-8]
        expected = 1.0
        for i in accuracy:
            root = solver.solve(f, i, guess, 0.1)
            self.assertFalse(abs(root - expected) > i)

    def _test_bracketed(self, solver, name,
                        f, guess):
        accuracy = [1.0e-4, 1.0e-6, 1.0e-8]
        expected = 1.0
        for i in accuracy:
            # guess on the left side of the root, increasing function
            root = solver.solve(f, i, guess, 0.0, 2.0)
            self.assertFalse(abs(root - expected) > i)

    def _test_solver(self, solver, name, accuracy):
        # guess on the left side of the root, increasing function
        self._test_not_bracketed(solver, name, F1(), 0.5)
        self._test_bracketed(solver, name, F1(), 0.5)
        # guess on the right side of the root, increasing function
        self._test_not_bracketed(solver, name, F1(), 1.5)
        self._test_bracketed(solver, name, F1(), 1.5)
        # guess on the left side of the root, decreasing function
        self._test_not_bracketed(solver, name, F2(), 0.5)
        self._test_bracketed(solver, name, F2(), 0.5)
        # guess on the right side of the root, decreasing function
        self._test_not_bracketed(solver, name, F2(), 1.5)
        self._test_bracketed(solver, name, F2(), 1.5)
        # situation where bisection is used in the finite difference
        # newton solver as the first step and where the initial
        # guess is equal to the next estimate (which causes an infinite
        # derivative if we do not handle this case with special care)
        self._test_not_bracketed(solver, name, F3(), 1.00001)
        # check that the last function call is made with the root value
        if accuracy != NullReal():
            self._test_last_call_with_root(solver, name, false, accuracy)
            self._test_last_call_with_root(solver, name, true, accuracy)

    def _test_last_call_with_root(self, solver, name,
                                  bracketed, accuracy):
        mins = [3.0, 2.25, 1.5, 1.0]
        maxs = [7.0, 5.75, 4.5, 3.0]
        steps = [0.2, 0.2, 0.1, 0.1]
        offsets = [25.0, 11.0, 5.0, 1.0]
        guesses = [4.5, 4.5, 2.5, 2.5]
        # expected=[ 5.0, 4.0, 3.0, 2.0 ]

        argument = 0.0

        for i in range(4):
            probe = Probe(argument, offsets[i])
            if bracketed:
                result = solver.solve(
                    probe, accuracy,
                    guesses[i], mins[i], maxs[i])
            else:
                result = solver.solve(
                    probe, accuracy,
                    guesses[i], steps[i])

            argument = probe.result_
            error = abs(result - argument)
            # the solver should have called the function with
            # the very same value it's returning. But the internal
            # 80bit length of the x87 FPU register might lead to
            # a very small glitch when compiled with -mfpmath=387 on gcc
            self.assertFalse(error > 2 * QL_EPSILON)
