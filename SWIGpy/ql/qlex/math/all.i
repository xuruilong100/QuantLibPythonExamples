#ifndef qlex_math_all
#define qlex_math_all

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i

%{
using QuantLib::CubicSpline;
using QuantLib::QuadraticSpline;
%}

class CubicSpline {
  public:
    CubicSpline(const std::vector<Real>& knots);
    Real operator()(Natural i, Real x) const;
};

class QuadraticSpline {
  public:
    QuadraticSpline(const std::vector<Real>& knots);
    Real operator()(Natural i, Real x) const;
};

#endif
