import unittest
from math import sqrt, exp

from QuantLib import *

from utilities import *


def createKlugeProcess():
    x0 = Array(2)
    x0[0] = 3.0
    x0[1] = 0.0

    beta = 5.0
    eta = 2.0
    jumpIntensity = 1.0
    speed = 1.0
    volatility = 2.0

    ouProcess = ExtendedOrnsteinUhlenbeckProcess(
        speed, volatility, x0[0], lambda x: 3.0)
    return ExtOUWithJumpsProcess(ouProcess, x0[1], beta, jumpIntensity, eta)


class linear(object):
    def __init__(self, alpha, beta):
        self.alpha = alpha
        self.beta = beta

    def __call__(self, x):
        return self.alpha + self.beta * x


fuelPrices = [
    20.74, 21.65, 20.78, 21.58, 21.43, 20.82, 22.02, 21.52, 21.02, 21.46, 21.75, 20.69, 22.16,
    20.38, 20.82, 20.68, 20.57, 21.92, 22.04, 20.45, 20.75, 21.92, 20.53, 20.67, 20.88, 21.02,
    20.82, 21.67, 21.82, 22.12, 20.45, 20.74, 22.39, 20.95, 21.71, 20.70, 20.94, 21.59, 22.33,
    21.13, 21.50, 21.42, 20.56, 21.23, 21.37, 21.90, 20.62, 21.17, 21.86, 22.04, 22.05, 21.00,
    20.70, 21.12, 21.26, 22.40, 21.31, 22.24, 21.96, 21.02, 21.71, 20.48, 21.36, 21.75, 21.90,
    20.44, 21.26, 22.29, 20.34, 21.79, 21.66, 21.50, 20.76, 20.27, 20.84, 20.24, 21.97, 20.52,
    20.98, 21.40, 20.39, 20.71, 20.78, 20.30, 21.56, 21.72, 20.27, 21.57, 21.82, 20.57, 21.33,
    20.51, 22.32, 21.99, 20.57, 22.11, 21.56, 22.24, 20.62, 21.70, 21.11, 21.19, 21.79, 20.46,
    22.21, 20.82, 20.52, 22.29, 20.71, 21.45, 22.40, 20.63, 20.95, 21.97, 22.20, 20.67, 21.01,
    22.25, 20.76, 21.33, 20.49, 20.33, 21.94, 20.64, 20.99, 21.09, 20.97, 22.17, 20.72, 22.06,
    20.86, 21.40, 21.75, 20.78, 21.79, 20.47, 21.19, 21.60, 20.75, 21.36, 21.61, 20.37, 21.67,
    20.28, 22.33, 21.37, 21.33, 20.87, 21.25, 22.01, 22.08, 20.81, 20.70, 21.84, 21.82, 21.68,
    21.24, 22.36, 20.83, 20.64, 21.03, 20.57, 22.34, 20.96, 21.54, 21.26, 21.43, 22.39]

powerPrices = [
    40.40, 36.71, 31.87, 25.81, 31.61, 35.00, 46.22, 60.68, 42.45, 38.01, 33.84, 29.79, 31.84,
    38.53, 49.23, 59.92, 43.85, 37.47, 34.89, 29.99, 30.85, 29.19, 29.25, 38.67, 36.90, 25.93,
    22.12, 20.19, 17.19, 19.29, 13.51, 18.14, 33.76, 30.48, 25.63, 18.01, 23.86, 32.41, 48.56,
    64.69, 38.42, 39.31, 32.73, 29.97, 31.41, 35.02, 46.85, 58.12, 39.14, 35.42, 32.61, 28.76,
    29.41, 35.83, 46.73, 61.41, 61.01, 59.43, 60.43, 66.29, 62.79, 62.66, 57.66, 51.63, 62.18,
    60.53, 61.94, 64.86, 59.57, 58.15, 53.74, 48.36, 45.64, 51.21, 51.54, 50.79, 54.50, 49.92,
    41.58, 39.81, 28.86, 37.42, 39.78, 42.36, 45.67, 36.84, 33.91, 28.75, 62.97, 63.84, 62.91,
    68.77, 64.33, 61.95, 59.12, 54.89, 63.62, 60.90, 66.57, 69.51, 64.71, 59.89, 57.28, 57.10,
    65.09, 63.82, 67.52, 70.51, 65.59, 59.36, 58.22, 54.64, 52.17, 53.02, 57.12, 53.50, 53.16,
    49.21, 52.21, 40.96, 49.01, 47.94, 49.89, 53.83, 52.96, 50.33, 51.72, 46.99, 39.06, 47.99,
    47.91, 52.35, 48.51, 47.39, 50.45, 43.66, 25.62, 35.76, 42.76, 46.51, 45.62, 46.79, 48.76,
    41.00, 52.65, 55.57, 57.67, 56.79, 55.15, 54.74, 50.31, 47.49, 53.72, 55.62, 55.89, 58.11,
    54.46, 52.92, 49.61, 44.68, 51.59, 57.44, 56.50, 55.12, 57.22, 54.61, 49.92, 45.20]


def createKlugeExtOUProcess():
    beta = 200
    eta = 1.0 / 0.2
    lmbd = 4.0
    alpha = 7.0
    volatility_x = 1.4
    kappa = 4.45
    volatility_u = sqrt(1.3)
    rho = 0.7

    x0 = Array(2)
    x0[0] = 0.0
    x0[1] = 0.0

    ouProcess = ExtendedOrnsteinUhlenbeckProcess(
        alpha, volatility_x, x0[0], lambda x: 0.0)
    lnPowerProcess = ExtOUWithJumpsProcess(ouProcess, x0[1], beta, lmbd, eta)

    u = 0.0
    lnGasProcess = ExtendedOrnsteinUhlenbeckProcess(
        kappa, volatility_u, u, lambda x: 0.0)

    klugeOUProcess = KlugeExtOUProcess(rho, lnPowerProcess, lnGasProcess)

    return klugeOUProcess


class VPPTest(unittest.TestCase):

    def testGemanRoncoroniProcess(self):

        TEST_MESSAGE(
            "Testing Geman-Roncoroni process...")

        backup = SavedSettings()

        today = Date(18, December, 2011)
        Settings.instance().evaluationDate = today
        dc = ActualActual(ActualActual.ISDA)

        rTS = flatRate(today, 0.03, dc)

        x0 = 3.3
        beta = 0.05
        alpha = 3.1
        gamma = -0.09
        delta = 0.07
        eps = -0.40
        zeta = -0.40
        d = 1.6
        k = 1.0
        tau = 0.5
        sig2 = 10.0
        a = -7.0
        b = -0.3
        theta1 = 35.0
        theta2 = 9.0
        theta3 = 0.10
        psi = 1.9

        grProcess = GemanRoncoroniProcess(
            x0, alpha, beta, gamma, delta, eps, zeta, d, k, tau, sig2, a, b,
            theta1, theta2, theta3, psi)

        speed = 5.0
        vol = sqrt(1.4)
        betaG = 0.08
        alphaG = 1.0
        x0G = 1.1

        f = linear(alphaG, betaG)

        eouProcess = ExtendedOrnsteinUhlenbeckProcess(
            speed, vol, x0G, f, ExtendedOrnsteinUhlenbeckProcess.Trapezodial)

        processes = [grProcess, eouProcess]

        correlation = Matrix(2, 2, 1.0)
        correlation[0][1] = correlation[1][0] = 0.25

        pArray = StochasticProcessArray(processes, correlation)

        T = 10.0
        stepsPerYear = 250
        steps = int(T * stepsPerYear)

        grid = TimeGrid(T, steps)

        rsg = GaussianRandomSequenceGenerator(
            UniformRandomSequenceGenerator(
                pArray.size() * (len(grid) - 1),
                UniformRandomGenerator(421)))

        npv = GeneralStatistics()
        onTime = GeneralStatistics()
        generator = GaussianMultiPathGenerator(pArray, grid, rsg, false)

        heatRate = 8.0
        nrTrails = 250

        for n in range(nrTrails):
            plantValue = 0.0
            path = generator.next()

            for i in range(1, steps + 1):
                t = i / stepsPerYear
                df = rTS.discount(t)

                fuelPrice = exp(path.value()[1][i])
                electricityPrice = exp(path.value()[0][i])

                sparkSpread = electricityPrice - heatRate * fuelPrice
                plantValue += max(0.0, sparkSpread) * df
                onTime.add(1.0 if sparkSpread > 0.0 else 0.0)

            npv.add(plantValue)

        expectedNPV = 12500
        calculatedNPV = npv.mean()
        errorEstimateNPV = npv.errorEstimate()

        self.assertFalse(abs(calculatedNPV - expectedNPV) > 3.0 * errorEstimateNPV)

        expectedOnTime = 0.43
        calculatedOnTime = onTime.mean()
        errorEstimateOnTime = sqrt(calculatedOnTime * (1 - calculatedOnTime)) / nrTrails

        self.assertFalse(abs(calculatedOnTime - expectedOnTime) > 3.0 * errorEstimateOnTime)

    def testSimpleExtOUStorageEngine(self):

        TEST_MESSAGE(
            "Testing simple-storage option based on ext. OU model...")

        backup = SavedSettings()

        settlementDate = Date(18, December, 2011)
        Settings.instance().evaluationDate = settlementDate
        dayCounter = ActualActual(ActualActual.ISDA)
        maturityDate = settlementDate + Period(12, Months)

        exerciseDates = DateVector(1, settlementDate + Period(1, Days))
        while exerciseDates.back() < maturityDate:
            exerciseDates.push_back(exerciseDates.back() + Period(1, Days))

        bermudanExercise = BermudanExercise(exerciseDates)

        x0 = 3.0
        speed = 1.0
        volatility = 0.5
        irRate = 0.1

        ouProcess = ExtendedOrnsteinUhlenbeckProcess(
            speed, volatility, x0, lambda x: 3.0)

        rTS = flatRate(settlementDate, irRate, dayCounter)

        storageEngine = FdSimpleExtOUStorageEngine(ouProcess, rTS, 1, 25)

        storageOption = VanillaStorageOption(bermudanExercise, 50, 0, 1)

        storageOption.setPricingEngine(storageEngine)

        expected = 69.5755
        calculated = storageOption.NPV()

        self.assertFalse(abs(expected - calculated) > 5e-2)

    def testKlugeExtOUSpreadOption(self):

        TEST_MESSAGE(
            "Testing simple Kluge ext-Ornstein-Uhlenbeck spread option...")

        backup = SavedSettings()

        settlementDate = Date(18, December, 2011)
        Settings.instance().evaluationDate = settlementDate

        dayCounter = ActualActual(ActualActual.ISDA)
        maturityDate = settlementDate + Period(1, Years)
        maturity = dayCounter.yearFraction(settlementDate, maturityDate)

        speed = 1.0
        vol = sqrt(1.4)
        betaG = 0.0
        alphaG = 3.0
        x0G = 3.0

        irRate = 0.0
        heatRate = 2.0
        rho = 0.5

        klugeProcess = createKlugeProcess()
        f = linear(alphaG, betaG)

        extOUProcess = ExtendedOrnsteinUhlenbeckProcess(
            speed, vol, x0G, f,
            ExtendedOrnsteinUhlenbeckProcess.Trapezodial)

        rTS = flatRate(settlementDate, irRate, dayCounter)

        klugeOUProcess = KlugeExtOUProcess(rho, klugeProcess, extOUProcess)

        payoff = PlainVanillaPayoff(Option.Call, 0.0)

        spreadFactors = Array(2)
        spreadFactors[0] = 1.0
        spreadFactors[1] = -heatRate
        basketPayoff = AverageBasketPayoff(payoff, spreadFactors)

        exercise = EuropeanExercise(maturityDate)

        option = BasketOption(basketPayoff, exercise)
        option.setPricingEngine(
            FdKlugeExtOUSpreadEngine(klugeOUProcess, rTS, 5, 200, 50, 20))

        grid = TimeGrid(maturity, 50)

        rsg = GaussianRandomSequenceGenerator(
            UniformRandomSequenceGenerator(
                klugeOUProcess.factors() * (len(grid) - 1),
                UniformRandomGenerator(1234)))

        generator = GaussianMultiPathGenerator(klugeOUProcess, grid, rsg, false)

        npv = GeneralStatistics()
        nTrails = 20000
        for i in range(nTrails):
            path = generator.next()

            p = Array(2)
            p[0] = path.value()[0].back() + path.value()[1].back()
            p[1] = path.value()[2].back()
            npv.add(basketPayoff(Exp(p)))

        calculated = option.NPV()
        expectedMC = npv.mean()
        mcError = npv.errorEstimate()
        self.assertFalse(abs(expectedMC - calculated) > 3 * mcError)

    @unittest.skip("testVPPPricing")
    def testVPPPricing(self):
        TEST_MESSAGE(
            "Testing VPP pricing using perfect foresight or FDM...")

    @unittest.skip("testKlugeExtOUMatrixDecomposition")
    def testKlugeExtOUMatrixDecomposition(self):
        TEST_MESSAGE(
            "Testing KlugeExtOU matrix decomposition...")
