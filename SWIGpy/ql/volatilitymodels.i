#ifndef ql_volatilitymodels_i
#define ql_volatilitymodels_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i

%{
using QuantLib::ConstantEstimator;
using QuantLib::ParkinsonSigma;
using QuantLib::SimpleLocalEstimator;
using QuantLib::GarmanKlassSigma1;
using QuantLib::GarmanKlassSigma3;
using QuantLib::GarmanKlassSigma4;
using QuantLib::GarmanKlassSigma5;
using QuantLib::GarmanKlassSigma6;
%}

class ConstantEstimator {
  public:
    ConstantEstimator(Size size);
    TimeSeries<Volatility> calculate(const TimeSeries<Volatility>&);
};

class ParkinsonSigma {
  public:
    ParkinsonSigma(Real yearFraction);
    TimeSeries<Volatility> calculate(const TimeSeries<IntervalPrice>&);
};

class GarmanKlassSigma1 {
  public:
    GarmanKlassSigma1(Real yearFraction, Real marketOpenFraction);
    TimeSeries<Volatility> calculate(const TimeSeries<IntervalPrice>&);
};

class GarmanKlassSigma3 {
  public:
    GarmanKlassSigma3(Real yearFraction, Real marketOpenFraction);
    TimeSeries<Volatility> calculate(const TimeSeries<IntervalPrice>&);
};

class GarmanKlassSigma4 {
  public:
    GarmanKlassSigma4(Real yearFraction);
    TimeSeries<Volatility> calculate(const TimeSeries<IntervalPrice>&);
};

class GarmanKlassSigma5 {
  public:
    GarmanKlassSigma5(Real yearFraction);
    TimeSeries<Volatility> calculate(const TimeSeries<IntervalPrice>&);
};

class GarmanKlassSigma6 {
  public:
    GarmanKlassSigma6(Real yearFraction, Real marketOpenFraction);
    TimeSeries<Volatility> calculate(const TimeSeries<IntervalPrice>&);
};

#endif
