import unittest

from QuantLib import *

from utilities import *


class TqrEigenDecompositionTest(unittest.TestCase):

    def testEigenValueDecomposition(self):
        TEST_MESSAGE(
            "Testing TQR eigenvalue decomposition...")

        diag = Array(5)
        sub = Array(4, 1)
        diag[0] = 11
        diag[1] = 7
        diag[2] = 6
        diag[3] = 2
        diag[4] = 0
        ev = [
            11.2467832217139119,
            7.4854967362908535,
            5.5251516080277518,
            2.1811760273123308,
            -0.4386075933448487]

        tqre = TqrEigenDecomposition(
            diag, sub,
            TqrEigenDecomposition.WithoutEigenVector)
        for i in range(len(diag)):
            expected = ev[i]
            calculated = tqre.eigenvalues()[i]
            tolerance = 1.0e-10
            self.assertFalse(abs(expected - calculated) > tolerance)

    def testZeroOffDiagEigenValues(self):
        TEST_MESSAGE(
            "Testing TQR zero-off-diagonal eigenvalues...")

        diag = Array(5)
        sub = Array(4, 1)
        sub[0] = sub[2] = 0
        diag[0] = 12
        diag[1] = 9
        diag[2] = 6
        diag[3] = 3
        diag[4] = 0

        tqre1 = TqrEigenDecomposition(diag, sub)

        sub[0] = sub[2] = 1e-14
        tqre2 = TqrEigenDecomposition(diag, sub)

        for i in range(len(diag)):
            expected = tqre2.eigenvalues()[i]
            calculated = tqre1.eigenvalues()[i]
            tolerance = 1.0e-10
            self.assertFalse(abs(expected - calculated) > tolerance)

    def testEigenVectorDecomposition(self):
        TEST_MESSAGE(
            "Testing TQR eigenvector decomposition...")

        diag = Array(2, 1)
        sub = Array(1, 1)

        tqre = TqrEigenDecomposition(diag, sub)
        tolerance = 1.0e-10

        self.assertFalse(
            abs(0.25 + tqre.eigenvectors()[0][0]
                * tqre.eigenvectors()[0][1]
                * tqre.eigenvectors()[1][0]
                * tqre.eigenvectors()[1][1]) > tolerance)
