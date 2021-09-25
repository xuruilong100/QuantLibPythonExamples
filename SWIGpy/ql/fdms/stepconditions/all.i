#ifndef ql_fdms_stepconditions_all_i
#define ql_fdms_stepconditions_all_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/fdms/StepCondition.i

%{
using QuantLib::FdmAmericanStepCondition;
using QuantLib::FdmArithmeticAverageCondition;
using QuantLib::FdmBermudanStepCondition;
using QuantLib::FdmSimpleStorageCondition;
using QuantLib::FdmSimpleSwingCondition;
using QuantLib::FdmSnapshotCondition;
using QuantLib::FdmStepConditionComposite;
using QuantLib::FdmDividendHandler;
using QuantLib::FdmVPPStepCondition;
using QuantLib::FdmVPPStepConditionParams;
using QuantLib::FdmVPPStepConditionMesher;
using QuantLib::FdmVPPStartLimitStepCondition;
%}

%shared_ptr(FdmAmericanStepCondition)
class FdmAmericanStepCondition : public FdmStepCondition {
  public:
    FdmAmericanStepCondition(
        ext::shared_ptr<FdmMesher> mesher,
        ext::shared_ptr<FdmInnerValueCalculator> calculator);
};

%shared_ptr(FdmArithmeticAverageCondition)
class FdmArithmeticAverageCondition : public FdmStepCondition {
  public:
    FdmArithmeticAverageCondition(
        std::vector<Time> averageTimes,
        Real, Size pastFixings,
        const ext::shared_ptr<FdmMesher> & mesher,
        Size equityDirection);
};

%shared_ptr(FdmBermudanStepCondition)
class FdmBermudanStepCondition : public FdmStepCondition {
  public:
    FdmBermudanStepCondition(
        const std::vector<Date> & exerciseDates,
        const Date& referenceDate,
        const DayCounter& dayCounter,
        ext::shared_ptr<FdmMesher> mesher,
        ext::shared_ptr<FdmInnerValueCalculator> calculator);

    const std::vector<Time>& exerciseTimes() const;
};

%shared_ptr(FdmSimpleStorageCondition)
class FdmSimpleStorageCondition : public FdmStepCondition {
  public:
    FdmSimpleStorageCondition(
        std::vector<Time> exerciseTimes,
        ext::shared_ptr<FdmMesher> mesher,
        ext::shared_ptr<FdmInnerValueCalculator> calculator,
        Real changeRate);
};

%shared_ptr(FdmSimpleSwingCondition)
class FdmSimpleSwingCondition : public FdmStepCondition {
  public:
    FdmSimpleSwingCondition(
        std::vector<Time> exerciseTimes,
        ext::shared_ptr<FdmMesher> mesher,
        ext::shared_ptr<FdmInnerValueCalculator> calculator,
        Size swingDirection,
        Size minExercises = 0);
};

%shared_ptr(FdmSnapshotCondition)
class FdmSnapshotCondition : public FdmStepCondition {
  public:
    explicit FdmSnapshotCondition(Time t);

    Time getTime() const;
    const Array& getValues() const;
};

%shared_ptr(FdmStepConditionComposite)
class FdmStepConditionComposite : public FdmStepCondition {
public:
    typedef std::list<ext::shared_ptr<FdmStepCondition > > Conditions;

    FdmStepConditionComposite(
        const std::list<std::vector<Time> >& stoppingTimes,
        Conditions conditions);

    const std::vector<Time>& stoppingTimes() const;
    const Conditions& conditions() const;

    static ext::shared_ptr<FdmStepConditionComposite> joinConditions(
        const ext::shared_ptr<FdmSnapshotCondition>& c1,
        const ext::shared_ptr<FdmStepConditionComposite>& c2);

    static ext::shared_ptr<FdmStepConditionComposite> vanillaComposite(
         const DividendSchedule& schedule,
         const ext::shared_ptr<Exercise>& exercise,
         const ext::shared_ptr<FdmMesher>& mesher,
         const ext::shared_ptr<FdmInnerValueCalculator>& calculator,
         const Date& refDate,
         const DayCounter& dayCounter);
};

%shared_ptr(FdmDividendHandler)
class FdmDividendHandler : public FdmStepCondition {
  public:
    FdmDividendHandler(
        const std::vector<ext::shared_ptr<Dividend>>& schedule,
        const ext::shared_ptr<FdmMesher>& mesher,
        const Date& referenceDate,
        const DayCounter& dayCounter,
        Size equityDirection);

    const std::vector<Time>& dividendTimes() const;
    const std::vector<Date>& dividendDates() const;
    const std::vector<Real>& dividends() const;
};

%shared_ptr(FdmVPPStepCondition)
class FdmVPPStepCondition : public FdmStepCondition {
  private:
    FdmVPPStepCondition();
  public:
    Size nStates() const;
    Real maxValue(const Array& states) const;
};

struct FdmVPPStepConditionParams {
    const Real heatRate;
    const Real pMin;
    const Real pMax;
    const Size tMinUp;
    const Size tMinDown;
    const Real startUpFuel;
    const Real startUpFixCost;
    const Real fuelCostAddon;
    %extend {
        FdmVPPStepConditionParams(
            Real heatRate,
            Real pMin,
            Real pMax,
            Size tMinUp,
            Size tMinDown,
            Real startUpFuel,
            Real startUpFixCost,
            Real fuelCostAddon) {
            FdmVPPStepConditionParams params = {
                heatRate,
                pMin,
                pMax,
                tMinUp,
                tMinDown,
                startUpFuel,
                startUpFixCost,
                fuelCostAddon};
            return new FdmVPPStepConditionParams(params);
        }
    }
};

struct FdmVPPStepConditionMesher {
    const Size stateDirection;
    const ext::shared_ptr<FdmMesher> mesher;
    %extend {
        FdmVPPStepConditionMesher(
            const Size& stateDirection,
            const ext::shared_ptr<FdmMesher>& mesher) {
            FdmVPPStepConditionMesher conditionMesher = {stateDirection, mesher};
            return new FdmVPPStepConditionMesher(conditionMesher);
        }
    }
};

%shared_ptr(FdmVPPStartLimitStepCondition)
class FdmVPPStartLimitStepCondition : public FdmVPPStepCondition {
  public:
    FdmVPPStartLimitStepCondition(
        const FdmVPPStepConditionParams& params,
        Size nStarts,
        const FdmVPPStepConditionMesher& mesh,
        const ext::shared_ptr<FdmInnerValueCalculator>& gasPrice,
        const ext::shared_ptr<FdmInnerValueCalculator>& sparkSpreadPrice);

    static Size nStates(Size tMinUp, Size tMinDown, Size nStarts);
};

%{
class FdmStepConditionProxy : public FdmStepCondition {
  public:
    FdmStepConditionProxy(
        PyObject* callback) : callback_(callback) {
        Py_XINCREF(callback_);
    }

    FdmStepConditionProxy(
        const FdmStepConditionProxy& p)
        : callback_(p.callback_) {
        Py_XINCREF(callback_);
    }

    FdmStepConditionProxy& operator=(
        const FdmStepConditionProxy& f) {
        if ((this != &f) && (callback_ != f.callback_)) {
            Py_XDECREF(callback_);
            callback_ = f.callback_;
            Py_XINCREF(callback_);
        }
        return *this;
    }

    ~FdmStepConditionProxy() {
        Py_XDECREF(callback_);
    }

    void applyTo(Array& a, Time t) const {
        PyObject* pyArray = SWIG_NewPointerObj(
            SWIG_as_voidptr(&a), SWIGTYPE_p_Array, 0);

        PyObject* pyResult = PyObject_CallMethod(
            callback_, "applyTo", "Od", pyArray, t);

        Py_XDECREF(pyArray);
    }

  private:
    PyObject* callback_;
};
%}

%shared_ptr(FdmStepConditionProxy)
class FdmStepConditionProxy : public FdmStepCondition {
  public:
    FdmStepConditionProxy(
        PyObject* callback);
};

#endif
