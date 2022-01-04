#ifndef ql_money_i
#define ql_money_i

%include ../ql/alltypes.i
%include currencies.i

%{
using QuantLib::Money;
typedef QuantLib::Money::Settings MoneySettings;
%}

class Money {
  public:
    Money();
    Money(Currency currency, Decimal value);
    Money(Decimal value, Currency currency);
    const Currency& currency() const;
    Decimal value() const;
    Money rounded() const;
    Money operator+() const;
    Money operator-() const;
    %extend {
        Money __add__(const Money& m) const { return *self+m; }
        Money __sub__(const Money& m) { return *self-m; }
        Money __mul__(Decimal x) { return *self*x; }
        Money __rmul__(Decimal x) { return *self*x; }
        Money __truediv__(Decimal x) { return *self/x; }
        Decimal __truediv__(const Money& m) { return *self/m; }

        bool __eq__(const Money& other) { return *self == other; }
        bool __ne__(const Money& other) { return *self != other; }
        bool __lt__(const Money& other) { return *self < other; }
        bool __gt__(const Money& other) { return other < *self; }
        bool __le__(const Money& other) { return !(other < *self); }
        bool __ge__(const Money& other) { return !(*self < other); }
        int __cmp__(const Money& other) {
            if (*self < other)
                return -1;
            else if (*self == other)
                return 0;
            else
                return 1;
        }
        std::string __str__() const {
            std::ostringstream out;
            out << *self;
            return out.str();
        }
        std::string __repr__() const {
            std::ostringstream out;
            out << *self;
            return out.str();
        }
    }
    enum ConversionType {
        NoConversion,
        BaseCurrencyConversion,
        AutomatedConversion };
};

bool close(const Money& m1, const Money& m2, Size n = 42);
bool close_enough(const Money& m1, const Money& m2, Size n = 42);

//typedef QuantLib::Money::Settings MoneySettings;

class MoneySettings {
  private:
    MoneySettings();
  public:
    static MoneySettings& instance();

    %extend {
        Money::ConversionType getConversionType() const {
            return self->conversionType();
        }
        void setConversionType(Money::ConversionType conversionType) {
            self->conversionType() = conversionType;
        }
        Currency getBaseCurrency() const {
            return self->baseCurrency();
        }
        void setBaseCurrency(const Currency& currency) {
            self->baseCurrency() = currency;
        }
    }

    %pythoncode %{
        conversionType = property(
            getConversionType, setConversionType, None)
        baseCurrency = property(
            getBaseCurrency, setBaseCurrency, None)
    %}
};

#endif
