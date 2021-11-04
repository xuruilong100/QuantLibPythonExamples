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
    ZeroCouponInflationSwapHelper(
        const Handle<Quote>& quote,
        const Period& lag,
        const Date& maturity,
        Calendar calendar,
        BusinessDayConvention bcd,
        DayCounter dayCounter,
        ext::shared_ptr<ZeroInflationIndex> zii,
        CPI::InterpolationType observationInterpolation,
        Handle<YieldTermStructure> nominalTermStructure);
};

%shared_ptr(YearOnYearInflationSwapHelper)
class YearOnYearInflationSwapHelper : public BootstrapHelper<YoYInflationTermStructure> {
  public:
    YearOnYearInflationSwapHelper(
        const Handle<Quote>& quote,
        const Period& lag,
        const Date& maturity,
        Calendar calendar,
        BusinessDayConvention bdc,
        DayCounter dayCounter,
        ext::shared_ptr<YoYInflationIndex> yii,
        Handle<YieldTermStructure> nominalTermStructure);
};

%shared_ptr(YoYOptionletHelper)
class YoYOptionletHelper : public BootstrapHelper<YoYOptionletVolatilitySurface> {
  public:
    YoYOptionletHelper(
        const Handle<Quote>& price,
        Real notional,
        YoYInflationCapFloor::Type capFloorType,
        Period& lag,
        DayCounter yoyDayCounter,
        Calendar paymentCalendar,
        Natural fixingDays,
        ext::shared_ptr<YoYInflationIndex> index,
        Rate strike,
        Size n,
        ext::shared_ptr<YoYInflationCapFloorEngine> pricer);
};

#endif
