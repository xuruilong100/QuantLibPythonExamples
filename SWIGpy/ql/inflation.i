#ifndef ql_inflation_i
#define ql_inflation_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i

%{
using QuantLib::Seasonality;
using QuantLib::MultiplicativePriceSeasonality;
using QuantLib::KerkhofSeasonality;
using QuantLib::YoYOptionletStripper;
using QuantLib::InterpolatedYoYOptionletStripper;
%}

%shared_ptr(Seasonality)
class Seasonality {
  private:
    Seasonality();
  public:
    Rate correctZeroRate(
        const Date& d, const Rate r,
        const InflationTermStructure& iTS) const;
    Rate correctYoYRate(
        const Date& d, const Rate r,
        const InflationTermStructure& iTS) const;
    bool isConsistent(
        const InflationTermStructure& iTS);
};

%shared_ptr(MultiplicativePriceSeasonality)
class MultiplicativePriceSeasonality : public Seasonality {
  public:
    MultiplicativePriceSeasonality(
        const Date& seasonalityBaseDate,
        Frequency frequency,
        const std::vector<Rate>& seasonalityFactors);
    void set(
        const Date& seasonalityBaseDate,
        Frequency frequency,
        std::vector<Rate> seasonalityFactors);
    Date seasonalityBaseDate() const;
    Frequency frequency() const;
    std::vector<Rate> seasonalityFactors() const;
    Rate seasonalityFactor(const Date& d) const;
};

%shared_ptr(KerkhofSeasonality)
class KerkhofSeasonality : public MultiplicativePriceSeasonality {
  public:
    KerkhofSeasonality(
        const Date& seasonalityBaseDate,
        const std::vector<Rate>& seasonalityFactors);
};

%shared_ptr(YoYOptionletStripper)
class YoYOptionletStripper {
  private:
    YoYOptionletStripper();

  public:
    void initialize(
        const ext::shared_ptr<YoYCapFloorTermPriceSurface>& ,
        const ext::shared_ptr<YoYInflationCapFloorEngine>& ,
        Real slope) const;
    Rate minStrike() const;
    Rate maxStrike() const;
    std::vector<Rate> strikes() const;
    std::pair<std::vector<Rate>, std::vector<Volatility>> slice(const Date& d) const;
};

%shared_ptr(InterpolatedYoYOptionletStripper<Linear>)
template <class Interpolator1D>
class InterpolatedYoYOptionletStripper : public YoYOptionletStripper {
  public:
    InterpolatedYoYOptionletStripper();
};

%template(InterpolatedYoYInflationOptionletStripper) InterpolatedYoYOptionletStripper<Linear>;

#endif
