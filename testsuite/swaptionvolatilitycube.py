import unittest

from QuantLib import *

from utilities import *


class SwaptionTenors(object):
    def __init__(self):
        self.options = PeriodVector()
        self.swaps = PeriodVector()


class SwaptionMarketConventions(object):
    def __init__(self):
        self.calendar = None
        self.optionBdc = None
        self.dayCounter = None

    def setConventions(self):
        self.calendar = TARGET()
        self.optionBdc = ModifiedFollowing
        self.dayCounter = Actual365Fixed()


class AtmVolatility(object):
    def __init__(self):
        self.tenors = SwaptionTenors()
        self.vols = Matrix()
        self.volsHandle = QuoteHandleVectorVector()

    def setMarketData(self):
        self.tenors.options.resize(6)
        self.tenors.options[0] = Period(1, Months)
        self.tenors.options[1] = Period(6, Months)
        self.tenors.options[2] = Period(1, Years)
        self.tenors.options[3] = Period(5, Years)
        self.tenors.options[4] = Period(10, Years)
        self.tenors.options[5] = Period(30, Years)
        self.tenors.swaps.resize(4)
        self.tenors.swaps[0] = Period(1, Years)
        self.tenors.swaps[1] = Period(5, Years)
        self.tenors.swaps[2] = Period(10, Years)
        self.tenors.swaps[3] = Period(30, Years)
        self.vols = Matrix(len(self.tenors.options), len(self.tenors.swaps))
        self.vols[0][0] = 0.1300
        self.vols[0][1] = 0.1560
        self.vols[0][2] = 0.1390
        self.vols[0][3] = 0.1220
        self.vols[1][0] = 0.1440
        self.vols[1][1] = 0.1580
        self.vols[1][2] = 0.1460
        self.vols[1][3] = 0.1260
        self.vols[2][0] = 0.1600
        self.vols[2][1] = 0.1590
        self.vols[2][2] = 0.1470
        self.vols[2][3] = 0.1290
        self.vols[3][0] = 0.1640
        self.vols[3][1] = 0.1470
        self.vols[3][2] = 0.1370
        self.vols[3][3] = 0.1220
        self.vols[4][0] = 0.1400
        self.vols[4][1] = 0.1300
        self.vols[4][2] = 0.1250
        self.vols[4][3] = 0.1100
        self.vols[5][0] = 0.1130
        self.vols[5][1] = 0.1090
        self.vols[5][2] = 0.1070
        self.vols[5][3] = 0.0930
        self.volsHandle.resize(len(self.tenors.options))
        for i in range(len(self.tenors.options)):
            tmp = QuoteHandleVector(len(self.tenors.swaps))
            for j in range(len(self.tenors.swaps)):
                tmp[j] = QuoteHandle(
                    SimpleQuote(self.vols[i][j]))
            self.volsHandle[i] = tmp


class VolatilityCube(object):
    def __init__(self):
        self.tenors = SwaptionTenors()
        self.volSpreads = Matrix()
        self.volSpreadsHandle = QuoteHandleVectorVector()
        self.strikeSpreads = DoubleVector()

    def setMarketData(self):
        self.tenors.options.resize(3)
        self.tenors.options[0] = Period(1, Years)
        self.tenors.options[1] = Period(10, Years)
        self.tenors.options[2] = Period(30, Years)
        self.tenors.swaps.resize(3)
        self.tenors.swaps[0] = Period(2, Years)
        self.tenors.swaps[1] = Period(10, Years)
        self.tenors.swaps[2] = Period(30, Years)
        self.strikeSpreads.resize(5)
        self.strikeSpreads[0] = -0.020
        self.strikeSpreads[1] = -0.005
        self.strikeSpreads[2] = +0.000
        self.strikeSpreads[3] = +0.005
        self.strikeSpreads[4] = +0.020
        self.volSpreads = Matrix(
            len(self.tenors.options) * len(self.tenors.swaps),
            len(self.strikeSpreads))
        self.volSpreads[0][0] = 0.0599
        self.volSpreads[0][1] = 0.0049
        self.volSpreads[0][2] = 0.0000
        self.volSpreads[0][3] = -0.0001
        self.volSpreads[0][4] = 0.0127
        self.volSpreads[1][0] = 0.0729
        self.volSpreads[1][1] = 0.0086
        self.volSpreads[1][2] = 0.0000
        self.volSpreads[1][3] = -0.0024
        self.volSpreads[1][4] = 0.0098
        self.volSpreads[2][0] = 0.0738
        self.volSpreads[2][1] = 0.0102
        self.volSpreads[2][2] = 0.0000
        self.volSpreads[2][3] = -0.0039
        self.volSpreads[2][4] = 0.0065
        self.volSpreads[3][0] = 0.0465
        self.volSpreads[3][1] = 0.0063
        self.volSpreads[3][2] = 0.0000
        self.volSpreads[3][3] = -0.0032
        self.volSpreads[3][4] = -0.0010
        self.volSpreads[4][0] = 0.0558
        self.volSpreads[4][1] = 0.0084
        self.volSpreads[4][2] = 0.0000
        self.volSpreads[4][3] = -0.0050
        self.volSpreads[4][4] = -0.0057
        self.volSpreads[5][0] = 0.0576
        self.volSpreads[5][1] = 0.0083
        self.volSpreads[5][2] = 0.0000
        self.volSpreads[5][3] = -0.0043
        self.volSpreads[5][4] = -0.0014
        self.volSpreads[6][0] = 0.0437
        self.volSpreads[6][1] = 0.0059
        self.volSpreads[6][2] = 0.0000
        self.volSpreads[6][3] = -0.0030
        self.volSpreads[6][4] = -0.0006
        self.volSpreads[7][0] = 0.0533
        self.volSpreads[7][1] = 0.0078
        self.volSpreads[7][2] = 0.0000
        self.volSpreads[7][3] = -0.0045
        self.volSpreads[7][4] = -0.0046
        self.volSpreads[8][0] = 0.0545
        self.volSpreads[8][1] = 0.0079
        self.volSpreads[8][2] = 0.0000
        self.volSpreads[8][3] = -0.0042
        self.volSpreads[8][4] = -0.0020
        self.volSpreadsHandle = QuoteHandleVectorVector(
            len(self.tenors.options) * len(self.tenors.swaps))
        for i in range(len(self.tenors.options) * len(self.tenors.swaps)):
            temp = QuoteHandleVector(len(self.strikeSpreads))
            for j in range(len(self.strikeSpreads)):
                temp[j] = QuoteHandle(
                    SimpleQuote(self.volSpreads[i][j]))
            self.volSpreadsHandle[i] = temp


class CommonVars(object):

    def __init__(self):
        self.conventions = SwaptionMarketConventions()
        self.conventions.setConventions()

        self.atm = AtmVolatility()
        self.atm.setMarketData()
        self.atmVolMatrix = RelinkableSwaptionVolatilityStructureHandle(
            SwaptionVolatilityMatrix(
                self.conventions.calendar,
                self.conventions.optionBdc,
                self.atm.tenors.options,
                self.atm.tenors.swaps,
                self.atm.volsHandle,
                self.conventions.dayCounter))
        self.normalVolMatrix = RelinkableSwaptionVolatilityStructureHandle(
            SwaptionVolatilityMatrix(
                self.conventions.calendar,
                self.conventions.optionBdc,
                self.atm.tenors.options,
                self.atm.tenors.swaps,
                self.atm.volsHandle,
                self.conventions.dayCounter, false,
                Normal))

        self.cube = VolatilityCube()
        self.cube.setMarketData()
        self.termStructure = RelinkableYieldTermStructureHandle()
        self.termStructure.linkTo(flatRate(0.05, Actual365Fixed()))
        self.swapIndexBase = EuriborSwapIsdaFixA(
            Period(2, Years), self.termStructure)
        self.shortSwapIndexBase = EuriborSwapIsdaFixA(
            Period(1, Years), self.termStructure)

        self.vegaWeighedSmileFit = false
        self.backup = SavedSettings()


class SwaptionVolatilityCubeTest(unittest.TestCase):

    def testSabrNormalVolatility(self):
        TEST_MESSAGE(
            "Testing sabr normal volatility...")

        vars = CommonVars()

        parametersGuess = QuoteHandleVectorVector()
        for i in range(len(vars.cube.tenors.options) * len(vars.cube.tenors.swaps)):
            tmp = QuoteHandleVector(4)

            tmp[0] = QuoteHandle(SimpleQuote(0.2))
            tmp[1] = QuoteHandle(SimpleQuote(0.5))
            tmp[2] = QuoteHandle(SimpleQuote(0.4))
            tmp[3] = QuoteHandle(SimpleQuote(0.0))
            parametersGuess.append(tmp)

        isParameterFixed = BoolVector(4, false)

        volCube = SwaptionVolCube1(
            vars.normalVolMatrix, vars.cube.tenors.options, vars.cube.tenors.swaps,
            vars.cube.strikeSpreads, vars.cube.volSpreadsHandle,
            vars.swapIndexBase, vars.shortSwapIndexBase, vars.vegaWeighedSmileFit,
            parametersGuess, isParameterFixed, true)
        tolerance = 7.0e-4
        self.makeAtmVolTest(vars, volCube, tolerance)

    def testAtmVols(self):
        TEST_MESSAGE(
            "Testing swaption volatility cube (atm vols)...")

        vars = CommonVars()

        volCube = SwaptionVolCube2(
            vars.atmVolMatrix,
            vars.cube.tenors.options,
            vars.cube.tenors.swaps,
            vars.cube.strikeSpreads,
            vars.cube.volSpreadsHandle,
            vars.swapIndexBase,
            vars.shortSwapIndexBase,
            vars.vegaWeighedSmileFit)

        tolerance = 1.0e-16
        self.makeAtmVolTest(vars, volCube, tolerance)

    def testSmile(self):
        TEST_MESSAGE(
            "Testing swaption volatility cube (smile)...")

        vars = CommonVars()

        volCube = SwaptionVolCube2(
            vars.atmVolMatrix,
            vars.cube.tenors.options,
            vars.cube.tenors.swaps,
            vars.cube.strikeSpreads,
            vars.cube.volSpreadsHandle,
            vars.swapIndexBase,
            vars.shortSwapIndexBase,
            vars.vegaWeighedSmileFit)

        tolerance = 1.0e-16
        self.makeVolSpreadsTest(vars, volCube, tolerance)

    def testSabrVols(self):
        TEST_MESSAGE(
            "Testing swaption volatility cube (sabr interpolation)...")

        vars = CommonVars()

        parametersGuess = QuoteHandleVectorVector(
            len(vars.cube.tenors.options) * len(vars.cube.tenors.swaps))
        for i in range(len(vars.cube.tenors.options) * len(vars.cube.tenors.swaps)):
            tmp = QuoteHandleVector(4)
            tmp[0] = QuoteHandle(SimpleQuote(0.2))
            tmp[1] = QuoteHandle(SimpleQuote(0.5))
            tmp[2] = QuoteHandle(SimpleQuote(0.4))
            tmp[3] = QuoteHandle(SimpleQuote(0.0))
            parametersGuess[i] = tmp

        isParameterFixed = BoolVector(4, false)

        volCube = SwaptionVolCube1(
            vars.atmVolMatrix,
            vars.cube.tenors.options,
            vars.cube.tenors.swaps,
            vars.cube.strikeSpreads,
            vars.cube.volSpreadsHandle,
            vars.swapIndexBase,
            vars.shortSwapIndexBase,
            vars.vegaWeighedSmileFit,
            parametersGuess,
            isParameterFixed,
            true)
        tolerance = 3.0e-4
        self.makeAtmVolTest(vars, volCube, tolerance)

        tolerance = 12.0e-4
        self.makeVolSpreadsTest(vars, volCube, tolerance)

    def testSpreadedCube(self):
        TEST_MESSAGE(
            "Testing spreaded swaption volatility cube...")

        vars = CommonVars()

        parametersGuess = QuoteHandleVectorVector(
            len(vars.cube.tenors.options) * len(vars.cube.tenors.swaps))
        for i in range(len(vars.cube.tenors.options) * len(vars.cube.tenors.swaps)):
            tmp = QuoteHandleVector(4)
            tmp[0] = QuoteHandle(SimpleQuote(0.2))
            tmp[1] = QuoteHandle(SimpleQuote(0.5))
            tmp[2] = QuoteHandle(SimpleQuote(0.4))
            tmp[3] = QuoteHandle(SimpleQuote(0.0))
            parametersGuess[i] = tmp

        isParameterFixed = BoolVector(4, false)

        volCube = SwaptionVolatilityStructureHandle(
            SwaptionVolCube1(
                vars.atmVolMatrix,
                vars.cube.tenors.options,
                vars.cube.tenors.swaps,
                vars.cube.strikeSpreads,
                vars.cube.volSpreadsHandle,
                vars.swapIndexBase,
                vars.shortSwapIndexBase,
                vars.vegaWeighedSmileFit,
                parametersGuess,
                isParameterFixed,
                true))

        spread = SimpleQuote(0.0001)
        spreadHandle = QuoteHandle(spread)
        spreadedVolCube = SpreadedSwaptionVolatility(volCube, spreadHandle)
        strikes = DoubleVector()
        for k in range(1, 100):
            strikes.append(k * .01)
        for i in range(len(vars.cube.tenors.options)):
            for j in range(len(vars.cube.tenors.swaps)):
                smileSectionByCube = volCube.smileSection(
                    vars.cube.tenors.options[i], vars.cube.tenors.swaps[j])
                smileSectionBySpreadedCube = spreadedVolCube.smileSection(
                    vars.cube.tenors.options[i], vars.cube.tenors.swaps[j])
                for strike in strikes:
                    diff = spreadedVolCube.volatility(
                        vars.cube.tenors.options[i],
                        vars.cube.tenors.swaps[j], strike) - \
                           volCube.volatility(
                               vars.cube.tenors.options[i],
                               vars.cube.tenors.swaps[j], strike)
                    self.assertFalse(abs(diff - spread.value()) > 1e-16)

                    diff = smileSectionBySpreadedCube.volatility(strike) - \
                           smileSectionByCube.volatility(strike)
                    self.assertFalse(abs(diff - spread.value()) > 1e-16)

        f = Flag()
        f.registerWith(spreadedVolCube)
        volCube.currentLink().update()
        self.assertFalse(not f.isUp())
        f.lower()
        spread.setValue(.001)
        self.assertFalse(not f.isUp())

    def testObservability(self):
        TEST_MESSAGE(
            "Testing volatility cube observability...")

        vars = CommonVars()

        parametersGuess = QuoteHandleVectorVector(
            len(vars.cube.tenors.options) * len(vars.cube.tenors.swaps))
        for i in range(len(vars.cube.tenors.options) * len(vars.cube.tenors.swaps)):
            tmp = QuoteHandleVector(4)
            tmp[0] = QuoteHandle(SimpleQuote(0.2))
            tmp[1] = QuoteHandle(SimpleQuote(0.5))
            tmp[2] = QuoteHandle(SimpleQuote(0.4))
            tmp[3] = QuoteHandle(SimpleQuote(0.0))
            parametersGuess[i] = tmp

        isParameterFixed = BoolVector(4, false)

        volCube1_0 = SwaptionVolCube1(
            vars.atmVolMatrix,
            vars.cube.tenors.options,
            vars.cube.tenors.swaps,
            vars.cube.strikeSpreads,
            vars.cube.volSpreadsHandle,
            vars.swapIndexBase,
            vars.shortSwapIndexBase,
            vars.vegaWeighedSmileFit,
            parametersGuess,
            isParameterFixed,
            true)

        referenceDate = Settings.instance().evaluationDate
        Settings.instance().evaluationDate = vars.conventions.calendar.advance(
            referenceDate, Period(1, Days), vars.conventions.optionBdc)

        volCube1_1 = SwaptionVolCube1(
            vars.atmVolMatrix,
            vars.cube.tenors.options,
            vars.cube.tenors.swaps,
            vars.cube.strikeSpreads,
            vars.cube.volSpreadsHandle,
            vars.swapIndexBase,
            vars.shortSwapIndexBase,
            vars.vegaWeighedSmileFit,
            parametersGuess,
            isParameterFixed,
            true)
        dummyStrike = 0.03
        for i in range(len(vars.cube.tenors.options)):
            for j in range(len(vars.cube.tenors.swaps)):
                for k in range(len(vars.cube.strikeSpreads)):
                    v0 = volCube1_0.volatility(
                        vars.cube.tenors.options[i], vars.cube.tenors.swaps[j],
                        dummyStrike + vars.cube.strikeSpreads[k], false)
                    v1 = volCube1_1.volatility(
                        vars.cube.tenors.options[i], vars.cube.tenors.swaps[j],
                        dummyStrike + vars.cube.strikeSpreads[k], false)
                    self.assertFalse(abs(v0 - v1) > 1e-14)

        Settings.instance().evaluationDate = referenceDate

        volCube2_0 = SwaptionVolCube2(
            vars.atmVolMatrix,
            vars.cube.tenors.options,
            vars.cube.tenors.swaps,
            vars.cube.strikeSpreads,
            vars.cube.volSpreadsHandle,
            vars.swapIndexBase,
            vars.shortSwapIndexBase,
            vars.vegaWeighedSmileFit)
        Settings.instance().evaluationDate = vars.conventions.calendar.advance(
            referenceDate, Period(1, Days), vars.conventions.optionBdc)

        volCube2_1 = SwaptionVolCube2(
            vars.atmVolMatrix,
            vars.cube.tenors.options,
            vars.cube.tenors.swaps,
            vars.cube.strikeSpreads,
            vars.cube.volSpreadsHandle,
            vars.swapIndexBase,
            vars.shortSwapIndexBase,
            vars.vegaWeighedSmileFit)

        for i in range(len(vars.cube.tenors.options)):
            for j in range(len(vars.cube.tenors.swaps)):
                for k in range(len(vars.cube.strikeSpreads)):
                    v0 = volCube2_0.volatility(
                        vars.cube.tenors.options[i], vars.cube.tenors.swaps[j],
                        dummyStrike + vars.cube.strikeSpreads[k], false)
                    v1 = volCube2_1.volatility(
                        vars.cube.tenors.options[i], vars.cube.tenors.swaps[j],
                        dummyStrike + vars.cube.strikeSpreads[k], false)
                    self.assertFalse(abs(v0 - v1) > 1e-14)

        Settings.instance().evaluationDate = referenceDate

    def testSabrParameters(self):
        TEST_MESSAGE(
            "Testing interpolation of SABR smile sections...")

        vars = CommonVars()

        parametersGuess = QuoteHandleVectorVector(
            len(vars.cube.tenors.options) * len(vars.cube.tenors.swaps))
        for i in range(len(vars.cube.tenors.options) * len(vars.cube.tenors.swaps)):
            tmp = QuoteHandleVector(4)
            tmp[0] = QuoteHandle(SimpleQuote(0.2))
            tmp[1] = QuoteHandle(SimpleQuote(0.5))
            tmp[2] = QuoteHandle(SimpleQuote(0.4))
            tmp[3] = QuoteHandle(SimpleQuote(0.0))
            parametersGuess[i] = tmp

        isParameterFixed = BoolVector(4, false)

        volCube = SwaptionVolCube1(
            vars.atmVolMatrix,
            vars.cube.tenors.options,
            vars.cube.tenors.swaps,
            vars.cube.strikeSpreads,
            vars.cube.volSpreadsHandle,
            vars.swapIndexBase,
            vars.shortSwapIndexBase,
            vars.vegaWeighedSmileFit,
            parametersGuess,
            isParameterFixed,
            true)

        volStructure = volCube
        tolerance = 1.0e-4

        smileSection1 = volStructure.smileSection(Period(10, Years), Period(2, Years))
        smileSection2 = volStructure.smileSection(Period(10, Years), Period(4, Years))
        smileSection3 = volStructure.smileSection(Period(10, Years), Period(3, Years))

        alpha1 = as_sabr_smile_section(smileSection1).alpha()
        alpha2 = as_sabr_smile_section(smileSection2).alpha()
        alpha3 = as_sabr_smile_section(smileSection3).alpha()
        alpha12 = 0.5 * (alpha1 + alpha2)
        self.assertFalse(abs(alpha3 - alpha12) > tolerance)

        beta1 = as_sabr_smile_section(smileSection1).beta()
        beta2 = as_sabr_smile_section(smileSection2).beta()
        beta3 = as_sabr_smile_section(smileSection3).beta()
        beta12 = 0.5 * (beta1 + beta2)
        self.assertFalse(abs(beta3 - beta12) > tolerance)

        rho1 = as_sabr_smile_section(smileSection1).rho()
        rho2 = as_sabr_smile_section(smileSection2).rho()
        rho3 = as_sabr_smile_section(smileSection3).rho()
        rho12 = 0.5 * (rho1 + rho2)
        self.assertFalse(abs(rho3 - rho12) > tolerance)

        nu1 = as_sabr_smile_section(smileSection1).nu()
        nu2 = as_sabr_smile_section(smileSection2).nu()
        nu3 = as_sabr_smile_section(smileSection3).nu()
        nu12 = 0.5 * (nu1 + nu2)
        self.assertFalse(abs(nu3 - nu12) > tolerance)

        forward1 = smileSection1.atmLevel()
        forward2 = smileSection2.atmLevel()
        forward3 = smileSection3.atmLevel()
        forward12 = 0.5 * (forward1 + forward2)
        self.assertFalse(abs(forward3 - forward12) > tolerance)

    def makeAtmVolTest(self,
                       common,
                       volCube,
                       tolerance):

        for option in common.atm.tenors.options:
            for swap in common.atm.tenors.swaps:
                strike = volCube.atmStrike(option, swap)
                d = common.atmVolMatrix.empty()
                expVol = common.atmVolMatrix.volatility(
                    option, swap, strike, true)
                actVol = volCube.volatility(option, swap, strike, true)
                error = abs(expVol - actVol)
                self.assertFalse(error > tolerance)

    def makeVolSpreadsTest(self,
                           common,
                           volCube,
                           tolerance):

        for i in range(len(common.cube.tenors.options)):
            for j in range(len(common.cube.tenors.swaps)):
                for k in range(len(common.cube.strikeSpreads)):
                    atmStrike = volCube.atmStrike(
                        common.cube.tenors.options[i],
                        common.cube.tenors.swaps[j])
                    atmVol = common.atmVolMatrix.volatility(
                        common.cube.tenors.options[i],
                        common.cube.tenors.swaps[j],
                        atmStrike, true)
                    vol = volCube.volatility(
                        common.cube.tenors.options[i],
                        common.cube.tenors.swaps[j],
                        atmStrike + common.cube.strikeSpreads[k], true)
                    spread = vol - atmVol
                    expVolSpread = common.cube.volSpreads[i * len(common.cube.tenors.swaps) + j][k]
                    error = abs(expVolSpread - spread)
                    self.assertFalse(error > tolerance)
