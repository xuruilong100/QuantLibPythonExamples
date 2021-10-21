#ifndef ql_volatility_models_i
#define ql_volatility_models_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i

%{
using QuantLib::VolatilityCompositor;
using QuantLib::ConstantEstimator;
using QuantLib::Garch11;
using QuantLib::ParkinsonSigma;
using QuantLib::SimpleLocalEstimator;
using QuantLib::GarmanKlassSigma1;
using QuantLib::GarmanKlassSigma3;
using QuantLib::GarmanKlassSigma4;
using QuantLib::GarmanKlassSigma5;
using QuantLib::GarmanKlassSigma6;
%}

class VolatilityCompositor {
  private:
    VolatilityCompositor();
  public:
    typedef TimeSeries<Volatility> time_series;
    time_series calculate(const time_series& volatilitySeries);
    void calibrate(const time_series& volatilitySeries);
};

class ConstantEstimator : public VolatilityCompositor {
  public:
    ConstantEstimator(Size size);
};

class Garch11 : public VolatilityCompositor {
  public:
    enum Mode {
        MomentMatchingGuess,
        GammaGuess,
        BestOfTwo,
        DoubleOptimization
    };

    Garch11(Real a, Real b, Real vl);
    Garch11(const time_series& qs, Mode mode = BestOfTwo);

    Real alpha() const;
    Real beta() const;
    Real omega() const;
    Real ltVol() const;
    Real logLikelihood() const;
    Mode mode() const;

    void calibrate(const time_series& quoteSeries, OptimizationMethod& method, const EndCriteria& endCriteria);
    void calibrate(const time_series& quoteSeries, OptimizationMethod& method, const EndCriteria& endCriteria, const Array& initialGuess);
    Real forecast(Real r, Real sigma2) const;
    static time_series calculate(const time_series& quoteSeries, Real alpha, Real beta, Real omega);
    %extend {
        void calibrate(const std::vector<Real> x) {
            self->calibrate(x.begin(), x.end());
        }
        void calibrate(
            const std::vector<Real> x,
            OptimizationMethod& method, EndCriteria endCriteria) {
            self->calibrate(
                x.begin(), x.end(),
                method, endCriteria);
        }
        void calibrate(
            const std::vector<Real> x,
            OptimizationMethod& method,
            EndCriteria endCriteria,
            const Array& initialGuess) {
            self->calibrate(
                x.begin(), x.end(),
                method, endCriteria,
                initialGuess);
        }
        static Real to_r2 (
            const std::vector<Real> x,
            std::vector<Volatility>& r2) {
                return Garch11::to_r2(x.begin(), x.end(), r2);
        }
        static Real costFunction(
            const std::vector<Real> x, Real alpha, Real beta, Real omega) {
                return Garch11::costFunction(
                    x.begin(), x.end(),
                    alpha, beta, omega);
        }
    }
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
