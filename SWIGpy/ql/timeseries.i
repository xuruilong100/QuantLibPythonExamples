#ifndef ql_timeseries_i
#define ql_timeseries_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i

%{
using QuantLib::TimeSeries;
using QuantLib::IntervalPrice;
%}

template <class T, class Container = std::map<Date, T> >
class TimeSeries {
    %rename(__len__) size;
  public:
    TimeSeries();
    %extend {
        TimeSeries(const std::vector<Date>& d, const std::vector<T>& v) {
            return new TimeSeries<T>(d.begin(), d.end(), v.begin());
        }
    }
    std::vector<Date> dates();
    std::vector<T> values();
    Size size();
    %extend {
        T __getitem__(const Date& d) {
            return (*self)[d];
        }
        void __setitem__(const Date& d, const T& value) {
            (*self)[d] = value;
        }
    }
};

%template(RealTimeSeries) TimeSeries<Real>;
%template(IntervalPriceTimeSeries) TimeSeries<IntervalPrice>;
%template(IntervalPriceVector) std::vector<IntervalPrice>;

class IntervalPrice {
  public:
    enum Type {
        Open,
        Close,
        High,
        Low
    };
    IntervalPrice(Real, Real, Real, Real);
    void setValue(Real, IntervalPrice::Type);
    void setValues(Real, Real, Real, Real);
    Real value(IntervalPrice::Type t);
    Real open();
    Real close();
    Real high();
    Real low();
    static TimeSeries<IntervalPrice> makeSeries(
        const std::vector<Date>& d,
        const std::vector<Real>& open,
        const std::vector<Real>& close,
        const std::vector<Real>& high,
        const std::vector<Real>& low);
    static std::vector<Real> extractValues(
        TimeSeries<IntervalPrice>,
        IntervalPrice::Type t);
    static TimeSeries<Real> extractComponent(
        TimeSeries<IntervalPrice>,
        IntervalPrice::Type t);
};

typedef RealTimeSeries VolatilityTimeSeries;

#endif
