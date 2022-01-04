import unittest
from utilities import *
from QuantLib import *

PPMT_MAX_DIM = 21200

dim002Discr_Sobol = [
    8.33e-004, 4.32e-004, 2.24e-004, 1.12e-004,
    5.69e-005, 2.14e-005]
dim002DiscrMersenneTwis = [
    8.84e-003, 5.42e-003, 5.23e-003, 4.47e-003,
    4.75e-003, 3.11e-003, 2.97e-003]
dim002DiscrPlain_Halton = [
    1.26e-003, 6.73e-004, 3.35e-004, 1.91e-004,
    1.11e-004, 5.05e-005, 2.42e-005]
dim002DiscrRShiftHalton = [1.32e-003, 7.25e-004]
dim002DiscrRStRShHalton = [1.35e-003, 9.43e-004]
dim002DiscrRStartHalton = [1.08e-003, 6.40e-004]
dim002Discr__Unit_Sobol = [
    8.33e-004, 4.32e-004, 2.24e-004, 1.12e-004,
    5.69e-005, 2.14e-005]

dim003Discr_Sobol = [
    1.21e-003, 6.37e-004, 3.40e-004, 1.75e-004,
    9.21e-005, 4.79e-005, 2.56e-005]
dim003DiscrMersenneTwis = [
    7.02e-003, 4.94e-003, 4.82e-003, 4.91e-003,
    3.33e-003, 2.80e-003, 2.62e-003]
dim003DiscrPlain_Halton = [
    1.63e-003, 9.62e-004, 4.83e-004, 2.67e-004,
    1.41e-004, 7.64e-005, 3.93e-005]
dim003DiscrRShiftHalton = [1.96e-003, 1.03e-003]
dim003DiscrRStRShHalton = [2.17e-003, 1.54e-003]
dim003DiscrRStartHalton = [1.48e-003, 7.77e-004]
dim003Discr__Unit_Sobol = [
    1.21e-003, 6.37e-004, 3.40e-004, 1.75e-004,
    9.21e-005, 4.79e-005, 2.56e-005]

dim005Discr_Sobol = [
    1.59e-003, 9.55e-004, 5.33e-004, 3.22e-004,
    1.63e-004, 9.41e-005, 5.19e-005]
dim005DiscrMersenneTwis = [
    4.28e-003, 3.48e-003, 2.48e-003, 1.98e-003,
    1.57e-003, 1.39e-003, 6.33e-004]
dim005DiscrPlain_Halton = [
    1.93e-003, 1.23e-003, 6.89e-004, 4.22e-004,
    2.13e-004, 1.25e-004, 7.17e-005]
dim005DiscrRShiftHalton = [2.02e-003, 1.36e-003]
dim005DiscrRStRShHalton = [2.11e-003, 1.25e-003]
dim005DiscrRStartHalton = [1.74e-003, 1.08e-003]
dim005Discr__Unit_Sobol = [
    1.85e-003, 9.39e-004, 5.19e-004, 2.99e-004,
    1.75e-004, 9.51e-005, 5.55e-005]

dim010DiscrJackel_Sobol = [
    7.08e-004, 5.31e-004, 3.60e-004, 2.18e-004,
    1.57e-004, 1.12e-004, 6.39e-005]
dim010DiscrSobLev_Sobol = [
    7.01e-004, 5.10e-004, 3.28e-004, 2.21e-004,
    1.57e-004, 1.08e-004, 6.38e-005]
dim010DiscrMersenneTwis = [
    8.83e-004, 6.56e-004, 4.87e-004, 3.37e-004,
    3.06e-004, 1.73e-004, 1.43e-004]
dim010DiscrPlain_Halton = [
    1.23e-003, 6.89e-004, 4.03e-004, 2.83e-004,
    1.61e-004, 1.08e-004, 6.69e-005]
dim010DiscrRShiftHalton = [9.25e-004, 6.40e-004]
dim010DiscrRStRShHalton = [8.41e-004, 5.42e-004]
dim010DiscrRStartHalton = [7.89e-004, 5.33e-004]
dim010Discr__Unit_Sobol = [
    7.67e-004, 4.92e-004, 3.47e-004, 2.34e-004,
    1.39e-004, 9.47e-005, 5.72e-005]

dim015DiscrJackel_Sobol = [
    1.59e-004, 1.23e-004, 7.73e-005, 5.51e-005,
    3.91e-005, 2.73e-005, 1.96e-005]
dim015DiscrSobLev_Sobol = [
    1.48e-004, 1.06e-004, 8.19e-005, 6.29e-005,
    4.16e-005, 2.54e-005, 1.73e-005]
dim015DiscrMersenneTwis = [
    1.63e-004, 1.12e-004, 8.36e-005, 6.09e-005,
    4.34e-005, 2.95e-005, 2.10e-005]
dim015DiscrPlain_Halton = [
    5.75e-004, 3.12e-004, 1.70e-004, 9.89e-005,
    5.33e-005, 3.45e-005, 2.11e-005]
dim015DiscrRShiftHalton = [1.75e-004, 1.19e-004]
dim015DiscrRStRShHalton = [1.66e-004, 1.34e-004]
dim015DiscrRStartHalton = [2.09e-004, 1.30e-004]
dim015Discr__Unit_Sobol = [
    2.24e-004, 1.39e-004, 9.86e-005, 6.02e-005,
    4.39e-005, 3.06e-005, 2.32e-005]

dim030DiscrJackel_Sobol = [
    6.43e-007, 5.28e-007, 3.88e-007, 2.49e-007,
    2.09e-007, 1.55e-007, 1.07e-007]
dim030DiscrSobLev_Sobol = [
    1.03e-006, 6.06e-007, 3.81e-007, 2.71e-007,
    2.68e-007, 1.73e-007, 1.21e-007]
dim030DiscrMersenneTwis = [
    4.38e-007, 3.25e-007, 4.47e-007, 2.85e-007,
    2.03e-007, 1.50e-007, 1.17e-007]
dim030DiscrPlain_Halton = [
    4.45e-004, 2.23e-004, 1.11e-004, 5.56e-005,
    2.78e-005, 1.39e-005, 6.95e-006]
dim030DiscrRShiftHalton = [8.11e-007, 6.05e-007]
dim030DiscrRStRShHalton = [1.85e-006, 1.03e-006]
dim030DiscrRStartHalton = [4.42e-007, 4.64e-007]
dim030Discr__Unit_Sobol = [
    4.35e-005, 2.17e-005, 1.09e-005, 5.43e-006,
    2.73e-006, 1.37e-006, 6.90e-007]

dim050DiscrJackel_Sobol = [
    2.98e-010, 2.91e-010, 2.62e-010, 1.53e-010,
    1.48e-010, 1.15e-010, 8.41e-011]
dim050DiscrSobLev_Sobol = [
    3.11e-010, 2.52e-010, 1.61e-010, 1.54e-010,
    1.11e-010, 8.60e-011, 1.17e-010]
dim050DiscrSobLem_Sobol = [
    4.57e-010, 6.84e-010, 3.68e-010, 2.20e-010,
    1.81e-010, 1.14e-010, 8.31e-011]
dim050DiscrMersenneTwis = [
    3.27e-010, 2.42e-010, 1.47e-010, 1.98e-010,
    2.31e-010, 1.30e-010, 8.09e-011]
dim050DiscrPlain_Halton = [
    4.04e-004, 2.02e-004, 1.01e-004, 5.05e-005,
    2.52e-005, 1.26e-005, 6.31e-006]
dim050DiscrRShiftHalton = [1.14e-010, 1.25e-010]
dim050DiscrRStRShHalton = [2.92e-010, 5.02e-010]
dim050DiscrRStartHalton = [1.93e-010, 6.82e-010]
dim050Discr__Unit_Sobol = [
    1.63e-005, 8.14e-006, 4.07e-006, 2.04e-006,
    1.02e-006, 5.09e-007, 2.54e-007]

dim100DiscrJackel_Sobol = [
    1.26e-018, 1.55e-018, 8.46e-019, 4.43e-019,
    4.04e-019, 2.44e-019, 4.86e-019]
dim100DiscrSobLev_Sobol = [
    1.17e-018, 2.65e-018, 1.45e-018, 7.28e-019,
    6.33e-019, 3.36e-019, 3.43e-019]
dim100DiscrSobLem_Sobol = [
    8.79e-019, 4.60e-019, 6.69e-019, 7.17e-019,
    5.81e-019, 2.97e-019, 2.64e-019]
dim100DiscrMersenneTwis = [
    5.30e-019, 7.29e-019, 3.71e-019, 3.33e-019,
    1.33e-017, 6.70e-018, 3.36e-018]
dim100DiscrPlain_Halton = [
    3.63e-004, 1.81e-004, 9.07e-005, 4.53e-005,
    2.27e-005, 1.13e-005, 5.66e-006]
dim100DiscrRShiftHalton = [3.36e-019, 2.19e-019]
dim100DiscrRStRShHalton = [4.44e-019, 2.24e-019]
dim100DiscrRStartHalton = [9.85e-020, 8.34e-019]
dim100Discr__Unit_Sobol = [
    4.97e-006, 2.48e-006, 1.24e-006, 6.20e-007,
    3.10e-007, 1.55e-007, 7.76e-008]

dimensionality = [2, 3, 5, 10, 15, 30, 50, 100]

# 7 discrepancy measures for each dimension of all sequence generators
# would take a few days ... too long for usual/frequent test running
discrepancyMeasuresNumber = 1


# let's add some generality here...


class MersenneFactory(object):
    def __init__(self):
        pass

    def make(self, dim, seed):
        return MersenneTwisterUniformRsg(dim, seed)

    def name(self):
        return "Mersenne Twister"


class SobolFactory(object):
    def __init__(self, unit):
        self.unit_ = unit

    def make(self, dim, seed):

        return SobolRsg(dim, seed, self.unit_)

    def name(self):
        prefix = ""
        if self.unit_ == SobolRsg.Unit:
            prefix = "unit-initialized "
        elif self.unit_ == SobolRsg.Jaeckel:
            prefix = "Jaeckel-initialized "
        elif self.unit_ == SobolRsg.SobolLevitan:
            prefix = "SobolLevitan-initialized "
        elif self.unit_ == SobolRsg.SobolLevitanLemieux:
            prefix = "SobolLevitanLemieux-initialized "
        elif self.unit_ == SobolRsg.Kuo:
            prefix = "Kuo"
        elif self.unit_ == SobolRsg.Kuo2:
            prefix = "Kuo2"
        elif self.unit_ == SobolRsg.Kuo3:
            prefix = "Kuo3"

        return prefix + "Sobol sequences: "


class HaltonFactory(object):
    def __init__(self, randomStart, randomShift):
        self.start_ = randomStart
        self.shift_ = randomShift

    def make(self, dim,
             seed):
        return HaltonRsg(dim, seed, self.start_, self.shift_)

    def name(self):
        prefix = "random-start " if self.start_ else ""
        if self.shift_:
            prefix += "random-shift "
        return prefix + "Halton"


class LowDiscrepancyTest(unittest.TestCase):
    def testSeedGenerator(self):
        TEST_MESSAGE("Testing random-seed generator...")
        SeedGenerator.instance().get()

    def testPolynomialsModuloTwo(self):
        TEST_MESSAGE("Testing " + str(PPMT_MAX_DIM) +
                     " primitive polynomials modulo two...")

        jj = [
            1, 1, 2, 2, 6, 6, 18,
            16, 48, 60, 176, 144, 630, 756,
            1800, 2048, 7710, 7776, 27594, 24000, 84672,
            120032, 356960, 276480, 1296000, 1719900, 4202496]

        i = 0
        j = 0
        n = 0
        polynomial = 0
        while n < PPMT_MAX_DIM or polynomial != -1:
            if polynomial == -1:
                i += 1  # Increase degree index
                j = 0  # Reset index of polynomial in degree.

            polynomial = primitivePolynomials(i, j)
            if polynomial == -1:
                n -= 1
                self.assertFalse(j != jj[i])
            j += 1  # Increase index of polynomial in degree i+1
            n += 1  # Increase overall polynomial counter

    def testSobol(self):
        TEST_MESSAGE("Testing Sobol sequences up to dimension " + str(PPMT_MAX_DIM) + "...")

        point = DoubleVector()
        tolerance = 1.0e-15

        # testing max dimensionality
        dimensionality = PPMT_MAX_DIM
        seed = 123456
        rsg = SobolRsg(dimensionality, seed)
        points = 100
        for i in range(points):
            point = rsg.nextSequence().value()
            self.assertFalse(len(point) != dimensionality)

        # testing homogeneity properties
        dimensionality = 33
        seed = 123456
        rsg = SobolRsg(dimensionality, seed)
        stat = SequenceStatistics(dimensionality)

        for j in range(1, 5):  # (j = 1 j < 5 j++): # five cycle
            points = int(pow(2.0, j)) - 1  # base 2
            for k in range(points):
                if j == 1:
                    point = rsg.nextSequence().value()
                    stat.add(point)

            mean = stat.mean()
            for i in range(dimensionality):
                error = abs(mean[i] - 0.5)
                if error > tolerance:
                    self.assertFalse(error > tolerance)

                # testing first dimension (van der Corput sequence)
        vanderCorputSequenceModuloTwo = [
            # first cycle (zero excluded)
            0.50000,
            # second cycle
            0.75000, 0.25000,
            # third cycle
            0.37500, 0.87500, 0.62500, 0.12500,
            # fourth cycle
            0.18750, 0.68750, 0.93750, 0.43750, 0.31250, 0.81250, 0.56250, 0.06250,
            # fifth cycle
            0.09375, 0.59375, 0.84375, 0.34375, 0.46875, 0.96875, 0.71875, 0.21875,
            0.15625, 0.65625, 0.90625, 0.40625, 0.28125, 0.78125, 0.53125, 0.03125]

        dimensionality = 1
        rsg = SobolRsg(dimensionality)
        points = int(pow(2.0, 5)) - 1  # five cycles
        for i in range(points):
            point = rsg.nextSequence().value()
            error = abs(point[0] - vanderCorputSequenceModuloTwo[i])
            self.assertFalse(error > tolerance)

    def testHalton(self):
        TEST_MESSAGE("Testing Halton sequences...")

        point = DoubleVector()
        tolerance = 1.0e-15

        # testing "high" dimensionality
        dimensionality = PPMT_MAX_DIM
        rsg = HaltonRsg(dimensionality, 0, false, false)
        points = 100
        for i in range(points):
            point = rsg.nextSequence().value()
            self.assertFalse(len(point) != dimensionality)

            # testing first and second dimension (van der Corput sequence)
        vanderCorputSequenceModuloTwo = [
            # first cycle (zero excluded)
            0.50000,
            # second cycle
            0.25000, 0.75000,
            # third cycle
            0.12500, 0.62500, 0.37500, 0.87500,
            # fourth cycle
            0.06250, 0.56250, 0.31250, 0.81250, 0.18750, 0.68750, 0.43750, 0.93750,
            # fifth cycle
            0.03125, 0.53125, 0.28125, 0.78125, 0.15625, 0.65625, 0.40625, 0.90625,
            0.09375, 0.59375, 0.34375, 0.84375, 0.21875, 0.71875, 0.46875, 0.96875, ]

        dimensionality = 1
        rsg = HaltonRsg(dimensionality, 0, false, false)
        points = int(pow(2.0, 5)) - 1  # five cycles
        for i in range(points):
            point = rsg.nextSequence().value()
            error = abs(point[0] - vanderCorputSequenceModuloTwo[i])
            self.assertFalse(error > tolerance)

        vanderCorputSequenceModuloThree = [
            # first cycle (zero excluded)
            1.0 / 3, 2.0 / 3,
            # second cycle
            1.0 / 9, 4.0 / 9, 7.0 / 9, 2.0 / 9, 5.0 / 9, 8.0 / 9,
            # third cycle
            1.0 / 27, 10.0 / 27, 19.0 / 27, 4.0 / 27, 13.0 / 27, 22.0 / 27,
            7.0 / 27, 16.0 / 27, 25.0 / 27, 2.0 / 27, 11.0 / 27, 20.0 / 27,
            5.0 / 27, 14.0 / 27, 23.0 / 27, 8.0 / 27, 17.0 / 27, 26.0 / 27]

        dimensionality = 2
        rsg = HaltonRsg(dimensionality, 0, false, false)
        points = int(pow(3.0, 3)) - 1  # three cycles of the higher dimension
        for i in range(points):
            point = rsg.nextSequence().value()
            error = abs(point[0] - vanderCorputSequenceModuloTwo[i])
            self.assertFalse(error > tolerance)
            error = abs(point[1] - vanderCorputSequenceModuloThree[i])
            self.assertFalse(error > tolerance)

            # testing homogeneity properties
        dimensionality = 33
        rsg = HaltonRsg(dimensionality, 0, false, false)
        stat = SequenceStatistics(dimensionality)

        mean = DoubleVector()
        stdev = DoubleVector()
        variance = DoubleVector()
        skewness = DoubleVector()
        kurtosis = DoubleVector()
        k = 0

        for j in range(1, 5):  # (j = 1 j < 5 j++): # five cycle
            points = int(pow(2.0, j)) - 1  # base 2
            if j == 1:
                for k in range(points):
                    point = rsg.nextSequence().value()
                    stat.add(point)

            mean = stat.mean()
            error = abs(mean[0] - 0.5)
            self.assertFalse(error > tolerance)

            # reset generator and gaussianstatistics
        rsg = HaltonRsg(dimensionality, 0, false, false)
        stat.reset(dimensionality)
        k = 0
        for j in range(1, 3):  # (j = 1 j < 3 j++): # three cycle
            points = int(pow(3.0, j)) - 1  # base 3
            if j == 1:
                for k in range(points):
                    point = rsg.nextSequence().value()
                    stat.add(point)

            mean = stat.mean()
            error = abs(mean[1] - 0.5)
            self.assertFalse(error > tolerance)

    def testFaure(self):
        TEST_MESSAGE("Testing Faure sequences...")

        point = DoubleVector()

        tolerance = 1.0e-15

        # testing "high" dimensionality
        dimensionality = PPMT_MAX_DIM
        rsg = FaureRsg(dimensionality)
        points = 100
        for i in range(points):
            point = rsg.nextSequence().value()
            self.assertFalse(len(point) != dimensionality)

        # 1-dimension Faure (van der Corput sequence base 2)
        vanderCorputSequenceModuloTwo = [
            # first cycle (zero excluded)
            0.50000,
            # second cycle
            0.75000, 0.25000,
            # third cycle
            0.37500, 0.87500, 0.62500, 0.12500,
            # fourth cycle
            0.18750, 0.68750, 0.93750, 0.43750, 0.31250, 0.81250, 0.56250, 0.06250,
            # fifth cycle
            0.09375, 0.59375, 0.84375, 0.34375, 0.46875, 0.96875, 0.71875, 0.21875,
            0.15625, 0.65625, 0.90625, 0.40625, 0.28125, 0.78125, 0.53125, 0.03125]
        dimensionality = 1
        rsg = FaureRsg(dimensionality)
        points = int(pow(2.0, 5)) - 1  # five cycles
        for i in range(points):
            point = rsg.nextSequence().value()
            error = abs(point[0] - vanderCorputSequenceModuloTwo[i])
            self.assertFalse(error > tolerance)

        # 2nd dimension of the 2-dimensional Faure sequence
        # (shuffled van der Corput sequence base 2)
        # checked with the code provided with "Economic generation of
        # low-discrepancy sequences with a b-ary gray code", by E. Thiemard
        FaureDimensionTwoOfTwo = [
            # first cycle (zero excluded)
            0.50000,
            # second cycle
            0.25000, 0.75000,
            # third cycle
            0.37500, 0.87500, 0.12500, 0.62500,
            # fourth cycle
            0.31250, 0.81250, 0.06250, 0.56250, 0.18750, 0.68750, 0.43750, 0.93750,
            # fifth cycle
            0.46875, 0.96875, 0.21875, 0.71875, 0.09375, 0.59375, 0.34375, 0.84375,
            0.15625, 0.65625, 0.40625, 0.90625, 0.28125, 0.78125, 0.03125, 0.53125]
        dimensionality = 2
        rsg = FaureRsg(dimensionality)
        points = int(pow(2.0, 5)) - 1  # five cycles
        for i in range(points):
            point = rsg.nextSequence().value()
            error = abs(point[0] - vanderCorputSequenceModuloTwo[i])
            self.assertFalse(error > tolerance)
            error = abs(point[1] - FaureDimensionTwoOfTwo[i])
            self.assertFalse(error > tolerance)

        # 3-dimension Faure sequence (shuffled van der Corput sequence base 3)
        # see "Monte Carlo Methods in Financial Engineering,"
        # by Paul Glasserman, 2004 Springer Verlag, pag. 299
        FaureDimensionOneOfThree = [
            # first cycle (zero excluded)
            1.0 / 3, 2.0 / 3,
            # second cycle
            7.0 / 9, 1.0 / 9, 4.0 / 9, 5.0 / 9, 8.0 / 9, 2.0 / 9]
        FaureDimensionTwoOfThree = [
            # first cycle (zero excluded)
            1.0 / 3, 2.0 / 3,
            # second cycle
            1.0 / 9, 4.0 / 9, 7.0 / 9, 2.0 / 9, 5.0 / 9, 8.0 / 9]
        FaureDimensionThreeOfThree = [
            # first cycle (zero excluded)
            1.0 / 3, 2.0 / 3,
            # second cycle
            4.0 / 9, 7.0 / 9, 1.0 / 9, 8.0 / 9, 2.0 / 9, 5.0 / 9]

        dimensionality = 3
        rsg = FaureRsg(dimensionality)
        points = int(pow(3.0, 2)) - 1  # three cycles
        for i in range(points):
            point = rsg.nextSequence().value()
            error = abs(point[0] - FaureDimensionOneOfThree[i])
            self.assertFalse(error > tolerance)
            error = abs(point[1] - FaureDimensionTwoOfThree[i])
            self.assertFalse(error > tolerance)
            error = abs(point[2] - FaureDimensionThreeOfThree[i])
            self.assertFalse(error > tolerance)

    def testMersenneTwisterDiscrepancy(self):
        TEST_MESSAGE("Testing Mersenne-twister discrepancy...")

        discrepancy = [
            dim002DiscrMersenneTwis, dim003DiscrMersenneTwis,
            dim005DiscrMersenneTwis, dim010DiscrMersenneTwis,
            dim015DiscrMersenneTwis, dim030DiscrMersenneTwis,
            dim050DiscrMersenneTwis, dim100DiscrMersenneTwis]

        self._testGeneratorDiscrepancy(
            MersenneFactory(),
            discrepancy,
            "MersenneDiscrepancy.txt",
            "DiscrMersenneTwis")

    def testPlainHaltonDiscrepancy(self):
        TEST_MESSAGE("Testing plain Halton discrepancy...")

        discrepancy = [
            dim002DiscrPlain_Halton, dim003DiscrPlain_Halton,
            dim005DiscrPlain_Halton, dim010DiscrPlain_Halton,
            dim015DiscrPlain_Halton, dim030DiscrPlain_Halton,
            dim050DiscrPlain_Halton, dim100DiscrPlain_Halton]

        self._testGeneratorDiscrepancy(
            HaltonFactory(false, false),
            discrepancy,
            "PlainHaltonDiscrepancy.txt",
            "DiscrPlain_Halton")

    def testRandomStartHaltonDiscrepancy(self):
        TEST_MESSAGE("Testing random-start Halton discrepancy...")

        discrepancy = [
            dim002DiscrRStartHalton, dim003DiscrRStartHalton,
            dim005DiscrRStartHalton, dim010DiscrRStartHalton,
            dim015DiscrRStartHalton, dim030DiscrRStartHalton,
            dim050DiscrRStartHalton, dim100DiscrRStartHalton]

        self._testGeneratorDiscrepancy(
            HaltonFactory(true, false),
            discrepancy,
            "RandomStartHaltonDiscrepancy.txt",
            "DiscrRStartHalton")

    def testRandomShiftHaltonDiscrepancy(self):
        TEST_MESSAGE("Testing random-shift Halton discrepancy...")

        discrepancy = [
            dim002DiscrRShiftHalton, dim003DiscrRShiftHalton,
            dim005DiscrRShiftHalton, dim010DiscrRShiftHalton,
            dim015DiscrRShiftHalton, dim030DiscrRShiftHalton,
            dim050DiscrRShiftHalton, dim100DiscrRShiftHalton]

        self._testGeneratorDiscrepancy(
            HaltonFactory(false, true),
            discrepancy,
            "RandomShiftHaltonDiscrepancy.txt",
            "DiscrRShiftHalton")

    def testRandomStartRandomShiftHaltonDiscrepancy(self):
        TEST_MESSAGE("Testing random-start, random-shift Halton discrepancy...")

        discrepancy = [
            dim002DiscrRStRShHalton, dim003DiscrRStRShHalton,
            dim005DiscrRStRShHalton, dim010DiscrRStRShHalton,
            dim015DiscrRStRShHalton, dim030DiscrRStRShHalton,
            dim050DiscrRStRShHalton, dim100DiscrRStRShHalton]

        self._testGeneratorDiscrepancy(
            HaltonFactory(true, true),
            discrepancy,
            "RandomStartRandomShiftHaltonDiscrepancy.txt",
            "DiscrRStRShHalton")

    def testJackelSobolDiscrepancy(self):
        TEST_MESSAGE("Testing Jaeckel-Sobol discrepancy...")

        discrepancy = [
            dim002Discr_Sobol, dim003Discr_Sobol,
            dim005Discr_Sobol, dim010DiscrJackel_Sobol,
            dim015DiscrJackel_Sobol, dim030DiscrJackel_Sobol,
            dim050DiscrJackel_Sobol, dim100DiscrJackel_Sobol]

        self._testGeneratorDiscrepancy(
            SobolFactory(SobolRsg.Jaeckel),
            discrepancy,
            "JackelSobolDiscrepancy.txt",
            "DiscrJackel_Sobol")

    def testSobolLevitanSobolDiscrepancy(self):
        TEST_MESSAGE("Testing Levitan-Sobol discrepancy...")

        discrepancy = [
            dim002Discr_Sobol, dim003Discr_Sobol,
            dim005Discr_Sobol, dim010DiscrSobLev_Sobol,
            dim015DiscrSobLev_Sobol, dim030DiscrSobLev_Sobol,
            dim050DiscrSobLev_Sobol, dim100DiscrSobLev_Sobol]

        self._testGeneratorDiscrepancy(
            SobolFactory(SobolRsg.SobolLevitan),
            discrepancy,
            "SobolLevitanSobolDiscrepancy.txt",
            "DiscrSobLev_Sobol")

    def testSobolLevitanLemieuxSobolDiscrepancy(self):
        TEST_MESSAGE("Testing Levitan-Lemieux-Sobol discrepancy...")

        discrepancy = [
            dim002Discr_Sobol, dim003Discr_Sobol,
            dim005Discr_Sobol, dim010DiscrSobLev_Sobol,
            dim015DiscrSobLev_Sobol, dim030DiscrSobLev_Sobol,
            dim050DiscrSobLem_Sobol, dim100DiscrSobLem_Sobol]

        self._testGeneratorDiscrepancy(
            SobolFactory(SobolRsg.SobolLevitanLemieux),
            discrepancy,
            "SobolLevitanLemieuxSobolDiscrepancy.txt",
            "DiscrSobLevLem_Sobol")

    def testUnitSobolDiscrepancy(self):
        TEST_MESSAGE("Testing unit Sobol discrepancy...")

        discrepancy = [
            dim002Discr__Unit_Sobol, dim003Discr__Unit_Sobol,
            dim005Discr__Unit_Sobol, dim010Discr__Unit_Sobol,
            dim015Discr__Unit_Sobol, dim030Discr__Unit_Sobol,
            dim050Discr__Unit_Sobol, dim100Discr__Unit_Sobol]

        self._testGeneratorDiscrepancy(
            SobolFactory(SobolRsg.Unit),
            discrepancy,
            "UnitSobolDiscrepancy.txt",
            "Discr__Unit_Sobol")

    def testRandomizedLowDiscrepancySequence(self):
        TEST_MESSAGE("Testing randomized low-discrepancy sequences up to "
                     "dimension " + str(PPMT_MAX_DIM) + "...")

        rldsg = RandomizedSobolLDS(PPMT_MAX_DIM)
        rldsg.nextSequence()
        rldsg.lastSequence()
        rldsg.nextRandomizer()

        t0 = MersenneTwisterUniformRng()
        t1 = SobolRsg(PPMT_MAX_DIM)
        t2 = MersenneTwisterUniformRsg(PPMT_MAX_DIM)
        rldsg2 = RandomizedSobolLDS(t1, t2)
        rldsg2.nextSequence()
        rldsg2.lastSequence()
        rldsg2.nextRandomizer()

        rldsg3 = RandomizedSobolLDS(t1)
        rldsg3.nextSequence()
        rldsg3.lastSequence()
        rldsg3.nextRandomizer()

    def testSobolSkipping(self):
        TEST_MESSAGE("Testing Sobol sequence skipping...")

        seed = 42
        dimensionality = [1, 10, 100, 1000]
        skip = [0, 1, 42, 512, 100000]
        integers = [
            SobolRsg.Unit,
            SobolRsg.Jaeckel,
            SobolRsg.SobolLevitan,
            SobolRsg.SobolLevitanLemieux]

        for integer in integers:
            for j in dimensionality:
                for k in skip:

                    # extract n samples
                    rsg1 = SobolRsg(j, seed, integer)
                    for l in range(k):
                        rsg1.nextInt32Sequence()

                    # skip n samples at once
                    rsg2 = SobolRsg(j, seed, integer)
                    rsg2.skipTo(k)

                    # compare next 100 samples
                    for m in range(100):
                        s1 = rsg1.nextInt32Sequence()
                        s2 = rsg2.nextInt32Sequence()
                        for n in range(len(s1)):
                            self.assertFalse(s1[n] != s2[n])

    def testRandomizedLattices(self):
        self._testRandomizedLatticeRule(LatticeRule.A, "A")
        self._testRandomizedLatticeRule(LatticeRule.B, "B")
        self._testRandomizedLatticeRule(LatticeRule.C, "C")
        self._testRandomizedLatticeRule(LatticeRule.D, "D")

    def _testRandomizedLatticeRule(self,
                                   name,
                                   nameString):
        maxDim = 30
        N = 1024
        numberBatches = 32

        TEST_MESSAGE(
            "Testing randomized lattice sequences (" + nameString + ") up to dimension " + str(maxDim) + "...")

        z = DoubleVector()

        z = LatticeRule.getRule(name, N)
        latticeGenerator = LatticeRsg(maxDim, z, N)

        seed = 12345678
        rng = MersenneTwisterUniformRng(seed)

        rsg = MersenneTwisterUniformRsg(maxDim, rng)

        rldsg = RandomizedLatticeLDS(latticeGenerator, rsg)

        outerStats = SequenceStatistics(maxDim)

        for i in range(numberBatches):
            innerStats = SequenceStatistics(maxDim)
            for j in range(N):
                innerStats.add(rldsg.nextSequence().value())

            outerStats.add(innerStats.mean())
            rldsg.nextRandomizer()

        means = DoubleVector(outerStats.mean())
        sds = DoubleVector(outerStats.errorEstimate())

        errorInSds = DoubleVector(maxDim)

        for i in range(maxDim):
            errorInSds[i] = (means[i] - 0.5) / sds[i]

        tolerance = 4.0

        for i in range(maxDim):
            self.assertFalse(abs(errorInSds[i]) > tolerance)

    def _testGeneratorDiscrepancy(self,
                                  generatorFactory,
                                  discrepancy,
                                  f,
                                  tag):
        tolerance = 1.0e-2

        point = DoubleVector()

        seed = 123456

        # more than 1 discrepancy measures take long time
        sampleLoops = max(1, discrepancyMeasuresNumber)

        for i in range(8):

            dim = dimensionality[i]
            stat = DiscrepancyStatistics(dim)

            rsg = generatorFactory.make(dim, seed)

            jMin = 10
            stat.reset()

            for j in range(jMin, jMin + sampleLoops):
                points = int(pow(2.0, j)) - 1
                for k in range(points):
                    point = rsg.nextSequence().value()
                    stat.add(point)

                discr = stat.discrepancy()

                self.assertFalse(abs(discr - discrepancy[i][j - jMin]) > tolerance * discr)
