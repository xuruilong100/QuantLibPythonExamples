#ifndef ql_money_i
#define ql_money_i

%include ../ql/alltypes.i
%include currencies.i

%{
using QuantLib::Money;
%}

class Money {
  public:
    Money(const Currency& currency, Decimal value);
    Money(Decimal value, const Currency& currency);
    const Currency& currency() const;
    Decimal value() const;
    Money rounded() const;
    Money operator+() const;
    Money operator-() const;
    %extend {
        Money operator+(const Money& m) { return *self+m; }
        Money operator-(const Money& m) { return *self-m; }
        Money operator*(Decimal x) { return *self*x; }
        Money operator/(Decimal x) { return *self/x; }
        Decimal operator/(const Money& m) { return *self/m; }

        Money __rmul__(Decimal x) { return *self*x; }
        bool __lt__(const Money& other) {
            return *self < other;
        }
        bool __gt__(const Money& other) {
            return other < *self;
        }
        bool __le__(const Money& other) {
            return !(other < *self);
        }
        bool __ge__(const Money& other) {
            return !(*self < other);
        }
        int __cmp__(const Money& other) {
            if (*self < other)
                return -1;
            else if (*self == other)
                return 0;
            else
                return 1;
        }
        std::string __str__() {
            std::ostringstream out;
            out << *self;
            return out.str();
        }
    }
    enum ConversionType {
        NoConversion,
        BaseCurrencyConversion,
        AutomatedConversion };
    %extend {
        static void setConversionType(ConversionType type) {
            Money::conversionType = type;
        }
        static void setBaseCurrency(const Currency& c) {
            Money::baseCurrency = c;
        }
    }
};

#endif
