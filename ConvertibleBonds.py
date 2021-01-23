import QuantLib as ql
import prettytable as pt

optType = ql.Option.Put
underlying = 36.0
spreadRate = 0.005
dividendYield = 0.02
riskFreeRate = 0.06
volatility = 0.20
settlementDays = 3
length = 5
redemption = 100.0
conversionRatio = redemption / underlying

# set up dates/schedules
calendar = ql.TARGET()
today = calendar.adjust(ql.Date.todaysDate())

ql.Settings.instance().evaluationDate = today

settlementDate = calendar.advance(today, settlementDays, ql.Days)
exerciseDate = calendar.advance(settlementDate, length, ql.Years)
issueDate = calendar.advance(exerciseDate, -length, ql.Years)
convention = ql.ModifiedFollowing
frequency = ql.Annual

schedule = ql.Schedule(
    issueDate,
    exerciseDate,
    ql.Period(frequency),
    calendar,
    convention,
    convention,
    ql.DateGeneration.Backward,
    False)

dividends = ql.DividendSchedule()
callability = ql.CallabilitySchedule()
coupons = ql.DoubleVector(1, 0.05)
bondDayCount = ql.Thirty360()

callLength = [2, 4]  # Call dates, years 2, 4.
putLength = [3]  # Put dates year 3

callPrices = [101.5, 100.85]
putPrices = [105.0]

# Load call schedules
for i in range(len(callLength)):
    callability.push_back(
        ql.SoftCallability(
            ql.CallabilityPrice(
                callPrices[i], ql.CallabilityPrice.Clean),
            schedule[callLength[i]],
            1.20))

for i in range(len(putLength)):
    callability.push_back(
        ql.Callability(
            ql.CallabilityPrice(
                putPrices[i], ql.CallabilityPrice.Clean),
            ql.Callability.Put,
            schedule[putLength[i]]))

# Assume dividends are paid every 6 months.
d = today + ql.Period(6, ql.Months)
while d < exerciseDate:
    dividends.push_back(
        ql.FixedDividend(1.0, d))
    d += ql.Period(6, ql.Months)

dayCounter = ql.Actual365Fixed()
maturity = dayCounter.yearFraction(settlementDate, exerciseDate)

print("option type =", optType)
print("Time to maturity =", format(maturity, '.6'))
print("Underlying price =", underlying)
print("Risk-free interest rate =", format(riskFreeRate, '%'))
print("Dividend yield =", format(dividendYield, '%'))
print("Volatility =", format(volatility, '%'))

exercise = ql.EuropeanExercise(exerciseDate)
amExercise = ql.AmericanExercise(settlementDate, exerciseDate)

underlyingH = ql.QuoteHandle(
    ql.SimpleQuote(underlying))
flatTermStructure = ql.YieldTermStructureHandle(
    ql.FlatForward(settlementDate, riskFreeRate, dayCounter))
flatDividendTS = ql.YieldTermStructureHandle(
    ql.FlatForward(settlementDate, dividendYield, dayCounter))
flatVolTS = ql.BlackVolTermStructureHandle(
    ql.BlackConstantVol(settlementDate, calendar, volatility, dayCounter))
stochasticProcess = ql.BlackScholesMertonProcess(
    underlyingH, flatDividendTS, flatTermStructure, flatVolTS)

timeSteps = 801
creditSpread = ql.QuoteHandle(ql.SimpleQuote(spreadRate))
rate = ql.SimpleQuote(riskFreeRate)

discountCurve = ql.YieldTermStructureHandle(
    ql.FlatForward(today, ql.QuoteHandle(rate), dayCounter))

europeanBond = ql.ConvertibleFixedCouponBond(
    exercise, conversionRatio,
    dividends, callability, creditSpread,
    issueDate, settlementDays, coupons,
    bondDayCount, schedule, redemption)

americanBond = ql.ConvertibleFixedCouponBond(
    amExercise, conversionRatio,
    dividends, callability, creditSpread,
    issueDate, settlementDays, coupons,
    bondDayCount, schedule, redemption)

tab = pt.PrettyTable(["Tree type", "European", "American"])

print('=' * 56)
print("Tsiveriotis-Fernandes method")
print('=' * 56)

engine = ql.BinomialJRConvertibleEngine(stochasticProcess, timeSteps)
europeanBond.setPricingEngine(engine)
americanBond.setPricingEngine(engine)
tab.add_row(["Jarrow-Rudd", europeanBond.NPV(), americanBond.NPV()])

engine = ql.BinomialCRRConvertibleEngine(stochasticProcess, timeSteps)
europeanBond.setPricingEngine(engine)
americanBond.setPricingEngine(engine)
tab.add_row(["Cox-Ross-Rubinstein", europeanBond.NPV(), americanBond.NPV()])

engine = ql.BinomialEQPConvertibleEngine(stochasticProcess, timeSteps)
europeanBond.setPricingEngine(engine)
americanBond.setPricingEngine(engine)
tab.add_row(["Additive equiprobabilities", europeanBond.NPV(), americanBond.NPV()])

engine = ql.BinomialTrigeorgisConvertibleEngine(stochasticProcess, timeSteps)
europeanBond.setPricingEngine(engine)
americanBond.setPricingEngine(engine)
tab.add_row(["Trigeorgis", europeanBond.NPV(), americanBond.NPV()])

engine = ql.BinomialTianConvertibleEngine(stochasticProcess, timeSteps)
europeanBond.setPricingEngine(engine)
americanBond.setPricingEngine(engine)
tab.add_row(["Tian", europeanBond.NPV(), americanBond.NPV()])

engine = ql.BinomialLRConvertibleEngine(stochasticProcess, timeSteps)
europeanBond.setPricingEngine(engine)
americanBond.setPricingEngine(engine)
tab.add_row(["Leisen-Reimer", europeanBond.NPV(), americanBond.NPV()])

engine = ql.BinomialJ4ConvertibleEngine(stochasticProcess, timeSteps)
europeanBond.setPricingEngine(engine)
americanBond.setPricingEngine(engine)
tab.add_row(["Joshi", europeanBond.NPV(), americanBond.NPV()])

tab.float_format = '.6'
tab.align = 'l'

print(tab)

'''
option type = Put
Time to maturity = 5.00274
Underlying price = 36
Risk-free interest rate = 6.000000 %
Dividend yield = 2.000000 %
Volatility = 20.000000 %


===============================================================
Tsiveriotis-Fernandes method
===============================================================
Tree type                          European      American      
---------------------------------------------------------------
Jarrow-Rudd                        105.703497    108.170240    
Cox-Ross-Rubinstein                105.709245    108.163654    
Additive equiprobabilities         105.640089    108.112839    
Trigeorgis                         105.709738    108.164097    
Tian                               105.726387    108.174582    
Leisen-Reimer                      105.677313    108.182176    
Joshi                              105.677313    108.182177    
===============================================================
'''
