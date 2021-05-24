#ifndef ql_termstructures_InflationTermStructure_i
#define ql_termstructures_InflationTermStructure_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i

%{
using QuantLib::InflationTermStructure;
%}

%shared_ptr(InflationTermStructure);
class InflationTermStructure : public TermStructure {
  private:
    InflationTermStructure();
  public:
    virtual Period observationLag() const;
    virtual Frequency frequency() const;
    virtual bool indexIsInterpolated() const;
    virtual Rate baseRate() const;
    virtual Handle<YieldTermStructure> nominalTermStructure() const;
    virtual Date baseDate() const;
    void setSeasonality(
        const ext::shared_ptr<Seasonality>& seasonality = ext::shared_ptr<Seasonality>());
    ext::shared_ptr<Seasonality> seasonality() const;
    bool hasSeasonality() const;
};

%inline %{
    Date inflationBaseDate(
        const Date& referenceDate,
        const Period& observationLag,
        Frequency frequency,
        bool indexIsInterpolated) {
        if (indexIsInterpolated) {
            return referenceDate - observationLag;
        } else {
            return QuantLib::inflationPeriod(
                       referenceDate - observationLag,
                       frequency).first;
        }
    }
%}

#endif
