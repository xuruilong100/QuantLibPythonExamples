#ifndef ql_interpolation_Interpolation_i
#define ql_interpolation_Interpolation_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i

%{
using QuantLib::Interpolation;
using QuantLib::MixedInterpolation;
%}

struct MixedInterpolation {
    enum Behavior {
        ShareRanges,
        SplitRanges
    };
};

%shared_ptr(Interpolation)
class Interpolation : public Extrapolator {
  private:
    Interpolation();
  public:
    bool empty() const;
    Real primitive(Real x, bool allowExtrapolation = false) const;
    Real derivative(Real x, bool allowExtrapolation = false) const;
    Real secondDerivative(Real x, bool allowExtrapolation = false) const;
    Real xMin() const;
    Real xMax() const;
    bool isInRange(Real x) const;
    void update();
    %extend {
        Real __call__(
          Real x, bool allowExtrapolation = false) {
          return (*self)(x, allowExtrapolation);
        }
    }
};

#endif
