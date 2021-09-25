#ifndef ql_interpolation_interpolation2d_all_i
#define ql_interpolation_interpolation2d_all_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/interpolation/Interpolation2D.i

%{
using QuantLib::BackwardflatLinearInterpolation;
using QuantLib::BicubicSpline;
using QuantLib::BilinearInterpolation;
using QuantLib::FlatExtrapolator2D;
using QuantLib::Polynomial2DSpline;
%}

%shared_ptr(BackwardflatLinearInterpolation)
class BackwardflatLinearInterpolation : public Interpolation2D {
  public:
    %extend {
        BackwardflatLinearInterpolation(
            const Array& x, const Array& y, const Matrix& z) {
            return new BackwardflatLinearInterpolation(
                x.begin(), x.end(), y.begin(), y.end(), z);
        }
    }
};

%shared_ptr(BicubicSpline)
class BicubicSpline : public Interpolation2D {
  public:
    %extend {
        BicubicSpline(
            const Array& x, const Array& y, const Matrix& z) {
            return new BicubicSpline(
                x.begin(), x.end(), y.begin(), y.end(), z);
        }
    }
    Real derivativeX(Real x, Real y) const;
    Real derivativeY(Real x, Real y) const;
    Real secondDerivativeX(Real x, Real y) const;
    Real secondDerivativeY(Real x, Real y) const;
    Real derivativeXY(Real x, Real y) const;
};

%shared_ptr(BilinearInterpolation)
class BilinearInterpolation : public Interpolation2D {
  public:
    %extend {
        BilinearInterpolation(
            const Array& x, const Array& y, const Matrix& z) {
            return new BilinearInterpolation(
                x.begin(), x.end(), y.begin(), y.end(), z);
        }
    }
};

%shared_ptr(FlatExtrapolator2D)
class FlatExtrapolator2D : public Interpolation2D {
  public:
    FlatExtrapolator2D(
        const ext::shared_ptr<Interpolation2D>& decoratedInterpolation);
};

%shared_ptr(Polynomial2DSpline)
class Polynomial2DSpline : public Interpolation2D {
  public:
    %extend {
        Polynomial2DSpline(
            const Array& x, const Array& y, const Matrix& z) {
            return new Polynomial2DSpline(
                x.begin(), x.end(), y.begin(), y.end(), z);
        }
    }
};

#endif
