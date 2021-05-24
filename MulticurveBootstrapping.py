import QuantLib as ql
import prettytable as pt

'''
*********************
***  MARKET DATA  ***
*********************
'''

calendar = ql.TARGET()
todaysDate = ql.Date(11, ql.December, 2012)
ql.Settings.instance().evaluationDate = todaysDate
todaysDate = ql.Settings.instance().evaluationDate

fixingDays = 2
settlementDate = calendar.advance(todaysDate, fixingDays, ql.Days)
# must be a business day
settlementDate = calendar.adjust(settlementDate)

print('Today:', todaysDate.weekday(), todaysDate)
print('Settlement date:', settlementDate.weekday(), settlementDate)

'''
********************
***    QUOTES    ***
********************
'''

# SimpleQuote stores a value which can be manually changed
# other Quote subclasses could read the value from a database
# or some kind of data feed.

# deposits
dONRate = ql.SimpleQuote(0.0004)
dTNRate = ql.SimpleQuote(0.0004)
dSNRate = ql.SimpleQuote(0.0004)

# OIS
ois1WRate = ql.SimpleQuote(0.00070)
ois2WRate = ql.SimpleQuote(0.00069)
ois3WRate = ql.SimpleQuote(0.00078)
ois1MRate = ql.SimpleQuote(0.00074)

# Dated OIS
oisDated1Rate = ql.SimpleQuote(0.000460)
oisDated2Rate = ql.SimpleQuote(0.000160)
oisDated3Rate = ql.SimpleQuote(-0.000070)
oisDated4Rate = ql.SimpleQuote(-0.000130)
oisDated5Rate = ql.SimpleQuote(-0.000140)

# OIS
ois15MRate = ql.SimpleQuote(0.00002)
ois18MRate = ql.SimpleQuote(0.00008)
ois21MRate = ql.SimpleQuote(0.00021)
ois2YRate = ql.SimpleQuote(0.00036)
ois3YRate = ql.SimpleQuote(0.00127)
ois4YRate = ql.SimpleQuote(0.00274)
ois5YRate = ql.SimpleQuote(0.00456)
ois6YRate = ql.SimpleQuote(0.00647)
ois7YRate = ql.SimpleQuote(0.00827)
ois8YRate = ql.SimpleQuote(0.00996)
ois9YRate = ql.SimpleQuote(0.01147)
ois10YRate = ql.SimpleQuote(0.0128)
ois11YRate = ql.SimpleQuote(0.01404)
ois12YRate = ql.SimpleQuote(0.01516)
ois15YRate = ql.SimpleQuote(0.01764)
ois20YRate = ql.SimpleQuote(0.01939)
ois25YRate = ql.SimpleQuote(0.02003)
ois30YRate = ql.SimpleQuote(0.02038)

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

dON = ql.DepositRateHelper(
    ql.QuoteHandle(dONRate),
    ql.Period(1, ql.Days), 0,
    calendar, ql.Following,
    False, depositDayCounter)
dTN = ql.DepositRateHelper(
    ql.QuoteHandle(dTNRate),
    ql.Period(1, ql.Days), 1,
    calendar, ql.Following,
    False, depositDayCounter)
dSN = ql.DepositRateHelper(
    ql.QuoteHandle(dSNRate),
    ql.Period(1, ql.Days), 2,
    calendar, ql.Following,
    False, depositDayCounter)

# OIS
eonia = ql.Eonia()

ois1W = ql.OISRateHelper(
    2, ql.Period(1, ql.Weeks),
    ql.QuoteHandle(ois1WRate), eonia)
ois2W = ql.OISRateHelper(
    2, ql.Period(2, ql.Weeks),
    ql.QuoteHandle(ois2WRate), eonia)
ois3W = ql.OISRateHelper(
    2, ql.Period(3, ql.Weeks),
    ql.QuoteHandle(ois3WRate), eonia)
ois1M = ql.OISRateHelper(
    2, ql.Period(1, ql.Months),
    ql.QuoteHandle(ois1MRate), eonia)

# Dated OIS
oisDated1 = ql.DatedOISRateHelper(
    ql.Date(16, ql.January, 2013),
    ql.Date(13, ql.February, 2013),
    ql.QuoteHandle(oisDated1Rate), eonia)
oisDated2 = ql.DatedOISRateHelper(
    ql.Date(13, ql.February, 2013),
    ql.Date(13, ql.March, 2013),
    ql.QuoteHandle(oisDated2Rate), eonia)
oisDated3 = ql.DatedOISRateHelper(
    ql.Date(13, ql.March, 2013),
    ql.Date(10, ql.April, 2013),
    ql.QuoteHandle(oisDated3Rate), eonia)
oisDated4 = ql.DatedOISRateHelper(
    ql.Date(10, ql.April, 2013),
    ql.Date(8, ql.May, 2013),
    ql.QuoteHandle(oisDated4Rate), eonia)
oisDated5 = ql.DatedOISRateHelper(
    ql.Date(8, ql.May, 2013),
    ql.Date(12, ql.June, 2013),
    ql.QuoteHandle(oisDated5Rate), eonia)

# OIS
ois15M = ql.OISRateHelper(
    2, ql.Period(15, ql.Months),
    ql.QuoteHandle(ois15MRate), eonia)
ois18M = ql.OISRateHelper(
    2, ql.Period(18, ql.Months),
    ql.QuoteHandle(ois18MRate), eonia)
ois21M = ql.OISRateHelper(
    2, ql.Period(21, ql.Months),
    ql.QuoteHandle(ois21MRate), eonia)
ois2Y = ql.OISRateHelper(
    2, ql.Period(2, ql.Years),
    ql.QuoteHandle(ois2YRate), eonia)
ois3Y = ql.OISRateHelper(
    2, ql.Period(3, ql.Years),
    ql.QuoteHandle(ois3YRate), eonia)
ois4Y = ql.OISRateHelper(
    2, ql.Period(4, ql.Years),
    ql.QuoteHandle(ois4YRate), eonia)
ois5Y = ql.OISRateHelper(
    2, ql.Period(5, ql.Years),
    ql.QuoteHandle(ois5YRate), eonia)
ois6Y = ql.OISRateHelper(
    2, ql.Period(6, ql.Years),
    ql.QuoteHandle(ois6YRate), eonia)
ois7Y = ql.OISRateHelper(
    2, ql.Period(7, ql.Years),
    ql.QuoteHandle(ois7YRate), eonia)
ois8Y = ql.OISRateHelper(
    2, ql.Period(8, ql.Years),
    ql.QuoteHandle(ois8YRate), eonia)
ois9Y = ql.OISRateHelper(
    2, ql.Period(9, ql.Years),
    ql.QuoteHandle(ois9YRate), eonia)
ois10Y = ql.OISRateHelper(
    2, ql.Period(10, ql.Years),
    ql.QuoteHandle(ois10YRate), eonia)
ois11Y = ql.OISRateHelper(
    2, ql.Period(11, ql.Years),
    ql.QuoteHandle(ois11YRate), eonia)
ois12Y = ql.OISRateHelper(
    2, ql.Period(12, ql.Years),
    ql.QuoteHandle(ois12YRate), eonia)
ois15Y = ql.OISRateHelper(
    2, ql.Period(15, ql.Years),
    ql.QuoteHandle(ois15YRate), eonia)
ois20Y = ql.OISRateHelper(
    2, ql.Period(20, ql.Years),
    ql.QuoteHandle(ois20YRate), eonia)
ois25Y = ql.OISRateHelper(
    2, ql.Period(25, ql.Years),
    ql.QuoteHandle(ois25YRate), eonia)
ois30Y = ql.OISRateHelper(
    2, ql.Period(30, ql.Years),
    ql.QuoteHandle(ois30YRate), eonia)

'''
*********************
**  CURVE BUILDING **
*********************

*********************
**   EONIA CURVE   **
*********************
'''

termStructureDayCounter = ql.Actual365Fixed()

# Eonia curve
eoniaInstruments = ql.RateHelperVector()
eoniaInstruments.push_back(dON)
eoniaInstruments.push_back(dTN)
eoniaInstruments.push_back(dSN)
eoniaInstruments.push_back(ois1W)
eoniaInstruments.push_back(ois2W)
eoniaInstruments.push_back(ois3W)
eoniaInstruments.push_back(ois1M)
eoniaInstruments.push_back(oisDated1)
eoniaInstruments.push_back(oisDated2)
eoniaInstruments.push_back(oisDated3)
eoniaInstruments.push_back(oisDated4)
eoniaInstruments.push_back(oisDated5)
eoniaInstruments.push_back(ois15M)
eoniaInstruments.push_back(ois18M)
eoniaInstruments.push_back(ois21M)
eoniaInstruments.push_back(ois2Y)
eoniaInstruments.push_back(ois3Y)
eoniaInstruments.push_back(ois4Y)
eoniaInstruments.push_back(ois5Y)
eoniaInstruments.push_back(ois6Y)
eoniaInstruments.push_back(ois7Y)
eoniaInstruments.push_back(ois8Y)
eoniaInstruments.push_back(ois9Y)
eoniaInstruments.push_back(ois10Y)
eoniaInstruments.push_back(ois11Y)
eoniaInstruments.push_back(ois12Y)
eoniaInstruments.push_back(ois15Y)
eoniaInstruments.push_back(ois20Y)
eoniaInstruments.push_back(ois25Y)
eoniaInstruments.push_back(ois30Y)

eoniaTermStructure = ql.PiecewiseCubicDiscount(
    todaysDate,
    eoniaInstruments,
    termStructureDayCounter)
eoniaTermStructure.enableExtrapolation()

# Term structures that will be used for pricing:
# the one used for discounting cash flows
discountingTermStructure = ql.RelinkableYieldTermStructureHandle()
# the one used for forward rate forecasting
forecastingTermStructure = ql.RelinkableYieldTermStructureHandle()

discountingTermStructure.linkTo(eoniaTermStructure)

'''
**********************
**    EURIBOR 6M    **
**********************
'''
euribor6M = ql.Euribor6M()

# deposits
d6MRate = ql.SimpleQuote(0.00312)

# FRAs
fra1Rate = ql.SimpleQuote(0.002930)
fra2Rate = ql.SimpleQuote(0.002720)
fra3Rate = ql.SimpleQuote(0.002600)
fra4Rate = ql.SimpleQuote(0.002560)
fra5Rate = ql.SimpleQuote(0.002520)
fra6Rate = ql.SimpleQuote(0.002480)
fra7Rate = ql.SimpleQuote(0.002540)
fra8Rate = ql.SimpleQuote(0.002610)
fra9Rate = ql.SimpleQuote(0.002670)
fra10Rate = ql.SimpleQuote(0.002790)
fra11Rate = ql.SimpleQuote(0.002910)
fra12Rate = ql.SimpleQuote(0.003030)
fra13Rate = ql.SimpleQuote(0.003180)
fra14Rate = ql.SimpleQuote(0.003350)
fra15Rate = ql.SimpleQuote(0.003520)
fra16Rate = ql.SimpleQuote(0.003710)
fra17Rate = ql.SimpleQuote(0.003890)
fra18Rate = ql.SimpleQuote(0.004090)

# swaps
s3yRate = ql.SimpleQuote(0.004240)
s4yRate = ql.SimpleQuote(0.005760)
s5yRate = ql.SimpleQuote(0.007620)
s6yRate = ql.SimpleQuote(0.009540)
s7yRate = ql.SimpleQuote(0.011350)
s8yRate = ql.SimpleQuote(0.013030)
s9yRate = ql.SimpleQuote(0.014520)
s10yRate = ql.SimpleQuote(0.015840)
s12yRate = ql.SimpleQuote(0.018090)
s15yRate = ql.SimpleQuote(0.020370)
s20yRate = ql.SimpleQuote(0.021870)
s25yRate = ql.SimpleQuote(0.022340)
s30yRate = ql.SimpleQuote(0.022560)
s35yRate = ql.SimpleQuote(0.022950)
s40yRate = ql.SimpleQuote(0.023480)
s50yRate = ql.SimpleQuote(0.024210)
s60yRate = ql.SimpleQuote(0.024630)

d6M = ql.DepositRateHelper(
    ql.QuoteHandle(d6MRate),
    ql.Period(6, ql.Months), 3,
    calendar, ql.Following,
    False, depositDayCounter)

fra1 = ql.FraRateHelper(
    ql.QuoteHandle(fra1Rate),
    1, euribor6M)
fra2 = ql.FraRateHelper(
    ql.QuoteHandle(fra2Rate),
    2, euribor6M)
fra3 = ql.FraRateHelper(
    ql.QuoteHandle(fra3Rate),
    3, euribor6M)
fra4 = ql.FraRateHelper(
    ql.QuoteHandle(fra4Rate),
    4, euribor6M)
fra5 = ql.FraRateHelper(
    ql.QuoteHandle(fra5Rate),
    5, euribor6M)
fra6 = ql.FraRateHelper(
    ql.QuoteHandle(fra6Rate),
    6, euribor6M)
fra7 = ql.FraRateHelper(
    ql.QuoteHandle(fra7Rate),
    7, euribor6M)
fra8 = ql.FraRateHelper(
    ql.QuoteHandle(fra8Rate),
    8, euribor6M)
fra9 = ql.FraRateHelper(
    ql.QuoteHandle(fra9Rate),
    9, euribor6M)
fra10 = ql.FraRateHelper(
    ql.QuoteHandle(fra10Rate),
    10, euribor6M)
fra11 = ql.FraRateHelper(
    ql.QuoteHandle(fra11Rate),
    11, euribor6M)
fra12 = ql.FraRateHelper(
    ql.QuoteHandle(fra12Rate),
    12, euribor6M)
fra13 = ql.FraRateHelper(
    ql.QuoteHandle(fra13Rate),
    13, euribor6M)
fra14 = ql.FraRateHelper(
    ql.QuoteHandle(fra14Rate),
    14, euribor6M)
fra15 = ql.FraRateHelper(
    ql.QuoteHandle(fra15Rate),
    15, euribor6M)
fra16 = ql.FraRateHelper(
    ql.QuoteHandle(fra16Rate),
    16, euribor6M)
fra17 = ql.FraRateHelper(
    ql.QuoteHandle(fra17Rate),
    17, euribor6M)
fra18 = ql.FraRateHelper(
    ql.QuoteHandle(fra18Rate),
    18, euribor6M)

# setup swaps

swFixedLegFrequency = ql.Annual
swFixedLegConvention = ql.Unadjusted
swFixedLegDayCounter = ql.Thirty360(ql.Thirty360.European)

swFloatingLegIndex = ql.Euribor6M()

s3y = ql.SwapRateHelper(
    ql.QuoteHandle(s3yRate), ql.Period(3, ql.Years),
    calendar, swFixedLegFrequency,
    swFixedLegConvention, swFixedLegDayCounter,
    swFloatingLegIndex,
    ql.QuoteHandle(), ql.Period(0, ql.Days),
    discountingTermStructure)

s4y = ql.SwapRateHelper(
    ql.QuoteHandle(s4yRate), ql.Period(4, ql.Years),
    calendar, swFixedLegFrequency,
    swFixedLegConvention, swFixedLegDayCounter,
    swFloatingLegIndex,
    ql.QuoteHandle(), ql.Period(0, ql.Days),
    discountingTermStructure)

s5y = ql.SwapRateHelper(
    ql.QuoteHandle(s5yRate), ql.Period(5, ql.Years),
    calendar, swFixedLegFrequency,
    swFixedLegConvention, swFixedLegDayCounter,
    swFloatingLegIndex,
    ql.QuoteHandle(), ql.Period(0, ql.Days),
    discountingTermStructure)

s6y = ql.SwapRateHelper(
    ql.QuoteHandle(s6yRate), ql.Period(6, ql.Years),
    calendar, swFixedLegFrequency,
    swFixedLegConvention, swFixedLegDayCounter,
    swFloatingLegIndex,
    ql.QuoteHandle(), ql.Period(0, ql.Days),
    discountingTermStructure)

s7y = ql.SwapRateHelper(
    ql.QuoteHandle(s7yRate), ql.Period(7, ql.Years),
    calendar, swFixedLegFrequency,
    swFixedLegConvention, swFixedLegDayCounter,
    swFloatingLegIndex,
    ql.QuoteHandle(), ql.Period(0, ql.Days),
    discountingTermStructure)

s8y = ql.SwapRateHelper(
    ql.QuoteHandle(s8yRate), ql.Period(8, ql.Years),
    calendar, swFixedLegFrequency,
    swFixedLegConvention, swFixedLegDayCounter,
    swFloatingLegIndex,
    ql.QuoteHandle(), ql.Period(0, ql.Days),
    discountingTermStructure)

s9y = ql.SwapRateHelper(
    ql.QuoteHandle(s9yRate), ql.Period(9, ql.Years),
    calendar, swFixedLegFrequency,
    swFixedLegConvention, swFixedLegDayCounter,
    swFloatingLegIndex,
    ql.QuoteHandle(), ql.Period(0, ql.Days),
    discountingTermStructure)

s10y = ql.SwapRateHelper(
    ql.QuoteHandle(s10yRate), ql.Period(10, ql.Years),
    calendar, swFixedLegFrequency,
    swFixedLegConvention, swFixedLegDayCounter,
    swFloatingLegIndex,
    ql.QuoteHandle(), ql.Period(0, ql.Days),
    discountingTermStructure)

s12y = ql.SwapRateHelper(
    ql.QuoteHandle(s12yRate), ql.Period(12, ql.Years),
    calendar, swFixedLegFrequency,
    swFixedLegConvention, swFixedLegDayCounter,
    swFloatingLegIndex,
    ql.QuoteHandle(), ql.Period(0, ql.Days),
    discountingTermStructure)

s15y = ql.SwapRateHelper(
    ql.QuoteHandle(s15yRate), ql.Period(15, ql.Years),
    calendar, swFixedLegFrequency,
    swFixedLegConvention, swFixedLegDayCounter,
    swFloatingLegIndex,
    ql.QuoteHandle(), ql.Period(0, ql.Days),
    discountingTermStructure)

s20y = ql.SwapRateHelper(
    ql.QuoteHandle(s20yRate), ql.Period(20, ql.Years),
    calendar, swFixedLegFrequency,
    swFixedLegConvention, swFixedLegDayCounter,
    swFloatingLegIndex,
    ql.QuoteHandle(), ql.Period(0, ql.Days),
    discountingTermStructure)

s25y = ql.SwapRateHelper(
    ql.QuoteHandle(s25yRate), ql.Period(25, ql.Years),
    calendar, swFixedLegFrequency,
    swFixedLegConvention, swFixedLegDayCounter,
    swFloatingLegIndex,
    ql.QuoteHandle(), ql.Period(0, ql.Days),
    discountingTermStructure)

s30y = ql.SwapRateHelper(
    ql.QuoteHandle(s30yRate), ql.Period(30, ql.Years),
    calendar, swFixedLegFrequency,
    swFixedLegConvention, swFixedLegDayCounter,
    swFloatingLegIndex,
    ql.QuoteHandle(), ql.Period(0, ql.Days),
    discountingTermStructure)

s35y = ql.SwapRateHelper(
    ql.QuoteHandle(s35yRate), ql.Period(35, ql.Years),
    calendar, swFixedLegFrequency,
    swFixedLegConvention, swFixedLegDayCounter,
    swFloatingLegIndex,
    ql.QuoteHandle(), ql.Period(0, ql.Days),
    discountingTermStructure)

s40y = ql.SwapRateHelper(
    ql.QuoteHandle(s40yRate), ql.Period(40, ql.Years),
    calendar, swFixedLegFrequency,
    swFixedLegConvention, swFixedLegDayCounter,
    swFloatingLegIndex,
    ql.QuoteHandle(), ql.Period(0, ql.Days),
    discountingTermStructure)

s50y = ql.SwapRateHelper(
    ql.QuoteHandle(s50yRate), ql.Period(50, ql.Years),
    calendar, swFixedLegFrequency,
    swFixedLegConvention, swFixedLegDayCounter,
    swFloatingLegIndex,
    ql.QuoteHandle(), ql.Period(0, ql.Days),
    discountingTermStructure)

s60y = ql.SwapRateHelper(
    ql.QuoteHandle(s60yRate), ql.Period(60, ql.Years),
    calendar, swFixedLegFrequency,
    swFixedLegConvention, swFixedLegDayCounter,
    swFloatingLegIndex,
    ql.QuoteHandle(), ql.Period(0, ql.Days),
    discountingTermStructure)

# Euribor 6M curve
euribor6MInstruments = ql.RateHelperVector()

euribor6MInstruments.push_back(d6M)
euribor6MInstruments.push_back(fra1)
euribor6MInstruments.push_back(fra2)
euribor6MInstruments.push_back(fra3)
euribor6MInstruments.push_back(fra4)
euribor6MInstruments.push_back(fra5)
euribor6MInstruments.push_back(fra6)
euribor6MInstruments.push_back(fra7)
euribor6MInstruments.push_back(fra8)
euribor6MInstruments.push_back(fra9)
euribor6MInstruments.push_back(fra10)
euribor6MInstruments.push_back(fra11)
euribor6MInstruments.push_back(fra12)
euribor6MInstruments.push_back(fra13)
euribor6MInstruments.push_back(fra14)
euribor6MInstruments.push_back(fra15)
euribor6MInstruments.push_back(fra16)
euribor6MInstruments.push_back(fra17)
euribor6MInstruments.push_back(fra18)
euribor6MInstruments.push_back(s3y)
euribor6MInstruments.push_back(s4y)
euribor6MInstruments.push_back(s5y)
euribor6MInstruments.push_back(s6y)
euribor6MInstruments.push_back(s7y)
euribor6MInstruments.push_back(s8y)
euribor6MInstruments.push_back(s9y)
euribor6MInstruments.push_back(s10y)
euribor6MInstruments.push_back(s12y)
euribor6MInstruments.push_back(s15y)
euribor6MInstruments.push_back(s20y)
euribor6MInstruments.push_back(s25y)
euribor6MInstruments.push_back(s30y)
euribor6MInstruments.push_back(s35y)
euribor6MInstruments.push_back(s40y)
euribor6MInstruments.push_back(s50y)
euribor6MInstruments.push_back(s60y)

# If needed, it's possible to change the tolerance the default is 1.0e-12.
tolerance = 1.0e-15
# The tolerance is passed in an explicit bootstrap object. Depending on
# the bootstrap algorithm, it's possible to pass other parameters.

euribor6MTermStructure = ql.PiecewiseCubicDiscount(
    settlementDate, euribor6MInstruments,
    termStructureDayCounter,
    ql.Cubic(),
    ql.IterativeBootstrap(tolerance))

'''
**********************
* SWAPS TO BE PRICED *
**********************
'''

# constant nominal 1,000,000 Euro
nominal = 1000000.0
# fixed leg
fixedLegFrequency = ql.Annual
fixedLegConvention = ql.Unadjusted
floatingLegConvention = ql.ModifiedFollowing
fixedLegDayCounter = ql.Thirty360(ql.Thirty360.European)
fixedRate = 0.007
floatingLegDayCounter = ql.Actual360()

# floating leg
floatingLegFrequency = ql.Semiannual
euriborIndex = ql.Euribor6M(forecastingTermStructure)
spread = 0.0

lengthInYears = 5
swapType = ql.VanillaSwap.Payer

maturity = settlementDate + ql.Period(lengthInYears, ql.Years)

fixedSchedule = ql.Schedule(
    settlementDate, maturity,
    ql.Period(fixedLegFrequency),
    calendar, fixedLegConvention,
    fixedLegConvention,
    ql.DateGeneration.Forward, False)
floatSchedule = ql.Schedule(
    settlementDate, maturity,
    ql.Period(floatingLegFrequency),
    calendar, floatingLegConvention,
    floatingLegConvention,
    ql.DateGeneration.Forward, False)
spot5YearSwap = ql.VanillaSwap(
    swapType, nominal,
    fixedSchedule, fixedRate, fixedLegDayCounter,
    floatSchedule, euriborIndex, spread,
    floatingLegDayCounter)
fwdStart = calendar.advance(settlementDate, 1, ql.Years)
fwdMaturity = fwdStart + ql.Period(lengthInYears, ql.Years)
fwdFixedSchedule = ql.Schedule(
    fwdStart, fwdMaturity,
    ql.Period(fixedLegFrequency),
    calendar, fixedLegConvention,
    fixedLegConvention,
    ql.DateGeneration.Forward, False)
fwdFloatSchedule = ql.Schedule(
    fwdStart, fwdMaturity,
    ql.Period(floatingLegFrequency),
    calendar, floatingLegConvention,
    floatingLegConvention,
    ql.DateGeneration.Forward, False)
oneYearForward5YearSwap = ql.VanillaSwap(
    swapType, nominal,
    fwdFixedSchedule, fixedRate, fixedLegDayCounter,
    fwdFloatSchedule, euriborIndex, spread,
    floatingLegDayCounter)

'''
****************
* SWAP PRICING *
****************
'''

# utilities for reporting
tab0 = pt.PrettyTable(
    ["term structure", "net present value", "fair spread", "fair fixed rate"])
tab1 = pt.PrettyTable(
    ["term structure", "net present value", "fair spread", "fair fixed rate"])
tab2 = pt.PrettyTable(
    ["term structure", "net present value", "fair spread", "fair fixed rate"])
tab3 = pt.PrettyTable(
    ["term structure", "net present value", "fair spread", "fair fixed rate"])

# calculations
print("5-year market swap-rate = {0:.2%}".format(s5yRate.value()))
print("5-years swap paying {0:.2%}".format(fixedRate))

swapEngine = ql.DiscountingSwapEngine(discountingTermStructure)

spot5YearSwap.setPricingEngine(swapEngine)
oneYearForward5YearSwap.setPricingEngine(swapEngine)

# Of course, you're not forced to really use different curves
forecastingTermStructure.linkTo(euribor6MTermStructure)
discountingTermStructure.linkTo(eoniaTermStructure)

NPV = spot5YearSwap.NPV()
fairSpread = spot5YearSwap.fairSpread()
fairRate = spot5YearSwap.fairRate()

tab0.add_row(["eonia disc", NPV, fairSpread * 100, fairRate * 100])

# let's check that the 5 years swap has been correctly re-priced
if not abs(fairRate - s5yRate.value()) < 1e-8:
    raise ValueError("5-years swap mispriced")

forecastingTermStructure.linkTo(euribor6MTermStructure)
discountingTermStructure.linkTo(euribor6MTermStructure)

NPV = spot5YearSwap.NPV()
fairSpread = spot5YearSwap.fairSpread()
fairRate = spot5YearSwap.fairRate()

tab0.add_row(["euribor disc", NPV, fairSpread * 100, fairRate * 100])

tab0.float_format = '.2'
print(tab0)

if not abs(fairRate - s5yRate.value()) < 1e-8:
    raise ValueError("5-years swap mispriced")

# now let's price the 1Y forward 5Y swap

print("5-years, 1-year forward swap paying {0:.2%}".format(fixedRate))

forecastingTermStructure.linkTo(euribor6MTermStructure)
discountingTermStructure.linkTo(eoniaTermStructure)

NPV = oneYearForward5YearSwap.NPV()
fairSpread = oneYearForward5YearSwap.fairSpread()
fairRate = oneYearForward5YearSwap.fairRate()

tab1.add_row(["eonia disc", NPV, fairSpread * 100, fairRate * 100])

forecastingTermStructure.linkTo(euribor6MTermStructure)
discountingTermStructure.linkTo(euribor6MTermStructure)

NPV = oneYearForward5YearSwap.NPV()
fairSpread = oneYearForward5YearSwap.fairSpread()
fairRate = oneYearForward5YearSwap.fairRate()

tab1.add_row(["euribor disc", NPV, fairSpread * 100, fairRate * 100])

tab1.float_format = '.2'
print(tab1)

# now let's say that the 5-years swap rate goes up to 0.009%.
# A smarter market element--say, connected to a data source-- would
# notice the change itself. Since we're using SimpleQuotes,
# we'll have to change the value manually--which forces us to
# downcast the handle and use the SimpleQuote
# interface. In any case, the point here is that a change in the
# value contained in the Quote triggers a new bootstrapping
# of the curve and a repricing of the swap.

fiveYearsRate = s5yRate
fiveYearsRate.setValue(0.0090)

print("5-year market swap-rate = {0:.2%}".format(s5yRate.value()))
print("5-years swap paying {0:.2%}".format(fixedRate))

# now get the updated results
forecastingTermStructure.linkTo(euribor6MTermStructure)
discountingTermStructure.linkTo(eoniaTermStructure)

NPV = spot5YearSwap.NPV()
fairSpread = spot5YearSwap.fairSpread()
fairRate = spot5YearSwap.fairRate()

tab2.add_row(["eonia disc", NPV, fairSpread * 100, fairRate * 100])

if not abs(fairRate - s5yRate.value()) < 1e-8:
    raise ValueError("5-years swap mispriced")

forecastingTermStructure.linkTo(euribor6MTermStructure)
discountingTermStructure.linkTo(euribor6MTermStructure)

NPV = spot5YearSwap.NPV()
fairSpread = spot5YearSwap.fairSpread()
fairRate = spot5YearSwap.fairRate()

tab2.add_row(["euribor disc", NPV, fairSpread * 100, fairRate * 100])

tab2.float_format = '.2'
print(tab2)

if not abs(fairRate - s5yRate.value()) < 1e-8:
    raise ValueError("5-years swap mispriced")

print("5-years, 1-year forward swap paying {0:.2%}".format(fixedRate))

forecastingTermStructure.linkTo(euribor6MTermStructure)
discountingTermStructure.linkTo(eoniaTermStructure)

NPV = oneYearForward5YearSwap.NPV()
fairSpread = oneYearForward5YearSwap.fairSpread()
fairRate = oneYearForward5YearSwap.fairRate()

tab3.add_row(["eonia disc", NPV, fairSpread * 100, fairRate * 100])

forecastingTermStructure.linkTo(euribor6MTermStructure)
discountingTermStructure.linkTo(euribor6MTermStructure)

NPV = oneYearForward5YearSwap.NPV()
fairSpread = oneYearForward5YearSwap.fairSpread()
fairRate = oneYearForward5YearSwap.fairRate()

tab3.add_row(["euribor disc", NPV, fairSpread * 100, fairRate * 100])

tab3.float_format = '.2'
print(tab3)

'''
Today: Tuesday, December 11th, 2012
Settlement date: Thursday, December 13th, 2012
====================================================================
5-year market swap-rate = 0.76 %
====================================================================
        5-years swap paying 0.70 %
term structure | net present value | fair spread | fair fixed rate | 
--------------------------------------------------------------------
    eonia disc |           3076.03 |     -0.06 % |          0.76 % | 
  euribor disc |           3049.06 |     -0.06 % |          0.76 % | 
--------------------------------------------------------------------
        5-years, 1-year forward swap paying 0.70 %
term structure | net present value | fair spread | fair fixed rate | 
--------------------------------------------------------------------
    eonia disc |          19202.89 |     -0.38 % |          1.09 % | 
  euribor disc |          19035.39 |     -0.38 % |          1.09 % | 
====================================================================
5-year market swap-rate = 0.90 %
====================================================================
        5-years swap paying 0.70 %
term structure | net present value | fair spread | fair fixed rate | 
--------------------------------------------------------------------
    eonia disc |           9922.67 |     -0.20 % |          0.90 % | 
  euribor disc |           9822.22 |     -0.20 % |          0.90 % | 
--------------------------------------------------------------------
        5-years, 1-year forward swap paying 0.70 %
term structure | net present value | fair spread | fair fixed rate | 
--------------------------------------------------------------------
    eonia disc |          19202.89 |     -0.38 % |          1.09 % | 
  euribor disc |          19018.47 |     -0.38 % |          1.09 % | 
'''
