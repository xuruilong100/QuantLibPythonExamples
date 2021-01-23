import QuantLib as ql
import prettytable as pt

'''
*********************
***  MARKET DATA  ***
*********************
'''

calendar = ql.TARGET()
settlementDate = ql.Date(18, ql.September, 2008)
# must be a business day
settlementDate = calendar.adjust(settlementDate)

fixingDays = 3
settlementDays = 3

todaysDate = calendar.advance(settlementDate, -fixingDays, ql.Days)
# nothing to do with Date::todaysDate
ql.Settings.instance().evaluationDate = todaysDate

print('Today:', todaysDate.weekday(), ',', todaysDate)
print('Settlement date:', settlementDate.weekday(), ',', settlementDate)

'''
Building of the bonds discounting yield curve

*********************
***  RATE HELPERS ***
*********************

RateHelpers are built from the above quotes together with
other instrument dependant infos.  Quotes are passed in
relinkable handles which could be relinked to some other
data source later.

Common data

ZC rates for the short end
'''

zc3mQuote = 0.0096
zc6mQuote = 0.0145
zc1yQuote = 0.0194

zc3mRate = ql.SimpleQuote(zc3mQuote)
zc6mRate = ql.SimpleQuote(zc6mQuote)
zc1yRate = ql.SimpleQuote(zc1yQuote)

zcBondsDayCounter = ql.Actual365Fixed()

zc3m = ql.DepositRateHelper(
    ql.QuoteHandle(zc3mRate),
    ql.Period(3, ql.Months),
    fixingDays,
    calendar,
    ql.ModifiedFollowing,
    True,
    zcBondsDayCounter)
zc6m = ql.DepositRateHelper(
    ql.QuoteHandle(zc6mRate),
    ql.Period(6, ql.Months),
    fixingDays,
    calendar,
    ql.ModifiedFollowing,
    True,
    zcBondsDayCounter)
zc1y = ql.DepositRateHelper(
    ql.QuoteHandle(zc1yRate),
    ql.Period(1, ql.Years),
    fixingDays,
    calendar,
    ql.ModifiedFollowing,
    True,
    zcBondsDayCounter)

# setup bonds
redemption = 100.0

numberOfBonds = 5

issueDates = [
    ql.Date(15, ql.March, 2005),
    ql.Date(15, ql.June, 2005),
    ql.Date(30, ql.June, 2006),
    ql.Date(15, ql.November, 2002),
    ql.Date(15, ql.May, 1987)]

maturities = [
    ql.Date(31, ql.August, 2010),
    ql.Date(31, ql.August, 2011),
    ql.Date(31, ql.August, 2013),
    ql.Date(15, ql.August, 2018),
    ql.Date(15, ql.May, 2038)]

couponRates = [
    0.02375,
    0.04625,
    0.03125,
    0.04000,
    0.04500]

marketQuotes = [
    100.390625,
    106.21875,
    100.59375,
    101.6875,
    102.140625]

quote = [ql.SimpleQuote(mq) for mq in marketQuotes]
# quote = ql.QuoteVector()
# for i in range(numberOfBonds):
#     quote.push_back(ql.SimpleQuote(marketQuotes[i]))
quoteHandle = [ql.RelinkableQuoteHandle(q) for q in quote]

# Definition of the rate helpers
bondsHelpers = ql.BondHelperVector()

for i in range(numberOfBonds):
    schedule = ql.Schedule(
        issueDates[i],
        maturities[i],
        ql.Period(ql.Semiannual),
        ql.UnitedStates(ql.UnitedStates.GovernmentBond),
        ql.Unadjusted, ql.Unadjusted,
        ql.DateGeneration.Backward, False)

    bondHelper = ql.FixedRateBondHelper(
        quoteHandle[i],
        settlementDays,
        100.0,
        schedule,
        ql.DoubleVector(1, couponRates[i]),
        ql.ActualActual(ql.ActualActual.Bond),
        ql.Unadjusted,
        redemption,
        issueDates[i])

    '''
    the above could also be done by creating a
    FixedRateBond instance and writing:

    ext::shared_ptr<BondHelper> bondHelper(
            new BondHelper(quoteHandle[i], bond))

    This would also work for bonds that still don't have a
    specialized helper, such as floating-rate bonds.
    '''

    bondsHelpers.push_back(bondHelper)

'''
*********************
**  CURVE BUILDING **
*********************
'''

# Any DayCounter would be fine.
# ActualActual::ISDA ensures that 30 years is 30.0
termStructureDayCounter = ql.ActualActual(ql.ActualActual.ISDA)

# A depo-bond curve
bondInstruments = ql.RateHelperVector()

# Adding the ZC bonds to the curve for the short end
bondInstruments.push_back(zc3m)
bondInstruments.push_back(zc6m)
bondInstruments.push_back(zc1y)

for i in range(numberOfBonds):
    bondInstruments.push_back(bondsHelpers[i])

bondDiscountingTermStructure = ql.PiecewiseLogLinearDiscount(
    settlementDate,
    bondInstruments,
    termStructureDayCounter)

# Building of the Libor forecasting curve
# deposits
d1wQuote = 0.043375
d1mQuote = 0.031875
d3mQuote = 0.0320375
d6mQuote = 0.03385
d9mQuote = 0.0338125
d1yQuote = 0.0335125
# swaps
s2yQuote = 0.0295
s3yQuote = 0.0323
s5yQuote = 0.0359
s10yQuote = 0.0412
s15yQuote = 0.0433

'''
********************
***    QUOTES    ***
********************
'''

# SimpleQuote stores a value which can be manually changed;
# other Quote subclasses could read the value from a database
# or some kind of data feed.

# deposits
d1wRate = ql.SimpleQuote(d1wQuote)
d1mRate = ql.SimpleQuote(d1mQuote)
d3mRate = ql.SimpleQuote(d3mQuote)
d6mRate = ql.SimpleQuote(d6mQuote)
d9mRate = ql.SimpleQuote(d9mQuote)
d1yRate = ql.SimpleQuote(d1yQuote)
# swaps
s2yRate = ql.SimpleQuote(s2yQuote)
s3yRate = ql.SimpleQuote(s3yQuote)
s5yRate = ql.SimpleQuote(s5yQuote)
s10yRate = ql.SimpleQuote(s10yQuote)
s15yRate = ql.SimpleQuote(s15yQuote)

'''
*********************
***  RATE HELPERS ***
*********************
'''

# RateHelpers are built from the above quotes together with
# other instrument dependant infos.  Quotes are passed in
# relinkable handles which could be relinked to some other
# data source later.

# deposits
depositDayCounter = ql.Actual360()

d1w = ql.DepositRateHelper(
    ql.QuoteHandle(d1wRate),
    ql.Period(1, ql.Weeks),
    fixingDays,
    calendar,
    ql.ModifiedFollowing,
    True,
    depositDayCounter)
d1m = ql.DepositRateHelper(
    ql.QuoteHandle(d1mRate),
    ql.Period(1, ql.Months),
    fixingDays,
    calendar,
    ql.ModifiedFollowing,
    True,
    depositDayCounter)
d3m = ql.DepositRateHelper(
    ql.QuoteHandle(d3mRate),
    ql.Period(3, ql.Months),
    fixingDays,
    calendar,
    ql.ModifiedFollowing,
    True,
    depositDayCounter)
d6m = ql.DepositRateHelper(
    ql.QuoteHandle(d6mRate),
    ql.Period(6, ql.Months),
    fixingDays,
    calendar,
    ql.ModifiedFollowing,
    True,
    depositDayCounter)
d9m = ql.DepositRateHelper(
    ql.QuoteHandle(d9mRate),
    ql.Period(9, ql.Months),
    fixingDays,
    calendar,
    ql.ModifiedFollowing,
    True,
    depositDayCounter)
d1y = ql.DepositRateHelper(
    ql.QuoteHandle(d1yRate),
    ql.Period(1, ql.Years),
    fixingDays,
    calendar,
    ql.ModifiedFollowing,
    True,
    depositDayCounter)

# setup swaps
swFixedLegFrequency = ql.Annual
swFixedLegConvention = ql.Unadjusted
swFixedLegDayCounter = ql.Thirty360(ql.Thirty360.European)
swFloatingLegIndex = ql.Euribor6M()

forwardStart = ql.Period(1, ql.Days)

s2y = ql.SwapRateHelper(
    ql.QuoteHandle(s2yRate),
    ql.Period(2, ql.Years),
    calendar,
    swFixedLegFrequency,
    swFixedLegConvention,
    swFixedLegDayCounter,
    swFloatingLegIndex,
    ql.QuoteHandle(),
    forwardStart)
s3y = ql.SwapRateHelper(
    ql.QuoteHandle(s3yRate),
    ql.Period(3, ql.Years),
    calendar,
    swFixedLegFrequency,
    swFixedLegConvention,
    swFixedLegDayCounter,
    swFloatingLegIndex,
    ql.QuoteHandle(),
    forwardStart)
s5y = ql.SwapRateHelper(
    ql.QuoteHandle(s5yRate),
    ql.Period(5, ql.Years),
    calendar,
    swFixedLegFrequency,
    swFixedLegConvention,
    swFixedLegDayCounter,
    swFloatingLegIndex,
    ql.QuoteHandle(),
    forwardStart)
s10y = ql.SwapRateHelper(
    ql.QuoteHandle(s10yRate),
    ql.Period(10, ql.Years),
    calendar,
    swFixedLegFrequency,
    swFixedLegConvention,
    swFixedLegDayCounter,
    swFloatingLegIndex,
    ql.QuoteHandle(),
    forwardStart)
s15y = ql.SwapRateHelper(
    ql.QuoteHandle(s15yRate),
    ql.Period(15, ql.Years),
    calendar,
    swFixedLegFrequency,
    swFixedLegConvention,
    swFixedLegDayCounter,
    swFloatingLegIndex,
    ql.QuoteHandle(),
    forwardStart)

'''
*********************
**  CURVE BUILDING **
*********************
'''

# // Any DayCounter would be fine.
# // ActualActual::ISDA ensures that 30 years is 30.0
#
# // A depo-swap curve

depoSwapInstruments = ql.RateHelperVector()
depoSwapInstruments.push_back(d1w)
depoSwapInstruments.push_back(d1m)
depoSwapInstruments.push_back(d3m)
depoSwapInstruments.push_back(d6m)
depoSwapInstruments.push_back(d9m)
depoSwapInstruments.push_back(d1y)
depoSwapInstruments.push_back(s2y)
depoSwapInstruments.push_back(s3y)
depoSwapInstruments.push_back(s5y)
depoSwapInstruments.push_back(s10y)
depoSwapInstruments.push_back(s15y)

depoSwapTermStructure = ql.PiecewiseLogLinearDiscount(
    settlementDate,
    depoSwapInstruments,
    termStructureDayCounter)

# // Term structures that will be used for pricing:
# // the one used for discounting cash flows
discountingTermStructure = ql.RelinkableYieldTermStructureHandle()
# the one used for forward rate forecasting
forecastingTermStructure = ql.RelinkableYieldTermStructureHandle()

'''
*********************
* BONDS TO BE PRICED *
**********************
'''

# Common data
faceAmount = 100

# Pricing engine
bondEngine = ql.DiscountingBondEngine(discountingTermStructure)

# Zero coupon bond
zeroCouponBond = ql.ZeroCouponBond(
    settlementDays,
    ql.UnitedStates(ql.UnitedStates.GovernmentBond),
    faceAmount,
    ql.Date(15, ql.August, 2013),
    ql.Following,
    116.92,
    ql.Date(15, ql.August, 2003))

zeroCouponBond.setPricingEngine(bondEngine)

# Fixed 4.5% US Treasury Note
fixedBondSchedule = ql.Schedule(
    ql.Date(15, ql.May, 2007),
    ql.Date(15, ql.May, 2017),
    ql.Period(ql.Semiannual),
    ql.UnitedStates(ql.UnitedStates.GovernmentBond),
    ql.Unadjusted,
    ql.Unadjusted,
    ql.DateGeneration.Backward,
    False)

fixedRateBond = ql.FixedRateBond(
    settlementDays,
    faceAmount,
    fixedBondSchedule,
    ql.DoubleVector(1, 0.045),
    ql.ActualActual(ql.ActualActual.Bond),
    ql.ModifiedFollowing,
    100.0,
    ql.Date(15, ql.May, 2007))

fixedRateBond.setPricingEngine(bondEngine)

# // Floating rate bond (3M USD Libor + 0.1%)
# // Should and will be priced on another curve later...

liborTermStructure = ql.RelinkableYieldTermStructureHandle()
libor3m = ql.USDLibor(ql.Period(3, ql.Months), liborTermStructure)
libor3m.addFixing(ql.Date(17, ql.July, 2008), 0.0278625)

floatingBondSchedule = ql.Schedule(
    ql.Date(21, ql.October, 2005),
    ql.Date(21, ql.October, 2010),
    ql.Period(ql.Quarterly),
    ql.UnitedStates(ql.UnitedStates.NYSE),
    ql.Unadjusted,
    ql.Unadjusted,
    ql.DateGeneration.Backward,
    True)

floatingRateBond = ql.FloatingRateBond(
    settlementDays,
    faceAmount,
    floatingBondSchedule,
    libor3m,
    ql.Actual360(),
    ql.ModifiedFollowing,
    2,
    ql.DoubleVector(1, 1.0),  # // Gearings
    ql.DoubleVector(1, 0.001),  # // Spreads
    ql.DoubleVector(),  # // Caps
    ql.DoubleVector(),  # // Floors
    True,  # // Fixing in arrears
    100.0,
    ql.Date(21, ql.October, 2005))

floatingRateBond.setPricingEngine(bondEngine)

# Coupon pricers
pricer = ql.BlackIborCouponPricer()

# optionLet volatilities
volatility = 0.0
vol = ql.OptionletVolatilityStructureHandle(
    ql.ConstantOptionletVolatility(
        settlementDays,
        calendar,
        ql.ModifiedFollowing,
        volatility,
        ql.Actual365Fixed()))

pricer.setCapletVolatility(vol)
ql.setCouponPricer(floatingRateBond.cashflows(), pricer)

# Yield curve bootstrapping
forecastingTermStructure.linkTo(depoSwapTermStructure)
discountingTermStructure.linkTo(bondDiscountingTermStructure)

# We are using the depo & swap curve to estimate the future Libor rates
liborTermStructure.linkTo(depoSwapTermStructure)

tab = pt.PrettyTable(['', 'ZC', 'Fixed', 'Floating'])
tab.add_row(
    ['Net present value',
     zeroCouponBond.NPV(),
     fixedRateBond.NPV(),
     floatingRateBond.NPV()])
tab.add_row(
    ['Clean price',
     zeroCouponBond.cleanPrice(),
     fixedRateBond.cleanPrice(),
     floatingRateBond.cleanPrice()])
tab.add_row(
    ['Dirty price',
     zeroCouponBond.dirtyPrice(),
     fixedRateBond.dirtyPrice(),
     floatingRateBond.dirtyPrice()])
tab.add_row(
    ['Accrued coupon',
     zeroCouponBond.accruedAmount(),
     fixedRateBond.accruedAmount(),
     floatingRateBond.accruedAmount()])
tab.add_row(
    ['Previous coupon',
     'N/A',
     fixedRateBond.previousCouponRate() * 100.0,
     floatingRateBond.previousCouponRate() * 100.0])
tab.add_row(
    ['Next coupon',
     'N/A',
     fixedRateBond.nextCouponRate() * 100.0,
     floatingRateBond.nextCouponRate() * 100.0])
tab.add_row(
    ['Yield',
     zeroCouponBond.bondYield(ql.Actual360(), ql.Compounded, ql.Annual) * 100.0,
     fixedRateBond.bondYield(ql.Actual360(), ql.Compounded, ql.Annual) * 100.0,
     floatingRateBond.bondYield(ql.Actual360(), ql.Compounded, ql.Annual) * 100.0])

tab.float_format = '.2'
print(tab)

print('Sample indirect computations (for the floating rate bond):')

print("Yield to Clean Price:",
      '{0:.2f}'.format(floatingRateBond.cleanPrice(
          floatingRateBond.bondYield(
              ql.Actual360(), ql.Compounded, ql.Annual),
          ql.Actual360(), ql.Compounded, ql.Annual, settlementDate)))

print('Clean Price to Yield:',
      '{0:.2%}'.format(floatingRateBond.bondYield(
          floatingRateBond.cleanPrice(), ql.Actual360(),
          ql.Compounded, ql.Annual, settlementDate)))

'''
Today: Monday, September 15th, 2008
Settlement date: Thursday, September 18th, 2008

                          ZC     Fixed  Floating
------------------------------------------------
 Net present value    100.92    107.67    102.36
       Clean price    100.92    106.13    101.80
       Dirty price    100.92    107.67    102.36
    Accrued coupon      0.00      1.54      0.56
   Previous coupon       N/A    4.50 %    2.89 %
       Next coupon       N/A    4.50 %    3.43 %
             Yield    3.00 %    3.65 %    2.20 %

Sample indirect computations (for the floating rate bond): 
------------------------------------------------
Yield to Clean Price: 101.80
Clean Price to Yield: 2.20 %
'''
