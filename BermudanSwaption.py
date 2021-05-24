import QuantLib as ql

# Number of swaptions to be calibrated to...

numRows = 5
numCols = 5

swapLenghts = [1, 2, 3, 4, 5]
swaptionVols = [
    0.1490, 0.1340, 0.1228, 0.1189, 0.1148,
    0.1290, 0.1201, 0.1146, 0.1108, 0.1040,
    0.1149, 0.1112, 0.1070, 0.1010, 0.0957,
    0.1047, 0.1021, 0.0980, 0.0951, 0.1270,
    0.1000, 0.0950, 0.0900, 0.1230, 0.1160]


def calibrateModel(model,
                   helpers):
    om = ql.LevenbergMarquardt()
    model.calibrate(
        helpers,
        om,
        ql.EndCriteria(400, 100, 1.0e-8, 1.0e-8, 1.0e-8))

    # Output the implied Black volatilities
    for i in range(numRows):
        helper = helpers[i]
        j = numCols - i - 1  # 1x5, 2x4, 3x3, 4x2, 5x1
        k = i * numCols + j
        npv = helper.modelValue()
        implied = helper.impliedVolatility(
            npv, 1e-4,
            1000, 0.05, 0.50)
        diff = implied - swaptionVols[k]

        print('{0}x{1}: model {2:.5%}, market {3:.5%} ({4:.5%})'.format(
            i + 1, swapLenghts[j], implied, swaptionVols[k], diff))


todaysDate = ql.Date(15, ql.February, 2002)
calendar = ql.TARGET()
settlementDate = ql.Date(19, ql.February, 2002)
ql.Settings.instance().evaluationDate = todaysDate

# flat yield term structure impling 1x5 swap at 5%
flatRate = ql.SimpleQuote(0.04875825)
rhTermStructure = ql.YieldTermStructureHandle(
    ql.FlatForward(settlementDate, ql.QuoteHandle(flatRate), ql.Actual365Fixed()))

# Define the ATM/OTM/ITM swaps
fixedLegFrequency = ql.Annual
fixedLegConvention = ql.Unadjusted
floatingLegConvention = ql.ModifiedFollowing
fixedLegDayCounter = ql.Thirty360(ql.Thirty360.European)
floatingLegFrequency = ql.Semiannual
typeSwap = ql.VanillaSwap.Payer
dummyFixedRate = 0.03
indexSixMonths = ql.Euribor6M(rhTermStructure)

startDate = calendar.advance(
    settlementDate, 1, ql.Years,
    floatingLegConvention)
maturity = calendar.advance(
    startDate, 5, ql.Years,
    floatingLegConvention)

fixedSchedule = ql.Schedule(
    startDate, maturity, ql.Period(fixedLegFrequency),
    calendar, fixedLegConvention, fixedLegConvention,
    ql.DateGeneration.Forward, False)
floatSchedule = ql.Schedule(
    startDate, maturity, ql.Period(floatingLegFrequency),
    calendar, floatingLegConvention, floatingLegConvention,
    ql.DateGeneration.Forward, False)

swap = ql.VanillaSwap(
    typeSwap, 1000.0,
    fixedSchedule, dummyFixedRate, fixedLegDayCounter,
    floatSchedule, indexSixMonths, 0.0,
    indexSixMonths.dayCounter())

swap.setPricingEngine(
    ql.DiscountingSwapEngine(rhTermStructure))

fixedATMRate = swap.fairRate()
fixedOTMRate = fixedATMRate * 1.2
fixedITMRate = fixedATMRate * 0.8

atmSwap = ql.VanillaSwap(
    typeSwap, 1000.0,
    fixedSchedule, fixedATMRate, fixedLegDayCounter,
    floatSchedule, indexSixMonths, 0.0,
    indexSixMonths.dayCounter())
otmSwap = ql.VanillaSwap(
    typeSwap, 1000.0,
    fixedSchedule, fixedOTMRate, fixedLegDayCounter,
    floatSchedule, indexSixMonths, 0.0,
    indexSixMonths.dayCounter())
itmSwap = ql.VanillaSwap(
    typeSwap, 1000.0,
    fixedSchedule, fixedITMRate, fixedLegDayCounter,
    floatSchedule, indexSixMonths, 0.0,
    indexSixMonths.dayCounter())

# defining the swaptions to be used in model calibration
swaptionMaturities = ql.PeriodVector()
swaptionMaturities.push_back(ql.Period(1, ql.Years))
swaptionMaturities.push_back(ql.Period(2, ql.Years))
swaptionMaturities.push_back(ql.Period(3, ql.Years))
swaptionMaturities.push_back(ql.Period(4, ql.Years))
swaptionMaturities.push_back(ql.Period(5, ql.Years))

swaptions = ql.BlackCalibrationHelperVector()

# List of times that have to be included in the timegrid
times = ql.DoubleVector()

for i in range(numRows):
    j = numCols - i - 1  # 1x5, 2x4, 3x3, 4x2, 5x1
    k = i * numCols + j
    vol = ql.SimpleQuote(swaptionVols[k])
    helper = ql.SwaptionHelper(
        swaptionMaturities[i],
        ql.Period(swapLenghts[j], ql.Years),
        ql.QuoteHandle(vol),
        indexSixMonths,
        indexSixMonths.tenor(),
        indexSixMonths.dayCounter(),
        indexSixMonths.dayCounter(),
        rhTermStructure)
    temp = helper.times()
    for t in temp:
        times.push_back(t)
    swaptions.append(helper)

# Building time-grid
grid = ql.TimeGrid(times, 30)

# defining the models
modelG2 = ql.G2(rhTermStructure)
modelHW = ql.HullWhite(rhTermStructure)
modelHW2 = ql.HullWhite(rhTermStructure)
modelBK = ql.BlackKarasinski(rhTermStructure)

# model calibrations

print('G2 (analytic formulae) calibration')
for i in range(len(swaptions)):
    swaptions[i].setPricingEngine(
        ql.G2SwaptionEngine(modelG2, 6.0, 16))

calibrateModel(modelG2, swaptions)
print(
    'calibrated to:\n'
    'a     = {0:.5}\n'
    'sigma = {1:.5}\n'
    'b     = {2:.5}\n'
    'eta   = {3:.5}\n'
    'rho   = {4:.5}\n'.format(
        modelG2.params()[0],
        modelG2.params()[1],
        modelG2.params()[2],
        modelG2.params()[3],
        modelG2.params()[4]))

print('Hull-White (analytic formulae) calibration')

for i in range(len(swaptions)):
    swaptions[i].setPricingEngine(
        ql.JamshidianSwaptionEngine(modelHW))

calibrateModel(modelHW, swaptions)
print(
    'calibrated to:\n'
    'a     = {0:.5}\n'
    'sigma = {1:.5}\n'.format(
        modelHW.params()[0],
        modelHW.params()[1]))

print('Hull-White (numerical) calibration')

for i in range(len(swaptions)):
    swaptions[i].setPricingEngine(
        ql.TreeSwaptionEngine(modelHW2, grid))

calibrateModel(modelHW2, swaptions)
print(
    'calibrated to:\n'
    'a     = {0:.5}\n'
    'sigma = {1:.5}\n'.format(
        modelHW2.params()[0],
        modelHW2.params()[1]))

print('Black-Karasinski (numerical) calibration')

for i in range(len(swaptions)):
    swaptions[i].setPricingEngine(
        ql.TreeSwaptionEngine(modelBK, grid))

calibrateModel(modelBK, swaptions)
print(
    'calibrated to:\n'
    'a     = {0:.5}\n'
    'sigma = {1:.5}\n'.format(
        modelBK.params()[0],
        modelBK.params()[1]))

# ATM Bermudan swaption pricing

print('Payer bermudan swaption '
      'struck at {0:%}'
      ' (ATM)'.format(fixedATMRate))

bermudanDates = ql.DateVector()
leg = swap.fixedLeg()
for i in range(len(leg)):
    coupon = ql.as_coupon(leg[i])
    bermudanDates.push_back(coupon.accrualStartDate())

bermudanExercise = ql.BermudanExercise(bermudanDates)
bermudanSwaption = ql.Swaption(atmSwap, bermudanExercise)

# Do the pricing for each model

# G2 price the European swaption here, it should switch to bermudan

bermudanSwaption.setPricingEngine(ql.TreeSwaptionEngine(modelG2, 50))
print("G2 (tree):      ", bermudanSwaption.NPV())
bermudanSwaption.setPricingEngine(ql.FdG2SwaptionEngine(modelG2))
print("G2 (fdm) :      ", bermudanSwaption.NPV())
bermudanSwaption.setPricingEngine(ql.TreeSwaptionEngine(modelHW, 50))
print("HW (tree):      ", bermudanSwaption.NPV())
bermudanSwaption.setPricingEngine(ql.FdHullWhiteSwaptionEngine(modelHW))
print("HW (fdm) :      ", bermudanSwaption.NPV())
bermudanSwaption.setPricingEngine(ql.TreeSwaptionEngine(modelHW2, 50))
print("HW (num, tree): ", bermudanSwaption.NPV())
bermudanSwaption.setPricingEngine(ql.FdHullWhiteSwaptionEngine(modelHW2))
print("HW (num, fdm) : ", bermudanSwaption.NPV())
bermudanSwaption.setPricingEngine(ql.TreeSwaptionEngine(modelBK, 50))
print("BK:             ", bermudanSwaption.NPV())

# OTM Bermudan swaption pricing

print('Payer bermudan swaption '
      'struck at {0:%}'
      ' (OTM)'.format(fixedOTMRate))

otmBermudanSwaption = ql.Swaption(otmSwap, bermudanExercise)

# Do the pricing for each model

otmBermudanSwaption.setPricingEngine(ql.TreeSwaptionEngine(modelG2, 50))
print("G2 (tree):      ", otmBermudanSwaption.NPV())
otmBermudanSwaption.setPricingEngine(ql.FdG2SwaptionEngine(modelG2))
print("G2 (fdm) :      ", otmBermudanSwaption.NPV())
otmBermudanSwaption.setPricingEngine(ql.TreeSwaptionEngine(modelHW, 50))
print("HW (tree):      ", otmBermudanSwaption.NPV())
otmBermudanSwaption.setPricingEngine(ql.FdHullWhiteSwaptionEngine(modelHW))
print("HW (fdm) :      ", otmBermudanSwaption.NPV())
otmBermudanSwaption.setPricingEngine(ql.TreeSwaptionEngine(modelHW2, 50))
print("HW (num, tree): ", otmBermudanSwaption.NPV())
otmBermudanSwaption.setPricingEngine(ql.FdHullWhiteSwaptionEngine(modelHW2))
print("HW (num, fdm) : ", otmBermudanSwaption.NPV())
otmBermudanSwaption.setPricingEngine(ql.TreeSwaptionEngine(modelBK, 50))
print("BK:             ", otmBermudanSwaption.NPV())

# ITM Bermudan swaption pricing

print('Payer bermudan swaption '
      'struck at {0:%}'
      ' (ITM)'.format(fixedITMRate))

itmBermudanSwaption = ql.Swaption(itmSwap, bermudanExercise)

# Do the pricing for each model

itmBermudanSwaption.setPricingEngine(ql.TreeSwaptionEngine(modelG2, 50))
print("G2 (tree):      ", itmBermudanSwaption.NPV())
itmBermudanSwaption.setPricingEngine(ql.FdG2SwaptionEngine(modelG2))
print("G2 (fdm) :      ", itmBermudanSwaption.NPV())
itmBermudanSwaption.setPricingEngine(ql.TreeSwaptionEngine(modelHW, 50))
print("HW (tree):      ", itmBermudanSwaption.NPV())
itmBermudanSwaption.setPricingEngine(ql.FdHullWhiteSwaptionEngine(modelHW))
print("HW (fdm) :      ", itmBermudanSwaption.NPV())
itmBermudanSwaption.setPricingEngine(ql.TreeSwaptionEngine(modelHW2, 50))
print("HW (num, tree): ", itmBermudanSwaption.NPV())
itmBermudanSwaption.setPricingEngine(ql.FdHullWhiteSwaptionEngine(modelHW2))
print("HW (num, fdm) : ", itmBermudanSwaption.NPV())
itmBermudanSwaption.setPricingEngine(ql.TreeSwaptionEngine(modelBK, 50))
print("BK:             ", itmBermudanSwaption.NPV())

'''
G2 (analytic formulae) calibration
1x5: model 10.04552 %, market 11.48000 % (-1.43448 %)
2x4: model 10.51233 %, market 11.08000 % (-0.56767 %)
3x3: model 10.70500 %, market 10.70000 % (+0.00500 %)
4x2: model 10.83816 %, market 10.21000 % (+0.62816 %)
5x1: model 10.94390 %, market 10.00000 % (+0.94390 %)
calibrated to:
a     = 0.050117, sigma = 0.0094504
b     = 0.050111, eta   = 0.0094503
rho   = -0.76332

Hull-White (analytic formulae) calibration
1x5: model 10.62037 %, market 11.48000 % (-0.85963 %)
2x4: model 10.62959 %, market 11.08000 % (-0.45041 %)
3x3: model 10.63414 %, market 10.70000 % (-0.06586 %)
4x2: model 10.64428 %, market 10.21000 % (+0.43428 %)
5x1: model 10.66132 %, market 10.00000 % (+0.66132 %)
calibrated to:
a = 0.046414, sigma = 0.0058693

Hull-White (numerical) calibration
1x5: model 10.31185 %, market 11.48000 % (-1.16815 %)
2x4: model 10.54619 %, market 11.08000 % (-0.53381 %)
3x3: model 10.66914 %, market 10.70000 % (-0.03086 %)
4x2: model 10.74020 %, market 10.21000 % (+0.53020 %)
5x1: model 10.79725 %, market 10.00000 % (+0.79725 %)
calibrated to:
a = 0.055229, sigma = 0.0061063

Black-Karasinski (numerical) calibration
1x5: model 10.32593 %, market 11.48000 % (-1.15407 %)
2x4: model 10.56575 %, market 11.08000 % (-0.51425 %)
3x3: model 10.67858 %, market 10.70000 % (-0.02142 %)
4x2: model 10.73678 %, market 10.21000 % (+0.52678 %)
5x1: model 10.77792 %, market 10.00000 % (+0.77792 %)
calibrated to:
a = 0.043389, sigma = 0.12075

Payer bermudan swaption struck at 5.00000 % (ATM)
G2 (tree):      14.111
G2 (fdm) :      14.113
HW (tree):      12.904
HW (fdm) :      12.91
HW (num, tree): 13.158
HW (num, fdm) : 13.157
BK:             13.002
Payer bermudan swaption struck at 6.00000 % (OTM)
G2 (tree):       3.1944
G2 (fdm) :       3.1809
HW (tree):       2.4921
HW (fdm) :       2.4596
HW (num, tree):  2.615
HW (num, fdm):   2.5829
BK:              3.2751
Payer bermudan swaption struck at 4.00000 % (ITM)
G2 (tree):       42.61
G2 (fdm) :       42.706
HW (tree):       42.253
HW (fdm) :       42.215
HW (num, tree):  42.364
HW (num, fdm) :  42.311
BK:              41.825
'''
