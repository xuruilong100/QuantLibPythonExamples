#ifndef Actual365_25_HPP
#define Actual365_25_HPP

#include <ql/time/daycounter.hpp>

namespace QuantLib {

//! Actual/365.25 day count convention

class Actual365_25 : public DayCounter {
  public:
    enum Convention { Standard,
                      Canadian,
                      NoLeap };
    explicit Actual365_25(Convention c = Actual365_25::Standard)
        : DayCounter(implementation(c)) {}

  private:
    class Impl : public DayCounter::Impl {
      public:
        std::string name() const {
            return std::string("Actual/365.25 (Fixed)");
        }
        Time yearFraction(const Date& d1,
                          const Date& d2,
                          const Date&,
                          const Date&) const {
            return daysBetween(d1, d2) / 365.25;
        }
    };
    class CA_Impl : public DayCounter::Impl {
      public:
        std::string name() const {
            return std::string("Actual/365.25 (Fixed) Canadian Bond");
        }
        Time yearFraction(const Date& d1,
                          const Date& d2,
                          const Date& refPeriodStart,
                          const Date& refPeriodEnd) const;
    };
    class NL_Impl : public DayCounter::Impl {
      public:
        std::string name() const {
            return std::string("Actual/365.25 (No Leap)");
        }
        Date::serial_type dayCount(const Date& d1,
                                   const Date& d2) const;
        Time yearFraction(const Date& d1,
                          const Date& d2,
                          const Date& refPeriodStart,
                          const Date& refPeriodEnd) const;
    };
    static ext::shared_ptr<DayCounter::Impl> implementation(Convention);
};

}    // namespace QuantLib

#endif    // Actual365_25_HPP
