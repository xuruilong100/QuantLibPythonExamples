#ifndef ql_ode_i
#define ql_ode_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i

%{
class OdeFct {
  public:
    OdeFct(PyObject* function) : function_(function) {
        Py_XINCREF(function_);
    }
    OdeFct(const OdeFct& f)
        : function_(f.function_) {
        Py_XINCREF(function_);
    }
    OdeFct& operator=(const OdeFct& f) {
        if ((this != &f) && (function_ != f.function_)) {
            Py_XDECREF(function_);
            function_ = f.function_;
            Py_XINCREF(function_);
        }
        return *this;
    }
    ~OdeFct() {
        Py_XDECREF(function_);
    }

    const Disposable<std::vector<Real>> operator()(
        Real x, const std::vector<Real>& y) const {

        PyObject* pyY = PyList_New(y.size());
        for (Size i = 0; i < y.size(); ++i)
            PyList_SetItem(
                pyY, i, PyFloat_FromDouble(y[i]));

        PyObject* pyResult = PyObject_CallFunction(
            function_, "dO", x, pyY);

        Py_XDECREF(pyY);

        QL_ENSURE(
            pyResult != NULL && PyList_Check(pyResult),
            "failed to call Python function");

        std::vector<Real> retVal(y.size());
        for (Size i = 0; i < y.size(); ++i)
            retVal[i] = PyFloat_AsDouble(
                PyList_GET_ITEM(pyResult, i));

        Py_XDECREF(pyResult);
        return retVal;
    }

  private:
    PyObject* function_;
};
%}

%{
using QuantLib::AdaptiveRungeKutta;
%}

template <class T = Real>
class AdaptiveRungeKutta {
  public:
    AdaptiveRungeKutta(
        const Real eps=1.0e-6,
        const Real h1=1.0e-4,
        const Real hmin=0.0);

    %extend {
        T operator()(
            PyObject* fct, T y1, Real x1, Real x2) {
            BinaryFunction f(fct);
            return self->operator()(f, y1, x1, x2);
        }
        std::vector<T> operator()(
            PyObject* fct, const std::vector<T>& y1,
            Real x1, Real x2) {
            OdeFct f(fct);
            return self->operator()(f, y1, x1, x2);
        }
    }
};

%template(RungeKutta) AdaptiveRungeKutta<Real>;

#endif
