# QuantLibPythonExamples

**MORE APIs, MORE examples, MORE test suites.**
-----------------------------------------------

## 简介

* 为构建 Python 包装而重构了 SWIG 接口代码。
* 用 Python 重新实现 QuantLib 的[示例](https://www.quantlib.org/reference/examples.html)。
* 用 Python 重新实现 QuantLib 的[测试](https://github.com/lballabio/QuantLib/tree/master/test-suite)。

> 相关博客：<https://www.cnblogs.com/xuruilong100/p/13281006.html>
>
> 环境：
> * QuantLib: 1.23
> * swig: 4.0.1
> * clang: 10.0.0-4ubuntu1
> * ubuntu: 20.04.2 LTS

---

## 如何创建 Python 包装

打开 `../SWIGpy/` 并运行下列命令。

1. 生成 `.cpp` 文件：

```
swig3.0 -c++ -python -outdir QuantLib -o QuantLib/ql_wrap.cpp quantlib.i
```

2. 编译 `.cpp` 文件：

```
CC=clang CXX=clang++ python3 setup.py build
```

3. 安装 Python 包装：

```
python3 setup.py install
```

---

## Examples（示例）

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

## Test suites（测试）

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
* [x] batesmodel
* [ ] bermudanswaption
* [ ] binaryoption
* [ ] blackdeltacalculator
* [x] blackformula
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
* [x] extendedtrees
* [ ] extensibleoptions
* [ ] fastfouriertransform
* [x] fdcev
* [ ] fdcir
* [x] fdheston
* [ ] fdmlinearop
* [x] fdsabr
* [ ] fittedbonddiscountcurve
* [x] forwardoption
* [ ] forwardrateagreement
* [ ] functions
* [ ] garch
* [ ] gaussianquadratures
* [x] gjrgarchmodel
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
* [x] jumpdiffusion
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
* [x] mclongstaffschwartzengine
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
