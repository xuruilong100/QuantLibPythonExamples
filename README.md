# QuantLibPythonExamples

**MORE APIs, MORE examples, MORE test suites.**
-----------------------------------------------

## Introduction

* Reconstructing SWIG interface files for building Python wrapper.
* Reimplementing of QuantLib [examples](https://www.quantlib.org/reference/examples.html) by Python.
* Reimplementing of QuantLib [test-suite](https://github.com/lballabio/QuantLib/tree/master/test-suite) by Python.

> Related blog (in Chinese): <https://www.cnblogs.com/xuruilong100/p/13281006.html>
>
> Environment:
> * QuantLib: 1.23
> * swig: 4.0.1
> * clang: 10.0.0-4ubuntu1
> * ubuntu: 20.04.2 LTS

---

## How to build Python wrapper

Open `../SWIGpy/` and run the following commands.

1. Generate `.cpp` file:

```
swig4.0 -c++ -python -outdir QuantLib -o QuantLib/ql_wrap.cpp SWIG/quantlib.i
```

2. Compile `.cpp` file:

```
CC=clang CXX=clang++ python3 setup.py build
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
* [ ] assetswap
* [ ] autocovariances
* [ ] barrieroption
* [ ] basismodels
* [ ] basketoption
* [ ] batesmodel
* [ ] bermudanswaption
* [ ] binaryoption
* [ ] blackdeltacalculator
* [ ] blackformula
* [ ] bonds
* [ ] brownianbridge
* [ ] businessdayconventions
* [ ] calendars
* [ ] callablebonds
* [ ] capflooredcoupon
* [ ] capfloor
* [ ] cashflows
* [ ] catbonds
* [ ] cdo
* [ ] cdsoption
* [ ] chooseroption
* [ ] cliquetoption
* [ ] cms
* [ ] cmsspread
* [ ] commodityunitofmeasure
* [ ] compiledboostversion
* [ ] compoundoption
* [ ] convertiblebonds
* [ ] covariance
* [ ] creditdefaultswap
* [ ] creditriskplus
* [ ] curvestates
* [ ] dates
* [ ] daycounters
* [ ] defaultprobabilitycurves
* [ ] digitalcoupon
* [ ] digitaloption
* [ ] distributions
* [ ] dividendoption
* [ ] doublebarrieroption
* [ ] doublebinaryoption
* [x] europeanoption
* [ ] everestoption
* [ ] exchangerate
* [ ] extendedtrees
* [ ] extensibleoptions
* [ ] fastfouriertransform
* [ ] fdcev
* [ ] fdcir
* [ ] fdheston
* [ ] fdmlinearop
* [ ] fdsabr
* [ ] fittedbonddiscountcurve
* [ ] forwardoption
* [ ] forwardrateagreement
* [ ] functions
* [ ] garch
* [ ] gaussianquadratures
* [ ] gjrgarchmodel
* [ ] gsr
* [x] hestonmodel
* [x] hestonslvmodel
* [ ] himalayaoption
* [ ] hybridhestonhullwhiteprocess
* [ ] indexes
* [ ] inflationcapflooredcoupon
* [ ] inflationcapfloor
* [ ] inflationcpibond
* [ ] inflationcpicapfloor
* [ ] inflationcpiswap
* [ ] inflation
* [ ] inflationvolatility
* [ ] instruments
* [ ] integrals
* [ ] interestrates
* [ ] interpolations
* [ ] jumpdiffusion
* [ ] lazyobject
* [ ] libormarketmodel
* [ ] libormarketmodelprocess
* [ ] linearleastsquaresregression
* [ ] lookbackoptions
* [ ] lowdiscrepancysequences
* [ ] margrabeoption
* [ ] marketmodel_cms
* [ ] marketmodel
* [ ] marketmodel_smmcapletalphacalibration
* [ ] marketmodel_smmcapletcalibration
* [ ] marketmodel_smmcaplethomocalibration
* [ ] marketmodel_smm
* [ ] markovfunctional
* [ ] matrices
* [ ] mclongstaffschwartzengine
* [ ] mersennetwister
* [ ] money
* [ ] noarbsabr
* [ ] normalclvmodel
* [ ] nthorderderivativeop
* [ ] nthtodefault
* [ ] numericaldifferentiation
* [ ] observable
* [ ] ode
* [ ] operators
* [ ] optimizers
* [ ] optionletstripper
* [ ] overnightindexedswap
* [ ] pagodaoption
* [ ] paralleltestrunner
* [ ] partialtimebarrieroption
* [ ] pathgenerator
* [ ] period
* [ ] piecewiseyieldcurve
* [ ] piecewisezerospreadedtermstructure
* [ ] quantooption
* [ ] quotes
* [ ] rangeaccrual
* [ ] riskneutraldensitycalculator
* [ ] riskstats
* [ ] rngtraits
* [ ] rounding
* [ ] sampledcurve
* [ ] schedule
* [ ] shortratemodels
* [ ] sofrfutures
* [ ] solvers
* [ ] speedlevel
* [ ] spreadoption
* [ ] squarerootclvmodel
* [ ] stats
* [ ] swapforwardmappings
* [ ] swap
* [ ] swaption
* [ ] swaptionvolatilitycube
* [ ] swaptionvolatilitymatrix
* [ ] swaptionvolstructuresutilities
* [ ] swingoption
* [ ] termstructures
* [ ] timegrid
* [ ] timeseries
* [ ] tqreigendecomposition
* [ ] tracing
* [ ] transformedgrid
* [ ] twoassetbarrieroption
* [ ] twoassetcorrelationoption
* [ ] ultimateforwardtermstructure
* [ ] variancegamma
* [ ] varianceoption
* [ ] varianceswaps
* [ ] volatilitymodels
* [ ] vpp
* [ ] zabr
