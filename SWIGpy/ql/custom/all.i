#ifndef ql_custom_all_i
#define ql_custom_all_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/termstructures/volatilitytermstructures/LocalVolTermStructure.i
%include ../ql/termstructures/volatilitytermstructures/blackvol/all.i
%include ../ql/payoffs.i
%include ../ql/optimizers.i

%{
class CustomLocalVolatility : public LocalVolTermStructure {
  public:
    CustomLocalVolatility(
        PyObject* localVolImpl,
        BusinessDayConvention bdc = Following,
        const DayCounter& dc = DayCounter()) :
        LocalVolTermStructure(bdc, dc),
        localVolImpl_(localVolImpl) {}
    CustomLocalVolatility(
        PyObject* localVolImpl,
        const Date& referenceDate,
        const Calendar& cal = Calendar(),
        BusinessDayConvention bdc = Following,
        const DayCounter& dc = DayCounter()) :
        LocalVolTermStructure(referenceDate, cal, bdc, dc),
        localVolImpl_(localVolImpl) {}
    CustomLocalVolatility(
        PyObject* localVolImpl,
        Natural settlementDays,
        const Calendar& cal,
        BusinessDayConvention bdc = Following,
        const DayCounter& dc = DayCounter()) :
        LocalVolTermStructure(settlementDays, cal, bdc, dc),
        localVolImpl_(localVolImpl) {}

    Date maxDate() const override {return Date::maxDate(); }
    Real minStrike() const override { return 0.0; }
    Real maxStrike() const override { return QL_MAX_REAL; }

  protected:
    Volatility localVolImpl(Time t, Real strike) const override {
        return localVolImpl_(t, strike);
    }
  private:
    BinaryFunction localVolImpl_;
};
%}

%shared_ptr(CustomLocalVolatility)
class CustomLocalVolatility : public LocalVolTermStructure {
  public:
    CustomLocalVolatility(
        PyObject* localVolImpl,
        BusinessDayConvention bdc = Following,
        const DayCounter& dc = DayCounter());
    CustomLocalVolatility(
        PyObject* localVolImpl,
        const Date& referenceDate,
        const Calendar& cal = Calendar(),
        BusinessDayConvention bdc = Following,
        const DayCounter& dc = DayCounter());
    CustomLocalVolatility(
        PyObject* localVolImpl,
        Natural settlementDays,
        const Calendar& cal,
        BusinessDayConvention bdc = Following,
        const DayCounter& dc = DayCounter());
};

%{
class CustomBlackVolatility : public BlackVolatilityTermStructure {
  public:
    CustomBlackVolatility(
        PyObject* blackVolImpl,
        BusinessDayConvention bdc = Following,
        const DayCounter& dc = DayCounter()) :
        BlackVolatilityTermStructure(bdc, dc),
        blackVolImpl_(blackVolImpl) {}

    CustomBlackVolatility(
        PyObject* blackVolImpl,
        const Date& referenceDate,
        const Calendar& cal = Calendar(),
        BusinessDayConvention bdc = Following,
        const DayCounter& dc = DayCounter()) :
        BlackVolatilityTermStructure(
            referenceDate, cal, bdc, dc),
        blackVolImpl_(blackVolImpl) {}

    CustomBlackVolatility(
        PyObject* blackVolImpl,
        Natural settlementDays,
        const Calendar& cal,
        BusinessDayConvention bdc = Following,
        const DayCounter& dc = DayCounter()) :
        BlackVolatilityTermStructure(
            settlementDays, cal, bdc, dc),
        blackVolImpl_(blackVolImpl) {}

    Date maxDate() const override { return Date::maxDate(); }
    Rate minStrike() const override { return 0.0; }
    Rate maxStrike() const override { return QL_MAX_REAL; }

  protected:
    Real blackVolImpl(
        Time maturity, Real strike) const override {
        return blackVolImpl_(maturity, strike);
    }
  private:
    BinaryFunction blackVolImpl_;
};
%}

%shared_ptr(CustomBlackVolatility)
class CustomBlackVolatility : public BlackVolatilityTermStructure {
  public:
    CustomBlackVolatility(
        PyObject* blackVolImpl,
        BusinessDayConvention bdc = Following,
        const DayCounter& dc = DayCounter());

    CustomBlackVolatility(
        PyObject* blackVolImpl,
        const Date& referenceDate,
        const Calendar& cal = Calendar(),
        BusinessDayConvention bdc = Following,
        const DayCounter& dc = DayCounter());

    CustomBlackVolatility(
        PyObject* blackVolImpl,
        Natural settlementDays,
        const Calendar& cal,
        BusinessDayConvention bdc = Following,
        const DayCounter& dc = DayCounter());
};

%{
class CustomCLVModelPayoff : public PlainVanillaPayoff {
  public:
    CustomCLVModelPayoff(
        PyObject* payoff,
        Option::Type type, Real strike) :
        PlainVanillaPayoff(type, strike),
        payoff_(payoff) {}
    Real operator()(Real x) const override {
        return PlainVanillaPayoff::operator()(payoff_(x));
    }
  private:
    UnaryFunction payoff_;
};
%}

%shared_ptr(CustomCLVModelPayoff)
class CustomCLVModelPayoff : public PlainVanillaPayoff {
  public:
    CustomCLVModelPayoff(
        PyObject* payoff,
        Option::Type type, Real strike);
};

%{
class CustomCostFunction : public CostFunction {
  private:
    PyObject* costFuncObj_;
  public:
    CustomCostFunction(PyObject* costFuncObj) : costFuncObj_(costFuncObj) {
        Py_XINCREF(costFuncObj_);
    }
    CustomCostFunction(const CustomCostFunction& f)
        : costFuncObj_(f.costFuncObj_) {
        Py_XINCREF(costFuncObj_);
    }
    CustomCostFunction(CustomCostFunction&& f) {
        std::swap(costFuncObj_, f.costFuncObj_);
    }
    CustomCostFunction& operator=(const CustomCostFunction& f) {
        if ((this != &f) && (costFuncObj_ != f.costFuncObj_)) {
            Py_XDECREF(costFuncObj_);
            costFuncObj_ = f.costFuncObj_;
            Py_XINCREF(costFuncObj_);
        }
        return *this;
    }
    ~CustomCostFunction() {
        Py_XDECREF(costFuncObj_);
    }

    Real value(const Array& x) const override {
        PyObject* array = PyList_New(x.size());
        PyObject* method = PyString_FromString("value");
        for (Size i = 0; i < x.size(); i++)
            PyList_SetItem(
                array, i, PyFloat_FromDouble(x[i]));
        PyObject* pyResult = PyObject_CallMethodObjArgs(
            costFuncObj_, method, array, NULL);
        Py_XDECREF(array);
        Py_XDECREF(method);
        QL_ENSURE(
            pyResult != NULL,
            "failed to call method `value`");
        Real result = PyFloat_AsDouble(pyResult);
        Py_XDECREF(pyResult);
        return result;
    }

    Array values(const Array& x) const override {
        PyObject* array = PyList_New(x.size());
        PyObject* method = PyString_FromString("values");
        for (Size i = 0; i < x.size(); i++)
            PyList_SetItem(
                array, i, PyFloat_FromDouble(x[i]));
        PyObject* pyResult = PyObject_CallMethodObjArgs(
            costFuncObj_, method, array, NULL);
        Py_XDECREF(array);
        Py_XDECREF(method);
        QL_ENSURE(
            pyResult != NULL,
            "failed to call method `values`");

        Array result(PyObject_Length(pyResult));
        for (Size i = 0; i < result.size(); i++) {
            PyObject* key = PyInt_FromLong(i);
            PyObject* item = PyObject_GetItem(pyResult, key);
            result[i] = PyFloat_AsDouble(item);
            Py_XDECREF(key);
            Py_XDECREF(item);
        }

        Py_XDECREF(pyResult);
        return result;
    }
};
%}

class CustomCostFunction : public CostFunction {
  public:
    CustomCostFunction(PyObject* function);
};

%{
class CustomConstraint : public Constraint {
    protected:
    class Impl : public Constraint::Impl {
        private:
        PyObject* impl_;
        public:
        Impl(PyObject* impl) : impl_(impl) {
            Py_XINCREF(impl_);
        }
        ~Impl() {
            Py_XDECREF(impl_);
        }

        bool test(const Array& params) const override {
            PyObject* array = PyList_New(params.size());
            PyObject* method = PyString_FromString("test");
            for (Size i = 0; i < params.size(); i++)
                PyList_SetItem(
                    array, i, PyFloat_FromDouble(params[i]));
            PyObject* pyResult = PyObject_CallMethodObjArgs(
                impl_, method, array, NULL);
            Py_XDECREF(array);
            Py_XDECREF(method);
            QL_ENSURE(
                pyResult != NULL,
                "failed to call method `test`");
            QL_ENSURE(
                static_cast<bool>(PyBool_Check(pyResult)),
                "method `test` should return bool");
            bool result = pyResult == Py_True;
            Py_XDECREF(pyResult);
            return result;
        }
        Array upperBound(const Array& params) const override {
            PyObject* array = PyList_New(params.size());
            PyObject* method = PyString_FromString("upperBound");
            for (Size i = 0; i < params.size(); i++)
                PyList_SetItem(
                    array, i, PyFloat_FromDouble(params[i]));
            PyObject* pyResult = PyObject_CallMethodObjArgs(
                impl_, method, array, NULL);
            Py_XDECREF(array);
            Py_XDECREF(method);
            QL_ENSURE(
                pyResult != NULL,
                "failed to call method `upperBound`");

            Array result(PyObject_Length(pyResult));
            for (Size i = 0; i < result.size(); i++) {
                PyObject* key = PyInt_FromLong(i);
                PyObject* item = PyObject_GetItem(pyResult, key);
                result[i] = PyFloat_AsDouble(item);
                Py_XDECREF(key);
                Py_XDECREF(item);
            }

            Py_XDECREF(pyResult);
            return result;
        }
        Array lowerBound(const Array& params) const override {
            PyObject* array = PyList_New(params.size());
            PyObject* method = PyString_FromString("lowerBound");
            for (Size i = 0; i < params.size(); i++)
                PyList_SetItem(
                    array, i, PyFloat_FromDouble(params[i]));
            PyObject* pyResult = PyObject_CallMethodObjArgs(
                impl_, method, array, NULL);
            Py_XDECREF(array);
            Py_XDECREF(method);
            QL_ENSURE(
                pyResult != NULL,
                "failed to call method `lowerBound`");
            
            Array result(PyObject_Length(pyResult));
            for (Size i = 0; i < result.size(); i++) {
                PyObject* key = PyInt_FromLong(i);
                PyObject* item = PyObject_GetItem(pyResult, key);
                result[i] = PyFloat_AsDouble(item);
                Py_XDECREF(key);
                Py_XDECREF(item);
            }

            Py_XDECREF(pyResult);
            return result;
        }
    };
    public:
    CustomConstraint(PyObject* impl) :
        Constraint(
            ext::shared_ptr<Constraint::Impl>(
                new CustomConstraint::Impl(impl))) {}
};
%}

%shared_ptr(CustomConstraint)
class CustomConstraint : public Constraint {
  public:
    CustomConstraint(PyObject* impl);
};

#endif
