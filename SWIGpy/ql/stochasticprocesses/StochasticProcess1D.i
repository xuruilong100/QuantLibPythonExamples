#ifndef ql_stochasticprocesses_StochasticProcess1D_i
#define ql_stochasticprocesses_StochasticProcess1D_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i

%{
using QuantLib::StochasticProcess1D;
using QuantLib::EulerDiscretization;
using QuantLib::EndEulerDiscretization;
typedef StochasticProcess1D::discretization discretization1D;
%}

%shared_ptr(discretization1D)
class discretization1D {
  private:
    discretization1D();
  public:
    Real drift(
        const StochasticProcess1D&,
        Time t0, Real x0, Time dt) const;
    Real diffusion(
        const StochasticProcess1D&,
        Time t0, Real x0, Time dt) const;
    Real variance(
        const StochasticProcess1D&,
        Time t0, Real x0, Time dt) const;
};

%shared_ptr(EulerDiscretization)
class EulerDiscretization : public discretization, public discretization1D {
};

%shared_ptr(EndEulerDiscretization)
class EndEulerDiscretization : public discretization, public discretization1D {
};

%shared_ptr(StochasticProcess1D)
class StochasticProcess1D : public StochasticProcess {
  public:
      Real x0() const;
      Real drift(Time t, Real x) const;
      Real diffusion(Time t, Real x) const;
      Real expectation(Time t0, Real x0, Time dt) const;
      Real stdDeviation(Time t0, Real x0, Time dt) const;
      Real variance(Time t0, Real x0, Time dt) const;
      Real evolve(Time t0, Real x0, Time dt, Real dw) const;
      Real apply(Real x0, Real dx) const;
};

%template(StochasticProcess1DVector) std::vector<ext::shared_ptr<StochasticProcess1D>>;

#endif
