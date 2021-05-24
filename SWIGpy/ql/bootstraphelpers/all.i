#ifndef ql_bootstraphelpers_all_i
#define ql_bootstraphelpers_all_i

%include ../ql/alltypes.i
%include ../ql/base.i
%include ../ql/common.i
%include ../ql/types.i

%{
using QuantLib::ZeroCouponInflationSwapHelper;
using QuantLib::YearOnYearInflationSwapHelper;
using QuantLib::YoYOptionletHelper;
%}

%shared_ptr(ZeroCouponInflationSwapHelper)
class ZeroCouponInflationSwapHelper : public BootstrapHelper<ZeroInflationTermStructure> {
  public:
    // using extend to prevent deprecation warning
    %extend {
        ZeroCouponInflationSwapHelper(
            const Handle<Quote>& quote,
            const Period& lag,    // lag on swap observation of index
            const Date& maturity,
            const Calendar& calendar,
            BusinessDayConvention bcd,
            const DayCounter& dayCounter,
            const ext::shared_ptr<ZeroInflationIndex>& index,
            const Handle<YieldTermStructure>& nominalTS = Handle<YieldTermStructure>()) {

            return new ZeroCouponInflationSwapHelper(
                quote, lag, maturity,
                calendar, bcd,
                dayCounter, index,
                nominalTS);
        }
    }
};

%shared_ptr(YearOnYearInflationSwapHelper)
class YearOnYearInflationSwapHelper : public BootstrapHelper<YoYInflationTermStructure> {
  public:
    // using extend to prevent deprecation warning
    %extend {
        YearOnYearInflationSwapHelper(
            const Handle<Quote>& quote,
            const Period& lag,
            const Date& maturity,
            const Calendar& calendar,
            BusinessDayConvention bdc,
            const DayCounter& dayCounter,
            const ext::shared_ptr<YoYInflationIndex>& index,
            const Handle<YieldTermStructure>& nominalTS = Handle<YieldTermStructure>()) {
            return new YearOnYearInflationSwapHelper(
                quote, lag, maturity,
                calendar, bdc,
                dayCounter, index,
                nominalTS);
        }
    }
};

%shared_ptr(YoYOptionletHelper)
class YoYOptionletHelper : public BootstrapHelper<YoYOptionletVolatilitySurface> {
  public:
    %extend {
        YoYOptionletHelper(
            const Handle<Quote>& price,
            Real notional,
            YoYInflationCapFloor::Type capFloorType,
            Period& lag,
            const DayCounter& yoyDayCounter,
            const Calendar& paymentCalendar,
            Natural fixingDays,
            const ext::shared_ptr<YoYInflationIndex>& index,
            Rate strike,
            Size n,
            const ext::shared_ptr<PricingEngine>& pricer) {
            ext::shared_ptr<YoYInflationCapFloorEngine> engine = ext::dynamic_pointer_cast<YoYInflationCapFloorEngine>(pricer);
            return new YoYOptionletHelper(
                price, notional, capFloorType, lag,
                yoyDayCounter, paymentCalendar, fixingDays,
                index, strike, n, engine);
        }
    }
};

#endif
