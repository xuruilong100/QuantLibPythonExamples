import QuantLib as ql
import prettytable as pt

# set up dates
calendar = ql.TARGET()
todaysDate = ql.Date(15, ql.May, 1998)
settlementDate = ql.Date(17, ql.May, 1998)
ql.Settings.instance().evaluationDate = todaysDate

# our options
optType = ql.Option.Put
underlying = 36.0
strike = 40.0
dividendYield = 0.00
riskFreeRate = 0.06
volatility = 0.20
maturity = ql.Date(17, ql.May, 1999)
dayCounter = ql.Actual365Fixed()

print('Option type =', optType)
print('Maturity =', maturity)
print('Underlying price =', underlying)
print('Strike =', strike)
print('Risk-free interest rate =', '{0:%}'.format(riskFreeRate))
print('Dividend yield =', '{0:%}'.format(dividendYield))
print('Volatility =', '{0:%}'.format(volatility))
print()

# show table

tab = pt.PrettyTable(['Method', 'European', 'Bermudan', 'American'])

exerciseDates = ql.DateVector()
for i in range(1, 5):
    exerciseDates.push_back(settlementDate + ql.Period(3 * i, ql.Months))

# exerciseDates = [settlementDate+ql.Period(3*i,ql.Months) for i in range(1,5)]

europeanExercise = ql.EuropeanExercise(maturity)
bermudanExercise = ql.BermudanExercise(exerciseDates)
americanExercise = ql.AmericanExercise(settlementDate, maturity)
underlyingH = ql.QuoteHandle(ql.SimpleQuote(underlying))

# bootstrap the yield/dividend/vol curves
flatTermStructure = ql.YieldTermStructureHandle(
    ql.FlatForward(settlementDate, riskFreeRate, dayCounter))
flatDividendTS = ql.YieldTermStructureHandle(
    ql.FlatForward(settlementDate, dividendYield, dayCounter))
flatVolTS = ql.BlackVolTermStructureHandle(
    ql.BlackConstantVol(
        settlementDate, calendar, volatility, dayCounter))
payoff = ql.PlainVanillaPayoff(optType, strike)
bsmProcess = ql.BlackScholesMertonProcess(
    underlyingH, flatDividendTS, flatTermStructure, flatVolTS)

# options
europeanOption = ql.VanillaOption(payoff, europeanExercise)
bermudanOption = ql.VanillaOption(payoff, bermudanExercise)
americanOption = ql.VanillaOption(payoff, americanExercise)

# Analytic formulas:

# Black-Scholes for European
method = 'Black-Scholes'
europeanOption.setPricingEngine(
    ql.AnalyticEuropeanEngine(bsmProcess))
tab.add_row([method, europeanOption.NPV(), 'N/A', 'N/A'])

# semi-analytic Heston for European
method = 'Heston semi-analytic'
hestonProcess = ql.HestonProcess(
    flatTermStructure, flatDividendTS, underlyingH,
    volatility * volatility, 1.0, volatility * volatility, 0.001, 0.0)
hestonModel = ql.HestonModel(hestonProcess)
europeanOption.setPricingEngine(
    ql.AnalyticHestonEngine(hestonModel))
tab.add_row([method, europeanOption.NPV(), 'N/A', 'N/A'])

# semi-analytic Bates for European
method = 'Bates semi-analytic'
batesProcess = ql.BatesProcess(
    flatTermStructure, flatDividendTS, underlyingH,
    volatility * volatility, 1.0, volatility * volatility,
    0.001, 0.0, 1e-14, 1e-14, 1e-14)
batesModel = ql.BatesModel(batesProcess)
europeanOption.setPricingEngine(
    ql.BatesEngine(batesModel))
tab.add_row([method, europeanOption.NPV(), 'N/A', 'N/A'])

# Barone-Adesi and Whaley approximation for American
method = 'Barone-Adesi/Whaley'
americanOption.setPricingEngine(
    ql.BaroneAdesiWhaleyEngine(bsmProcess))
tab.add_row([method, 'N/A', 'N/A', americanOption.NPV()])

# Bjerksund and Stensland approximation for American
method = 'Bjerksund/Stensland'
americanOption.setPricingEngine(
    ql.BjerksundStenslandEngine(bsmProcess))
tab.add_row([method, 'N/A', 'N/A', americanOption.NPV()])

# Integral
method = 'Integral'
europeanOption.setPricingEngine(
    ql.IntegralEngine(bsmProcess))
tab.add_row([method, europeanOption.NPV(), 'N/A', 'N/A'])

# Finite differences
timeSteps = 801
method = 'Finite differences'
fdengine = ql.FdBlackScholesVanillaEngine(bsmProcess, timeSteps, timeSteps - 1)
europeanOption.setPricingEngine(fdengine)
bermudanOption.setPricingEngine(fdengine)
americanOption.setPricingEngine(fdengine)
tab.add_row([method, europeanOption.NPV(), bermudanOption.NPV(), americanOption.NPV()])

# Binomial method: Jarrow-Rudd
method = 'Binomial Jarrow-Rudd'
jrengine = ql.BinomialJRVanillaEngine(bsmProcess, timeSteps)
europeanOption.setPricingEngine(jrengine)
bermudanOption.setPricingEngine(jrengine)
americanOption.setPricingEngine(jrengine)
tab.add_row([method, europeanOption.NPV(), bermudanOption.NPV(), americanOption.NPV()])

# Binomial method: Cox-Ross-Rubinstein
method = 'Binomial Cox-Ross-Rubinstein'
crrengine = ql.BinomialCRRVanillaEngine(bsmProcess, timeSteps)
europeanOption.setPricingEngine(crrengine)
bermudanOption.setPricingEngine(crrengine)
americanOption.setPricingEngine(crrengine)
tab.add_row([method, europeanOption.NPV(), bermudanOption.NPV(), americanOption.NPV()])

# Binomial method: Additive equiprobabilities
method = 'Additive equiprobabilities'
eqpengine = ql.BinomialEQPVanillaEngine(bsmProcess, timeSteps)
europeanOption.setPricingEngine(eqpengine)
bermudanOption.setPricingEngine(eqpengine)
americanOption.setPricingEngine(eqpengine)
tab.add_row([method, europeanOption.NPV(), bermudanOption.NPV(), americanOption.NPV()])

# Binomial method: Binomial Trigeorgis
method = 'Binomial Trigeorgis'
trengine = ql.BinomialTrigeorgisVanillaEngine(bsmProcess, timeSteps)
europeanOption.setPricingEngine(trengine)
bermudanOption.setPricingEngine(trengine)
americanOption.setPricingEngine(trengine)
tab.add_row([method, europeanOption.NPV(), bermudanOption.NPV(), americanOption.NPV()])

# Binomial method: Binomial Tian
method = 'Binomial Tian'
tiengine = ql.BinomialTianVanillaEngine(bsmProcess, timeSteps)
europeanOption.setPricingEngine(tiengine)
bermudanOption.setPricingEngine(tiengine)
americanOption.setPricingEngine(tiengine)
tab.add_row([method, europeanOption.NPV(), bermudanOption.NPV(), americanOption.NPV()])

# Binomial method: Binomial Leisen-Reimer
method = 'Binomial Leisen-Reimer'
lrengine = ql.BinomialLRVanillaEngine(bsmProcess, timeSteps)
europeanOption.setPricingEngine(lrengine)
bermudanOption.setPricingEngine(lrengine)
americanOption.setPricingEngine(lrengine)
tab.add_row([method, europeanOption.NPV(), bermudanOption.NPV(), americanOption.NPV()])

# Binomial method: Binomial Joshi
method = 'Binomial Joshi'
j4engine = ql.BinomialJ4VanillaEngine(bsmProcess, timeSteps)
europeanOption.setPricingEngine(j4engine)
bermudanOption.setPricingEngine(j4engine)
americanOption.setPricingEngine(j4engine)
tab.add_row([method, europeanOption.NPV(), bermudanOption.NPV(), americanOption.NPV()])

timeSteps = 1
# Monte Carlo Method: MC (crude)
method = 'MC (crude)'
mcSeed = 42
mcengine1 = ql.MCPREuropeanEngine(
    bsmProcess,
    timeSteps=timeSteps,
    requiredTolerance=0.02,
    seed=mcSeed)
# mcengine1 = ql.MCEuropeanEngine(
#     bsmProcess,
#     'PseudoRandom',
#     timeSteps=timeSteps,
#     requiredTolerance=0.02,
#     seed=mcSeed)

europeanOption.setPricingEngine(mcengine1)
tab.add_row([method, europeanOption.NPV(), 'N/A', 'N/A'])

# Monte Carlo Method: QMC (Sobol)
method = 'QMC (Sobol)'
nSamples = 32768  # 2^15
mcengine2 = ql.MCLDEuropeanEngine(
    bsmProcess,
    timeSteps=timeSteps,
    requiredSamples=nSamples)
# mcengine2 = ql.MCEuropeanEngine(
#     bsmProcess,
#     'LowDiscrepancy',
#     timeSteps=timeSteps,
#     requiredSamples=nSamples)
europeanOption.setPricingEngine(mcengine2)
tab.add_row([method, europeanOption.NPV(), 'N/A', 'N/A'])

# Monte Carlo Method: MC (Longstaff Schwartz)
method = 'MC (Longstaff Schwartz)'
mcengine3 = ql.MCPRAmericanEngine(
    bsmProcess,
    timeSteps=100,
    antitheticVariate=True,
    nCalibrationSamples=4096,
    requiredTolerance=0.02,
    seed=mcSeed)
# mcengine3 = ql.MCAmericanEngine(
#     bsmProcess,
#     'PseudoRandom',
#     timeSteps=100,
#     antitheticVariate=True,
#     nCalibrationSamples=4096,
#     requiredTolerance=0.02,
#     seed=mcSeed)
americanOption.setPricingEngine(mcengine3)
tab.add_row([method, 'N/A', 'N/A', americanOption.NPV()])

tab.float_format = '.6'
tab.align = 'l'
print(tab)

'''
Option type = Put
Maturity = May 17th, 1999
Underlying price = 36
Strike = 40
Risk-free interest rate = 6.000000 %
Dividend yield = 0.000000 %
Volatility = 20.000000 %


Method                             European      Bermudan      American      
Black-Scholes                      3.844308      N/A           N/A           
Heston semi-analytic               3.844306      N/A           N/A           
Bates semi-analytic                3.844306      N/A           N/A           
Barone-Adesi/Whaley                N/A           N/A           4.459628      
Bjerksund/Stensland                N/A           N/A           4.453064      
Integral                           3.844309      N/A           N/A           
Finite differences                 3.844330      4.360765      4.486113      
Binomial Jarrow-Rudd               3.844132      4.361174      4.486552      
Binomial Cox-Ross-Rubinstein       3.843504      4.360861      4.486415      
Additive equiprobabilities         3.836911      4.354455      4.480097      
Binomial Trigeorgis                3.843557      4.360909      4.486461      
Binomial Tian                      3.844171      4.361176      4.486413      
Binomial Leisen-Reimer             3.844308      4.360713      4.486076      
Binomial Joshi                     3.844308      4.360713      4.486076      
MC (crude)                         3.834522      N/A           N/A           
QMC (Sobol)                        3.844613      N/A           N/A           
MC (Longstaff Schwartz)            N/A           N/A           4.456935      
'''
