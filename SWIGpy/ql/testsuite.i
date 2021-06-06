#ifndef ql_testsuite_i
#define ql_testsuite_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i

%{
using QuantLib::Observable;
using QuantLib::Observer;

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

class Flag : public Observer {
  private:
    bool up_;
  public:
    Flag() : up_(false) {}
    void raise() { up_ = true; }
    void lower() { up_ = false; }
    bool isUp() const { return up_; }
    void update() { raise(); }
};

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

class Flag {
    %rename(raiseFlag) raise;
  public:
    Flag();
    void raise();
    void lower();
    bool isUp() const;
    void update();
    void registerWith(
        const ext::shared_ptr<Observable>&);
    void unregisterWith(
        const ext::shared_ptr<Observable>&);
};

#endif
