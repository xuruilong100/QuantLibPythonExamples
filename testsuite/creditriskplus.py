import unittest
from utilities import *
from QuantLib import *


class CreditRiskPlusTest(unittest.TestCase):
    def testReferenceValues(self):
        TEST_MESSAGE(
            "Testing extended credit risk plus model against reference values...")

        tol = 1E-8

        # /* Reference Values are taken from [1] Integrating Correlations, Risk,
        # July 1999, table A, table B and figure 1 */

        sector1Exposure = DoubleVector(1000, 1.0)
        sector1Pd = DoubleVector(1000, 0.04)
        sector1Sector = SizeVector(1000, 0)

        sector2Exposure = DoubleVector(1000, 2.0)
        sector2Pd = DoubleVector(1000, 0.02)
        sector2Sector = SizeVector(1000, 1)

        exposure = DoubleVector()
        for i in range(len(sector1Exposure)):
            exposure.push_back(sector1Exposure[i])
        for i in range(len(sector2Exposure)):
            exposure.push_back(sector2Exposure[i])

        pd = DoubleVector()
        for i in range(len(sector1Pd)):
            pd.push_back(sector1Pd[i])
        for i in range(len(sector2Pd)):
            pd.push_back(sector2Pd[i])

        sector = SizeVector()
        for i in range(len(sector1Sector)):
            sector.push_back(sector1Sector[i])
        for i in range(len(sector2Sector)):
            sector.push_back(sector2Sector[i])

        relativeDefaultVariance = DoubleVector()
        relativeDefaultVariance.push_back(0.75 * 0.75)
        relativeDefaultVariance.push_back(0.75 * 0.75)

        rho = Matrix(2, 2)
        rho[0][0] = rho[1][1] = 1.0
        rho[0][1] = rho[1][0] = 0.50

        unit = 0.1

        cr = CreditRiskPlus(exposure, pd, sector, relativeDefaultVariance, rho, unit)

        self.assertFalse(abs(cr.sectorExposures()[0] - 1000.0) > tol)
        self.assertFalse(abs(cr.sectorExposures()[1] - 2000.0) > tol)
        self.assertFalse(abs(cr.sectorExpectedLoss()[0] - 40.0) > tol)
        self.assertFalse(abs(cr.sectorExpectedLoss()[1] - 40.0) > tol)
        self.assertFalse(abs(cr.sectorUnexpectedLoss()[0] - 30.7) > 0.05)
        self.assertFalse(abs(cr.sectorUnexpectedLoss()[1] - 31.3) > 0.05)
        self.assertFalse(abs(cr.exposure() - 3000.0) > tol)
        self.assertFalse(abs(cr.expectedLoss() - 80.0) > tol)
        self.assertFalse(abs(cr.unexpectedLoss() - 53.1) > 0.01)

        # the overall relative default variance in the paper seems generously rounded,
        # but since EL and UL is matching closely and the former is retrieved
        # as a simple expression in the latter, we do not suspect a problem in our
        # calculation

        self.assertFalse(abs(cr.relativeDefaultVariance() - 0.65 * 0.65) > 0.001)
        self.assertFalse(abs(cr.lossQuantile(0.99) - 250) > 0.5)
