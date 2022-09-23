import unittest
from math import sqrt, log

from QuantLib import *

from utilities import *


class CommonVars(object):

    def __init__(self):
        self.fixingDays = 2
        self.nominal = 1000000.0
        self.termStructure = RelinkableYieldTermStructureHandle()
        self.index = Euribor6M(self.termStructure)
        self.calendar = self.index.fixingCalendar()
        self.today = self.calendar.adjust(Settings.instance().evaluationDate)
        Settings.instance().evaluationDate = self.today
        self.settlement = self.calendar.advance(self.today, self.fixingDays, Days)
        self.termStructure.linkTo(flatRate(self.settlement, 0.05, Actual365Fixed()))
        self.optionTolerance = 1.e-04
        self.blackTolerance = 1e-10
        self.backup = SavedSettings()


class DigitalCouponTest(unittest.TestCase):

    def testAssetOrNothing(self):
        TEST_MESSAGE(
            "Testing European asset-or-nothing digital coupon...")

        vars = CommonVars()

        vols = [0.05, 0.15, 0.30]
        strikes = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07]
        gearings = [1.0, 2.8]
        spreads = [0.0, 0.005]

        gap = 1e-7

        replication = DigitalReplication(Replication.Central, gap)
        for capletVol in vols:
            volH = RelinkableOptionletVolatilityStructureHandle()
            volH.linkTo(ConstantOptionletVolatility(
                vars.today, vars.calendar, Following, capletVol, Actual360()))
            for strike in strikes:
                for k in range(9, 10):
                    startDate = vars.calendar.advance(
                        vars.settlement, Period(k + 1, Years))
                    endDate = vars.calendar.advance(
                        vars.settlement, Period(k + 2, Years))
                    nullstrike = NullReal()
                    paymentDate = endDate
                    for h in range(len(gearings)):

                        gearing = gearings[h]
                        spread = spreads[h]

                        underlying = IborCoupon(
                            paymentDate, vars.nominal,
                            startDate, endDate,
                            vars.fixingDays, vars.index,
                            gearing, spread)

                        digitalCappedCoupon = DigitalCoupon(
                            underlying, strike, Position.Short, false, nullstrike,
                            nullstrike, Position.Short, false, nullstrike, replication)
                        pricer = BlackIborCouponPricer(volH)
                        digitalCappedCoupon.setPricer(pricer)

                        accrualPeriod = underlying.accrualPeriod()
                        discount = vars.termStructure.discount(endDate)
                        exerciseDate = underlying.fixingDate()
                        forward = underlying.rate()
                        effFwd = (forward - spread) / gearing
                        effStrike = (strike - spread) / gearing
                        stdDev = sqrt(volH.blackVariance(exerciseDate, effStrike))
                        phi = CumulativeNormalDistribution()
                        d1 = log(effFwd / effStrike) / stdDev + 0.5 * stdDev
                        d2 = d1 - stdDev
                        N_d1 = phi(d1)
                        N_d2 = phi(d2)
                        nd1Price = (gearing * effFwd * N_d1 + spread * N_d2) * \
                                   vars.nominal * accrualPeriod * discount
                        optionPrice = digitalCappedCoupon.callOptionRate() * \
                                      vars.nominal * accrualPeriod * discount
                        error = abs(nd1Price - optionPrice)
                        self.assertFalse(error > vars.optionTolerance)

                        if spread == 0.0:
                            exercise = EuropeanExercise(exerciseDate)
                            discountAtFixing = vars.termStructure.discount(exerciseDate)

                            fwd = SimpleQuote(effFwd * discountAtFixing)
                            qRate = SimpleQuote(0.0)

                            qTS = flatRate(vars.today, qRate, Actual360())
                            vol = SimpleQuote(0.0)
                            volTS = flatVol(vars.today, capletVol, Actual360())

                            callPayoff = AssetOrNothingPayoff(Option.Call, effStrike)
                            stochProcess = BlackScholesMertonProcess(
                                QuoteHandle(fwd),
                                YieldTermStructureHandle(qTS),
                                vars.termStructure,
                                BlackVolTermStructureHandle(volTS))

                            engine = AnalyticEuropeanEngine(stochProcess)
                            callOpt = VanillaOption(callPayoff, exercise)
                            callOpt.setPricingEngine(engine)
                            callVO = vars.nominal * gearing * accrualPeriod * callOpt.NPV() * \
                                     discount / discountAtFixing * forward / effFwd
                            error = abs(nd1Price - callVO)
                            self.assertFalse(error > vars.blackTolerance)

                        digitalFlooredCoupon = DigitalCoupon(
                            underlying,
                            nullstrike, Position.Long, false, nullstrike,
                            strike, Position.Long, false, nullstrike,
                            replication)
                        digitalFlooredCoupon.setPricer(pricer)

                        N_d1 = phi(-d1)
                        N_d2 = phi(-d2)
                        nd1Price = (gearing * effFwd * N_d1 + spread * N_d2) * \
                                   vars.nominal * accrualPeriod * discount
                        optionPrice = digitalFlooredCoupon.putOptionRate() * \
                                      vars.nominal * accrualPeriod * discount
                        error = abs(nd1Price - optionPrice)
                        self.assertFalse(error > vars.optionTolerance)

                        if spread == 0.0:
                            exercise = EuropeanExercise(exerciseDate)
                            discountAtFixing = vars.termStructure.discount(exerciseDate)

                            fwd = SimpleQuote(effFwd * discountAtFixing)
                            qRate = SimpleQuote(0.0)

                            qTS = flatRate(vars.today, qRate, Actual360())
                            vol = SimpleQuote(0.0)

                            volTS = flatVol(vars.today, capletVol, Actual360())
                            stochProcess = BlackScholesMertonProcess(
                                QuoteHandle(fwd),
                                YieldTermStructureHandle(qTS),
                                vars.termStructure,
                                BlackVolTermStructureHandle(volTS))

                            putPayoff = AssetOrNothingPayoff(Option.Put, effStrike)
                            engine = AnalyticEuropeanEngine(stochProcess)
                            putOpt = VanillaOption(putPayoff, exercise)
                            putOpt.setPricingEngine(engine)
                            putVO = vars.nominal * gearing * accrualPeriod * putOpt.NPV() * \
                                    discount / discountAtFixing * forward / effFwd
                            error = abs(nd1Price - putVO)
                            self.assertFalse(error > vars.blackTolerance)

    def testAssetOrNothingDeepInTheMoney(self):
        TEST_MESSAGE(
            "Testing European deep in-the-money asset-or-nothing "
            "digital coupon...")

        vars = CommonVars()

        gearing = 1.0
        spread = 0.0

        capletVolatility = 0.0001
        volatility = RelinkableOptionletVolatilityStructureHandle()
        volatility.linkTo(
            ConstantOptionletVolatility(
                vars.today, vars.calendar, Following,
                capletVolatility, Actual360()))
        gap = 1e-4
        replication = DigitalReplication(Replication.Central, gap)

        for k in range(10):
            startDate = vars.calendar.advance(vars.settlement, Period(k + 1, Years))
            endDate = vars.calendar.advance(vars.settlement, Period(k + 2, Years))
            nullstrike = NullReal()
            paymentDate = endDate

            underlying = IborCoupon(
                paymentDate, vars.nominal,
                startDate, endDate,
                vars.fixingDays, vars.index,
                gearing, spread)

            strike = 0.001
            digitalCappedCoupon = DigitalCoupon(
                underlying, strike, Position.Short, false, nullstrike,
                nullstrike, Position.Short, false, nullstrike, replication)
            pricer = BlackIborCouponPricer(volatility)
            digitalCappedCoupon.setPricer(pricer)

            accrualPeriod = underlying.accrualPeriod()
            discount = vars.termStructure.discount(endDate)

            targetOptionPrice = underlying.price(vars.termStructure)
            targetPrice = 0.0
            digitalPrice = digitalCappedCoupon.price(vars.termStructure)
            error = abs(targetPrice - digitalPrice)
            tolerance = 1e-08
            self.assertFalse(error > tolerance)

            replicationOptionPrice = digitalCappedCoupon.callOptionRate() * \
                                     vars.nominal * accrualPeriod * discount
            error = abs(targetOptionPrice - replicationOptionPrice)
            optionTolerance = 1e-08
            self.assertFalse(error > optionTolerance)

            strike = 0.99
            digitalFlooredCoupon = DigitalCoupon(
                underlying, nullstrike, Position.Long, false, nullstrike,
                strike, Position.Long, false, nullstrike, replication)
            digitalFlooredCoupon.setPricer(pricer)

            targetOptionPrice = underlying.price(vars.termStructure)
            targetPrice = underlying.price(vars.termStructure) + targetOptionPrice
            digitalPrice = digitalFlooredCoupon.price(vars.termStructure)
            error = abs(targetPrice - digitalPrice)
            tolerance = 2.5e-06
            self.assertFalse(error > tolerance)

            replicationOptionPrice = digitalFlooredCoupon.putOptionRate() * \
                                     vars.nominal * accrualPeriod * discount
            error = abs(targetOptionPrice - replicationOptionPrice)
            optionTolerance = 2.5e-06
            self.assertFalse(error > optionTolerance)

    def testAssetOrNothingDeepOutTheMoney(self):
        TEST_MESSAGE(
            "Testing European deep out-the-money asset-or-nothing "
            "digital coupon...")

        vars = CommonVars()

        gearing = 1.0
        spread = 0.0

        capletVolatility = 0.0001
        volatility = RelinkableOptionletVolatilityStructureHandle()
        volatility.linkTo(
            ConstantOptionletVolatility(
                vars.today, vars.calendar, Following,
                capletVolatility, Actual360()))
        gap = 1e-4
        replication = DigitalReplication(Replication.Central, gap)

        for k in range(10):
            startDate = vars.calendar.advance(vars.settlement, Period(k + 1, Years))
            endDate = vars.calendar.advance(vars.settlement, Period(k + 2, Years))
            nullstrike = NullReal()
            paymentDate = endDate

            underlying = IborCoupon(
                paymentDate, vars.nominal,
                startDate, endDate,
                vars.fixingDays, vars.index,
                gearing, spread)

            strike = 0.99
            digitalCappedCoupon = DigitalCoupon(
                underlying,
                strike, Position.Short, false, nullstrike,
                nullstrike, Position.Long, false, nullstrike,
                replication)
            pricer = BlackIborCouponPricer(volatility)
            digitalCappedCoupon.setPricer(pricer)

            accrualPeriod = underlying.accrualPeriod()
            discount = vars.termStructure.discount(endDate)

            targetPrice = underlying.price(vars.termStructure)
            digitalPrice = digitalCappedCoupon.price(vars.termStructure)
            error = abs(targetPrice - digitalPrice)
            tolerance = 1e-10
            self.assertFalse(error > tolerance)

            targetOptionPrice = 0.
            replicationOptionPrice = digitalCappedCoupon.callOptionRate() * vars.nominal * accrualPeriod * discount
            error = abs(targetOptionPrice - replicationOptionPrice)
            optionTolerance = 1e-08
            self.assertFalse(error > optionTolerance)

            strike = 0.01
            digitalFlooredCoupon = DigitalCoupon(
                underlying,
                nullstrike, Position.Long, false, nullstrike,
                strike, Position.Long, false, nullstrike,
                replication)
            digitalFlooredCoupon.setPricer(pricer)

            targetPrice = underlying.price(vars.termStructure)
            digitalPrice = digitalFlooredCoupon.price(vars.termStructure)
            tolerance = 1e-08
            error = abs(targetPrice - digitalPrice)
            self.assertFalse(error > tolerance)

            targetOptionPrice = 0.0
            replicationOptionPrice = digitalFlooredCoupon.putOptionRate() * \
                                     vars.nominal * accrualPeriod * discount
            error = abs(targetOptionPrice - replicationOptionPrice)
            self.assertFalse(error > optionTolerance)

    def testCashOrNothing(self):
        TEST_MESSAGE(
            "Testing European cash-or-nothing digital coupon...")

        vars = CommonVars()

        vols = [0.05, 0.15, 0.30]
        strikes = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07]

        gearing = 3.0
        spread = -0.0002

        gap = 1e-08

        replication = DigitalReplication(Replication.Central, gap)

        for capletVol in vols:
            volH = RelinkableOptionletVolatilityStructureHandle()
            volH.linkTo(ConstantOptionletVolatility(
                vars.today, vars.calendar, Following, capletVol, Actual360()))
            for strike in strikes:
                for k in range(10):
                    startDate = vars.calendar.advance(vars.settlement, Period(k + 1, Years))
                    endDate = vars.calendar.advance(vars.settlement, Period(k + 2, Years))
                    nullstrike = NullReal()
                    cashRate = 0.01

                    paymentDate = endDate
                    underlying = IborCoupon(
                        paymentDate, vars.nominal,
                        startDate, endDate,
                        vars.fixingDays, vars.index,
                        gearing, spread)

                    digitalCappedCoupon = DigitalCoupon(
                        underlying, strike, Position.Short, false, cashRate,
                        nullstrike, Position.Short, false, nullstrike, replication)
                    pricer = BlackIborCouponPricer(volH)
                    digitalCappedCoupon.setPricer(pricer)

                    exerciseDate = underlying.fixingDate()
                    forward = underlying.rate()
                    effFwd = (forward - spread) / gearing
                    effStrike = (strike - spread) / gearing
                    accrualPeriod = underlying.accrualPeriod()
                    discount = vars.termStructure.discount(endDate)
                    stdDev = sqrt(volH.blackVariance(exerciseDate, effStrike))
                    ITM = blackFormulaCashItmProbability(
                        Option.Call, effStrike, effFwd, stdDev)
                    nd2Price = ITM * vars.nominal * accrualPeriod * discount * cashRate
                    optionPrice = digitalCappedCoupon.callOptionRate() * \
                                  vars.nominal * accrualPeriod * discount
                    error = abs(nd2Price - optionPrice)
                    self.assertFalse(error > vars.optionTolerance)

                    exercise = EuropeanExercise(exerciseDate)
                    discountAtFixing = vars.termStructure.discount(exerciseDate)
                    fwd = SimpleQuote(effFwd * discountAtFixing)
                    qRate = SimpleQuote(0.0)
                    qTS = flatRate(vars.today, qRate, Actual360())
                    vol = SimpleQuote(0.0)
                    volTS = flatVol(
                        vars.today, capletVol, Actual360())
                    callPayoff = CashOrNothingPayoff(
                        Option.Call, effStrike, cashRate)
                    stochProcess = BlackScholesMertonProcess(
                        QuoteHandle(fwd),
                        YieldTermStructureHandle(qTS),
                        vars.termStructure,
                        BlackVolTermStructureHandle(volTS))
                    engine = AnalyticEuropeanEngine(stochProcess)
                    callOpt = VanillaOption(callPayoff, exercise)
                    callOpt.setPricingEngine(engine)
                    callVO = vars.nominal * accrualPeriod * \
                             callOpt.NPV() * discount / discountAtFixing
                    error = abs(nd2Price - callVO)
                    self.assertFalse(error > vars.blackTolerance)

                    digitalFlooredCoupon = DigitalCoupon(
                        underlying, nullstrike, Position.Long, false, nullstrike,
                        strike, Position.Long, false, cashRate, replication)
                    digitalFlooredCoupon.setPricer(pricer)

                    ITM = blackFormulaCashItmProbability(
                        Option.Put, effStrike, effFwd, stdDev)
                    nd2Price = ITM * vars.nominal * accrualPeriod * discount * cashRate
                    optionPrice = digitalFlooredCoupon.putOptionRate() * \
                                  vars.nominal * accrualPeriod * discount
                    error = abs(nd2Price - optionPrice)
                    self.assertFalse(error > vars.optionTolerance)

                    putPayoff = CashOrNothingPayoff(Option.Put, effStrike, cashRate)
                    putOpt = VanillaOption(putPayoff, exercise)
                    putOpt.setPricingEngine(engine)
                    putVO = vars.nominal * accrualPeriod * putOpt.NPV() * discount / discountAtFixing
                    error = abs(nd2Price - putVO)
                    self.assertFalse(error > vars.blackTolerance)

    def testCashOrNothingDeepInTheMoney(self):
        TEST_MESSAGE(
            "Testing European deep in-the-money cash-or-nothing digital coupon...")

        vars = CommonVars()

        gearing = 1.0
        spread = 0.0

        capletVolatility = 0.0001
        volatility = RelinkableOptionletVolatilityStructureHandle()
        volatility.linkTo(
            ConstantOptionletVolatility(
                vars.today, vars.calendar, Following,
                capletVolatility, Actual360()))

        for k in range(10):
            startDate = vars.calendar.advance(vars.settlement, Period(k + 1, Years))
            endDate = vars.calendar.advance(vars.settlement, Period(k + 2, Years))
            nullstrike = NullReal()
            cashRate = 0.01
            gap = 1e-4
            replication = DigitalReplication(Replication.Central, gap)
            paymentDate = endDate

            underlying = IborCoupon(
                paymentDate, vars.nominal,
                startDate, endDate,
                vars.fixingDays, vars.index,
                gearing, spread)

            strike = 0.001
            digitalCappedCoupon = DigitalCoupon(
                underlying, strike, Position.Short, false, cashRate,
                nullstrike, Position.Short, false, nullstrike, replication)
            pricer = BlackIborCouponPricer(volatility)
            digitalCappedCoupon.setPricer(pricer)

            accrualPeriod = underlying.accrualPeriod()
            discount = vars.termStructure.discount(endDate)

            targetOptionPrice = cashRate * vars.nominal * accrualPeriod * discount
            targetPrice = underlying.price(vars.termStructure) - targetOptionPrice
            digitalPrice = digitalCappedCoupon.price(vars.termStructure)

            error = abs(targetPrice - digitalPrice)
            tolerance = 1e-07
            self.assertFalse(error > tolerance)

            replicationOptionPrice = digitalCappedCoupon.callOptionRate() * \
                                     vars.nominal * accrualPeriod * discount
            error = abs(targetOptionPrice - replicationOptionPrice)
            optionTolerance = 1e-07
            self.assertFalse(error > optionTolerance)

            strike = 0.99
            digitalFlooredCoupon = DigitalCoupon(
                underlying, nullstrike, Position.Long, false, nullstrike,
                strike, Position.Long, false, cashRate, replication)
            digitalFlooredCoupon.setPricer(pricer)

            targetPrice = underlying.price(vars.termStructure) + targetOptionPrice
            digitalPrice = digitalFlooredCoupon.price(vars.termStructure)
            error = abs(targetPrice - digitalPrice)
            self.assertFalse(error > tolerance)

            replicationOptionPrice = digitalFlooredCoupon.putOptionRate() * \
                                     vars.nominal * accrualPeriod * discount
            error = abs(targetOptionPrice - replicationOptionPrice)
            self.assertFalse(error > optionTolerance)

    def testCashOrNothingDeepOutTheMoney(self):
        TEST_MESSAGE(
            "Testing European deep out-the-money cash-or-nothing "
            "digital coupon...")

        vars = CommonVars()

        gearing = 1.0
        spread = 0.0

        capletVolatility = 0.0001
        volatility = RelinkableOptionletVolatilityStructureHandle()
        volatility.linkTo(
            ConstantOptionletVolatility(
                vars.today, vars.calendar, Following,
                capletVolatility, Actual360()))

        for k in range(10):
            startDate = vars.calendar.advance(vars.settlement, Period(k + 1, Years))
            endDate = vars.calendar.advance(vars.settlement, Period(k + 2, Years))
            nullstrike = NullReal()
            cashRate = 0.01
            gap = 1e-4
            replication = DigitalReplication(Replication.Central, gap)
            paymentDate = endDate

            underlying = IborCoupon(
                paymentDate, vars.nominal,
                startDate, endDate,
                vars.fixingDays, vars.index,
                gearing, spread)

            strike = 0.99
            digitalCappedCoupon = DigitalCoupon(
                underlying, strike, Position.Short, false, cashRate,
                nullstrike, Position.Short, false, nullstrike, replication)

            pricer = BlackIborCouponPricer(volatility)
            digitalCappedCoupon.setPricer(pricer)

            accrualPeriod = underlying.accrualPeriod()
            discount = vars.termStructure.discount(endDate)

            targetPrice = underlying.price(vars.termStructure)
            digitalPrice = digitalCappedCoupon.price(vars.termStructure)
            error = abs(targetPrice - digitalPrice)
            tolerance = 1e-10
            self.assertFalse(error > tolerance)

            targetOptionPrice = 0.
            replicationOptionPrice = digitalCappedCoupon.callOptionRate() * \
                                     vars.nominal * accrualPeriod * discount
            error = abs(targetOptionPrice - replicationOptionPrice)
            optionTolerance = 1e-10
            self.assertFalse(error > optionTolerance)

            strike = 0.01
            digitalFlooredCoupon = DigitalCoupon(
                underlying, nullstrike, Position.Long, false, nullstrike,
                strike, Position.Long, false, cashRate, replication)
            digitalFlooredCoupon.setPricer(pricer)

            targetPrice = underlying.price(vars.termStructure)
            digitalPrice = digitalFlooredCoupon.price(vars.termStructure)
            tolerance = 1e-09
            error = abs(targetPrice - digitalPrice)
            self.assertFalse(error > tolerance)

            targetOptionPrice = 0.0
            replicationOptionPrice = digitalFlooredCoupon.putOptionRate() * \
                                     vars.nominal * accrualPeriod * discount
            error = abs(targetOptionPrice - replicationOptionPrice)
            self.assertFalse(error > optionTolerance)

    def testCallPutParity(self):
        TEST_MESSAGE(
            "Testing call/put parity for European digital coupon...")

        vars = CommonVars()

        vols = [0.05, 0.15, 0.30]
        strikes = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07]

        gearing = 1.0
        spread = 0.0

        gap = 1e-04
        replication = DigitalReplication(Replication.Central, gap)

        for capletVolatility in vols:
            volatility = RelinkableOptionletVolatilityStructureHandle()
            volatility.linkTo(
                ConstantOptionletVolatility(
                    vars.today, vars.calendar, Following, capletVolatility, Actual360()))
            for strike in strikes:
                for k in range(10):
                    startDate = vars.calendar.advance(vars.settlement, Period(k + 1, Years))
                    endDate = vars.calendar.advance(vars.settlement, Period(k + 2, Years))
                    nullstrike = NullReal()

                    paymentDate = endDate

                    underlying = IborCoupon(
                        paymentDate, vars.nominal,
                        startDate, endDate,
                        vars.fixingDays, vars.index,
                        gearing, spread)

                    cashRate = 0.01

                    cash_digitalCallCoupon = DigitalCoupon(
                        underlying, strike, Position.Long, false, cashRate,
                        nullstrike, Position.Long, false, nullstrike, replication)
                    pricer = BlackIborCouponPricer(volatility)
                    cash_digitalCallCoupon.setPricer(pricer)

                    cash_digitalPutCoupon = DigitalCoupon(
                        underlying, nullstrike, Position.Long, false, nullstrike,
                        strike, Position.Short, false, cashRate, replication)

                    cash_digitalPutCoupon.setPricer(pricer)
                    digitalPrice = cash_digitalCallCoupon.price(vars.termStructure) - \
                                   cash_digitalPutCoupon.price(vars.termStructure)

                    accrualPeriod = underlying.accrualPeriod()
                    discount = vars.termStructure.discount(endDate)
                    targetPrice = vars.nominal * accrualPeriod * discount * cashRate

                    error = abs(targetPrice - digitalPrice)
                    tolerance = 1.e-08
                    self.assertFalse(error > tolerance)

                    asset_digitalCallCoupon = DigitalCoupon(
                        underlying, strike, Position.Long, false, nullstrike,
                        nullstrike, Position.Long, false, nullstrike, replication)
                    asset_digitalCallCoupon.setPricer(pricer)

                    asset_digitalPutCoupon = DigitalCoupon(
                        underlying, nullstrike, Position.Long, false, nullstrike,
                        strike, Position.Short, false, nullstrike, replication)
                    asset_digitalPutCoupon.setPricer(pricer)
                    digitalPrice = asset_digitalCallCoupon.price(vars.termStructure) - \
                                   asset_digitalPutCoupon.price(vars.termStructure)

                    targetPrice = vars.nominal * accrualPeriod * discount * underlying.rate()
                    error = abs(targetPrice - digitalPrice)
                    tolerance = 1.e-07
                    self.assertFalse(error > tolerance)

    def testReplicationType(self):
        TEST_MESSAGE(
            "Testing replication type for European digital coupon...")

        vars = CommonVars()

        vols = [0.05, 0.15, 0.30]
        strikes = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07]

        gearing = 1.0
        spread = 0.0

        gap = 1e-04
        subReplication = DigitalReplication(Replication.Sub, gap)
        centralReplication = DigitalReplication(Replication.Central, gap)
        superReplication = DigitalReplication(Replication.Super, gap)

        for capletVolatility in vols:
            volatility = RelinkableOptionletVolatilityStructureHandle()
            volatility.linkTo(
                ConstantOptionletVolatility(
                    vars.today, vars.calendar, Following,
                    capletVolatility, Actual360()))
            for strike in strikes:
                for k in range(10):
                    startDate = vars.calendar.advance(vars.settlement, Period(k + 1, Years))
                    endDate = vars.calendar.advance(vars.settlement, Period(k + 2, Years))
                    nullstrike = NullReal()

                    paymentDate = endDate

                    underlying = IborCoupon(
                        paymentDate, vars.nominal,
                        startDate, endDate,
                        vars.fixingDays, vars.index,
                        gearing, spread)

                    cashRate = 0.005

                    sub_cash_longDigitalCallCoupon = DigitalCoupon(
                        underlying, strike, Position.Long, false, cashRate,
                        nullstrike, Position.Long, false, nullstrike, subReplication)
                    central_cash_longDigitalCallCoupon = DigitalCoupon(
                        underlying, strike, Position.Long, false, cashRate,
                        nullstrike, Position.Long, false, nullstrike, centralReplication)
                    over_cash_longDigitalCallCoupon = DigitalCoupon(
                        underlying, strike, Position.Long, false, cashRate,
                        nullstrike, Position.Long, false, nullstrike, superReplication)
                    pricer = BlackIborCouponPricer(volatility)
                    sub_cash_longDigitalCallCoupon.setPricer(pricer)
                    central_cash_longDigitalCallCoupon.setPricer(pricer)
                    over_cash_longDigitalCallCoupon.setPricer(pricer)
                    sub_digitalPrice = sub_cash_longDigitalCallCoupon.price(vars.termStructure)
                    central_digitalPrice = central_cash_longDigitalCallCoupon.price(vars.termStructure)
                    over_digitalPrice = over_cash_longDigitalCallCoupon.price(vars.termStructure)
                    tolerance = 1.e-09
                    self.assertFalse(
                        ((sub_digitalPrice > central_digitalPrice) and
                         abs(central_digitalPrice - sub_digitalPrice) > tolerance) or
                        ((central_digitalPrice > over_digitalPrice) and
                         abs(central_digitalPrice - over_digitalPrice) > tolerance))

                    sub_cash_shortDigitalCallCoupon = DigitalCoupon(
                        underlying, strike, Position.Short, false, cashRate,
                        nullstrike, Position.Long, false, nullstrike, subReplication)
                    central_cash_shortDigitalCallCoupon = DigitalCoupon(
                        underlying, strike, Position.Short, false, cashRate,
                        nullstrike, Position.Long, false, nullstrike, centralReplication)
                    over_cash_shortDigitalCallCoupon = DigitalCoupon(
                        underlying, strike, Position.Short, false, cashRate,
                        nullstrike, Position.Long, false, nullstrike, superReplication)
                    sub_cash_shortDigitalCallCoupon.setPricer(pricer)
                    central_cash_shortDigitalCallCoupon.setPricer(pricer)
                    over_cash_shortDigitalCallCoupon.setPricer(pricer)
                    sub_digitalPrice = sub_cash_shortDigitalCallCoupon.price(vars.termStructure)
                    central_digitalPrice = central_cash_shortDigitalCallCoupon.price(vars.termStructure)
                    over_digitalPrice = over_cash_shortDigitalCallCoupon.price(vars.termStructure)
                    self.assertFalse(
                        ((sub_digitalPrice > central_digitalPrice) and
                         abs(central_digitalPrice - sub_digitalPrice) > tolerance) or
                        ((central_digitalPrice > over_digitalPrice) and
                         abs(central_digitalPrice - over_digitalPrice) > tolerance))

                    sub_cash_longDigitalPutCoupon = DigitalCoupon(
                        underlying, nullstrike, Position.Long, false, nullstrike,
                        strike, Position.Long, false, cashRate, subReplication)
                    central_cash_longDigitalPutCoupon = DigitalCoupon(
                        underlying, nullstrike, Position.Long, false, nullstrike,
                        strike, Position.Long, false, cashRate, centralReplication)
                    over_cash_longDigitalPutCoupon = DigitalCoupon(
                        underlying, nullstrike, Position.Long, false, nullstrike,
                        strike, Position.Long, false, cashRate, superReplication)
                    sub_cash_longDigitalPutCoupon.setPricer(pricer)
                    central_cash_longDigitalPutCoupon.setPricer(pricer)
                    over_cash_longDigitalPutCoupon.setPricer(pricer)
                    sub_digitalPrice = sub_cash_longDigitalPutCoupon.price(vars.termStructure)
                    central_digitalPrice = central_cash_longDigitalPutCoupon.price(vars.termStructure)
                    over_digitalPrice = over_cash_longDigitalPutCoupon.price(vars.termStructure)
                    self.assertFalse(
                        ((sub_digitalPrice > central_digitalPrice) and
                         abs(central_digitalPrice - sub_digitalPrice) > tolerance) or
                        ((central_digitalPrice > over_digitalPrice) and
                         abs(central_digitalPrice - over_digitalPrice) > tolerance))

                    sub_cash_shortDigitalPutCoupon = DigitalCoupon(
                        underlying, nullstrike, Position.Long, false, nullstrike,
                        strike, Position.Short, false, cashRate, subReplication)
                    central_cash_shortDigitalPutCoupon = DigitalCoupon(
                        underlying, nullstrike, Position.Long, false, nullstrike,
                        strike, Position.Short, false, cashRate, centralReplication)
                    over_cash_shortDigitalPutCoupon = DigitalCoupon(
                        underlying, nullstrike, Position.Long, false, nullstrike,
                        strike, Position.Short, false, cashRate, superReplication)
                    sub_cash_shortDigitalPutCoupon.setPricer(pricer)
                    central_cash_shortDigitalPutCoupon.setPricer(pricer)
                    over_cash_shortDigitalPutCoupon.setPricer(pricer)
                    sub_digitalPrice = sub_cash_shortDigitalPutCoupon.price(vars.termStructure)
                    central_digitalPrice = central_cash_shortDigitalPutCoupon.price(vars.termStructure)
                    over_digitalPrice = over_cash_shortDigitalPutCoupon.price(vars.termStructure)
                    self.assertFalse(
                        ((sub_digitalPrice > central_digitalPrice) and
                         abs(central_digitalPrice - sub_digitalPrice) > tolerance) or
                        ((central_digitalPrice > over_digitalPrice) and
                         abs(central_digitalPrice - over_digitalPrice) > tolerance))
