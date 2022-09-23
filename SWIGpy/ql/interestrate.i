#ifndef ql_interest_rate_i
#define ql_interest_rate_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i

%{
using QuantLib::InterestRate;
%}

class InterestRate {
  public:
    InterestRate();
    InterestRate(
        Rate r,
        const DayCounter& dc,
        Compounding comp,
        Frequency freq);
    Rate rate() const;
    DayCounter dayCounter() const;
    Compounding compounding() const;
    Frequency frequency() const;
    DiscountFactor discountFactor(Time t) const;
    DiscountFactor discountFactor(const Date& d1, const Date& d2,
                                  const Date& refStart = Date(),
                                  const Date& refEnd = Date()) const;
    Real compoundFactor(Time t) const;
    Real compoundFactor(const Date& d1, const Date& d2,
                        const Date& refStart = Date(),
                        const Date& refEnd = Date()) const;
    static InterestRate impliedRate(Real compound,
                                    const DayCounter& resultDC,
                                    Compounding comp,
                                    Frequency freq,
                                    Time t);
    static InterestRate impliedRate(Real compound,
                                    const DayCounter& resultDC,
                                    Compounding comp,
                                    Frequency freq,
                                    const Date& d1,
                                    const Date& d2,
                                    const Date& refStart = Date(),
                                    const Date& refEnd = Date());
    InterestRate equivalentRate(Compounding comp,
                                Frequency freq,
                                Time t) const;
    InterestRate equivalentRate(const DayCounter& resultDayCounter,
                                Compounding comp,
                                Frequency freq,
                                const Date& d1,
                                const Date& d2,
                                const Date& refStart = Date(),
                                const Date& refEnd = Date()) const;
    %extend {
        std::string __str__() {
            std::ostringstream out;
            out << *self;
            return out.str();
        }
    }
};

%template(InterestRateVector) std::vector<InterestRate>;

#endif
