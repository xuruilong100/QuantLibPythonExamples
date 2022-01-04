#ifndef ql_interpolation_safetrait2ds_all_i
#define ql_interpolation_safetrait2ds_all_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/interpolation/safeinterpolation2ds/all.i

%{
class SafeBicubic {
  public:
    SafeInterpolation2D interpolate(
        const Array& x, const Array& y, const Matrix& z) const {
            return SafeBicubicSpline(
                x, y, z);
    }
};

class SafeBackwardflatLinear {
  public:
    SafeInterpolation2D interpolate(
        const Array& x, const Array& y, const Matrix& z) const {
            return SafeBackwardflatLinearInterpolation(
                x, y, z);
    }
};

class SafeBilinear {
  public:
    SafeInterpolation2D interpolate(
        const Array& x, const Array& y, const Matrix& z) const {
            return SafeBilinearInterpolation(
                x, y, z);
    }
};

class SafePolynomial {
  public:
    SafeInterpolation2D interpolate(
        const Array& x, const Array& y, const Matrix& z) const {
            return SafePolynomial2DSpline(
                x, y, z);
    }
};
%}

class SafeBicubic {
  public:
    SafeInterpolation2D interpolate(
        const Array& x, const Array& y, const Matrix& z) const;
};

class SafeBackwardflatLinear {
  public:
    SafeInterpolation2D interpolate(
        const Array& x, const Array& y, const Matrix& z) const;
};

class SafeBilinear {
  public:
    SafeInterpolation2D interpolate(
        const Array& x, const Array& y, const Matrix& z) const;
};

class SafePolynomial {
  public:
    SafeInterpolation2D interpolate(
        const Array& x, const Array& y, const Matrix& z) const;
};

#endif
