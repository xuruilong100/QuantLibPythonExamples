#ifndef ql_day_counters_i
#define ql_day_counters_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i

%{
using QuantLib::DayCounter;
%}

class DayCounter {
  public:
    DayCounter();
    BigInteger dayCount(const Date& d1, const Date& d2) const;
    Time yearFraction(const Date& d1, const Date& d2,
                      const Date& startRef = Date(),
                      const Date& endRef = Date()) const;
    std::string name() const;
    bool empty() const;
    %extend {
        std::string __str__() {
            return self->name()+" day counter";
        }
        bool __eq__(const DayCounter& other) {
            return (*self) == other;
        }
        bool __ne__(const DayCounter& other) {
            return (*self) != other;
        }
    }
    %pythoncode %{
    def __hash__(self):
        return hash(self.name())
    %}
};

namespace QuantLib {

class Actual360 : public DayCounter {
  public:
    Actual360(
        const bool includeLastDay = false);
};

class Actual364 : public DayCounter {};

class Actual365Fixed : public DayCounter {
  public:
    enum Convention {
        Standard,
        Canadian,
        NoLeap
    };
    Actual365Fixed(
        Convention c = Standard);
};

class ActualActual : public DayCounter {
  public:
    enum Convention {
        ISMA,
        Bond,
        ISDA,
        Historical,
        Actual365,
        AFB,
        Euro
    };
    ActualActual(
        Convention c,
        const Schedule& schedule = Schedule());
};

class Business252 : public DayCounter {
  public:
    Business252(
        Calendar c = Brazil());
};

class OneDayCounter : public DayCounter {};

class SimpleDayCounter : public DayCounter {};

class Thirty360 : public DayCounter {
  public:
    enum Convention {
        USA,
        BondBasis,
        European,
        EurobondBasis,
        Italian,
        German,
        ISMA,
        ISDA,
        NASD
    };
    Thirty360(
        Convention c,
        const Date& terminationDate = Date());
};

class Thirty365 : public DayCounter {};

}

#endif
