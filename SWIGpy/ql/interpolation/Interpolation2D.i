#ifndef ql_interpolation_Interpolation2D_i
#define ql_interpolation_Interpolation2D_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i

%{
using QuantLib::Interpolation2D;
%}

%shared_ptr(Interpolation2D)
class Interpolation2D : public Extrapolator {
  private:
    Interpolation2D();
  public:
    Real xMin() const;
    Real xMax() const;
    std::vector<Real> xValues() const;
    Size locateX(Real x) const;
    Real yMin() const;
    Real yMax() const;
    std::vector<Real> yValues() const;
    Size locateY(Real y) const;
    const Matrix& zData() const;
    bool isInRange(Real x, Real y) const;
    void update();
    %extend {
        Real __call__(
          Real x, Real y, bool allowExtrapolation = false) {
          return (*self)(x, y, allowExtrapolation);
        }
    }
};

#endif
