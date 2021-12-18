#include <qlex/time/daycounters/Actual365_25.hpp>

namespace QuantLib {

ext::shared_ptr<DayCounter::Impl>
Actual365_25::implementation(Actual365_25::Convention c) {
    switch (c) {
    case Standard:
        return ext::shared_ptr<DayCounter::Impl>(new Impl);
    case Canadian:
        return ext::shared_ptr<DayCounter::Impl>(new CA_Impl);
    case NoLeap:
        return ext::shared_ptr<DayCounter::Impl>(new NL_Impl);
    default:
        QL_FAIL("unknown Actual/365.25 (Fixed) convention");
    }
}

Time Actual365_25::CA_Impl::yearFraction(const Date& d1,
                                         const Date& d2,
                                         const Date& refPeriodStart,
                                         const Date& refPeriodEnd) const {
    if (d1 == d2)
        return 0.0;

    // We need the period to calculate the frequency
    QL_REQUIRE(refPeriodStart != Date(), "invalid refPeriodStart");
    QL_REQUIRE(refPeriodEnd != Date(), "invalid refPeriodEnd");

    Time dcs = daysBetween(d1, d2);
    Time dcc = daysBetween(refPeriodStart, refPeriodEnd);
    Integer months = Integer(0.5 + 12 * dcc / 365);
    QL_REQUIRE(months != 0,
               "invalid reference period for Act/365 Canadian; "
               "must be longer than a month");
    Integer frequency = Integer(12 / months);

    if (dcs < 365 / frequency)
        return (dcs / 365.0) * 365.0 / 365.25;

    return (1. / frequency - (dcc - dcs) / 365.0) * 365.0 / 365.25;
}

Date::serial_type Actual365_25::NL_Impl::dayCount(const Date& d1,
                                                  const Date& d2) const {

    static const Integer MonthOffset[] = {
        0, 31, 59, 90, 120, 151,        // Jan - Jun
        181, 212, 243, 273, 304, 334    // Jun - Dec
    };

    Date::serial_type s1 = d1.dayOfMonth() + MonthOffset[d1.month() - 1] + (d1.year() * 365);
    Date::serial_type s2 = d2.dayOfMonth() + MonthOffset[d2.month() - 1] + (d2.year() * 365);

    if (d1.month() == Feb && d1.dayOfMonth() == 29) {
        --s1;
    }

    if (d2.month() == Feb && d2.dayOfMonth() == 29) {
        --s2;
    }

    return s2 - s1;
}

Time Actual365_25::NL_Impl::yearFraction(const Date& d1,
                                         const Date& d2,
                                         const Date& d3,
                                         const Date& d4) const {
    return dayCount(d1, d2) / 365.25;
}

}    // namespace QuantLib
