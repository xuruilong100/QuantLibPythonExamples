import QuantLib as ql
from math import log


def CubicSplineSpotRate(knots,
                        weights,
                        t):
    spline = ql.CubicSpline(knots)
    s = len(weights)
    d = 1.0

    for i in range(s):
        d += weights[i] * spline(i + 1, t)

    r = -log(d) / t

    return r


bondNum = 50

cleanPrice = [
    100.002, 99.92, 99.805, 99.75, 100.305, 99.76, 99.75, 99.975, 100.0416, 100.0574,
    99.5049, 101.0971, 101.137, 100.7199, 99.8883, 100.908, 103.3553, 99.5034, 103.913, 97.4229,
    104.5636, 99.7527, 104.3708, 99.6051, 104.8603, 101.3415, 105.29, 102.4969, 103.7602, 100.2803,
    102.6046, 102.5291, 99.4748, 95.9702, 97.1815, 114.2849, 100.2847, 112.23, 98.397, 102.0235,
    99.8483, 121.2711, 125.9157, 114.5791, 103.2202, 123.4668, 113.4694, 103.1873, 91.5603, 95.4441]

priceHandle = ql.QuoteHandleVector(bondNum)

for i in range(bondNum):
    priceHandle[i] = ql.QuoteHandle(ql.SimpleQuote(cleanPrice[i]))

issueYear = [
    2002, 2006, 2003, 2006, 1998, 2006, 2003, 2006, 1999, 2007,
    2004, 2007, 1999, 2007, 2004, 2007, 1999, 2005, 2000, 2005,
    2000, 2006, 2001, 2006, 2001, 2007, 2002, 2007, 2002, 2003,
    2003, 2004, 2004, 2005, 2005, 1986, 2006, 1986, 2006, 2007,
    2007, 1993, 1997, 1998, 1998, 2000, 2000, 2003, 2004, 2006]

issueMonth = [
    ql.Aug, ql.Mar, ql.Apr, ql.May, ql.Jul, ql.Aug, ql.Sep, ql.Nov, ql.Jan, ql.Feb,
    ql.Feb, ql.May, ql.Jul, ql.Aug, ql.Aug, ql.Sep, ql.Oct, ql.Feb, ql.May, ql.Aug,
    ql.Sep, ql.Feb, ql.May, ql.Aug, ql.Dec, ql.Feb, ql.Jun, ql.Aug, ql.Dec, ql.Jun,
    ql.Oct, ql.Apr, ql.Oct, ql.Apr, ql.Oct, ql.Jun, ql.Apr, ql.Sep, ql.Oct, ql.Apr,
    ql.Sep, ql.Dec, ql.Jul, ql.Jan, ql.Oct, ql.Jan, ql.Oct, ql.Jan, ql.Dec, ql.Dec]

issueDay = [
    14, 8, 11, 30, 4, 30, 25, 30, 4, 28, 2, 30, 4, 24, 25, 21, 22,
    24, 5, 26, 29, 26, 23, 30, 28, 28, 26, 24, 31, 24, 21, 25, 27, 28,
    30, 20, 26, 20, 31, 27, 21, 29, 3, 4, 7, 4, 27, 22, 24, 28]

maturityYear = [
    2008, 2008, 2008, 2008, 2008, 2008, 2008, 2008, 2009, 2009,
    2009, 2009, 2009, 2009, 2009, 2009, 2010, 2010, 2010, 2010,
    2011, 2011, 2011, 2011, 2012, 2012, 2012, 2012, 2013, 2013,
    2014, 2014, 2015, 2015, 2016, 2016, 2016, 2016, 2017, 2017,
    2018, 2024, 2027, 2028, 2028, 2030, 2031, 2034, 2037, 2039]

maturityMonth = [
    ql.Feb, ql.Mar, ql.Apr, ql.Jun, ql.Jul, ql.Sep, ql.Oct, ql.Dec, ql.Jan, ql.Mar,
    ql.Apr, ql.Jun, ql.Jul, ql.Sep, ql.Oct, ql.Dec, ql.Jan, ql.Apr, ql.Jul, ql.Oct,
    ql.Jan, ql.Apr, ql.Jul, ql.Oct, ql.Jan, ql.Apr, ql.Jul, ql.Oct, ql.Jan, ql.Jul,
    ql.Jan, ql.Jul, ql.Jan, ql.Jul, ql.Jan, ql.Jun, ql.Jul, ql.Sep, ql.Jan, ql.Jul,
    ql.Jan, ql.Jan, ql.Jul, ql.Jan, ql.Jul, ql.Jan, ql.Jan, ql.Jul, ql.Jan, ql.Jul]

maturityDay = [
    15, 14, 11, 13, 4, 12, 10, 12, 4, 13, 17, 12, 4, 11, 9, 11,
    4, 9, 4, 8, 4, 8, 4, 14, 4, 13, 4, 12, 4, 4, 4, 4, 4, 4, 4,
    20, 4, 20, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]

issueDate = ql.DateVector(bondNum)
maturityDate = ql.DateVector(bondNum)

for i in range(bondNum):
    idate = ql.Date(issueDay[i], issueMonth[i], issueYear[i])
    mdate = ql.Date(maturityDay[i], maturityMonth[i], maturityYear[i])
    issueDate[i] = idate
    maturityDate[i] = mdate

couponRate = [
    0.0425, 0.03, 0.03, 0.0325, 0.0475, 0.035, 0.035, 0.0375, 0.0375, 0.0375,
    0.0325, 0.045, 0.045, 0.04, 0.035, 0.04, 0.05375, 0.0325, 0.0525, 0.025,
    0.0525, 0.035, 0.05, 0.035, 0.05, 0.04, 0.05, 0.0425, 0.045, 0.0375, 0.0425,
    0.0425, 0.0375, 0.0325, 0.035, 0.06, 0.04, 0.05625, 0.0375, 0.0425, 0.04,
    0.0625, 0.065, 0.05625, 0.0475, 0.0625, 0.055, 0.0475, 0.04, 0.0425]

frequency = ql.Annual
dayCounter = ql.Actual365Fixed(ql.Actual365Fixed.Standard)
paymentConv = ql.Unadjusted
terminationDateConv = ql.Unadjusted
convention = ql.Unadjusted
redemption = 100.0
faceAmount = 100.0

calendar = ql.Germany(ql.Germany.Eurex)
today = calendar.adjust(ql.Date(30, ql.Jan, 2008))
ql.Settings.instance().evaluationDate = today

bondSettlementDays = 0
bondSettlementDate = calendar.advance(
    today,
    ql.Period(bondSettlementDays, ql.Days))

instruments = ql.BondHelperVector(bondNum)
maturity = ql.DoubleVector(bondNum)

for i in range(bondNum):
    bondCoupon = [couponRate[i]]
    schedule = ql.Schedule(
        issueDate[i],
        maturityDate[i],
        ql.Period(frequency),
        calendar,
        convention,
        terminationDateConv,
        ql.DateGeneration.Backward,
        False)

    helper = ql.FixedRateBondHelper(
        priceHandle[i],
        bondSettlementDays,
        faceAmount,
        schedule,
        bondCoupon,
        dayCounter,
        paymentConv,
        redemption)

    maturity[i] = dayCounter.yearFraction(
        bondSettlementDate, helper.maturityDate())

    instruments[i] = helper

tolerance = 1.0e-6
max = 5000

optMethod = ql.LevenbergMarquardt()

knotCubic = ql.CubicSplinesFitting.autoKnots(maturity)
knotQuadratic = ql.QuadraticSplinesFitting.autoKnots(maturity)
termstrcKnotes = [
    0.000000, 1.006027, 2.380274, 5.033425, 9.234521, 31.446575]

print("knotCubic:\t")
for v in knotCubic:
    print('{0:.6f}'.format(v))

print()
print("termstrc knots:\t")
for v in termstrcKnotes:
    print('{0:.6f}'.format(v))

print()

print("knotQuadratic:\t")
for v in knotQuadratic:
    print('{0:.6f}'.format(v))

csf = ql.CubicSplinesFitting(
    knotCubic, ql.Array(), optMethod)
qsf = ql.QuadraticSplinesFitting(
    knotQuadratic, ql.Array(), optMethod)

tsCubicSplines = ql.FittedBondDiscountCurve(
    bondSettlementDate,
    instruments, dayCounter,
    csf, tolerance, max)
tsQuadraticSplines = ql.FittedBondDiscountCurve(
    bondSettlementDate,
    instruments, dayCounter,
    qsf, tolerance, max)

weightsCubic = tsCubicSplines.fitResults().solution()
weightsQuadratic = tsQuadraticSplines.fitResults().solution()
termstrcWeights = ql.Array(7)
termstrcWeights[0] = 1.9320e-02
termstrcWeights[1] = -8.4936e-05
termstrcWeights[2] = -3.2009e-04
termstrcWeights[3] = -3.7101e-04
termstrcWeights[4] = 7.2921e-04
termstrcWeights[5] = 2.0159e-03
termstrcWeights[6] = -4.1632e-02

print("Cubic weights: \t", weightsCubic)
print("Quadratic weights: \t", weightsQuadratic)
print("termstrc weights: \t", termstrcWeights)

print()

print("Cubic final cost value:\t", tsCubicSplines.fitResults().minimumCostValue())
print("Quadratic final cost value:\t", tsQuadraticSplines.fitResults().minimumCostValue())

print()

for i in range(bondNum):
    t = dayCounter.yearFraction(
        bondSettlementDate, maturityDate[i])

    spotRateCubic = tsCubicSplines.zeroRate(
        t, ql.Continuous, frequency).rate() * 100.0
    spotRateQuadratic = tsQuadraticSplines.zeroRate(
        t, ql.Continuous, frequency).rate() * 100.0
    termstrcSpot = CubicSplineSpotRate(termstrcKnotes, termstrcWeights, t) * 100.0

    print('{0:.3f}\t'.format(t),
          "{0:.3f},\t".format(spotRateCubic),
          "{0:.3f},\t".format(spotRateQuadratic),
          "{0:.3f},\t".format(termstrcSpot),
          "{0:.3f},\t".format(spotRateCubic - termstrcSpot),
          "{0:.3f}".format(spotRateQuadratic - termstrcSpot))
