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
> * QuantLib: 1.24
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
* [x] autocovariances
* [x] barrieroption
* [ ] basismodels
* [x] basketoption
* [x] batesmodel
* [ ] bermudanswaption
* [x] binaryoption
* [x] blackdeltacalculator
* [x] blackformula
* [ ] bonds
* [ ] brownianbridge
* [x] businessdayconventions
* [x] calendars
* [ ] callablebonds
* [ ] capflooredcoupon
* [ ] capfloor
* [ ] cashflows
* [ ] catbonds
* [ ] cdo
* [ ] cdsoption
* [x] chooseroption
* [x] cliquetoption
* [ ] cms
* [ ] cmsspread
* [x] commodityunitofmeasure
* [ ] compiledboostversion
* [x] compoundoption
* [ ] convertiblebonds
* [x] covariance
* [ ] creditdefaultswap
* [x] creditriskplus
* [x] currency
* [ ] curvestates
* [x] dates
* [x] daycounters
* [ ] defaultprobabilitycurves
* [ ] digitalcoupon
* [ ] digitaloption
* [x] distributions
* [ ] dividendoption
* [x] doublebarrieroption
* [x] doublebinaryoption
* [x] europeanoption
* [x] everestoption
* [x] exchangerate
* [x] extendedtrees
* [x] extensibleoptions
* [x] fastfouriertransform
* [x] fdcev
* [ ] fdcir
* [x] fdheston
* [ ] fdmlinearop
* [x] fdsabr
* [ ] fittedbonddiscountcurve
* [x] forwardoption
* [ ] forwardrateagreement
* [x] functions
* [x] garch
* [x] gaussianquadratures
* [x] gjrgarchmodel
* [ ] gsr
* [x] hestonmodel
* [x] hestonslvmodel
* [x] himalayaoption
* [x] hybridhestonhullwhiteprocess
* [x] indexes
* [ ] inflationcapflooredcoupon
* [ ] inflationcapfloor
* [ ] inflationcpibond
* [ ] inflationcpicapfloor
* [ ] inflationcpiswap
* [ ] inflation
* [ ] inflationvolatility
* [x] instruments
* [x] integrals
* [x] interestrates
* [x] interpolations
* [x] jumpdiffusion
* [x] lazyobject
* [ ] libormarketmodel
* [ ] libormarketmodelprocess
* [ ] linearleastsquaresregression
* [x] lookbackoptions
* [x] lowdiscrepancysequences
* [x] margrabeoption
* [ ] marketmodel_cms
* [ ] marketmodel
* [ ] marketmodel_smmcapletalphacalibration
* [ ] marketmodel_smmcapletcalibration
* [ ] marketmodel_smmcaplethomocalibration
* [ ] marketmodel_smm
* [ ] markovfunctional
* [x] matrices
* [x] mclongstaffschwartzengine
* [x] mersennetwister
* [x] money
* [ ] noarbsabr
* [ ] normalclvmodel
* [ ] nthorderderivativeop
* [ ] nthtodefault
* [x] numericaldifferentiation
* [ ] observable
* [ ] ode
* [ ] operators
* [ ] optimizers
* [ ] optionletstripper
* [ ] overnightindexedswap
* [x] pagodaoption
* [ ] paralleltestrunner
* [x] partialtimebarrieroption
* [x] pathgenerator
* [x] period
* [ ] piecewiseyieldcurve
* [ ] piecewisezerospreadedtermstructure
* [ ] quantooption
* [x] quotes
* [ ] rangeaccrual
* [x] riskneutraldensitycalculator
* [x] riskstats
* [x] rngtraits
* [x] rounding
* [ ] sampledcurve
* [x] schedule
* [ ] shortratemodels
* [ ] sofrfutures
* [x] solvers
* [ ] speedlevel
* [x] spreadoption
* [ ] squarerootclvmodel
* [x] stats
* [ ] swapforwardmappings
* [ ] swap
* [ ] swaption
* [ ] swaptionvolatilitycube
* [ ] swaptionvolatilitymatrix
* [ ] swaptionvolstructuresutilities
* [ ] swingoption
* [x] termstructures
* [x] timegrid
* [x] timeseries
* [x] tqreigendecomposition
* [ ] tracing
* [x] transformedgrid
* [x] twoassetbarrieroption
* [x] twoassetcorrelationoption
* [ ] ultimateforwardtermstructure
* [ ] variancegamma
* [ ] varianceoption
* [ ] varianceswaps
* [ ] volatilitymodels
* [ ] vpp
* [ ] zabr
