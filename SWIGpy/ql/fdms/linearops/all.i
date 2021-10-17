#ifndef ql_fdms_linearops_all_i
#define ql_fdms_linearops_all_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/linearalgebra.i
%include ../ql/fdms/FdmLinearOp.i

%{
using QuantLib::FdmLinearOpComposite;
using QuantLib::TripleBandLinearOp;
using QuantLib::NinePointLinearOp;
using QuantLib::NthOrderDerivativeOp;

using QuantLib::Fdm2dBlackScholesOp;
using QuantLib::FdmBatesOp;
using QuantLib::FdmBlackScholesOp;
using QuantLib::FdmBlackScholesFwdOp;
using QuantLib::FdmCEVOp;
using QuantLib::FdmCIROp;
using QuantLib::FdmDupire1dOp;
using QuantLib::FdmExtOUJumpOp;
using QuantLib::FdmExtendedOrnsteinUhlenbeckOp;
using QuantLib::FdmG2Op;
using QuantLib::FdmHestonFwdOp;
using QuantLib::FdmHestonHullWhiteOp;
using QuantLib::FdmHestonOp;
using QuantLib::FdmHullWhiteOp;
using QuantLib::FdmKlugeExtOUOp;
using QuantLib::FdmLocalVolFwdOp;
using QuantLib::FdmOrnsteinUhlenbeckOp;
using QuantLib::FdmSabrOp;
using QuantLib::FdmSquareRootFwdOp;
using QuantLib::FdmZabrOp;

using QuantLib::FirstDerivativeOp;
using QuantLib::SecondDerivativeOp;
using QuantLib::SecondOrderMixedDerivativeOp;
using QuantLib::ModTripleBandLinearOp;
%}

%shared_ptr(FdmLinearOpComposite)
class FdmLinearOpComposite : public FdmLinearOp {
  public:
    Size size() const;
    void setTime(Time t1, Time t2);

    Array apply_mixed(const Array& r) const;
    Array apply_direction(Size direction, const Array& r) const;
    Array solve_splitting(Size direction, const Array& r, Real s) const;
    Array preconditioner(const Array& r, Real s) const;

  private:
      FdmLinearOpComposite();
};

%{
class FdmLinearOpCompositeProxy : public FdmLinearOpComposite {
  public:
    FdmLinearOpCompositeProxy(
        PyObject* callback) : callback_(callback) {
        Py_XINCREF(callback_);
    }

    FdmLinearOpCompositeProxy& operator=(
        const FdmLinearOpCompositeProxy& f) {
        if ((this != &f) && (callback_ != f.callback_)) {
            Py_XDECREF(callback_);
            callback_ = f.callback_;
            Py_XINCREF(callback_);
        }
        return *this;
    }

    FdmLinearOpCompositeProxy(
        const FdmLinearOpCompositeProxy& p)
        : callback_(p.callback_) {
        Py_XINCREF(callback_);
    }

    ~FdmLinearOpCompositeProxy() {
        Py_XDECREF(callback_);
    }

    Size size() const {
        PyObject* pyResult = PyObject_CallMethod(
            callback_, "size", NULL);

        QL_ENSURE(
            pyResult != NULL,
            "failed to call size() on Python object");

        Size result = PyInt_AsLong(pyResult);
        Py_XDECREF(pyResult);

        return result;
    }

    void setTime(Time t1, Time t2) {
        PyObject* pyResult = PyObject_CallMethod(
            callback_, "setTime", "dd", t1, t2);

        QL_ENSURE(
            pyResult != NULL,
            "failed to call setTime() on Python object");

        Py_XDECREF(pyResult);
    }

    Disposable<Array> apply(const Array& r) const {
        return apply(r, "apply");
    }

    Disposable<Array> apply_mixed(const Array& r) const {
        return apply(r, "apply_mixed");
    }

    Disposable<Array> apply_direction(Size direction, const Array& r) const {
        PyObject* pyArray = SWIG_NewPointerObj(
            SWIG_as_voidptr(&r), SWIGTYPE_p_Array, 0);

        PyObject* pyResult = PyObject_CallMethod(
            callback_, "apply_direction", "kO",
            (unsigned long)(direction), pyArray);

        Py_XDECREF(pyArray);

        return extractArray(pyResult, "apply_direction");
    }

    Disposable<Array> solve_splitting(
        Size direction, const Array& r, Real s) const {

        PyObject* pyArray = SWIG_NewPointerObj(
            SWIG_as_voidptr(&r), SWIGTYPE_p_Array, 0);

        PyObject* pyResult = PyObject_CallMethod(
            callback_, "solve_splitting", "kOd",
            (unsigned long)(direction), pyArray, s);

        Py_XDECREF(pyArray);

        return extractArray(
            pyResult, "solve_splitting");
    }

    Disposable<Array> preconditioner(const Array& r, Real s) const {
        PyObject* pyArray = SWIG_NewPointerObj(
            SWIG_as_voidptr(&r), SWIGTYPE_p_Array, 0);

        PyObject* pyResult = PyObject_CallMethod(
            callback_, "preconditioner", "Od", pyArray, s);

        Py_XDECREF(pyArray);

        return extractArray(pyResult, "preconditioner");
    }

  private:
    Disposable<Array> apply(
        const Array& r, const std::string& methodName) const {

        PyObject* pyArray = SWIG_NewPointerObj(
            SWIG_as_voidptr(&r), SWIGTYPE_p_Array, 0);

#if !defined(PY_VERSION_HEX) || PY_VERSION_HEX < 0x03040000
        std::vector<char> cstr(
            methodName.c_str(), methodName.c_str() + methodName.size() + 1);
        PyObject* pyResult = PyObject_CallMethod(
            callback_, &cstr[0], "O", pyArray);
#else
        PyObject* pyResult = PyObject_CallMethod(
            callback_, methodName.c_str(), "O", pyArray);
#endif
        Py_XDECREF(pyArray);

        return extractArray(pyResult, methodName);
    }

  private:
    PyObject* callback_;
};
%}

%shared_ptr(FdmLinearOpCompositeProxy)
class FdmLinearOpCompositeProxy : public FdmLinearOpComposite {
  public:
    FdmLinearOpCompositeProxy(PyObject* callback);
};

%shared_ptr(TripleBandLinearOp)
class TripleBandLinearOp : public FdmLinearOp {
  public:
    TripleBandLinearOp(
        Size direction,
        const ext::shared_ptr<FdmMesher>& mesher);

    Array apply(const Array& r) const;
    Array solve_splitting(const Array& r, Real a, Real b = 1.0) const;

    TripleBandLinearOp mult(const Array& u) const;
    TripleBandLinearOp multR(const Array& u) const;
    TripleBandLinearOp add(const TripleBandLinearOp& m) const;
    TripleBandLinearOp add(const Array& u) const;

    void axpyb(
        const Array& a, const TripleBandLinearOp& x,
        const TripleBandLinearOp& y, const Array& b);
    void swap(TripleBandLinearOp& m);
};

%shared_ptr(NinePointLinearOp)
class NinePointLinearOp : public FdmLinearOp {
  public:
    NinePointLinearOp(
        Size d0, Size d1,
        const ext::shared_ptr<FdmMesher>& mesher);
};

%shared_ptr(NthOrderDerivativeOp)
class NthOrderDerivativeOp : public FdmLinearOp {
  public:
    NthOrderDerivativeOp(
        Size direction, Size order, Integer nPoints,
        const ext::shared_ptr<FdmMesher>& mesher);
};

%shared_ptr(FdmBatesOp)
class FdmBatesOp : public FdmLinearOpComposite {
  public:
    FdmBatesOp(
        const ext::shared_ptr<FdmMesher>& mesher,
        const ext::shared_ptr<BatesProcess>& batesProcess,
        const FdmBoundaryConditionSet& bcSet,
        Size integroIntegrationOrder,
        const ext::shared_ptr<FdmQuantoHelper>& quantoHelper = ext::shared_ptr<FdmQuantoHelper>());
};

%shared_ptr(FdmBlackScholesOp)
class FdmBlackScholesOp : public FdmLinearOpComposite {
  public:
    FdmBlackScholesOp(
        const ext::shared_ptr<FdmMesher>& mesher,
        const ext::shared_ptr<GeneralizedBlackScholesProcess>& process,
        Real strike,
        bool localVol = false,
        Real illegalLocalVolOverwrite = -Null<Real>(),
        Size direction = 0,
        const ext::shared_ptr<FdmQuantoHelper>& quantoHelper = ext::shared_ptr<FdmQuantoHelper>());
};

%shared_ptr(Fdm2dBlackScholesOp)
class Fdm2dBlackScholesOp : public FdmLinearOpComposite {
  public:
    Fdm2dBlackScholesOp(
        const ext::shared_ptr<FdmMesher>& mesher,
        const ext::shared_ptr<GeneralizedBlackScholesProcess>& p1,
        const ext::shared_ptr<GeneralizedBlackScholesProcess>& p2,
        Real correlation,
        Time maturity,
        bool localVol = false,
        Real illegalLocalVolOverwrite = -Null<Real>());
};

%shared_ptr(FdmCEVOp)
class FdmCEVOp : public FdmLinearOpComposite {
  public:
      FdmCEVOp(
        const ext::shared_ptr<FdmMesher>& mesher,
        const ext::shared_ptr<YieldTermStructure>& rTS,
        Real f0, Real alpha, Real beta,
        Size direction);
};

%shared_ptr(FdmCIROp)
class FdmCIROp : public FdmLinearOpComposite {
  public:
    FdmCIROp(const ext::shared_ptr<FdmMesher>& mesher,
             const ext::shared_ptr<CoxIngersollRossProcess>& cirProcess,
             const ext::shared_ptr<GeneralizedBlackScholesProcess>& bsProcess,
             Real rho,
             Real strike);
};

%shared_ptr(FdmExtOUJumpOp)
class FdmExtOUJumpOp : public FdmLinearOpComposite {
  public:
    FdmExtOUJumpOp(
        const ext::shared_ptr<FdmMesher>& mesher,
        const ext::shared_ptr<ExtOUWithJumpsProcess>& process,
        const ext::shared_ptr<YieldTermStructure>& rTS,
        const FdmBoundaryConditionSet& bcSet,
        Size integroIntegrationOrder);
};

%shared_ptr(FdmExtendedOrnsteinUhlenbeckOp)
class FdmExtendedOrnsteinUhlenbeckOp : public FdmLinearOpComposite {
  public:
    FdmExtendedOrnsteinUhlenbeckOp(
        const ext::shared_ptr<FdmMesher>& mesher,
        ext::shared_ptr<ExtendedOrnsteinUhlenbeckProcess> p,
        ext::shared_ptr<YieldTermStructure> rTS,
        FdmBoundaryConditionSet bcSet,
        Size direction = 0);
};

%shared_ptr(FdmKlugeExtOUOp)
class FdmKlugeExtOUOp : public FdmLinearOpComposite {
  public:
    FdmKlugeExtOUOp(
        const ext::shared_ptr<FdmMesher>& mesher,
        const ext::shared_ptr<KlugeExtOUProcess>& klugeOUProcess,
        const ext::shared_ptr<YieldTermStructure>& rTS,
        const FdmBoundaryConditionSet& bcSet,
        Size integroIntegrationOrder);
};

%shared_ptr(FdmG2Op)
class FdmG2Op : public FdmLinearOpComposite {
  public:
    FdmG2Op(
        const ext::shared_ptr<FdmMesher>& mesher,
        const ext::shared_ptr<G2>& model,
        Size direction1, Size direction2);
};

%shared_ptr(FdmHestonHullWhiteOp)
class FdmHestonHullWhiteOp : public FdmLinearOpComposite {
  public:
    FdmHestonHullWhiteOp(
        const ext::shared_ptr<FdmMesher>& mesher,
        const ext::shared_ptr<HestonProcess>& hestonProcess,
        const ext::shared_ptr<HullWhiteProcess>& hwProcess,
        Real equityShortRateCorrelation);
};

%shared_ptr(FdmHestonOp)
class FdmHestonOp : public FdmLinearOpComposite {
  public:
    FdmHestonOp(
	    const ext::shared_ptr<FdmMesher>& mesher,
	    const ext::shared_ptr<HestonProcess>& hestonProcess,
	    const ext::shared_ptr<FdmQuantoHelper>& quantoHelper = ext::shared_ptr<FdmQuantoHelper>(),
	    const ext::shared_ptr<LocalVolTermStructure>& leverageFct = ext::shared_ptr<LocalVolTermStructure>());
};

%shared_ptr(FdmHullWhiteOp)
class FdmHullWhiteOp : public FdmLinearOpComposite {
  public:
    FdmHullWhiteOp(
        const ext::shared_ptr<FdmMesher>& mesher,
        const ext::shared_ptr<HullWhite>& model,
        Size direction);
};

%shared_ptr(FdmLocalVolFwdOp)
class FdmLocalVolFwdOp : public FdmLinearOpComposite {
  public:
      FdmLocalVolFwdOp(
        const ext::shared_ptr<FdmMesher>& mesher,
        const ext::shared_ptr<Quote>& spot,
        ext::shared_ptr<YieldTermStructure> rTS,
        ext::shared_ptr<YieldTermStructure> qTS,
        const ext::shared_ptr<LocalVolTermStructure>& localVol,
        Size direction = 0);
};

%shared_ptr(FdmOrnsteinUhlenbeckOp)
class FdmOrnsteinUhlenbeckOp : public FdmLinearOpComposite {
  public:
    FdmOrnsteinUhlenbeckOp(
        const ext::shared_ptr<FdmMesher>& mesher,
        const ext::shared_ptr<OrnsteinUhlenbeckProcess>& p,
        const ext::shared_ptr<YieldTermStructure>& rTS,
        Size direction = 0);
};

%shared_ptr(FdmSabrOp)
class FdmSabrOp : public FdmLinearOpComposite {
  public:
      FdmSabrOp(
        const ext::shared_ptr<FdmMesher>& mesher,
        const ext::shared_ptr<YieldTermStructure>& rTS,
        Real f0,
        Real alpha,
        Real beta,
        Real nu,
        Real rho);
};

%shared_ptr(FdmZabrOp)
class FdmZabrOp : public FdmLinearOpComposite {
  public:
    FdmZabrOp(
        const ext::shared_ptr<FdmMesher>& mesher,
        const Real beta,
        const Real nu,
        const Real rho,
        const Real gamma);
};

%shared_ptr(FdmDupire1dOp)
class FdmDupire1dOp : public FdmLinearOpComposite {
  public:
    FdmDupire1dOp(
        const ext::shared_ptr<FdmMesher>& mesher,
        const Array& localVolatility);
};

%shared_ptr(FdmBlackScholesFwdOp)
class FdmBlackScholesFwdOp : public FdmLinearOpComposite {
  public:
    FdmBlackScholesFwdOp(
        const ext::shared_ptr<FdmMesher>& mesher,
        const ext::shared_ptr<GeneralizedBlackScholesProcess>& process,
        Real strike,
        bool localVol = false,
        Real illegalLocalVolOverwrite = -Null<Real>(),
        Size direction = 0);
};

%shared_ptr(FdmSquareRootFwdOp)
class FdmSquareRootFwdOp : public FdmLinearOpComposite {
  public:
    enum TransformationType { Plain, Power, Log };

    FdmSquareRootFwdOp(
        const ext::shared_ptr<FdmMesher>& mesher,
        Real kappa, Real theta, Real sigma,
        Size direction,
        TransformationType type = Plain);
};

%shared_ptr(FdmHestonFwdOp)
class FdmHestonFwdOp : public FdmLinearOpComposite {
  public:
    FdmHestonFwdOp(
        const ext::shared_ptr<FdmMesher>& mesher,
        const ext::shared_ptr<HestonProcess>& process,
        FdmSquareRootFwdOp::TransformationType type = FdmSquareRootFwdOp::Plain,
        const ext::shared_ptr<LocalVolTermStructure>& leverageFct = ext::shared_ptr<LocalVolTermStructure>());
};

%shared_ptr(FirstDerivativeOp)
class FirstDerivativeOp : public TripleBandLinearOp {
  public:
    FirstDerivativeOp(
        Size direction,
        const ext::shared_ptr<FdmMesher>& mesher);
};

%shared_ptr(SecondDerivativeOp)
class SecondDerivativeOp : public TripleBandLinearOp {
  public:
    SecondDerivativeOp(
        Size direction,
        const ext::shared_ptr<FdmMesher>& mesher);
};

%shared_ptr(SecondOrderMixedDerivativeOp)
class SecondOrderMixedDerivativeOp : public NinePointLinearOp {
public:
    SecondOrderMixedDerivativeOp(
        Size d0, Size d1,
        const ext::shared_ptr<FdmMesher>& mesher);
};

%shared_ptr(ModTripleBandLinearOp)
class ModTripleBandLinearOp : public TripleBandLinearOp {
  public:
    ModTripleBandLinearOp(
        Size direction,
        const ext::shared_ptr<FdmMesher>& mesher);
};

#endif
