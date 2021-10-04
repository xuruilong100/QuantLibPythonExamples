import QuantLib as ql
import prettytable as pt


def printBasket(basket):
    tab = pt.PrettyTable(
        ['Expiry', 'Maturity', 'Nominal', 'Rate', 'Pay/Rec', 'Market ivol'])

    for j in range(len(basket)):
        helper = ql.as_swaption_helper(basket[j])

        endDate = helper.underlyingSwap().fixedSchedule().dates()[-1]  # .back()
        nominal = helper.underlyingSwap().nominal()
        vol = helper.volatility().value()
        rate = helper.underlyingSwap().fixedRate()
        expiry = helper.swaption().exercise().date(0)
        typeSwap = helper.swaption().type()

        tab.add_row(
            [expiry.to_date(), endDate.to_date(), nominal, rate,
             "Payer" if typeSwap == ql.VanillaSwap.Payer else "Receiver",
             vol])

    tab.float_format = '.6'
    print(tab)


def printModelCalibration(basket,
                          volatility):
    tab = pt.PrettyTable(
        ['Expiry', 'Model sigma', 'Model price',
         'market price', 'Model ivol', 'Market ivol'])

    for j in range(len(basket)):
        helper = ql.as_swaption_helper(basket[j])
        expiry = helper.swaption().exercise().date(0)

        tab.add_row(
            [expiry.to_date(),
             volatility[j],
             basket[j].modelValue(),
             basket[j].marketValue(),
             basket[j].impliedVolatility(
                 basket[j].modelValue(), 1E-6, 1000, 0.0, 2.0),
             basket[j].volatility().value()])

    tab.float_format = '.6'
    print(tab)

    if len(volatility) > len(basket):  # // only for markov model
        print(volatility.back())


print('Gaussian1dModel Examples')
print("\nThis is some example code showing how to use the GSR"
      "\n(Gaussian short rate) and Markov Functional model.")

refDate = ql.Date(30, ql.April, 2014)
ql.Settings.instance().evaluationDate = refDate
print('The evaluation date for this example is set to',
      ql.Settings.instance().evaluationDate)

forward6mLevel = 0.025
oisLevel = 0.02

forward6mQuote = ql.QuoteHandle(ql.SimpleQuote(forward6mLevel))
oisQuote = ql.QuoteHandle(ql.SimpleQuote(oisLevel))

yts6m = ql.YieldTermStructureHandle(
    ql.FlatForward(
        0, ql.TARGET(), forward6mQuote, ql.Actual365Fixed()))
ytsOis = ql.YieldTermStructureHandle(
    ql.FlatForward(
        0, ql.TARGET(), oisQuote, ql.Actual365Fixed()))

euribor6m = ql.Euribor(ql.Period(6, ql.Months), yts6m)

print("\nWe assume a multicurve setup, for simplicity with flat yield"
      "\nterm structures. The discounting curve is an Eonia curve at"
      "\na level of",
      oisLevel,
      "and the forwarding curve is an Euribior 6m curve"
      "\nat a level of",
      forward6mLevel)

volLevel = 0.20

volQuote = ql.QuoteHandle(ql.SimpleQuote(volLevel))
swaptionVol = ql.SwaptionVolatilityStructureHandle(
    ql.ConstantSwaptionVolatility(
        0, ql.TARGET(), ql.ModifiedFollowing, volQuote, ql.Actual365Fixed()))

print("\nFor the volatility we assume a flat swaption volatility at", volLevel)

strike = 0.04

print("\nWe consider a standard 10y bermudan payer swaption"
      "\nwith yearly exercises at a strike of",
      strike)

effectiveDate = ql.TARGET().advance(
    refDate, ql.Period(2, ql.Days))
maturityDate = ql.TARGET().advance(
    effectiveDate, ql.Period(10, ql.Years))

fixedSchedule = ql.Schedule(
    effectiveDate,
    maturityDate,
    ql.Period(1, ql.Years),
    ql.TARGET(),
    ql.ModifiedFollowing,
    ql.ModifiedFollowing,
    ql.DateGeneration.Forward,
    False)
floatingSchedule = ql.Schedule(
    effectiveDate,
    maturityDate,
    ql.Period(6, ql.Months),
    ql.TARGET(),
    ql.ModifiedFollowing,
    ql.ModifiedFollowing,
    ql.DateGeneration.Forward,
    False)

underlying = ql.NonstandardSwap(
    ql.VanillaSwap(
        ql.VanillaSwap.Payer,
        1.0, fixedSchedule,
        strike, 
        ql.Thirty360(
            ql.Thirty360.BondBasis),
        floatingSchedule,
        euribor6m, 0.00,
        ql.Actual360()))

exerciseDates = ql.DateVector()
for i in range(1, 10):
    exerciseDates.push_back(
        ql.TARGET().advance(
            fixedSchedule[i], ql.Period(-2, ql.Days)))

exercise = ql.BermudanExercise(exerciseDates, False)
swaption = ql.NonstandardSwaption(underlying, exercise)

print("\nThe model is a one factor Hull White model with piecewise"
      "\nvolatility adapted to our exercise dates.")

stepDates = exerciseDates[0:-1]
sigmas = ql.DoubleVector(len(stepDates) + 1, 0.01)
reversion = 0.01

print("\nThe reversion is just kept constant at a level of", reversion)

print("\nThe model's curve is set to the 6m forward curve. Note that"
      "\nthe model adapts automatically to other curves where appropriate"
      "\n(e.g. if an index requires a different forwarding curve) or"
      "\nwhere explicitly specified (e.g. in a swaption pricing engine).")

gsr = ql.Gsr(
    yts6m, stepDates, sigmas, reversion)

swaptionEngine = ql.Gaussian1dSwaptionEngine(
    gsr, 64, 7.0, True, False, ytsOis)

nonstandardSwaptionEngine = ql.Gaussian1dNonstandardSwaptionEngine(
    gsr, 64, 7.0, True, False, ql.QuoteHandle(), ytsOis)

swaption.setPricingEngine(nonstandardSwaptionEngine)

print("\nThe engine can generate a calibration basket in two modes."
      "\nThe first one is called Naive and generates ATM swaptions adapted to"
      "\nthe exercise dates of the swaption and its maturity date")

print("\nThe resulting basket looks as follows:")

swapBase = ql.EuriborSwapIsdaFixA(
    ql.Period(10, ql.Years), yts6m, ytsOis)

basket = swaption.calibrationBasket(
    swapBase, swaptionVol.currentLink(),
    ql.BasketGeneratingEngine.Naive)

printBasket(basket)

print("\nLet's calibrate our model to this basket. We use a specialized"
      "\ncalibration method calibrating the sigma function one by one to"
      "\nthe calibrating vanilla swaptions. The result of this is as follows:")

for i in range(len(basket)):
    basket[i].setPricingEngine(swaptionEngine)

method = ql.LevenbergMarquardt()
ec = ql.EndCriteria(
    1000, 10, 1E-8, 1E-8, 1E-8)

gsr.calibrateVolatilitiesIterative(basket, method, ec)

printModelCalibration(basket, gsr.volatility())

print("\nFinally we price our bermudan swaption in the calibrated model:")

npv = swaption.NPV()

print("\nBermudan swaption NPV (ATM calibrated GSR) =", npv)

print("\nThere is another mode to generate a calibration basket called"
      "\nMaturityStrikeByDeltaGamma. This means that the maturity,"
      "\nthe strike and the nominal of the calibrating swaptions are"
      "\nobtained matching the NPV, first derivative and second derivative"
      "\nof the swap you will exercise into at at each bermudan call date."
      "\nThe derivatives are taken with respect to the model's state variable."
      "\nLet's try this in our case.")

basket = swaption.calibrationBasket(
    swapBase, swaptionVol.currentLink(),
    ql.BasketGeneratingEngine.MaturityStrikeByDeltaGamma)

printBasket(basket)

print("\nThe calibrated nominal is close to the exotics nominal."
      "\nThe expiries and maturity dates of the vanillas are the same"
      "\nas in the case above. The difference is the strike which"
      "\nis now equal to the exotics strike.")

print("\nLet's see how this affects the exotics npv. The"
      "\nrecalibrated model is:")

for i in range(len(basket)):
    basket[i].setPricingEngine(swaptionEngine)

gsr.calibrateVolatilitiesIterative(basket, method, ec)

printModelCalibration(basket, gsr.volatility())

print("\nAnd the bermudan's price becomes:")

npv = swaption.NPV()

print("\nBermudan swaption NPV (deal strike calibrated GSR) =", npv)

print("\nWe can do more complicated things, let's e.g. modify the"
      "\nnominal schedule to be linear amortizing and see what"
      "\nthe effect on the generated calibration basket is:")

nominalFixed = ql.DoubleVector()
nominalFloating = ql.DoubleVector()

for i in range(len(fixedSchedule) - 1):
    tmpNom = 1.0 - float(i / (len(fixedSchedule) - 1))
    nominalFixed.push_back(tmpNom)
    nominalFloating.push_back(tmpNom)
    nominalFloating.push_back(
        tmpNom)  # // we use that the swap is 6m vs. 1y here

strikes = ql.DoubleVector(len(nominalFixed), strike)

underlying2 = ql.NonstandardSwap(
    ql.VanillaSwap.Payer,
    nominalFixed, nominalFloating,
    fixedSchedule,
    strikes, ql.Thirty360(ql.Thirty360.BondBasis),
    floatingSchedule, euribor6m, 1.0, 0.0,
    ql.Actual360())

swaption2 = ql.NonstandardSwaption(underlying2, exercise)

swaption2.setPricingEngine(nonstandardSwaptionEngine)

basket = swaption2.calibrationBasket(
    swapBase, swaptionVol.currentLink(),
    ql.BasketGeneratingEngine.MaturityStrikeByDeltaGamma)

printBasket(basket)

print("\nThe notional is weighted over the underlying exercised"
      "\ninto and the maturity is adjusted downwards. The rate"
      "\non the other hand is not affected.")

print("\nYou can also price exotic bond's features. If you have e.g. a"
      "\nbermudan callable fixed bond you can set up the call right"
      "\nas a swaption to enter into a one leg swap with notional"
      "\nreimbursement at maturity."
      "\nThe exercise should then be written as a rebated exercise"
      "\npaying the notional in case of exercise.")

nominalFixed2 = ql.DoubleVector(len(nominalFixed), 1.0)
nominalFloating2 = ql.DoubleVector(len(nominalFloating), 0.0)  # // null the second leg

underlying3 = ql.NonstandardSwap(
    ql.VanillaSwap.Receiver,
    nominalFixed2, nominalFloating2,
    fixedSchedule, strikes,
    ql.Thirty360(ql.Thirty360.BondBasis), floatingSchedule,
    euribor6m, 1.0, 0.0, ql.Actual360(),
    False, True)  # // final capital exchange

exercise2 = ql.RebatedExercise(exercise, -1.0, 2, ql.TARGET())

swaption3 = ql.NonstandardSwaption(underlying3, exercise2)

oas0 = ql.SimpleQuote(0.0)
oas100 = ql.SimpleQuote(0.01)

oas = ql.RelinkableQuoteHandle(oas0)

nonstandardSwaptionEngine2 = ql.Gaussian1dNonstandardSwaptionEngine(
    gsr, 64, 7.0, True, False, oas)
# // change discounting to 6m

swaption3.setPricingEngine(nonstandardSwaptionEngine2)

basket = swaption3.calibrationBasket(
    swapBase, swaptionVol.currentLink(),
    ql.BasketGeneratingEngine.MaturityStrikeByDeltaGamma)

printBasket(basket)

print("\nNote that nominals are not exactly 1.0 here. This is"
      "\nbecause we do our bond discounting on 6m level while"
      "\nthe swaptions are still discounted on OIS level."
      "\n(You can try this by changing the OIS level to the"
      "\n6m level, which will produce nominals near 1.0)."
      "\nThe npv of the call right is (after recalibrating the model)")

for i in range(len(basket)):
    basket[i].setPricingEngine(swaptionEngine)

gsr.calibrateVolatilitiesIterative(basket, method, ec)
npv3 = swaption3.NPV()

print("\nBond's bermudan call right npv =", npv3)

print("\nUp to now, no credit spread is included in the pricing."
      "\nWe can do so by specifying an oas in the pricing engine."
      "\nLet's set the spread level to 100bp and regenerate"
      "\nthe calibration basket.")

oas.linkTo(oas100)

basket = swaption3.calibrationBasket(
    swapBase, swaptionVol.currentLink(),
    ql.BasketGeneratingEngine.MaturityStrikeByDeltaGamma)

printBasket(basket)

print("\nThe adjusted basket takes the credit spread into account."
      "\nThis is consistent to a hedge where you would have a"
      "\nmargin on the float leg around 100bp,too.")

print("\nThe npv becomes:")

for i in range(len(basket)):
    basket[i].setPricingEngine(swaptionEngine)

gsr.calibrateVolatilitiesIterative(basket, method, ec)
npv4 = swaption3.NPV()

print("\nBond's bermudan call right npv (oas = 100bp) =", npv4)

print("\nThe next instrument we look at is a CMS 10Y vs Euribor"
      "\n6M swaption. The maturity is again 10 years and the option"
      "\nis exercisable on a yearly basis")

underlying4 = ql.FloatFloatSwap(
    ql.VanillaSwap.Payer, 1.0, 1.0,
    fixedSchedule, swapBase,
    ql.Thirty360(ql.Thirty360.BondBasis), floatingSchedule,
    euribor6m, ql.Actual360(), False,
    False, 1.0, 0.0, ql.NullReal(),
    ql.NullReal(), 1.0, 0.0010)

swaption4 = ql.FloatFloatSwaption(underlying4, exercise)

floatSwaptionEngine = ql.Gaussian1dFloatFloatSwaptionEngine(
    gsr, 64, 7.0, True, False,
    ql.QuoteHandle(), ytsOis, True)

swaption4.setPricingEngine(floatSwaptionEngine)

print("\nSince the underlying is quite exotic already, we start with"
      "\npricing this using the LinearTsrPricer for CMS coupon estimation")

reversionQuote = ql.QuoteHandle(ql.SimpleQuote(reversion))

leg0 = underlying4.leg(0)
leg1 = underlying4.leg(1)

cmsPricer = ql.LinearTsrPricer(swaptionVol, reversionQuote)
iborPricer = ql.BlackIborCouponPricer()

ql.setCouponPricer(leg0, cmsPricer)
ql.setCouponPricer(leg1, iborPricer)

swapPricer = ql.DiscountingSwapEngine(ytsOis)

underlying4.setPricingEngine(swapPricer)
npv5 = underlying4.NPV()

print("Underlying CMS Swap NPV =", npv5)
print("      CMS     Leg  NPV =", underlying4.legNPV(0))
print("      Euribor Leg  NPV =", underlying4.legNPV(1))

print("\nWe generate a naive calibration basket and calibrate"
      "\nthe GSR model to it:")

basket = swaption4.calibrationBasket(
    swapBase, swaptionVol.currentLink(),
    ql.BasketGeneratingEngine.Naive)

for i in range(len(basket)):
    basket[i].setPricingEngine(swaptionEngine)

gsr.calibrateVolatilitiesIterative(basket, method, ec)

printBasket(basket)
printModelCalibration(basket, gsr.volatility())

print("\nThe npv of the bermudan swaption is")

npv6 = swaption4.NPV()

print("\nFloat swaption NPV (GSR) =", npv6)

print("\nIn this case it is also interesting to look at the"
      "\nunderlying swap npv in the GSR model.")

print("\nFloat swap NPV (GSR) =", swaption4.underlyingValue())

print("\nNot surprisingly, the underlying is priced differently"
      "\ncompared to the LinearTsrPricer, since a different"
      "\nsmile is implied by the GSR model.")

print("\nThis is exactly where the Markov functional model"
      "\ncomes into play, because it can calibrate to any"
      "\ngiven underlying smile (as long as it is arbitrage"
      "\nfree). We try this now. Of course the usual use case"
      "\nis not to calibrate to a flat smile as in our simple"
      "\nexample, still it should be possible, of course...")

markovStepDates = exerciseDates
cmsFixingDates = markovStepDates
markovSigmas = ql.DoubleVector(len(markovStepDates) + 1, 0.01)
tenors = ql.PeriodVector(
    len(cmsFixingDates), ql.Period(10, ql.Years))

settings = ql.MarkovFunctionalSettings()
settings.withYGridPoints(16)

markov = ql.MarkovFunctional(
    yts6m, reversion, markovStepDates,
    markovSigmas, swaptionVol,
    cmsFixingDates, tenors, swapBase,
    settings)

swaptionEngineMarkov = ql.Gaussian1dSwaptionEngine(
    markov, 8, 5.0, True, False, ytsOis)

floatEngineMarkov = ql.Gaussian1dFloatFloatSwaptionEngine(
    markov, 16, 7.0, True, False,
    ql.QuoteHandle(), ytsOis, True)

swaption4.setPricingEngine(floatEngineMarkov)

npv7 = swaption4.NPV()

print("\nThe option npv is the markov model is:")

print("\nFloat swaption NPV (Markov) =", npv7)

print("\nThis is not too far from the GSR price.")

print("\nMore interesting is the question how well the Markov"
      "\nmodel did its job to match our input smile. For this"
      "\nwe look at the underlying npv under the Markov model")

print("\nFloat swap NPV (Markov) =", swaption4.underlyingValue())

print("\nThis is closer to our terminal swap rate model price."
      "\nA perfect match is not expected anyway, because the"
      "\ndynamics of the underlying rate in the linear"
      "\nmodel is different from the Markov model, of"
      "\ncourse.")

print("\nThe Markov model can not only calibrate to the"
      "\nunderlying smile, but has at the same time a"
      "\nsigma function (similar to the GSR model) which"
      "\ncan be used to calibrate to a second instrument"
      "\nset. We do this here to calibrate to our coterminal"
      "\nATM swaptions from above.")

print("\nThis is a computationally demanding task, so"
      "\ndepending on your machine, this may take a"
      "\nwhile now...")

for i in range(len(basket)):
    basket[i].setPricingEngine(swaptionEngineMarkov)

markov.calibrate(basket, method, ec)

printModelCalibration(basket, markov.volatility())

print("\nNow let's have a look again at the underlying pricing."
      "\nIt shouldn't have changed much, because the underlying"
      "\nsmile is still matched.")

npv8 = swaption4.underlyingValue()

print("\nFloat swap NPV (Markov) =", npv8)

print("\nThis is close to the previous value as expected.")

print("\nAs a final remark we note that the calibration to"
      "\ncoterminal swaptions is not particularly reasonable"
      "\nhere, because the european call rights are not"
      "\nwell represented by these swaptions."
      "\nSecondly, our CMS swaption is sensitive to the"
      "\ncorrelation between the 10y swap rate and the"
      "\nEuribor 6M rate. Since the Markov model is one factor"
      "\nit will most probably underestimate the market value"
      "\nby construction.")

print("\nThat was it. Thank you for running this demo. Bye.")

'''
Gaussian1dModel Examples

This is some example code showing how to use the GSR 
(Gaussian short rate) and Markov Functional model.

The evaluation date for this example is set to April 30th, 2014

We assume a multicurve setup, for simplicity with flat yield 
term structures. The discounting curve is an Eonia curve at
a level of 0.02 and the forwarding curve is an Euribior 6m curve
at a level of 0.025

For the volatility we assume a flat swaption volatility at 0.2

We consider a standard 10y bermudan payer swaption 
with yearly exercises at a strike of 0.04

The model is a one factor Hull White model with piecewise 
volatility adapted to our exercise dates.

The reversion is just kept constant at a level of 0.01

The model's curve is set to the 6m forward curve. Note that 
the model adapts automatically to other curves where appropriate 
(e.g. if an index requires a different forwarding curve) or 
where explicitly specified (e.g. in a swaption pricing engine).

The engine can generate a calibration basket in two modes.
The first one is called Naive and generates ATM swaptions adapted to
the exercise dates of the swaption and its maturity date

The resulting basket looks as follows:

Expiry              Maturity            Nominal             Rate          Pay/Rec     Market ivol   
==================================================================================================
April 30th, 2015    May 6th, 2024       1.000000            0.025307      Receiver    0.200000      
May 3rd, 2016       May 6th, 2024       1.000000            0.025300      Receiver    0.200000      
May 3rd, 2017       May 6th, 2024       1.000000            0.025303      Receiver    0.200000      
May 3rd, 2018       May 6th, 2024       1.000000            0.025306      Receiver    0.200000      
May 2nd, 2019       May 6th, 2024       1.000000            0.025311      Receiver    0.200000      
April 30th, 2020    May 6th, 2024       1.000000            0.025300      Receiver    0.200000      
May 3rd, 2021       May 6th, 2024       1.000000            0.025306      Receiver    0.200000      
May 3rd, 2022       May 6th, 2024       1.000000            0.025318      Receiver    0.200000      
May 3rd, 2023       May 6th, 2024       1.000000            0.025353      Receiver    0.200000      

Let's calibrate our model to this basket. We use a specialized
calibration method calibrating the sigma function one by one to
the calibrating vanilla swaptions. The result of this is as follows:

Expiry              Model sigma   Model price         market price        Model ivol    Market ivol   
====================================================================================================
April 30th, 2015    0.005178      0.016111            0.016111            0.199999      0.200000      
May 3rd, 2016       0.005156      0.020062            0.020062            0.200000      0.200000      
May 3rd, 2017       0.005149      0.021229            0.021229            0.200000      0.200000      
May 3rd, 2018       0.005129      0.020738            0.020738            0.200000      0.200000      
May 2nd, 2019       0.005132      0.019096            0.019096            0.200000      0.200000      
April 30th, 2020    0.005074      0.016537            0.016537            0.200000      0.200000      
May 3rd, 2021       0.005091      0.013253            0.013253            0.200000      0.200000      
May 3rd, 2022       0.005097      0.009342            0.009342            0.200000      0.200000      
May 3rd, 2023       0.005001      0.004910            0.004910            0.200000      0.200000      

Finally we price our bermudan swaption in the calibrated model:

Bermudan swaption NPV (ATM calibrated GSR) = 0.003808

There is another mode to generate a calibration basket called
MaturityStrikeByDeltaGamma. This means that the maturity,
the strike and the nominal of the calibrating swaptions are
obtained matching the NPV, first derivative and second derivative
of the swap you will exercise into at at each bermudan call date.
The derivatives are taken with respect to the model's state variable.
Let's try this in our case.

Expiry              Maturity            Nominal             Rate          Pay/Rec     Market ivol   
==================================================================================================
April 30th, 2015    May 6th, 2024       0.999977            0.040000      Payer       0.200000      
May 3rd, 2016       May 6th, 2024       1.000001            0.040000      Payer       0.200000      
May 3rd, 2017       May 6th, 2024       0.999999            0.040000      Payer       0.200000      
May 3rd, 2018       May 7th, 2024       0.999945            0.040000      Payer       0.200000      
May 2nd, 2019       May 6th, 2024       0.999909            0.040000      Payer       0.200000      
April 30th, 2020    May 6th, 2024       1.000000            0.040000      Payer       0.200000      
May 3rd, 2021       May 6th, 2024       1.000002            0.040000      Payer       0.200000      
May 3rd, 2022       May 6th, 2024       0.999994            0.040000      Payer       0.200000      
May 3rd, 2023       May 6th, 2024       1.000003            0.040000      Payer       0.200000      

The calibrated nominal is close to the exotics nominal.
The expiries and maturity dates of the vanillas are the same
as in the case above. The difference is the strike which
is now equal to the exotics strike.

Let's see how this affects the exotics npv. The 
recalibrated model is:

Expiry              Model sigma   Model price         market price        Model ivol    Market ivol   
====================================================================================================
April 30th, 2015    0.006508      0.000191            0.000191            0.200000      0.200000      
May 3rd, 2016       0.006502      0.001412            0.001412            0.200000      0.200000      
May 3rd, 2017       0.006480      0.002905            0.002905            0.200000      0.200000      
May 3rd, 2018       0.006464      0.004091            0.004091            0.200000      0.200000      
May 2nd, 2019       0.006422      0.004766            0.004766            0.200000      0.200000      
April 30th, 2020    0.006445      0.004869            0.004869            0.200000      0.200000      
May 3rd, 2021       0.006433      0.004433            0.004433            0.200000      0.200000      
May 3rd, 2022       0.006332      0.003454            0.003454            0.200000      0.200000      
May 3rd, 2023       0.006295      0.001973            0.001973            0.200000      0.200000      

And the bermudan's price becomes:

Bermudan swaption NPV (deal strike calibrated GSR) = 0.007627

We can do more complicated things, let's e.g. modify the
nominal schedule to be linear amortizing and see what
the effect on the generated calibration basket is:

Expiry              Maturity            Nominal             Rate          Pay/Rec     Market ivol   
==================================================================================================
April 30th, 2015    August 5th, 2021    0.719177            0.039998      Payer       0.200000      
May 3rd, 2016       December 6th, 2021  0.641956            0.040003      Payer       0.200000      
May 3rd, 2017       May 5th, 2022       0.564393            0.040005      Payer       0.200000      
May 3rd, 2018       September 7th, 2022 0.486533            0.040004      Payer       0.200000      
May 2nd, 2019       January 6th, 2023   0.409777            0.040008      Payer       0.200000      
April 30th, 2020    May 5th, 2023       0.334094            0.039994      Payer       0.200000      
May 3rd, 2021       September 5th, 2023 0.255766            0.039995      Payer       0.200000      
May 3rd, 2022       January 5th, 2024   0.177035            0.040031      Payer       0.200000      
May 3rd, 2023       May 6th, 2024       0.099999            0.040000      Payer       0.200000      

The notional is weighted over the underlying exercised 
into and the maturity is adjusted downwards. The rate
on the other hand is not affected.

You can also price exotic bond's features. If you have e.g. a
bermudan callable fixed bond you can set up the call right 
as a swaption to enter into a one leg swap with notional
reimbursement at maturity.
The exercise should then be written as a rebated exercise
paying the notional in case of exercise.

The calibration basket looks like this:

Expiry              Maturity            Nominal             Rate          Pay/Rec     Market ivol   
==================================================================================================
April 30th, 2015    April 5th, 2024     0.984119            0.039952      Payer       0.200000      
May 3rd, 2016       April 5th, 2024     0.985543            0.039952      Payer       0.200000      
May 3rd, 2017       May 6th, 2024       0.987047            0.039952      Payer       0.200000      
May 3rd, 2018       May 7th, 2024       0.988449            0.039952      Payer       0.200000      
May 2nd, 2019       May 6th, 2024       0.990031            0.039952      Payer       0.200000      
April 30th, 2020    May 6th, 2024       0.991627            0.039951      Payer       0.200000      
May 3rd, 2021       May 6th, 2024       0.993095            0.039951      Payer       0.200000      
May 3rd, 2022       May 6th, 2024       0.994202            0.039952      Payer       0.200000      
May 3rd, 2023       May 6th, 2024       0.996664            0.039949      Payer       0.200000      

Note that nominals are not exactly 1.0 here. This is
because we do our bond discounting on 6m level while
the swaptions are still discounted on OIS level.
(You can try this by changing the OIS level to the 
6m level, which will produce nominals near 1.0).
The npv of the call right is (after recalibrating the model)

Bond's bermudan call right npv = 0.115409

Up to now, no credit spread is included in the pricing.
We can do so by specifying an oas in the pricing engine.
Let's set the spread level to 100bp and regenerate
the calibration basket.

Expiry              Maturity            Nominal             Rate          Pay/Rec     Market ivol   
==================================================================================================
April 30th, 2015    February 5th, 2024  0.961306            0.029608      Payer       0.200000      
May 3rd, 2016       March 5th, 2024     0.965325            0.029605      Payer       0.200000      
May 3rd, 2017       April 5th, 2024     0.969529            0.029608      Payer       0.200000      
May 3rd, 2018       April 8th, 2024     0.973640            0.029610      Payer       0.200000      
May 2nd, 2019       April 8th, 2024     0.978116            0.029608      Payer       0.200000      
April 30th, 2020    May 6th, 2024       0.982678            0.029612      Payer       0.200000      
May 3rd, 2021       May 6th, 2024       0.987309            0.029609      Payer       0.200000      
May 3rd, 2022       May 6th, 2024       0.991354            0.029603      Payer       0.200000      
May 3rd, 2023       May 6th, 2024       0.996596            0.029586      Payer       0.200000      

The adjusted basket takes the credit spread into account.
This is consistent to a hedge where you would have a
margin on the float leg around 100bp,too.

The npv becomes:

Bond's bermudan call right npv (oas = 100bp) = 0.044980

The next instrument we look at is a CMS 10Y vs Euribor 
6M swaption. The maturity is again 10 years and the option
is exercisable on a yearly basis

Since the underlying is quite exotic already, we start with
pricing this using the LinearTsrPricer for CMS coupon estimation
Underlying CMS Swap NPV = 0.004447
       CMS     Leg  NPV = -0.231736
       Euribor Leg  NPV = 0.236183

We generate a naive calibration basket and calibrate 
the GSR model to it:

Expiry              Maturity            Nominal             Rate          Pay/Rec     Market ivol   
==================================================================================================
April 30th, 2015    May 6th, 2024       1.000000            0.025307      Receiver    0.200000      
May 3rd, 2016       May 6th, 2024       1.000000            0.025300      Receiver    0.200000      
May 3rd, 2017       May 6th, 2024       1.000000            0.025303      Receiver    0.200000      
May 3rd, 2018       May 6th, 2024       1.000000            0.025306      Receiver    0.200000      
May 2nd, 2019       May 6th, 2024       1.000000            0.025311      Receiver    0.200000      
April 30th, 2020    May 6th, 2024       1.000000            0.025300      Receiver    0.200000      
May 3rd, 2021       May 6th, 2024       1.000000            0.025306      Receiver    0.200000      
May 3rd, 2022       May 6th, 2024       1.000000            0.025318      Receiver    0.200000      
May 3rd, 2023       May 6th, 2024       1.000000            0.025353      Receiver    0.200000      

Expiry              Model sigma   Model price         market price        Model ivol    Market ivol   
====================================================================================================
April 30th, 2015    0.005178      0.016111            0.016111            0.200000      0.200000      
May 3rd, 2016       0.005156      0.020062            0.020062            0.200000      0.200000      
May 3rd, 2017       0.005149      0.021229            0.021229            0.200000      0.200000      
May 3rd, 2018       0.005129      0.020738            0.020738            0.200000      0.200000      
May 2nd, 2019       0.005132      0.019096            0.019096            0.200000      0.200000      
April 30th, 2020    0.005074      0.016537            0.016537            0.200000      0.200000      
May 3rd, 2021       0.005091      0.013253            0.013253            0.200000      0.200000      
May 3rd, 2022       0.005097      0.009342            0.009342            0.200000      0.200000      
May 3rd, 2023       0.005001      0.004910            0.004910            0.200000      0.200000      

The npv of the bermudan swaption is

Float swaption NPV (GSR) = 0.004291

In this case it is also interesting to look at the 
underlying swap npv in the GSR model.

Float swap NPV (GSR) = 0.005250

Not surprisingly, the underlying is priced differently
compared to the LinearTsrPricer, since a different
smile is implied by the GSR model.

This is exactly where the Markov functional model
comes into play, because it can calibrate to any
given underlying smile (as long as it is arbitrage
free). We try this now. Of course the usual use case
is not to calibrate to a flat smile as in our simple
example, still it should be possible, of course...

The option npv is the markov model is:

Float swaption NPV (Markov) = 0.003549

This is not too far from the GSR price.

More interesting is the question how well the Markov
model did its job to match our input smile. For this
we look at the underlying npv under the Markov model

Float swap NPV (Markov) = 0.004301

This is closer to our terminal swap rate model price.
A perfect match is not expected anyway, because the
dynamics of the underlying rate in the linear
model is different from the Markov model, of
course.

The Markov model can not only calibrate to the
underlying smile, but has at the same time a
sigma function (similar to the GSR model) which
can be used to calibrate to a second instrument
set. We do this here to calibrate to our coterminal
ATM swaptions from above.

This is a computationally demanding task, so
depending on your machine, this may take a
while now...

Expiry              Model sigma   Model price         market price        Model ivol    Market ivol   
====================================================================================================
April 30th, 2015    0.010000      0.016111            0.016111            0.199997      0.200000      
May 3rd, 2016       0.012276      0.020062            0.020062            0.200002      0.200000      
May 3rd, 2017       0.010535      0.021229            0.021229            0.200001      0.200000      
May 3rd, 2018       0.010414      0.020738            0.020738            0.200001      0.200000      
May 2nd, 2019       0.010361      0.019096            0.019096            0.199999      0.200000      
April 30th, 2020    0.010340      0.016537            0.016537            0.200001      0.200000      
May 3rd, 2021       0.010365      0.013253            0.013253            0.199999      0.200000      
May 3rd, 2022       0.010382      0.009342            0.009342            0.200001      0.200000      
May 3rd, 2023       0.010392      0.004910            0.004910            0.200000      0.200000      
                    0.009959

Now let's have a look again at the underlying pricing.
It shouldn't have changed much, because the underlying
smile is still matched.

Float swap NPV (Markov) = 0.004331

This is close to the previous value as expected.

As a final remark we note that the calibration to
coterminal swaptions is not particularly reasonable
here, because the european call rights are not
well represented by these swaptions.
Secondly, our CMS swaption is sensitive to the
correlation between the 10y swap rate and the
Euribor 6M rate. Since the Markov model is one factor
it will most probably underestimate the market value
by construction.

That was it. Thank you for running this demo. Bye.
Hit any key to continue...
'''
