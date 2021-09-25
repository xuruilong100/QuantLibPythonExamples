#ifndef ql_interpolation_trait2ds_all_i
#define ql_interpolation_trait2ds_all_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/interpolation/Interpolation2D.i

// 2D interpolation traits

%{
using QuantLib::Bicubic;
using QuantLib::BackwardflatLinear;
using QuantLib::Bilinear;
using QuantLib::Polynomial;
%}

class Bicubic {
  public:
    %extend {
        Interpolation2D interpolate(
            const Array& x, const Array& y, const Matrix& z) const {
                return self->interpolate(
                    x.begin(), x.end(), y.begin(), y.end(), z);
        }
    }
};

class BackwardflatLinear {
  public:
    %extend {
        Interpolation2D interpolate(
            const Array& x, const Array& y, const Matrix& z) const {
                return self->interpolate(
                    x.begin(), x.end(), y.begin(), y.end(), z);
        }
    }
};

class Bilinear {
  public:
    %extend {
        Interpolation2D interpolate(
            const Array& x, const Array& y, const Matrix& z) const {
                return self->interpolate(
                    x.begin(), x.end(), y.begin(), y.end(), z);
        }
    }
};

class Polynomial {
  public:
    %extend {
        Interpolation2D interpolate(
            const Array& x, const Array& y, const Matrix& z) const {
                return self->interpolate(
                    x.begin(), x.end(), y.begin(), y.end(), z);
        }
    }
};


#endif
