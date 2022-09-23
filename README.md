# QuantLibPythonExamples

**MORE APIs, MORE examples, MORE test suites.**
-----------------------------------------------

## Introduction

* Reconstructing SWIG interface files for building Python wrapper.
* Reimplementing QuantLib [examples](https://www.quantlib.org/reference/examples.html) by Python.
* Reimplementing QuantLib [test-suite](https://github.com/lballabio/QuantLib/tree/master/test-suite) by Python.

> Related blog (in Chinese): <https://www.cnblogs.com/xuruilong100/p/13281006.html>
>
> Environment:
> * QuantLib: 1.27
> * swig: 4.0.2
> * icx, icpx: Intel(R) oneAPI DPC++/C++ Compiler 2022.1.0 (2022.1.0.20220316)
> * ubuntu: 22.04 LTS

---

## How to build Python wrapper

Open `../SWIGpy/` and run the following commands.

1. Generate `.cpp` file:

```
swig4.0 -w509 -c++ -python -outdir QuantLib -o QuantLib/ql_wrap.cpp quantlib.i
```

2. Compile `.cpp` file:

```
CC=icx CXX=icpx python3 setup.py build
```

3. Install Python wrapper:

```
python3 setup.py install
```

---

## Examples

* [ ] BasketLosses
* [x] BermudanSwaption
* [x] Bonds
* [ ] CallableBonds
* [ ] CDS
* [x] ConvertibleBonds
* [ ] CVAIRS
* [ ] DiscreteHedging
* [x] EquityOption
* [ ] FittedBondCurve
* [ ] FRA
* [x] Gaussian1dModels
* [ ] GlobalOptimizer
* [ ] LatentModel
* [ ] MarketModels
* [ ] MultidimIntegral
* [x] Replication
* [ ] Repo
* [x] MulticurveBootstrapping

---

## Test suites

* [x] americanoption
* [x] amortizingbond
* [x] andreasenhugevolatilityinterpl
* [x] array
* [x] asianoptions
* [x] assetswap
* [x] autocovariances
* [x] barrieroption
* [x] basismodels
* [x] basisswapratehelpers
* [x] basketoption
* [x] batesmodel
* [x] bermudanswaption
* [x] binaryoption
* [x] blackdeltacalculator
* [x] blackformula
* [x] bondforward
* [x] bonds
* [x] brownianbridge
* [x] businessdayconventions
* [x] calendars
* [x] callablebonds
* [x] capflooredcoupon
* [x] capfloor
* [x] cashflows
* [x] catbonds
* [ ] cdo
* [x] cdsoption
* [x] chooseroption
* [x] cliquetoption
* [x] cms
* [x] cmsspread
* [x] commodityunitofmeasure
* [x] compoundoption
* [x] convertiblebonds
* [x] covariance
* [x] creditdefaultswap
* [x] creditriskplus
* [x] crosscurrencyratehelpers
* [x] currency
* [x] curvestates
* [x] dates
* [x] daycounters
* [x] defaultprobabilitycurves
* [x] digitalcoupon
* [x] digitaloption
* [x] distributions
* [x] dividendoption
* [x] doublebarrieroption
* [x] doublebinaryoption
* [x] europeanoption
* [x] everestoption
* [x] exchangerate
* [x] extendedtrees
* [x] extensibleoptions
* [x] fastfouriertransform
* [x] fdcev
* [x] fdcir
* [x] fdheston
* [ ] fdmlinearop
* [x] fdsabr
* [x] fittedbonddiscountcurve
* [x] forwardoption
* [x] forwardrateagreement
* [x] functions
* [x] garch
* [x] gaussianquadratures
* [x] gjrgarchmodel
* [x] gsr
* [x] hestonmodel
* [x] hestonslvmodel
* [x] himalayaoption
* [x] hybridhestonhullwhiteprocess
* [x] indexes
* [x] inflation
* [x] inflationcapfloor
* [x] inflationcapflooredcoupon
* [x] inflationcpibond
* [x] inflationcpicapfloor
* [x] inflationcpiswap
* [x] inflationvolatility
* [x] inflationzciisinterpolation
* [x] instruments
* [x] integrals
* [x] interestrates
* [x] interpolations
* [x] jumpdiffusion
* [x] lazyobject
* [x] libormarketmodel
* [x] libormarketmodelprocess
* [ ] linearleastsquaresregression
* [x] lookbackoptions
* [x] lowdiscrepancysequences
* [x] margrabeoption
* [x] marketmodel_cms
* [x] marketmodel
* [x] marketmodel_smmcapletalphacalibration
* [x] marketmodel_smmcapletcalibration
* [x] marketmodel_smmcaplethomocalibration
* [x] marketmodel_smm
* [x] markovfunctional
* [x] matrices
* [x] mclongstaffschwartzengine
* [x] mersennetwister
* [x] money
* [x] noarbsabr
* [x] normalclvmodel
* [ ] nthorderderivativeop
* [ ] nthtodefault
* [x] numericaldifferentiation
* [ ] observable
* [ ] ode
* [x] operators
* [x] optimizers
* [x] optionletstripper
* [x] overnightindexedcoupon
* [x] overnightindexedswap
* [x] pagodaoption
* [x] partialtimebarrieroption
* [x] pathgenerator
* [x] period
* [x] piecewiseyieldcurve
* [x] piecewisezerospreadedtermstructure
* [x] quantooption
* [x] quotes
* [x] rangeaccrual
* [x] riskneutraldensitycalculator
* [x] riskstats
* [x] rngtraits
* [x] rounding
* [x] sampledcurve
* [x] schedule
* [x] settings
* [x] shortratemodels
* [x] sofrfutures
* [x] solvers
* [x] spreadoption
* [x] squarerootclvmodel
* [x] stats
* [x] subperiodcoupons
* [x] svivolatility
* [x] swap
* [x] swapforwardmappings
* [x] swaption
* [x] swaptionvolatilitycube
* [x] swaptionvolatilitymatrix
* [x] swingoption
* [x] termstructures
* [x] timegrid
* [x] timeseries
* [x] tqreigendecomposition
* [ ] tracing
* [x] transformedgrid
* [x] twoassetbarrieroption
* [x] twoassetcorrelationoption
* [x] ultimateforwardtermstructure
* [x] variancegamma
* [x] varianceoption
* [x] varianceswaps
* [x] volatilitymodels
* [x] vpp
* [x] zabr
* [x] zerocouponswap
