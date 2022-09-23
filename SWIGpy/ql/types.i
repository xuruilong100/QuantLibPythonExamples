#ifndef ql_types_i
#define ql_types_i

%include ../ql/alltypes.i
%include common.i
%include std_common.i

%{
using QuantLib::Integer;
using QuantLib::BigInteger;
using QuantLib::Natural;
using QuantLib::BigNatural;
using QuantLib::Real;
using QuantLib::Decimal;
using QuantLib::Time;
using QuantLib::Rate;
using QuantLib::Spread;
using QuantLib::DiscountFactor;
using QuantLib::Volatility;
using QuantLib::Probability;
using QuantLib::Size;
%}

typedef int Integer;
typedef long BigInteger;
typedef unsigned int Natural;
typedef unsigned long BigNatural;
typedef double Real;

typedef Real Decimal;
typedef Real Time;
typedef Real Rate;
typedef Real Spread;
typedef Real DiscountFactor;
typedef Real Volatility;
typedef Real Probability;
// typedef size_t Size;        // for windows
typedef BigNatural Size;    // for ubuntu

#endif
