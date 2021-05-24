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

%shared_ptr(Seasonality);
class Seasonality {
  private:
    Seasonality();

  public:
    virtual Rate correctZeroRate(
        const Date& d, const Rate r,
        const InflationTermStructure& iTS) const;
    virtual Rate correctYoYRate(
        const Date& d, const Rate r,
        const InflationTermStructure& iTS) const;
    virtual bool isConsistent(
        const InflationTermStructure& iTS);
};

%shared_ptr(MultiplicativePriceSeasonality)
class MultiplicativePriceSeasonality : public Seasonality {
  public:
    MultiplicativePriceSeasonality(
        const Date& seasonalityBaseDate,
        Frequency frequency,
        const std::vector<Rate>& seasonalityFactors);
};

%shared_ptr(KerkhofSeasonality)
class KerkhofSeasonality : public Seasonality {
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
    %extend {
        virtual void initialize(
            const ext::shared_ptr<YoYCapFloorTermPriceSurface>& surf,
            const ext::shared_ptr<PricingEngine>& pricer,
            Real slope) const {
            ext::shared_ptr<YoYInflationCapFloorEngine> engine = ext::dynamic_pointer_cast<YoYInflationCapFloorEngine>(pricer);
            return (self)->initialize(surf, engine, slope);
        }
    }
    virtual Rate maxStrike() const;
    virtual std::vector<Rate> strikes() const;
    virtual std::pair<std::vector<Rate>, std::vector<Volatility>> slice(const Date& d) const;
};

%shared_ptr(InterpolatedYoYOptionletStripper<Linear>)
template <class Interpolator1D>
class InterpolatedYoYOptionletStripper : public YoYOptionletStripper {
  public:
    InterpolatedYoYOptionletStripper();
};

%template(InterpolatedYoYInflationOptionletStripper) InterpolatedYoYOptionletStripper<Linear>;

#endif
