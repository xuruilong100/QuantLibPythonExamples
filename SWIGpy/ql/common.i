#ifndef ql_common_i
#define ql_common_i

%include ../ql/alltypes.i
%include ../ql/defines.i
%include ../ql/types.i
%include ../ql/vectors.i
%include ../ql/date.i
%include ../ql/scheduler.i

%{
// This is necessary to avoid compile failures on
// GCC 4
// see http://svn.boost.org/trac/boost/ticket/1793

#if defined(NDEBUG)
#define BOOST_DISABLE_ASSERTS 1
#endif

#include <boost/algorithm/string/case_conv.hpp>
%}

%{
using QuantLib::Null;
using QuantLib::Error;
using QuantLib::Handle;
using QuantLib::RelinkableHandle;
using QuantLib::Sample;
using QuantLib::LsmBasisSystem;
using QuantLib::CPI;
using QuantLib::Duration;
using QuantLib::Futures;
using QuantLib::Position;
using QuantLib::Protection;
using QuantLib::Settlement;
using QuantLib::CostFunction;
using QuantLib::close;
using QuantLib::close_enough;
typedef int intOrNull;
typedef double doubleOrNull;
%}

%{
using QuantLib::VolatilityType;
using QuantLib::ShiftedLognormal;
using QuantLib::Normal;
%}
%{
using QuantLib::BusinessDayConvention;
using QuantLib::Following;
using QuantLib::ModifiedFollowing;
using QuantLib::Preceding;
using QuantLib::ModifiedPreceding;
using QuantLib::Unadjusted;
using QuantLib::HalfMonthModifiedFollowing;
using QuantLib::Nearest;
using QuantLib::JointCalendarRule;
using QuantLib::JoinHolidays;
using QuantLib::JoinBusinessDays;
%}
%{
using QuantLib::Weekday;
using QuantLib::Sunday;
using QuantLib::Monday;
using QuantLib::Tuesday;
using QuantLib::Wednesday;
using QuantLib::Thursday;
using QuantLib::Friday;
using QuantLib::Saturday;
using QuantLib::Month;
using QuantLib::January;
using QuantLib::February;
using QuantLib::March;
using QuantLib::April;
using QuantLib::May;
using QuantLib::June;
using QuantLib::July;
using QuantLib::August;
using QuantLib::September;
using QuantLib::October;
using QuantLib::November;
using QuantLib::December;
using QuantLib::Jan;
using QuantLib::Feb;
using QuantLib::Mar;
using QuantLib::Apr;
using QuantLib::Jun;
using QuantLib::Jul;
using QuantLib::Aug;
using QuantLib::Sep;
using QuantLib::Oct;
using QuantLib::Nov;
using QuantLib::Dec;
using QuantLib::TimeUnit;
using QuantLib::Days;
using QuantLib::Weeks;
using QuantLib::Months;
using QuantLib::Years;
using QuantLib::Hours;
using QuantLib::Minutes;
using QuantLib::Seconds;
using QuantLib::Milliseconds;
using QuantLib::Microseconds;
using QuantLib::Frequency;
using QuantLib::NoFrequency;
using QuantLib::Once;
using QuantLib::Annual;
using QuantLib::Semiannual;
using QuantLib::EveryFourthMonth;
using QuantLib::Quarterly;
using QuantLib::Bimonthly;
using QuantLib::Monthly;
using QuantLib::EveryFourthWeek;
using QuantLib::Biweekly;
using QuantLib::Weekly;
using QuantLib::Daily;
using QuantLib::OtherFrequency;
%}
%{
using QuantLib::Compounding;
using QuantLib::Simple;
using QuantLib::Compounded;
using QuantLib::Continuous;
using QuantLib::SimpleThenCompounded;
using QuantLib::CompoundedThenSimple;
%}
%{
using QuantLib::ASX;
using QuantLib::ECB;
using QuantLib::IMM;
using QuantLib::DateGeneration;
using QuantLib::Pillar;
%}

%inline %{
    int NullSize() { return Null<Size>(); }
    double NullReal() { return Null<Real>(); }
    double NullTime() { return Null<Time>(); }
    Date NullDate() { return Null<Date>(); }
    Array NullArray() { return Null<Array>(); }
%}

%typemap(in) intOrNull {
    if ($input == Py_None)
        $1 = Null<int>();
    else if (PyInt_Check($input))
        $1 = int(PyInt_AsLong($input));
    else
        SWIG_exception(SWIG_TypeError,"int expected");
}

%typecheck(SWIG_TYPECHECK_INTEGER) intOrNull {
    $1 = ($input == Py_None || PyInt_Check($input)) ? 1 : 0;
}

%typemap(out) intOrNull {
    if ($1 == Null<int>()) {
        Py_INCREF(Py_None);
        $result = Py_None;
    } else {
        $result = PyInt_FromLong(long($1));
    }
}

%typemap(in) doubleOrNull {
    if ($input == Py_None)
        $1 = Null<double>();
    else if (PyFloat_Check($input))
        $1 = PyFloat_AsDouble($input);
    else
        SWIG_exception(SWIG_TypeError,"double expected");
}

%typecheck(SWIG_TYPECHECK_DOUBLE) doubleOrNull {
    $1 = ($input == Py_None || PyFloat_Check($input)) ? 1 : 0;
}

%typemap(out) doubleOrNull {
    if ($1 == Null<double>()) {
        Py_INCREF(Py_None);
        $result = Py_None;
    } else {
        $result = PyFloat_FromDouble($1);
    }
}


namespace ext {
%extend shared_ptr {
    T* operator->() {
        return (*self).operator->();
    }
    bool __nonzero__() {
        return !!(*self);
    }
    bool __bool__() {
        return !!(*self);
    }
}
}

template <class T>
class Handle {
  public:
  Handle(const ext::shared_ptr<T>& = ext::shared_ptr<T>());
    const ext::shared_ptr<T>& operator->() const;
    const ext::shared_ptr<T>& currentLink() const;
    const ext::shared_ptr<T>& operator*() const;
    bool empty() const;
    %extend {
        bool __nonzero__() {
            return !self->empty();
        }
        bool __bool__() {
            return !self->empty();
        }
        ext::shared_ptr<Observable> asObservable() const {
            return ext::shared_ptr<Observable>(*self);
        }
    }
};

template <class T>
class RelinkableHandle : public Handle<T> {
  public:
    RelinkableHandle(
        const ext::shared_ptr<T>& = ext::shared_ptr<T>(),
        bool registerAsObserver = true);
    void linkTo(
        const ext::shared_ptr<T>&,
        bool registerAsObserver = true);
    %extend {
        void reset() {
            self->linkTo(ext::shared_ptr<T>());
        }
    }
};

namespace ext {
template <typename T1 = void, typename T2 = void, typename T3 = void>
struct tuple;

template <>
struct tuple<void, void, void> {
};

template <typename T1>
struct tuple<T1, void, void> {
    tuple(T1);
    %extend {
        T1 first() const {
            return ext::get<0>(*self);
        }
    }
};

template <typename T1, typename T2>
struct tuple<T1, T2, void> {
    tuple(T1, T2);
    %extend {
        T1 first() const {
            return ext::get<0>(*self);
        }
        T2 second() const {
            return ext::get<1>(*self);
        }
    }
};

template <typename T1, typename T2, typename T3>
struct tuple<T1, T2, T3> {
    tuple(T1, T2, T3);
    %extend {
        T1 first() const {
            return ext::get<0>(*self);
        }
        T2 second() const {
            return ext::get<1>(*self);
        }
        T3 third() const {
            return ext::get<2>(*self);
        }
    }
};
}    // namespace ext

template <class T>
class Sample {
  private:
    Sample();
  public:
    %extend {
        const T& value() { return self->value; }
        Real weight() { return self->weight; }
    }
};

%template(SampleNumber) Sample<Real>;
%template(SampleArray) Sample<Array>;
%template(SampleRealVector) Sample<std::vector<Real>>;

bool close(Real x, Real y);
bool close(Real x, Real y, Size n);
bool close_enough(Real x, Real y);
bool close_enough(Real x, Real y, Size n);

%inline %{
    void enableTracing() {
        QL_TRACE_ENABLE;
    }
    void disableTracing() {
        QL_TRACE_DISABLE;
    }
%}

struct LsmBasisSystem {
    enum PolynomType {
        Monomial,
        Laguerre,
        Hermite,
        Hyperbolic,
        Legendre,
        Chebyshev,
        Chebyshev2nd
    };
};

struct CPI {
    enum InterpolationType {
        AsIndex, Flat, Linear };
};

struct Duration {
    enum Type { Simple, Macaulay, Modified };
};

struct Futures {
    enum Type { IMM, ASX };
};

struct Position {
    enum Type { Long, Short };
};

struct Settlement {
    enum Type {
        Physical,
        Cash
    };
    enum Method {
        PhysicalOTC,
        PhysicalCleared,
        CollateralizedCashPrice,
        ParYieldCurve
    };
};

struct Protection {
    enum Side { Buyer, Seller };
};

%{
class UnaryFunction {
  public:
    UnaryFunction(PyObject* function) : function_(function) {
        Py_XINCREF(function_);
    }
    UnaryFunction(const UnaryFunction& f) : function_(f.function_) {
        Py_XINCREF(function_);
    }
    UnaryFunction& operator=(const UnaryFunction& f) {
        if ((this != &f) && (function_ != f.function_)) {
            Py_XDECREF(function_);
            function_ = f.function_;
            Py_XINCREF(function_);
        }
        return *this;
    }
    ~UnaryFunction() {
        Py_XDECREF(function_);
    }
    Real operator()() const {
        PyObject* pyResult = PyObject_CallFunction(
            function_, NULL);
        QL_ENSURE(pyResult != NULL, "failed to call Python function");
        Real result = PyFloat_AsDouble(pyResult);
        Py_XDECREF(pyResult);
        return result;
    }
    Real operator()(Real x) const {
        PyObject* pyResult = PyObject_CallFunction(
            function_, "d", x);
        QL_ENSURE(pyResult != NULL, "failed to call Python function");
        Real result = PyFloat_AsDouble(pyResult);
        Py_XDECREF(pyResult);
        return result;
    }
    Real operator()(const Date& x) const {
        PyObject* pyResult = PyObject_CallFunction(
            function_, "(3)", x.dayOfMonth(), x.month(), x.year());
        QL_ENSURE(pyResult != NULL, "failed to call Python function");
        Real result = PyFloat_AsDouble(pyResult);
        Py_XDECREF(pyResult);
        return result;
    }
    Real derivative(Real x) const {
        PyObject* pyResult = PyObject_CallMethod(
            function_, "derivative", "d", x);
        QL_ENSURE(
            pyResult != NULL,
            "failed to call derivative() on Python object");
        Real result = PyFloat_AsDouble(pyResult);
        Py_XDECREF(pyResult);
        return result;
    }

  private:
    PyObject* function_;
};

class BinaryFunction {
  public:
    BinaryFunction(PyObject* function) : function_(function) {
        Py_XINCREF(function_);
    }
    BinaryFunction(const BinaryFunction& f)
        : function_(f.function_) {
        Py_XINCREF(function_);
    }
    BinaryFunction& operator=(const BinaryFunction& f) {
        if ((this != &f) && (function_ != f.function_)) {
            Py_XDECREF(function_);
            function_ = f.function_;
            Py_XINCREF(function_);
        }
        return *this;
    }
    ~BinaryFunction() {
        Py_XDECREF(function_);
    }
    Real operator()(Real x, Real y) const {
        PyObject* pyResult = PyObject_CallFunction(
            function_, "dd", x, y);
        QL_ENSURE(
            pyResult != NULL, "failed to call Python function");
        Real result = PyFloat_AsDouble(pyResult);
        Py_XDECREF(pyResult);
        return result;
    }

  private:
    PyObject* function_;
};

class PyCostFunction : public CostFunction {
  public:
    PyCostFunction(PyObject* function) : function_(function) {
        Py_XINCREF(function_);
    }
    PyCostFunction(const PyCostFunction& f)
        : function_(f.function_) {
        Py_XINCREF(function_);
    }
    PyCostFunction& operator=(const PyCostFunction& f) {
        if ((this != &f) && (function_ != f.function_)) {
            Py_XDECREF(function_);
            function_ = f.function_;
            Py_XINCREF(function_);
        }
        return *this;
    }
    ~PyCostFunction() {
        Py_XDECREF(function_);
    }
    Real value(const Array& x) const {
        PyObject* tuple = PyTuple_New(x.size());
        for (Size i = 0; i < x.size(); i++)
            PyTuple_SetItem(
                tuple, i, PyFloat_FromDouble(x[i]));
        PyObject* pyResult = PyObject_CallObject(
            function_, tuple);
        Py_XDECREF(tuple);
        QL_ENSURE(
            pyResult != NULL,
            "failed to call Python function");
        Real result = PyFloat_AsDouble(pyResult);
        Py_XDECREF(pyResult);
        return result;
    }
    Disposable<Array> values(const Array& x) const {
        QL_FAIL("Not implemented");
        // Should be straight forward to copy from a python list
        // to an array
    }

  private:
    PyObject* function_;
};
%}

%define QL_TYPECHECK_VOLATILITYTYPE       8210    %enddef

enum VolatilityType {
    ShiftedLognormal,
    Normal
};

%typemap(in) boost::optional<VolatilityType> %{
    if($input == Py_None)
        $1 = boost::none;
    else if (PyInt_Check($input))
        $1 = (VolatilityType) PyInt_AsLong($input);
    else
        $1 = (VolatilityType) PyLong_AsLong($input);
%}

%typecheck (QL_TYPECHECK_VOLATILITYTYPE) boost::optional<VolatilityType> {
    if (PyInt_Check($input) || PyLong_Check($input) || Py_None == $input)
        $1 = 1;
    else
        $1 = 0;
}

enum BusinessDayConvention {
    Following,
    ModifiedFollowing,
    Preceding,
    ModifiedPreceding,
    Unadjusted,
    HalfMonthModifiedFollowing,
    Nearest
};

enum JointCalendarRule {
    JoinHolidays, JoinBusinessDays
};

enum Weekday {
    Sunday    = 1,
    Monday    = 2,
    Tuesday   = 3,
    Wednesday = 4,
    Thursday  = 5,
    Friday    = 6,
    Saturday  = 7
};

enum Month {
    January   = 1,
    February  = 2,
    March     = 3,
    April     = 4,
    May       = 5,
    June      = 6,
    July      = 7,
    August    = 8,
    September = 9,
    October   = 10,
    November  = 11,
    December  = 12,
    Jan = 1,
    Feb = 2,
    Mar = 3,
    Apr = 4,
    Jun = 6,
    Jul = 7,
    Aug = 8,
    Sep = 9,
    Oct = 10,
    Nov = 11,
    Dec = 12
};

enum TimeUnit {
    Days,
    Weeks,
    Months,
    Years,
    Hours,
    Minutes,
    Seconds,
    Milliseconds,
    Microseconds
};

enum Frequency {
    NoFrequency = -1,
    Once = 0,
    Annual = 1,
    Semiannual = 2,
    EveryFourthMonth = 3,
    Quarterly = 4,
    Bimonthly = 6,
    Monthly = 12,
    EveryFourthWeek = 13,
    Biweekly = 26,
    Weekly = 52,
    Daily = 365,
    OtherFrequency = 999
};

enum Compounding {
    Simple,
    Compounded,
    Continuous,
    SimpleThenCompounded,
    CompoundedThenSimple
};

struct ASX {
    enum Month {
        F = 1,
        G = 2,
        H = 3,
        J = 4,
        K = 5,
        M = 6,
        N = 7,
        Q = 8,
        U = 9,
        V = 10,
        X = 11,
        Z = 12
    };

    static bool isASXdate(
        const Date& d,
        bool mainCycle = true);
    static bool isASXcode(
        const std::string& code,
        bool mainCycle = true);
    static std::string code(
        const Date& asxDate);
    static Date date(
        const std::string& asxCode,
        const Date& referenceDate = Date());
    static Date nextDate(
        const Date& d = Date(),
        bool mainCycle = true);
    static Date nextDate(
        const std::string& asxCode,
        bool mainCycle = true,
        const Date& referenceDate = Date());
    static std::string nextCode(
        const Date& d = Date(),
        bool mainCycle = true);
    static std::string nextCode(
        const std::string& asxCode,
        bool mainCycle = true,
        const Date& referenceDate = Date());
};

struct ECB {
	static const std::set<Date>& knownDates();
	static void addDate(const Date& d);
	static void removeDate(const Date& d);
	static Date date(Month m, Year y);
	static Date date(
		const std::string& ecbCode,
		const Date& referenceDate = Date());
	static std::string code(const Date& ecbDate);
	static Date nextDate(const Date& d = Date());
	static Date nextDate(
		const std::string& ecbCode,
		const Date& referenceDate = Date());
	static std::vector<Date> nextDates(const Date& d = Date());
	static std::vector<Date> nextDates(
		const std::string& ecbCode,
		const Date& referenceDate = Date());
	static bool isECBdate(const Date& d);
	static bool isECBcode(const std::string& in);
	static std::string nextCode(const Date& d = Date());
	static std::string nextCode(const std::string& ecbCode);
};

struct IMM {
    enum Month {
        F = 1,
        G = 2,
        H = 3,
        J = 4,
        K = 5,
        M = 6,
        N = 7,
        Q = 8,
        U = 9,
        V = 10,
        X = 11,
        Z = 12
    };

    static bool isIMMdate(
        const Date& d,
        bool mainCycle = true);
    static bool isIMMcode(
        const std::string& code,
        bool mainCycle = true);
    static std::string code(
        const Date& immDate);
    static Date date(
        const std::string& immCode,
        const Date& referenceDate = Date());
    static Date nextDate(
        const Date& d = Date(),
        bool mainCycle = true);
    static Date nextDate(
        const std::string& immCode,
        bool mainCycle = true,
        const Date& referenceDate = Date());
    static std::string nextCode(
        const Date& d = Date(),
        bool mainCycle = true);
    static std::string nextCode(
        const std::string& immCode,
        bool mainCycle = true,
        const Date& referenceDate = Date());
};

struct DateGeneration {
    enum Rule {
        Backward,
        Forward,
        Zero,
        ThirdWednesday,
        ThirdWednesdayInclusive,
        Twentieth,
        TwentiethIMM,
        OldCDS,
        CDS,
        CDS2015
    };
};

struct Pillar {
    enum Choice { MaturityDate, LastRelevantDate, CustomDate};
};

#endif
