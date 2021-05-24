#ifndef ql_rounding_i
#define ql_rounding_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i

%{
using QuantLib::Rounding;
using QuantLib::CeilingTruncation;
using QuantLib::ClosestRounding;
using QuantLib::DownRounding;
using QuantLib::FloorTruncation;
using QuantLib::UpRounding;
%}

class Rounding {
  public:
    Rounding();
    Decimal operator()(Decimal value) const;
};

class UpRounding : public Rounding {
  public:
    UpRounding(Integer precision, Integer digit = 5);
};

class DownRounding : public Rounding {
  public:
    DownRounding(Integer precision, Integer digit = 5);
};

class ClosestRounding : public Rounding {
  public:
    ClosestRounding(Integer precision, Integer digit = 5);
};

class CeilingTruncation : public Rounding {
  public:
    CeilingTruncation(Integer precision, Integer digit = 5);
};

class FloorTruncation : public Rounding {
  public:
    FloorTruncation(Integer precision, Integer digit = 5);
};

#endif
