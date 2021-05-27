import QuantLib as ql
import prettytable as pt

today = ql.Date(29, ql.May, 2006)
ql.Settings.instance().evaluationDate = today

# the option to replicate
barrierType = ql.Barrier.DownOut
barrier = 70.0
rebate = 0.0
type = ql.Option.Put
underlyingValue = 100.0
underlying = ql.SimpleQuote(underlyingValue)
strike = 100.0
riskFreeRate = ql.SimpleQuote(0.04)
volatility = ql.SimpleQuote(0.20)
maturity = today + ql.Period(1, ql.Years)

tab1 = pt.PrettyTable(['Option', 'NPV', 'Error'])
tab2 = pt.PrettyTable(['Option', 'NPV', 'Error'])
tab3 = pt.PrettyTable(['Option', 'NPV', 'Error'])

tab1.float_format = '.6'
tab2.float_format = '.6'
tab3.float_format = '.6'

print("Initial market conditions")

# bootstrap the yield/vol curves
dayCounter = ql.Actual365Fixed()
h1 = ql.QuoteHandle(riskFreeRate)
h2 = ql.QuoteHandle(volatility)
flatRate = ql.YieldTermStructureHandle(
    ql.FlatForward(
        0, ql.NullCalendar(), h1, dayCounter))
flatVol = ql.BlackVolTermStructureHandle(
    ql.BlackConstantVol(
        0, ql.NullCalendar(), h2, dayCounter))

# instantiate the option
exercise = ql.EuropeanExercise(maturity)
payoff = ql.PlainVanillaPayoff(type, strike)
bsProcess = ql.BlackScholesProcess(
    ql.QuoteHandle(underlying),
    flatRate, flatVol)
barrierEngine = ql.AnalyticBarrierEngine(bsProcess)
europeanEngine = ql.AnalyticEuropeanEngine(bsProcess)

referenceOption = ql.BarrierOption(
    barrierType, barrier, rebate,
    payoff, exercise)

referenceOption.setPricingEngine(barrierEngine)

referenceValue = referenceOption.NPV()

tab1.add_row(["Original barrier option", referenceValue, 'N/A'])

# Replicating portfolios
portfolio1 = ql.CompositeInstrument()
portfolio2 = ql.CompositeInstrument()
portfolio3 = ql.CompositeInstrument()

# Final payoff first (the same for all portfolios):
# as shown in Joshi, a put struck at K...
put1 = ql.EuropeanOption(payoff, exercise)
put1.setPricingEngine(europeanEngine)
portfolio1.add(put1)
portfolio2.add(put1)
portfolio3.add(put1)
# ...minus a digital put struck at B of notional K-B...
digitalPayoff = ql.CashOrNothingPayoff(ql.Option.Put, barrier, 1.0)
digitalPut = ql.EuropeanOption(digitalPayoff, exercise)
digitalPut.setPricingEngine(europeanEngine)
portfolio1.subtract(digitalPut, strike - barrier)
portfolio2.subtract(digitalPut, strike - barrier)
portfolio3.subtract(digitalPut, strike - barrier)
# ...minus a put option struck at B.
lowerPayoff = ql.PlainVanillaPayoff(ql.Option.Put, barrier)
put2 = ql.EuropeanOption(lowerPayoff, exercise)
put2.setPricingEngine(europeanEngine)
portfolio1.subtract(put2)
portfolio2.subtract(put2)
portfolio3.subtract(put2)

# Now we use puts struck at B to kill the value of the
# portfolio on a number of points (B,t).  For the first
# portfolio, we'll use 12 dates at one-month's distance.

for i in range(12, 0, -1):
    # First, we instantiate the option...
    innerMaturity = today + ql.Period(i, ql.Months)
    innerExercise = ql.EuropeanExercise(innerMaturity)
    innerPayoff = ql.PlainVanillaPayoff(ql.Option.Put, barrier)
    putn = ql.EuropeanOption(innerPayoff, innerExercise)
    putn.setPricingEngine(europeanEngine)
    # ...second, we evaluate the current portfolio and the
    # latest put at (B,t)...
    killDate = today + ql.Period((i - 1), ql.Months)
    ql.Settings.instance().evaluationDate = killDate
    underlying.setValue(barrier)
    portfolioValue = portfolio1.NPV()
    putValue = putn.NPV()
    # ...finally, we estimate the notional that kills the
    # portfolio value at that point...
    notional = portfolioValue / putValue
    # ...and we subtract from the portfolio a put with such
    # notional.
    portfolio1.subtract(putn, notional)

# The portfolio being complete, we return to today's market...
ql.Settings.instance().evaluationDate = today
underlying.setValue(underlyingValue)
# ...and output the value.

portfolioValue = portfolio1.NPV()
error = portfolioValue - referenceValue
tab1.add_row(["Replicating portfolio (12 dates)", portfolioValue, error])

# For the second portfolio, we'll use 26 dates at two-weeks'
# distance.

for i in range(52, 1, -2):
    # Same as above.
    innerMaturity = today + ql.Period(i, ql.Weeks)
    innerExercise = ql.EuropeanExercise(innerMaturity)
    innerPayoff = ql.PlainVanillaPayoff(ql.Option.Put, barrier)
    putn = ql.EuropeanOption(innerPayoff, innerExercise)
    putn.setPricingEngine(europeanEngine)
    killDate = today + ql.Period(i - 2, ql.Weeks)
    ql.Settings.instance().evaluationDate = killDate
    underlying.setValue(barrier)
    portfolioValue = portfolio2.NPV()
    putValue = putn.NPV()
    notional = portfolioValue / putValue
    portfolio2.subtract(putn, notional)

ql.Settings.instance().evaluationDate = today
underlying.setValue(underlyingValue)
portfolioValue = portfolio2.NPV()
error = portfolioValue - referenceValue
tab1.add_row(["Replicating portfolio (26 dates)", portfolioValue, error])

# For the third portfolio, we'll use 52 dates at one-week's
# distance.

for i in range(52, 0, -1):
    # Same as above.
    innerMaturity = today + ql.Period(i, ql.Weeks)
    innerExercise = ql.EuropeanExercise(innerMaturity)
    innerPayoff = ql.PlainVanillaPayoff(ql.Option.Put, barrier)
    putn = ql.EuropeanOption(innerPayoff, innerExercise)
    putn.setPricingEngine(europeanEngine)
    killDate = today + ql.Period(i - 1, ql.Weeks)
    ql.Settings.instance().evaluationDate = killDate
    underlying.setValue(barrier)
    portfolioValue = portfolio3.NPV()
    putValue = putn.NPV()
    notional = portfolioValue / putValue
    portfolio3.subtract(putn, notional)

ql.Settings.instance().evaluationDate = today
underlying.setValue(underlyingValue)
portfolioValue = portfolio3.NPV()
error = portfolioValue - referenceValue
tab1.add_row(["Replicating portfolio (52 dates)", portfolioValue, error])

# Now we modify the market condition to see whether the
# replication holds. First, we change the underlying value so
# that the option is out of the money.

print(tab1)

print("Modified market conditions: out of the money")

underlying.setValue(110.0)

referenceValue = referenceOption.NPV()

tab2.add_row(["Original barrier option", referenceValue, "N/A"])
portfolioValue = portfolio1.NPV()
error = portfolioValue - referenceValue
tab2.add_row(["Replicating portfolio (12 dates)", portfolioValue, error])
portfolioValue = portfolio2.NPV()
error = portfolioValue - referenceValue
tab2.add_row(["Replicating portfolio (26 dates)", portfolioValue, error])
portfolioValue = portfolio3.NPV()
error = portfolioValue - referenceValue
tab2.add_row(["Replicating portfolio (52 dates)", portfolioValue, error])

print(tab2)

# Next, we change the underlying value so that the option is
# in the money.

print("Modified market conditions: in the money")

underlying.setValue(90.0)

referenceValue = referenceOption.NPV()

tab3.add_row(["Original barrier option", referenceValue, "N/A"])
portfolioValue = portfolio1.NPV()
error = portfolioValue - referenceValue
tab3.add_row(["Replicating portfolio (12 dates)", portfolioValue, error])
portfolioValue = portfolio2.NPV()
error = portfolioValue - referenceValue
tab3.add_row(["Replicating portfolio (26 dates)", portfolioValue, error])
portfolioValue = portfolio3.NPV()
error = portfolioValue - referenceValue
tab3.add_row(["Replicating portfolio (52 dates)", portfolioValue, error])

print(tab3)

# Finally, a word of warning for those (shame on them) who
# run the example but do not read the code.

print("The replication seems to be less robust when volatility and \n"
      "risk-free rate are changed. Feel free to experiment with \n"
      "the example and contribute a patch if you spot any errors.")

'''
===========================================================================
Initial market conditions
===========================================================================
Option                                       NPV            Error          
---------------------------------------------------------------------------
Original barrier option                      4.260726       N/A            
Replicating portfolio (12 dates)             4.322358       0.061632       
Replicating portfolio (26 dates)             4.295464       0.034738       
Replicating portfolio (52 dates)             4.280909       0.020183       
===========================================================================
Modified market conditions: out of the money
===========================================================================
Option                                       NPV            Error          
---------------------------------------------------------------------------
Original barrier option                      2.513058       N/A            
Replicating portfolio (12 dates)             2.539365       0.026307       
Replicating portfolio (26 dates)             2.528362       0.015304       
Replicating portfolio (52 dates)             2.522105       0.009047       
===========================================================================
Modified market conditions: in the money
===========================================================================
Option                                       NPV            Error          
---------------------------------------------------------------------------
Original barrier option                      5.739125       N/A            
Replicating portfolio (12 dates)             5.851239       0.112114       
Replicating portfolio (26 dates)             5.799867       0.060742       
Replicating portfolio (52 dates)             5.773678       0.034553       
===========================================================================

The replication seems to be less robust when volatility and 
risk-free rate are changed. Feel free to experiment with 
the example and contribute a patch if you spot any errors.
'''
