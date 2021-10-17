#ifndef ql_exercise_i
#define ql_exercise_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i

%{
using QuantLib::Exercise;
using QuantLib::EarlyExercise;
using QuantLib::AmericanExercise;
using QuantLib::BermudanExercise;
using QuantLib::EuropeanExercise;
using QuantLib::RebatedExercise;
using QuantLib::SwingExercise;
%}

%shared_ptr(Exercise)
class Exercise {
  public:
    enum Type {
        American, Bermudan, European
    };
    explicit Exercise(Type type);
    Type type() const;
    Date date(Size index);
    Date dateAt(Size index);
    const std::vector<Date>& dates();
    Date lastDate() const;
};

%shared_ptr(EuropeanExercise)
class EuropeanExercise : public Exercise {
  public:
    EuropeanExercise(const Date& date);
};

%shared_ptr(RebatedExercise)
class RebatedExercise : public Exercise {
  public:
    RebatedExercise(const Exercise& exercise,
                    Real rebate = 0.0,
                    Natural rebateSettlementDays = 0,
                    const Calendar& rebatePaymentCalendar = NullCalendar(),
                    BusinessDayConvention rebatePaymentConvention = Following);
    RebatedExercise(const Exercise& exercise,
                    const std::vector<Real>& rebates,
                    Natural rebateSettlementDays = 0,
                    const Calendar& rebatePaymentCalendar = NullCalendar(),
                    BusinessDayConvention rebatePaymentConvention = Following);
    Real rebate(Size index) const;
    Date rebatePaymentDate(Size index) const;
    const std::vector<Real>& rebates() const;
};

%shared_ptr(EarlyExercise)
class EarlyExercise : public Exercise {
  public:
    EarlyExercise(Exercise::Type type,
                  bool payoffAtExpiry = false);
    bool payoffAtExpiry() const;
};

%shared_ptr(AmericanExercise)
class AmericanExercise : public EarlyExercise {
  public:
    AmericanExercise(
        const Date& earliestDate,
        const Date& latestDate,
        bool payoffAtExpiry = false);
    AmericanExercise(
        const Date& latestDate,
        bool payoffAtExpiry = false);
};

%shared_ptr(BermudanExercise)
class BermudanExercise : public EarlyExercise {
  public:
    BermudanExercise(
        const std::vector<Date>& dates,
        bool payoffAtExpiry = false);
};

%shared_ptr(SwingExercise)
class SwingExercise : public BermudanExercise {
  public:
    explicit SwingExercise(
        const std::vector<Date>& dates,
        const std::vector<Size>& seconds = std::vector<Size>());
    SwingExercise(
        const Date& from,
        const Date& to,
        Size stepSizeSecs);

    const std::vector<Size>& seconds() const;
    std::vector<Time> exerciseTimes(
        const DayCounter& dc,
        const Date& refDate);
};

#endif
