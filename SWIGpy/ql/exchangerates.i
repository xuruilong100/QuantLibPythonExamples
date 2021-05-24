#ifndef ql_exchange_rates_i
#define ql_exchange_rates_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i

%{
using QuantLib::ExchangeRate;
using QuantLib::ExchangeRateManager;
%}

class ExchangeRate {
  public:
    enum Type {
        Direct,
        Derived
    };
    ExchangeRate(
        const Currency& source,
        const Currency& target,
        Decimal rate);

    const Currency& source() const;
    const Currency& target() const;
    Type type() const;
    Decimal rate() const;

    Money exchange(const Money& amount) const;
    static ExchangeRate chain(
        const ExchangeRate& r1,
        const ExchangeRate& r2);
};

class ExchangeRateManager {
  private:
    ExchangeRateManager();

  public:
    static ExchangeRateManager& instance();
    void add(
        const ExchangeRate&,
        const Date& startDate = Date::minDate(),
        const Date& endDate = Date::maxDate());
    ExchangeRate lookup(
        const Currency& source,
        const Currency& target,
        const Date& date,
        ExchangeRate::Type type = ExchangeRate::Derived) const;
    void clear();
};

#endif
