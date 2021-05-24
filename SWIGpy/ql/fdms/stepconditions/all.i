#ifndef ql_fdms_stepconditions_all_i
#define ql_fdms_stepconditions_all_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/fdms/StepCondition.i

%{
using QuantLib::FdmSnapshotCondition;
using QuantLib::FdmStepConditionComposite;
using QuantLib::FdmAmericanStepCondition;
using QuantLib::FdmArithmeticAverageCondition;
using QuantLib::FdmSimpleSwingCondition;
using QuantLib::FdmBermudanStepCondition;
using QuantLib::FdmSimpleStorageCondition;
using QuantLib::FdmSimpleSwingCondition;
using QuantLib::FdmDividendHandler;
%}

%{
class FdmStepConditionProxy : public StepCondition<Array> {
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
class FdmStepConditionProxy : public StepCondition<Array> {
  public:
    FdmStepConditionProxy(
        PyObject* callback);
};

%shared_ptr(FdmSnapshotCondition)
class FdmSnapshotCondition : public StepCondition<Array> {
public:
    explicit FdmSnapshotCondition(Time t);

    Time getTime() const;
    const Array& getValues() const;
};

%template(FdmStepConditionVector) std::vector<ext::shared_ptr<StepCondition<Array> > > ;

%shared_ptr(FdmStepConditionComposite)
class FdmStepConditionComposite : public StepCondition<Array> {
public:
    typedef std::vector<ext::shared_ptr<StepCondition<Array> > > Conditions;
    %extend {
        FdmStepConditionComposite(
            const std::vector<Time> & stoppingTimes,
            const std::vector<ext::shared_ptr<StepCondition<Array> > > & conditions) {
            return new FdmStepConditionComposite(
                std::list<std::vector<Time> >(1, stoppingTimes),
                std::list<ext::shared_ptr<StepCondition<Array> > >(
                    conditions.begin(), conditions.end()));
        }
    }

    const std::vector<Time>& stoppingTimes() const;
    const std::vector<ext::shared_ptr<StepCondition<Array> > > & conditions() const;

    static ext::shared_ptr<FdmStepConditionComposite> joinConditions(
        const ext::shared_ptr<FdmSnapshotCondition>& c1,
        const ext::shared_ptr<FdmStepConditionComposite>& c2);

    static ext::shared_ptr<FdmStepConditionComposite> vanillaComposite(
         const std::vector<ext::shared_ptr<Dividend> >& schedule,
         const ext::shared_ptr<Exercise>& exercise,
         const ext::shared_ptr<FdmMesher>& mesher,
         const ext::shared_ptr<FdmInnerValueCalculator>& calculator,
         const Date& refDate,
         const DayCounter& dayCounter);
};

%shared_ptr(FdmAmericanStepCondition)
class FdmAmericanStepCondition : public StepCondition<Array> {
  public:
    FdmAmericanStepCondition(
        const ext::shared_ptr<FdmMesher> & mesher,
        const ext::shared_ptr<FdmInnerValueCalculator> & calculator);
};

%shared_ptr(FdmArithmeticAverageCondition)
class FdmArithmeticAverageCondition : public StepCondition<Array> {
  public:
    FdmArithmeticAverageCondition(
        const std::vector<Time> & averageTimes,
        Real, Size pastFixings,
        const ext::shared_ptr<FdmMesher> & mesher,
        Size equityDirection);
};

%shared_ptr(FdmBermudanStepCondition)
class FdmBermudanStepCondition : public StepCondition<Array> {
  public:
    FdmBermudanStepCondition(
        const std::vector<Date> & exerciseDates,
        const Date& referenceDate,
        const DayCounter& dayCounter,
        const ext::shared_ptr<FdmMesher> & mesher,
        const ext::shared_ptr<FdmInnerValueCalculator> & calculator);

    const std::vector<Time>& exerciseTimes() const;
};

%shared_ptr(FdmSimpleStorageCondition)
class FdmSimpleStorageCondition : public StepCondition<Array> {
  public:
    FdmSimpleStorageCondition(
        const std::vector<Time> & exerciseTimes,
        const ext::shared_ptr<FdmMesher>& mesher,
        const ext::shared_ptr<FdmInnerValueCalculator>& calculator,
        Real changeRate);
};

%shared_ptr(FdmSimpleSwingCondition)
class FdmSimpleSwingCondition : public StepCondition<Array> {
  public:
    FdmSimpleSwingCondition(
        const std::vector<Time> & exerciseTimes,
        const ext::shared_ptr<FdmMesher>& mesher,
        const ext::shared_ptr<FdmInnerValueCalculator>& calculator,
        Size swingDirection,
        Size minExercises = 0);
};

%shared_ptr(FdmDividendHandler)
class FdmDividendHandler : public StepCondition<Array> {
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

#endif
