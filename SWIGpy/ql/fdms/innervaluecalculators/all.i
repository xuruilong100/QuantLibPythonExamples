#ifndef ql_fdms_innervaluecalculators_all_i
#define ql_fdms_innervaluecalculators_all_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/fdms/FdmInnerValueCalculator.i

%{
using QuantLib::FdmCellAveragingInnerValue;
using QuantLib::FdmLogInnerValue;
using QuantLib::FdmAffineModelSwapInnerValue;
using QuantLib::EscrowedDividendAdjustment;
using QuantLib::FdmEscrowedLogInnerValueCalculator;
using QuantLib::FdmExpExtOUInnerValueCalculator;
using QuantLib::FdmShoutLogInnerValueCalculator;
using QuantLib::FdmSpreadPayoffInnerValue;
using QuantLib::FdmLogBasketInnerValue;
using QuantLib::FdmZeroInnerValue;
%}

%shared_ptr(EscrowedDividendAdjustment)
class EscrowedDividendAdjustment {
  public:
    EscrowedDividendAdjustment(
        DividendSchedule dividendSchedule,
        Handle<YieldTermStructure> rTS,
        Handle<YieldTermStructure> qTS,
        ext::function<Real(Date)> toTime,
        Time maturity);
    %extend {
        EscrowedDividendAdjustment(
            DividendSchedule dividendSchedule,
            Handle<YieldTermStructure> rTS,
            Handle<YieldTermStructure> qTS,
            PyObject* toTime,
            Time maturity) {
                return new EscrowedDividendAdjustment(
                    dividendSchedule,
                    rTS, qTS,
                    UnaryFunction(toTime),
                    maturity);
            }
    }

    Real dividendAdjustment(Time t) const;

    const Handle<YieldTermStructure>& riskFreeRate() const;
    const Handle<YieldTermStructure>& dividendYield() const;
};

%shared_ptr(FdmEscrowedLogInnerValueCalculator)
class FdmEscrowedLogInnerValueCalculator: public FdmInnerValueCalculator {
  public:
    FdmEscrowedLogInnerValueCalculator(
        ext::shared_ptr<EscrowedDividendAdjustment> escrowedDividendAdj,
        ext::shared_ptr<Payoff> payoff,
        ext::shared_ptr<FdmMesher> mesher,
        Size direction);
};

%shared_ptr(FdmExpExtOUInnerValueCalculator)
class FdmExpExtOUInnerValueCalculator : public FdmInnerValueCalculator {
  public:
    typedef std::vector<std::pair<Time, Real> > Shape;

    FdmExpExtOUInnerValueCalculator(
        ext::shared_ptr<Payoff> payoff,
        ext::shared_ptr<FdmMesher> mesher,
        ext::shared_ptr<Shape> shape = ext::shared_ptr<Shape>(),
        Size direction = 0);
};

%shared_ptr(FdmLogBasketInnerValue)
class FdmLogBasketInnerValue : public FdmInnerValueCalculator {
  public:
    FdmLogBasketInnerValue(
        const ext::shared_ptr<BasketPayoff>& payoff,
        const ext::shared_ptr<FdmMesher>& mesher);
};

%shared_ptr(FdmShoutLogInnerValueCalculator)
class FdmShoutLogInnerValueCalculator: public FdmInnerValueCalculator {
  public:
    FdmShoutLogInnerValueCalculator(
        Handle<BlackVolTermStructure> blackVolatility,
        ext::shared_ptr<EscrowedDividendAdjustment> escrowedDividendAdj,
        Time maturity,
        ext::shared_ptr<PlainVanillaPayoff> payoff,
        ext::shared_ptr<FdmMesher> mesher,
        Size direction);
};

%shared_ptr(FdmSpreadPayoffInnerValue)
class FdmSpreadPayoffInnerValue : public FdmInnerValueCalculator {
  public:
    FdmSpreadPayoffInnerValue(
        ext::shared_ptr<BasketPayoff> payoff,
        ext::shared_ptr<FdmInnerValueCalculator> calc1,
        ext::shared_ptr<FdmInnerValueCalculator> calc2);
};

%shared_ptr(FdmZeroInnerValue)
class FdmZeroInnerValue : public FdmInnerValueCalculator {
  public:
    FdmZeroInnerValue();
};

%{
class FdmInnerValueCalculatorProxy : public FdmInnerValueCalculator {
  public:
    FdmInnerValueCalculatorProxy(
        PyObject* callback) : callback_(callback) {
        Py_XINCREF(callback_);
    }

    FdmInnerValueCalculatorProxy(
        const FdmInnerValueCalculatorProxy& p)
        : callback_(p.callback_) {
        Py_XINCREF(callback_);
    }

    FdmInnerValueCalculatorProxy& operator=(
        const FdmInnerValueCalculatorProxy& f) {
        if ((this != &f) && (callback_ != f.callback_)) {
            Py_XDECREF(callback_);
            callback_ = f.callback_;
            Py_XINCREF(callback_);
        }
        return *this;
    }

    ~FdmInnerValueCalculatorProxy() {
        Py_XDECREF(callback_);
    }

    Real innerValue(
        const FdmLinearOpIterator& iter, Time t) {
        return getValue(iter, t, "innerValue");
    }

    Real avgInnerValue(
        const FdmLinearOpIterator& iter, Time t) {
        return getValue(iter, t, "avgInnerValue");
    }

  private:
    Real getValue(
        const FdmLinearOpIterator& iter,
        Time t,
        const std::string& methodName) {
        PyObject* pyIter = SWIG_NewPointerObj(
            SWIG_as_voidptr(&iter), SWIGTYPE_p_FdmLinearOpIterator, 0);

#if !defined(PY_VERSION_HEX) || PY_VERSION_HEX < 0x03040000
        std::vector<char> cstr(
            methodName.c_str(), methodName.c_str() + methodName.size() + 1);
        PyObject* pyResult = PyObject_CallMethod(
            callback_, &cstr[0], "Od", pyIter, t);
#else
        PyObject* pyResult = PyObject_CallMethod(callback_, methodName.c_str(), "Od", pyIter, t);
#endif
        Py_XDECREF(pyIter);
        QL_ENSURE(
            pyResult != NULL,
            "failed to call innerValue function on Python object");
        const Real result = PyFloat_AsDouble(pyResult);
        Py_XDECREF(pyResult);
        return result;
    }

    PyObject* callback_;
};
%}

%shared_ptr(FdmInnerValueCalculatorProxy)
class FdmInnerValueCalculatorProxy : public FdmInnerValueCalculator {
  public:
    FdmInnerValueCalculatorProxy(
        PyObject* callback);
};

%shared_ptr(FdmCellAveragingInnerValue)
class FdmCellAveragingInnerValue : public FdmInnerValueCalculator {
  public:
    %extend {
        FdmCellAveragingInnerValue(
            const ext::shared_ptr<Payoff>& payoff,
            const ext::shared_ptr<FdmMesher>& mesher,
            Size direction,
            PyObject* gridMapping) {
                UnaryFunction f(gridMapping);
                return new FdmCellAveragingInnerValue(
                    payoff, mesher, direction, f);
        }
        FdmCellAveragingInnerValue(
            const ext::shared_ptr<Payoff>& payoff,
            const ext::shared_ptr<FdmMesher>& mesher,
            Size direction) {
                return new FdmCellAveragingInnerValue(
                    payoff, mesher, direction);
        }
    }
};

%shared_ptr(FdmLogInnerValue)
class FdmLogInnerValue : public FdmCellAveragingInnerValue {
  public:
    FdmLogInnerValue(
        const ext::shared_ptr<Payoff>& payoff,
        const ext::shared_ptr<FdmMesher>& mesher,
        Size direction);
};

%template(TimeToDateMap) std::map<Time, Date>;

%shared_ptr(FdmAffineModelSwapInnerValue<G2>)
%shared_ptr(FdmAffineModelSwapInnerValue<HullWhite>)
template <class ModelType>
class FdmAffineModelSwapInnerValue : public FdmInnerValueCalculator {
  public:
    FdmAffineModelSwapInnerValue(
        ext::shared_ptr<ModelType> disModel,
        ext::shared_ptr<ModelType> fwdModel,
        const ext::shared_ptr<VanillaSwap>& swap,
        std::map<Time, Date> exerciseDates,
        ext::shared_ptr<FdmMesher> mesher,
        Size direction);
};

%template(FdmAffineG2ModelSwapInnerValue) FdmAffineModelSwapInnerValue<G2>;
%template(FdmAffineHullWhiteModelSwapInnerValue) FdmAffineModelSwapInnerValue<HullWhite>;

#endif
