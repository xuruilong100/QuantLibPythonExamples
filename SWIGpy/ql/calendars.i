#ifndef ql_calendar_i
#define ql_calendar_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include stl.i

%{
using QuantLib::Calendar;
%}

class Calendar {
  protected:
    Calendar();
  public:
    bool isWeekend(Weekday w);
    Date endOfMonth(const Date&);
    bool isBusinessDay(const Date&);
    bool isHoliday(const Date&);
    bool isEndOfMonth(const Date&);
    void addHoliday(const Date&);
    void removeHoliday(const Date&);
    Date adjust(const Date& d,
                BusinessDayConvention convention = QuantLib::Following);
    Date advance(const Date& d, Integer n, TimeUnit unit,
                 BusinessDayConvention convention = QuantLib::Following,
                 bool endOfMonth = false);
    Date advance(const Date& d, const Period& period,
                 BusinessDayConvention convention = QuantLib::Following,
                 bool endOfMonth = false);
    BigInteger businessDaysBetween(const Date& from,
                                   const Date& to,
                                   bool includeFirst = true,
                                   bool includeLast = false);
    std::vector<Date> holidayList(const Date& from,
                                  const Date& to,
                                  bool includeWeekEnds = false);
    std::vector<Date> businessDayList(const Date& from,
                                      const Date& to);
    std::string name();
    %extend {
        std::string __str__() {
            return self->name()+" calendar";
        }
        bool __eq__(const Calendar& other) {
            return (*self) == other;
        }
        bool __ne__(const Calendar& other) {
            return (*self) != other;
        }
    }

    %pythoncode %{
    def __hash__(self):
        return hash(self.name())
    %}
};

namespace QuantLib {

class Argentina : public Calendar {
  public:
    enum Market { Merval };
    Argentina(Market m = Merval);
};

class Australia : public Calendar {};

class Brazil : public Calendar {
  public:
    enum Market { Settlement,
                  Exchange };
    Brazil(Market m = Settlement);
};

class Canada : public Calendar {
  public:
    enum Market { Settlement,
                  TSX };
    Canada(Market m = Settlement);
};

class China : public Calendar {
  public:
    enum Market { SSE,
                  IB };
    China(Market m = SSE);
};

class CzechRepublic : public Calendar {
  public:
    enum Market { PSE };
    CzechRepublic(Market m = PSE);
};

class Denmark : public Calendar {};
class Finland : public Calendar {};

class France : public Calendar {
  public:
    enum Market { Settlement,
                  Exchange };
    France(Market m = Settlement);
};

class Germany : public Calendar {
  public:
    enum Market { Settlement,
                  FrankfurtStockExchange,
                  Xetra,
                  Eurex };
    Germany(Market m = FrankfurtStockExchange);
};

class HongKong : public Calendar {
  public:
    enum Market { HKEx };
    HongKong(Market m = HKEx);
};

class Hungary : public Calendar {};

class Iceland : public Calendar {
  public:
    enum Market { ICEX };
    Iceland(Market m = ICEX);
};

class India : public Calendar {
  public:
    enum Market { NSE };
    India(Market m = NSE);
};

class Indonesia : public Calendar {
  public:
    enum Market { BEJ,
                  JSX };
    Indonesia(Market m = BEJ);
};

class Israel : public Calendar {
  public:
    enum Market { Settlement,
                  TASE };
    Israel(Market m = Settlement);
};

class Italy : public Calendar {
  public:
    enum Market { Settlement,
                  Exchange };
    Italy(Market m = Settlement);
};

class Japan : public Calendar {};

class Mexico : public Calendar {
  public:
    enum Market { BMV };
    Mexico(Market m = BMV);
};

class NewZealand : public Calendar {};
class Norway : public Calendar {};
class Poland : public Calendar {};

class Russia : public Calendar {
  public:
    enum Market { Settlement,
                  MOEX };
    Russia(Market m = Settlement);
};

class Romania : public Calendar {};

class SaudiArabia : public Calendar {
  public:
    enum Market { Tadawul };
    SaudiArabia(Market m = Tadawul);
};

class Singapore : public Calendar {
  public:
    enum Market { SGX };
    Singapore(Market m = SGX);
};

class Slovakia : public Calendar {
  public:
    enum Market { BSSE };
    Slovakia(Market m = BSSE);
};

class SouthAfrica : public Calendar {};

class SouthKorea : public Calendar {
  public:
    enum Market { Settlement,
                  KRX };
    SouthKorea(Market m = KRX);
};

class Sweden : public Calendar {};
class Switzerland : public Calendar {};

class Taiwan : public Calendar {
  public:
    enum Market { TSEC };
    Taiwan(Market m = TSEC);
};

class TARGET : public Calendar {};
class Thailand : public Calendar {};
class Turkey : public Calendar {};

class Ukraine : public Calendar {
  public:
    enum Market { USE };
    Ukraine(Market m = USE);
};

class UnitedKingdom : public Calendar {
  public:
    enum Market { Settlement,
                  Exchange,
                  Metals };
    UnitedKingdom(Market m = Settlement);
};

class UnitedStates : public Calendar {
  public:
    enum Market { Settlement,
                  NYSE,
                  GovernmentBond,
                  NERC,
                  LiborImpact,
                  FederalReserve };
    UnitedStates(Market m = Settlement);
};

class NullCalendar : public Calendar {};

class WeekendsOnly : public Calendar {};

class JointCalendar : public Calendar {
  public:
    JointCalendar(const Calendar&, const Calendar&,
                  JointCalendarRule rule = QuantLib::JoinHolidays);
    JointCalendar(const Calendar&, const Calendar&, const Calendar&,
                  JointCalendarRule rule = QuantLib::JoinHolidays);
    JointCalendar(const Calendar&, const Calendar&,
                  const Calendar&, const Calendar&,
                  JointCalendarRule rule = QuantLib::JoinHolidays);
};

class BespokeCalendar : public Calendar {
  public:
    BespokeCalendar(const std::string& name);
    void addWeekend(Weekday);
};
}    // namespace QuantLib


#endif
