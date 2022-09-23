import unittest

from QuantLib import *

from utilities import *


class FastFourierTransformTest(unittest.TestCase):

    def testSimple(self):
        TEST_MESSAGE(
            "Testing complex direct FFT...")
        tmp = [
            complex(0, 0), complex(1, 1), complex(3, 3), complex(4, 4),
            complex(4, 4), complex(3, 3), complex(1, 1), complex(0, 0)]
        a = ComplexVector(8)
        for i in range(8):
            a[i] = tmp[i]
        fft = FastFourierTransform(3)
        b = fft.transform(a)
        expected = [
            complex(16, 16), complex(-4.8284, -11.6569),
            complex(0, 0), complex(-0.3431, 0.8284),
            complex(0, 0), complex(0.8284, -0.3431),
            complex(0, 0), complex(-11.6569, -4.8284)]
        for i in range(8):
            self.assertFalse(
                (abs(b[i].real - expected[i].real) > 1.0e-2) or
                (abs(b[i].imag - expected[i].imag) > 1.0e-2))

    def testInverse(self):
        TEST_MESSAGE(
            "Testing convolution via inverse FFT...")

        x = ComplexVector(3)
        x[0] = complex(1)
        x[1] = complex(2)
        x[2] = complex(3)

        order = FastFourierTransform.min_order(len(x)) + 1
        fft = FastFourierTransform(order)
        nFrq = fft.output_size()
        tmp = ComplexVector(nFrq)
        z = complex()

        ft = fft.inverse_transform(x)
        for i in range(nFrq):
            tmp[i] = complex(abs(ft[i]) ** 2)
            ft[i] = z

        ft = fft.inverse_transform(tmp)

        calculated = ft[0].real / nFrq
        expected = x[0] * x[0] + x[1] * x[1] + x[2] * x[2]
        self.assertFalse(abs(calculated - expected) > 1.0e-10)

        calculated = ft[1].real / nFrq
        expected = x[0] * x[1] + x[1] * x[2]
        self.assertFalse(abs(calculated - expected) > 1.0e-10)

        calculated = ft[2].real / nFrq
        expected = x[0] * x[2]
        self.assertFalse(abs(calculated - expected) > 1.0e-10)
