#ifndef ql_testsuite_i
#define ql_testsuite_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i

%{
ext::shared_ptr<YieldTermStructure>
flatRate(const Date& today,
         const ext::shared_ptr<Quote>& forward,
         const DayCounter& dc) {
    return ext::shared_ptr<YieldTermStructure>(
        new FlatForward(today, Handle<Quote>(forward), dc));
}

ext::shared_ptr<YieldTermStructure>
flatRate(const Date& today,
         Rate forward,
         const DayCounter& dc) {
    return flatRate(
        today, ext::shared_ptr<Quote>(new SimpleQuote(forward)), dc);
}

ext::shared_ptr<YieldTermStructure>
flatRate(const ext::shared_ptr<Quote>& forward,
         const DayCounter& dc) {
    return ext::shared_ptr<YieldTermStructure>(
        new FlatForward(0, NullCalendar(), Handle<Quote>(forward), dc));
}

ext::shared_ptr<YieldTermStructure>
flatRate(Rate forward,
         const DayCounter& dc) {
    return flatRate(ext::shared_ptr<Quote>(new SimpleQuote(forward)),
                    dc);
}

ext::shared_ptr<BlackVolTermStructure>
flatVol(const Date& today,
        const ext::shared_ptr<Quote>& vol,
        const DayCounter& dc) {
    return ext::shared_ptr<BlackVolTermStructure>(
        new BlackConstantVol(
            today, NullCalendar(), Handle<Quote>(vol), dc));
}

ext::shared_ptr<BlackVolTermStructure>
flatVol(const Date& today, Volatility vol,
        const DayCounter& dc) {
    return flatVol(
        today, ext::shared_ptr<Quote>(new SimpleQuote(vol)), dc);
}

ext::shared_ptr<BlackVolTermStructure>
flatVol(const ext::shared_ptr<Quote>& vol,
        const DayCounter& dc) {
    return ext::shared_ptr<BlackVolTermStructure>(
        new BlackConstantVol(
            0, NullCalendar(), Handle<Quote>(vol), dc));
}

ext::shared_ptr<BlackVolTermStructure>
flatVol(Volatility vol,
        const DayCounter& dc) {
    return flatVol(
        ext::shared_ptr<Quote>(new SimpleQuote(vol)), dc);
}

Real relativeError(Real x1, Real x2, Real reference) {
    if (reference != 0.0)
        return std::fabs(x1 - x2) / reference;
    else
        // fall back to absolute error
        return std::fabs(x1 - x2);
}
%}

ext::shared_ptr<YieldTermStructure>
flatRate(const Date& today,
         const ext::shared_ptr<Quote>& forward,
         const DayCounter& dc);

ext::shared_ptr<YieldTermStructure>
flatRate(const Date& today,
         Rate forward,
         const DayCounter& dc);

ext::shared_ptr<YieldTermStructure>
flatRate(const ext::shared_ptr<Quote>& forward,
         const DayCounter& dc);

ext::shared_ptr<YieldTermStructure>
flatRate(Rate forward,
         const DayCounter& dc);

ext::shared_ptr<BlackVolTermStructure>
flatVol(const Date& today,
        const ext::shared_ptr<Quote>& vol,
        const DayCounter& dc);

ext::shared_ptr<BlackVolTermStructure>
flatVol(const Date& today, Volatility vol,
        const DayCounter& dc);

ext::shared_ptr<BlackVolTermStructure>
flatVol(const ext::shared_ptr<Quote>& vol,
        const DayCounter& dc);

ext::shared_ptr<BlackVolTermStructure>
flatVol(Volatility vol,
        const DayCounter& dc);

Real relativeError(Real x1, Real x2, Real reference);

#endif
