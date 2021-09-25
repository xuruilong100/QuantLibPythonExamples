#ifndef ql_scheduler_i
#define ql_scheduler_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/date.i

%define QL_TYPECHECK_DATEGENERATION       7210    %enddef

%{
using QuantLib::Schedule;
using QuantLib::MakeSchedule;
%}

%typemap(in) boost::optional<DateGeneration::Rule> %{
    if($input == Py_None)
        $1 = boost::none;
    else if (PyInt_Check($input))
        $1 = (DateGeneration::Rule) PyInt_AsLong($input);
    else
        $1 = (DateGeneration::Rule) PyLong_AsLong($input);
%}

%typecheck (QL_TYPECHECK_DATEGENERATION) boost::optional<DateGeneration::Rule> {
    if (PyInt_Check($input) || PyLong_Check($input) || Py_None == $input)
        $1 = 1;
    else
        $1 = 0;
}

class Schedule {
    %rename(__len__) size;
    //%ignore date;

  public:
    Schedule(
        const std::vector<Date>&,
        const Calendar& calendar = NullCalendar(),
        const BusinessDayConvention convention = Unadjusted,
        boost::optional<BusinessDayConvention>
            terminationDateConvention = boost::none,
        const boost::optional<Period> tenor = boost::none,
        boost::optional<DateGeneration::Rule> rule = boost::none,
        boost::optional<bool> endOfMonth = boost::none,
        std::vector<bool> isRegular = std::vector<bool>(0));
    Schedule(
        const Date& effectiveDate,
        const Date& terminationDate,
        const Period& tenor,
        const Calendar& calendar,
        BusinessDayConvention convention,
        BusinessDayConvention terminationDateConvention,
        DateGeneration::Rule rule,
        bool endOfMonth,
        const Date& firstDate = Date(),
        const Date& nextToLastDate = Date());
    Schedule();

    Size size() const;
    const Date& at(Size i) const;
    const Date& date(Size i) const;
    Date previousDate(const Date& refDate) const;
    Date nextDate(const Date& refDate) const;
    const std::vector<Date>& dates() const;
    bool hasIsRegular() const;
    bool isRegular(Size i) const;
    const std::vector<bool>& isRegular() const;

    bool empty() const;
    const Calendar& calendar() const;
    const Date& startDate() const;
    const Date& endDate() const;
    bool hasTenor() const;
    const Period& tenor() const;
    BusinessDayConvention businessDayConvention() const;
    bool hasTerminationDateBusinessDayConvention() const;
    BusinessDayConvention terminationDateBusinessDayConvention() const;
    bool hasRule() const;
    DateGeneration::Rule rule() const;
    bool hasEndOfMonth() const;
    bool endOfMonth() const;
    Schedule after(const Date& truncationDate) const;
    Schedule until(const Date& truncationDate) const;
    %extend {
        Date __getitem__(Integer i) {
            Integer size_ = static_cast<Integer>(self->size());
            if (i >= 0 && i < size_) {
                return self->date(i);
            } else if (i < 0 && -i <= size_) {
                return self->date(size_ + i);
            } else {
                throw std::out_of_range("schedule index out of range");
            }
        }
    }
};

%rename (_MakeSchedule) MakeSchedule;
class MakeSchedule {
    %rename("fromDate") from;
  public:
    MakeSchedule();

    MakeSchedule& from(const Date& effectiveDate);
    MakeSchedule& to(const Date& terminationDate);
    MakeSchedule& withTenor(const Period&);
    MakeSchedule& withFrequency(Frequency);
    MakeSchedule& withCalendar(const Calendar&);
    MakeSchedule& withConvention(BusinessDayConvention);
    MakeSchedule& withTerminationDateConvention(BusinessDayConvention);
    MakeSchedule& withRule(DateGeneration::Rule);
    MakeSchedule& forwards();
    MakeSchedule& backwards();
    MakeSchedule& endOfMonth(bool flag=true);
    MakeSchedule& withFirstDate(const Date& d);
    MakeSchedule& withNextToLastDate(const Date& d);

    %extend{
        Schedule makeSchedule(){
            return (Schedule)(* $self);
        }
    }
};

#endif
