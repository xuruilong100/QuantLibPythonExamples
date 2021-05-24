#ifndef ql_parameter_i
#define ql_parameter_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i

%{
using QuantLib::Parameter;
using QuantLib::ConstantParameter;
using QuantLib::NullParameter;
using QuantLib::PiecewiseConstantParameter;
%}

class Parameter {
  public:
    Parameter();
    const Array& params() const;
    void setParam(Size i, Real x);
    bool testParams(const Array& params) const;
    Size size() const ;
    Real operator()(Time t) const;
    const Constraint& constraint() const;
};

//! Standard constant parameter \f$ a(t) = a \f$
class ConstantParameter : public Parameter {
  public:
    ConstantParameter(
        const Constraint& constraint);
    ConstantParameter(
        Real value, const Constraint& constraint);

};

//! %Parameter which is always zero \f$ a(t) = 0 \f$
class NullParameter : public Parameter {
  public:
    NullParameter();
};

//! Piecewise-constant parameter
/*! \f$ a(t) = a_i if t_{i-1} \geq t < t_i \f$.
    This kind of parameter is usually used to enhance the fitting of a
    model
*/
class PiecewiseConstantParameter : public Parameter {
  public:
     PiecewiseConstantParameter(
         const std::vector<Time>& times,
         const Constraint& constraint=QuantLib::NoConstraint());
};

#endif
