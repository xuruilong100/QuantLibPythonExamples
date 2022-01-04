#ifndef ql_interpolation_safeinterpolation2d_all_i
#define ql_interpolation_safeinterpolation2d_all_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/interpolation/SafeInterpolation2D.i

%{
class SafeBackwardflatLinearInterpolation : public SafeInterpolation2D {
  public:
    SafeBackwardflatLinearInterpolation(
        const Array& x, const Array& y, const Matrix& z) :
        SafeInterpolation2D(x, y, z) {
        i_ = ext::shared_ptr<Interpolation2D>(
            new BackwardflatLinearInterpolation(
                x_.begin(), x_.end(), y_.begin(), y_.end(), z_));
    }
};

class SafeBicubicSpline : public SafeInterpolation2D {
  public:
    SafeBicubicSpline(
        const Array& x, const Array& y, const Matrix& z) :
        SafeInterpolation2D(x, y, z) {
        i_ = ext::shared_ptr<Interpolation2D>(
            new BicubicSpline(
                x_.begin(), x_.end(), y_.begin(), y_.end(), z_));
    }

    Real derivativeX(Real x, Real y) const {return ext::dynamic_pointer_cast<BicubicSpline>(i_)->derivativeX(x, y);}
    Real derivativeY(Real x, Real y) const {return ext::dynamic_pointer_cast<BicubicSpline>(i_)->derivativeY(x, y);}
    Real secondDerivativeX(Real x, Real y) const {return ext::dynamic_pointer_cast<BicubicSpline>(i_)->secondDerivativeX(x, y);}
    Real secondDerivativeY(Real x, Real y) const {return ext::dynamic_pointer_cast<BicubicSpline>(i_)->secondDerivativeY(x, y);}
    Real derivativeXY(Real x, Real y) const {return ext::dynamic_pointer_cast<BicubicSpline>(i_)->derivativeXY(x, y);}
};

class SafeBilinearInterpolation : public SafeInterpolation2D {
  public:
    SafeBilinearInterpolation(
        const Array& x, const Array& y, const Matrix& z) :
        SafeInterpolation2D(x, y, z) {
        i_ = ext::shared_ptr<Interpolation2D>(
            new BilinearInterpolation(
                x_.begin(), x_.end(), y_.begin(), y_.end(), z_));
    }
};

class SafePolynomial2DSpline : public SafeInterpolation2D {
  public:
    SafePolynomial2DSpline(
        const Array& x, const Array& y, const Matrix& z) :
        SafeInterpolation2D(x, y, z) {
        i_ = ext::shared_ptr<Interpolation2D>(
            new Polynomial2DSpline(
                x_.begin(), x_.end(), y_.begin(), y_.end(), z_));
    }
};

class SafeKernelInterpolation2D : public SafeInterpolation2D{
  public:
    SafeKernelInterpolation2D(
        const Array& x,
        const Array& y,
        const Matrix& z,
        const GaussianKernel& kernel) :
        SafeInterpolation2D(x, y, z) {
        i_ = ext::shared_ptr<Interpolation2D>(
            new KernelInterpolation2D(
                x_.begin(), x_.end(),
                y_.begin(), y_.end(),
                z, kernel));
    }
    SafeKernelInterpolation2D(
        const Array& x,
        const Array& y,
        const Matrix& z,
        PyObject* kernel) :
        SafeInterpolation2D(x, y, z) {
        i_ = ext::shared_ptr<Interpolation2D>(
            new KernelInterpolation2D(
                x_.begin(), x_.end(),
                y_.begin(), y_.end(),
                z, UnaryFunction(kernel)));
    }
};
%}

%shared_ptr(SafeBackwardflatLinearInterpolation)
class SafeBackwardflatLinearInterpolation : public SafeInterpolation2D {
  public:
    SafeBackwardflatLinearInterpolation(
        const Array& x, const Array& y, const Matrix& z);
};

%shared_ptr(SafeBicubicSpline)
class SafeBicubicSpline : public SafeInterpolation2D {
  public:
    SafeBicubicSpline(
        const Array& x, const Array& y, const Matrix& z);

    Real derivativeX(Real x, Real y) const;
    Real derivativeY(Real x, Real y) const;
    Real secondDerivativeX(Real x, Real y) const;
    Real secondDerivativeY(Real x, Real y) const;
    Real derivativeXY(Real x, Real y) const;
};

%shared_ptr(SafeBilinearInterpolation)
class SafeBilinearInterpolation : public SafeInterpolation2D {
  public:
    SafeBilinearInterpolation(
        const Array& x, const Array& y, const Matrix& z);
};

%shared_ptr(SafePolynomial2DSpline)
class SafePolynomial2DSpline : public SafeInterpolation2D {
  public:
    SafePolynomial2DSpline(
        const Array& x, const Array& y, const Matrix& z);
};

%shared_ptr(SafeKernelInterpolation2D)
class SafeKernelInterpolation2D : public SafeInterpolation2D{
  public:
    SafeKernelInterpolation2D(
        const Array& x,
        const Array& y,
        const Matrix& z,
        const GaussianKernel& kernel);
    SafeKernelInterpolation2D(
        const Array& x,
        const Array& y,
        const Matrix& z,
        PyObject* kernel);
};

#endif
