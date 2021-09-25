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
using QuantLib::InterpolationParameter;
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

class ConstantParameter : public Parameter {
  public:
    ConstantParameter(
        const Constraint& constraint);
    ConstantParameter(
        Real value, const Constraint& constraint);
};

class NullParameter : public Parameter {
  public:
    NullParameter();
};

class PiecewiseConstantParameter : public Parameter {
  public:
    PiecewiseConstantParameter(
        std::vector<Time> times,
        const Constraint& constraint = NoConstraint());
};

#endif
