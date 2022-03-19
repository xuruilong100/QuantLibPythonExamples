import unittest
from utilities import *
from QuantLib import *


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
                # // every handle must be reassigned, as the ones created by
                # // default are all linked together.
                tmp[j] = QuoteHandle(
                    SimpleQuote(self.vols[i][j]))
            self.volsHandle[i] = tmp


class CommonVars(object):

    # setup
    def __init__(self):
        self.conventions = SwaptionMarketConventions()
        self.conventions.setConventions()
        self.atm = AtmVolatility()
        self.atm.setMarketData()
        Settings.instance().evaluationDate = self.conventions.calendar.adjust(Date.todaysDate())
        self.atmVolMatrix = RelinkableSwaptionVolatilityStructureHandle(
            SwaptionVolatilityMatrix(self.conventions.calendar,
                                     self.conventions.optionBdc,
                                     self.atm.tenors.options,
                                     self.atm.tenors.swaps,
                                     self.atm.volsHandle,
                                     self.conventions.dayCounter))
        self.termStructure = RelinkableYieldTermStructureHandle()
        self.termStructure.linkTo(
            FlatForward(0, self.conventions.calendar,
                        0.05, Actual365Fixed()))

    # utilities
    # def makeObservabilityTest(self,
    #                           description,
    #                           vol,
    #                           mktDataFloating,
    #                           referenceDateFloating):
    #     dummyStrike = .02
    #     referenceDate = Settings.instance().evaluationDate
    #     initialVol = vol.volatility(
    #         referenceDate + self.atm.tenors.options[0],
    #         self.atm.tenors.swaps[0], dummyStrike, false)
    #     # testing evaluation date change ...
    #     Settings.instance().evaluationDate = referenceDate - Period(1, Years)
    #     newVol = vol.volatility(
    #         referenceDate + self.atm.tenors.options[0],
    #         self.atm.tenors.swaps[0], dummyStrike, false)
    #     Settings.instance().evaluationDate = referenceDate
    #     self.assertFalse(referenceDateFloating and (initialVol == newVol))
    #
    #     self.assertFalse(not referenceDateFloating and (initialVol != newVol))
    #
    #     # test market data change...
    #     if mktDataFloating:
    #         initialVolatility = self.atm.volsHandle[0][0].value()
    #         as_simple_quote(
    #             self.atm.volsHandle[0][0].currentLink()).setValue(10)
    #         newVol = vol.volatility(
    #             referenceDate + self.atm.tenors.options[0],
    #             self.atm.tenors.swaps[0], dummyStrike, false)
    #         # ext.dynamic_pointer_cast<SimpleQuote>(
    #         as_simple_quote(
    #             self.atm.volsHandle[0][0].currentLink()).setValue(initialVolatility)
    #         self.assertFalse(initialVol == newVol)

    # def makeCoherenceTest(self,
    #                       description,
    #                       vol):
    # 
    #     for i in range(self.atm.tenors.options.size()):
    #         optionDate = vol.optionDateFromTenor(self.atm.tenors.options[i])
    #         self.assertFalse(optionDate != vol.optionDates()[i])
    #         optionTime = vol.timeFromReference(optionDate)
    #         self.assertFalse(not close(optionTime, vol.optionTimes()[i]))
    # 
    #     engine = BlackSwaptionEngine(self.termStructure,
    #                                  SwaptionVolatilityStructureHandle(vol))
    # 
    #     for j in range(self.atm.tenors.swaps.size()):
    #         swapLength = vol.swapLength(self.atm.tenors.swaps[j])
    #         self.assertFalse(not close(swapLength, years(self.atm.tenors.swaps[j])))
    # 
    #         swapIndex = EuriborSwapIsdaFixA(self.atm.tenors.swaps[j], self.termStructure)
    # 
    #         for i in range(self.atm.tenors.options.size()):
    #             tolerance = 1.0e-16
    #             expVol = self.atm.vols[i][j]
    # 
    #             actVol = vol.volatility(self.atm.tenors.options[i],
    #                                     self.atm.tenors.swaps[j], 0.05, true)
    #             error = abs(expVol - actVol)
    #             self.assertFalse(error > tolerance)
    # 
    #             optionDate = vol.optionDateFromTenor(self.atm.tenors.options[i])
    #             actVol = vol.volatility(optionDate,
    #                                     self.atm.tenors.swaps[j], 0.05, true)
    #             error = abs(expVol - actVol)
    #             self.assertFalse(error > tolerance)
    # 
    #             optionTime = vol.timeFromReference(optionDate)
    #             actVol = vol.volatility(optionTime, swapLength,
    #                                     0.05, true)
    #             error = abs(expVol - actVol)
    #             self.assertFalse(error > tolerance)
    # 
    #             # ATM swaption
    #             swaption = MakeSwaption(swapIndex, self.atm.tenors.options[i])
    #             swaption.withPricingEngine(engine)
    #             swaption=swaption.makeSwaption()
    # 
    #             exerciseDate = swaption.exercise().dates().front()
    #             self.assertFalse(exerciseDate != vol.optionDates()[i])
    # 
    #             start = swaption.underlyingSwap().startDate()
    #             end = swaption.underlyingSwap().maturityDate()
    #             swapLength2 = vol.swapLength(start, end)
    #             self.assertFalse(not close(swapLength2, swapLength))
    # 
    #             npv = swaption.NPV()
    #             actVol = swaption.impliedVolatility(npv, self.termStructure,
    #                                                 expVol * 0.98, 1e-6,
    #                                                 100, 10.0e-7, 4.0,
    #                                                 ShiftedLognormal, 0.0)
    #             error = abs(expVol - actVol)
    #             tolerance2 = 0.000001
    #             self.assertFalse(error > tolerance2)


class SwaptionVolatilityMatrixTest(unittest.TestCase):

    def testSwaptionVolMatrixCoherence(self):
        TEST_MESSAGE("Testing swaption volatility matrix...")

        vars = CommonVars()

        # vol
        # description

        # floating reference date, floating market data
        description = "floating reference date, floating market data"
        vol = SwaptionVolatilityMatrix(vars.conventions.calendar,
                                       vars.conventions.optionBdc,
                                       vars.atm.tenors.options,
                                       vars.atm.tenors.swaps,
                                       vars.atm.volsHandle,
                                       vars.conventions.dayCounter)
        self.makeCoherenceTest(vars, description, vol)

        # fixed reference date, floating market data
        description = "fixed reference date, floating market data"
        vol = SwaptionVolatilityMatrix(Settings.instance().evaluationDate,
                                       vars.conventions.calendar,
                                       vars.conventions.optionBdc,
                                       vars.atm.tenors.options,
                                       vars.atm.tenors.swaps,
                                       vars.atm.volsHandle,
                                       vars.conventions.dayCounter)
        self.makeCoherenceTest(vars, description, vol)

        # floating reference date, fixed market data
        description = "floating reference date, fixed market data"
        vol = SwaptionVolatilityMatrix(vars.conventions.calendar,
                                       vars.conventions.optionBdc,
                                       vars.atm.tenors.options,
                                       vars.atm.tenors.swaps,
                                       vars.atm.volsHandle,
                                       vars.conventions.dayCounter)
        self.makeCoherenceTest(vars, description, vol)

        # fixed reference date, fixed market data
        description = "fixed reference date, fixed market data"
        vol = SwaptionVolatilityMatrix(Settings.instance().evaluationDate,
                                       vars.conventions.calendar,
                                       vars.conventions.optionBdc,
                                       vars.atm.tenors.options,
                                       vars.atm.tenors.swaps,
                                       vars.atm.volsHandle,
                                       vars.conventions.dayCounter)
        self.makeCoherenceTest(vars, description, vol)

    def testSwaptionVolMatrixObservability(self):
        TEST_MESSAGE("Testing swaption volatility matrix observability...")

        vars = CommonVars()

        # vol
        # description

        # floating reference date, floating market data
        description = "floating reference date, floating market data"
        vol = SwaptionVolatilityMatrix(vars.conventions.calendar,
                                       vars.conventions.optionBdc,
                                       vars.atm.tenors.options,
                                       vars.atm.tenors.swaps,
                                       vars.atm.volsHandle,
                                       vars.conventions.dayCounter)
        self.makeObservabilityTest(vars, description, vol, true, true)

        # fixed reference date, floating market data
        description = "fixed reference date, floating market data"
        vol = SwaptionVolatilityMatrix(Settings.instance().evaluationDate,
                                       vars.conventions.calendar,
                                       vars.conventions.optionBdc,
                                       vars.atm.tenors.options,
                                       vars.atm.tenors.swaps,
                                       vars.atm.volsHandle,
                                       vars.conventions.dayCounter)
        self.makeObservabilityTest(vars, description, vol, true, false)

        # floating reference date, fixed market data
        description = "floating reference date, fixed market data"
        vol = SwaptionVolatilityMatrix(vars.conventions.calendar,
                                       vars.conventions.optionBdc,
                                       vars.atm.tenors.options,
                                       vars.atm.tenors.swaps,
                                       vars.atm.volsHandle,
                                       vars.conventions.dayCounter)
        self.makeObservabilityTest(vars, description, vol, false, true)

        # fixed reference date, fixed market data
        description = "fixed reference date, fixed market data"
        vol = SwaptionVolatilityMatrix(Settings.instance().evaluationDate,
                                       vars.conventions.calendar,
                                       vars.conventions.optionBdc,
                                       vars.atm.tenors.options,
                                       vars.atm.tenors.swaps,
                                       vars.atm.volsHandle,
                                       vars.conventions.dayCounter)
        self.makeObservabilityTest(vars, description, vol, false, false)

        # fixed reference date and fixed market data, option dates
        # SwaptionVolatilityMatrix(referenceDate,
        #                         exerciseDates,
        #                         swapTenors,
        #                         Matrix& volatilities,
        #                         dayCounter)

    def makeCoherenceTest(self,
                          common,
                          description,
                          vol):

        for i in range(common.atm.tenors.options.size()):
            optionDate = vol.optionDateFromTenor(common.atm.tenors.options[i])
            self.assertFalse(optionDate != vol.optionDates()[i])
            optionTime = vol.timeFromReference(optionDate)
            self.assertFalse(not close(optionTime, vol.optionTimes()[i]))

        engine = BlackSwaptionEngine(common.termStructure,
                                     SwaptionVolatilityStructureHandle(vol))

        for j in range(common.atm.tenors.swaps.size()):
            swapLength = vol.swapLength(common.atm.tenors.swaps[j])
            self.assertFalse(not close(swapLength, years(common.atm.tenors.swaps[j])))

            swapIndex = EuriborSwapIsdaFixA(common.atm.tenors.swaps[j], common.termStructure)

            for i in range(common.atm.tenors.options.size()):
                tolerance = 1.0e-16
                expVol = common.atm.vols[i][j]

                actVol = vol.volatility(common.atm.tenors.options[i],
                                        common.atm.tenors.swaps[j], 0.05, true)
                error = abs(expVol - actVol)
                self.assertFalse(error > tolerance)

                optionDate = vol.optionDateFromTenor(common.atm.tenors.options[i])
                actVol = vol.volatility(optionDate,
                                        common.atm.tenors.swaps[j], 0.05, true)
                error = abs(expVol - actVol)
                self.assertFalse(error > tolerance)

                optionTime = vol.timeFromReference(optionDate)
                actVol = vol.volatility(optionTime, swapLength,
                                        0.05, true)
                error = abs(expVol - actVol)
                self.assertFalse(error > tolerance)

                # ATM swaption
                swaption = MakeSwaption(swapIndex, common.atm.tenors.options[i])
                swaption.withPricingEngine(engine)
                swaption = swaption.makeSwaption()

                exerciseDate = swaption.exercise().dates()[0]
                self.assertFalse(exerciseDate != vol.optionDates()[i])

                start = swaption.underlyingSwap().startDate()
                end = swaption.underlyingSwap().maturityDate()
                swapLength2 = vol.swapLength(start, end)
                self.assertFalse(not close(swapLength2, swapLength))

                npv = swaption.NPV()
                actVol = swaption.impliedVolatility(npv, common.termStructure,
                                                    expVol * 0.98, 1e-6,
                                                    100, 10.0e-7, 4.0,
                                                    ShiftedLognormal, 0.0)
                error = abs(expVol - actVol)
                tolerance2 = 0.000001
                self.assertFalse(error > tolerance2)

    def makeObservabilityTest(self,
                              common,
                              description,
                              vol,
                              mktDataFloating,
                              referenceDateFloating):
        dummyStrike = .02
        referenceDate = Settings.instance().evaluationDate
        initialVol = vol.volatility(
            referenceDate + common.atm.tenors.options[0],
            common.atm.tenors.swaps[0], dummyStrike, false)
        # testing evaluation date change ...
        Settings.instance().evaluationDate = referenceDate - Period(1, Years)
        newVol = vol.volatility(
            referenceDate + common.atm.tenors.options[0],
            common.atm.tenors.swaps[0], dummyStrike, false)
        Settings.instance().evaluationDate = referenceDate
        self.assertFalse(referenceDateFloating and (initialVol == newVol))

        self.assertFalse(not referenceDateFloating and (initialVol != newVol))

        # test market data change...
        if mktDataFloating:
            initialVolatility = common.atm.volsHandle[0][0].value()
            as_simple_quote(
                common.atm.volsHandle[0][0].currentLink()).setValue(10)
            newVol = vol.volatility(
                referenceDate + common.atm.tenors.options[0],
                common.atm.tenors.swaps[0], dummyStrike, false)
            # ext.dynamic_pointer_cast<SimpleQuote>(
            as_simple_quote(
                common.atm.volsHandle[0][0].currentLink()).setValue(initialVolatility)
            self.assertFalse(initialVol == newVol)
