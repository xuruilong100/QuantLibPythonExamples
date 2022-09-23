#ifndef ql_termstructures_InflationTermStructure_i
#define ql_termstructures_InflationTermStructure_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i

%{
using QuantLib::InflationTermStructure;
using QuantLib::inflationPeriod;
%}

%shared_ptr(InflationTermStructure)
class InflationTermStructure : public TermStructure {
  private:
    InflationTermStructure();
  public:
    Period observationLag() const;
    Frequency frequency() const;
    Rate baseRate() const;
    Date baseDate() const;
    void setSeasonality(
        const ext::shared_ptr<Seasonality>& seasonality = ext::shared_ptr<Seasonality>());
    ext::shared_ptr<Seasonality> seasonality() const;
    bool hasSeasonality() const;
};

std::pair<Date, Date> inflationPeriod(const Date& d, Frequency frequency);

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
