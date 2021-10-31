#ifndef ql_date_i
#define ql_date_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i

%define QL_TYPECHECK_PERIOD                      5220    %enddef

%{
using QuantLib::Day;
using QuantLib::Year;
using QuantLib::Hour;
using QuantLib::Minute;
using QuantLib::Second;
using QuantLib::Millisecond;
using QuantLib::Microsecond;
%}

typedef Integer Day;
typedef Integer Year;
typedef Integer Hour;
typedef Integer Minute;
typedef Integer Second;
typedef Integer Millisecond;
typedef Integer Microsecond;

%{
using QuantLib::Period;
using QuantLib::PeriodParser;
%}

class Period {
  public:
    Period();
    Period(Integer n, TimeUnit units);
    explicit Period(Frequency);
    Integer length() const;
    TimeUnit units() const;
    Frequency frequency() const;
    %extend {
        Period(const std::string& str) {
            return new Period(PeriodParser::parse(str));
        }
        std::string __str__() {
            std::ostringstream out;
            out << *self;
            return out.str();
        }
        std::string __repr__() {
            std::ostringstream out;
            out << "Period(\"" << QuantLib::io::short_period(*self) << "\")";
            return out.str();
        }
        Period __neg__() {
            return -(*self);
        }
        Period __add__(const Period& p) {
            return *self + p;
        }
        Period __sub__(const Period& p) {
            return *self - p;
        }
        Period __mul__(Integer n) {
            return *self * n;
        }
        Period __rmul__(Integer n) {
            return *self * n;
        }
        bool __lt__(const Period& other) {
            return *self < other;
        }
        bool __gt__(const Period& other) {
            return other < *self;
        }
        bool __le__(const Period& other) {
            return !(other < *self);
        }
        bool __ge__(const Period& other) {
            return !(*self < other);
        }
        bool __eq__(const Period& other) {
            return *self == other;
        }
        int __cmp__(const Period& other) {
            return *self < other  ? -1 :
                   *self == other ?  0 :
                                     1;
        }
    }
    %pythoncode %{
    def __hash__(self):
        return hash(str(self))
    %}
};

%typemap(in) boost::optional<Period> %{
    if($input == Py_None)
        $1 = boost::none;
    else
    {
        Period *temp;
        if (!SWIG_IsOK(SWIG_ConvertPtr($input,(void **) &temp, $descriptor(Period*),0)))
            SWIG_exception_fail(SWIG_TypeError, "in method '$symname', expecting type Period");
        $1 = (boost::optional<Period>) *temp;
    }
%}

%typecheck (QL_TYPECHECK_PERIOD) boost::optional<Period> {
    if($input == Py_None)
        $1 = 1;
    else {
        Period *temp;
        int res = SWIG_ConvertPtr($input,(void **) &temp, $descriptor(Period*),0);
        $1 = SWIG_IsOK(res) ? 1 : 0;
    }
}

%template(PeriodVector) std::vector<Period>;

class PeriodParser {
  public:
    static Period parse(const std::string& str);
};

%{
using QuantLib::Date;
using QuantLib::DateParser;
%}

%pythoncode %{
import datetime as _datetime
%}

%{
// used in Date(string, string) defined below
void _replace_format(
    std::string& s,
    const std::string& old_format,
    const std::string& new_format) {
    std::string::size_type i = s.find(old_format);
    if (i != std::string::npos)
        s.replace(i, old_format.length(), new_format);
}
%}

class Date {
  public:
    Date();
    Date(Day d, Month m, Year y);
    Date(BigInteger serialNumber);
    %#ifdef QL_HIGH_RESOLUTION_DATE
    %extend {
        Date(Day d, Month m, Year y,
             Hour hours, Minute minutes, Second seconds,
             Millisecond millisec = 0,
             Microsecond microsec = 0) {
            return new Date(
                d, m, y, hours, minutes, seconds,
                millisec, microsec);
        }
    }
    %#endif

    Weekday weekday() const;
    Day dayOfMonth() const;
    Day dayOfYear() const;
    Month month() const;
    Year year() const;
    BigInteger serialNumber() const;

    %#ifdef QL_HIGH_RESOLUTION_DATE
    Hour hours() const;
    Minute minutes() const;
    Second seconds() const;
    Millisecond milliseconds() const;
    Microsecond microseconds() const;
    Time fractionOfDay() const;
    Time fractionOfSecond() const;
    %#endif

    static bool isLeap(Year y);
    static Date minDate();
    static Date maxDate();
    static Date todaysDate();
    static Date endOfMonth(const Date&);
    static bool isEndOfMonth(const Date&);
    static Date nextWeekday(const Date&, Weekday);
    static Date nthWeekday(Size n, Weekday, Month m, Year y);

    %#ifdef QL_HIGH_RESOLUTION_DATE
    static Date localDateTime();
    static Date universalDateTime();
    %#endif

    Date operator+(BigInteger days) const;
    Date operator-(BigInteger days) const;
    Date operator+(const Period&) const;
    Date operator-(const Period&) const;
    %extend {
        Date(const std::string& str, std::string fmt) {
            // convert our old format into the corresponding Boost one
            _replace_format(fmt, "YYYY", "%Y");
            _replace_format(fmt, "yyyy", "%Y");
            _replace_format(fmt, "YY", "%y");
            _replace_format(fmt, "yy", "%y");
            _replace_format(fmt, "MM", "%m");
            _replace_format(fmt, "mm", "%m");
            _replace_format(fmt, "DD", "%d");
            _replace_format(fmt, "dd", "%d");
            return new Date(
                DateParser::parseFormatted(str,fmt));
        }
        Day day() const {
            return self->dayOfMonth();
        }
        Integer weekdayNumber() {
            return int(self->weekday());
        }
        std::string __str__() {
            std::ostringstream out;
            out << *self;
            return out.str();
        }
        std::string __repr__() {
            std::ostringstream out;
            out << *self;
            return out.str();
        }
        std::string ISO() {
            std::ostringstream out;
            out << QuantLib::io::iso_date(*self);
            return out.str();
        }
        BigInteger operator-(const Date& other) {
            return *self - other;
        }
        bool __eq__(const Date& other) {
            return *self == other;
        }
        int __cmp__(const Date& other) {
            if (*self < other)
                return -1;
            else if (*self == other)
                return 0;
            else
                return 1;
        }
        bool __nonzero__() {
            return (*self != Date());
        }
        bool __bool__() {
            return (*self != Date());
        }
        int __hash__() {
            return self->serialNumber();
        }
        bool __lt__(const Date& other) {
            return *self < other;
        }
        bool __gt__(const Date& other) {
            return other < *self;
        }
        bool __le__(const Date& other) {
            return !(other < *self);
        }
        bool __ge__(const Date& other) {
            return !(*self < other);
        }
        bool __ne__(const Date& other) {
            return *self != other;
        }
    }
    %pythoncode %{
    def to_date(self):
        return _datetime.date(
            self.year(), self.month(), self.dayOfMonth())

    @staticmethod
    def from_date(date):
        return Date(date.day, date.month, date.year)
    %}
};

class DateParser {
  public:
    static Date parseFormatted(
        const std::string& str, const std::string& fmt);
    static Date parseISO(const std::string& str);
    %extend {
        static Date parse(
            const std::string& str, std::string fmt) {
            // convert our old format into the corresponding Boost one
            _replace_format(fmt, "YYYY", "%Y");
            _replace_format(fmt, "yyyy", "%Y");
            _replace_format(fmt, "YY", "%y");
            _replace_format(fmt, "yy", "%y");
            _replace_format(fmt, "MM", "%m");
            _replace_format(fmt, "mm", "%m");
            _replace_format(fmt, "DD", "%d");
            _replace_format(fmt, "dd", "%d");
            return DateParser::parseFormatted(str,fmt);
        }
    }
};

%pythoncode %{
Date._old___add__ = Date.__add__
Date._old___sub__ = Date.__sub__
def Date_new___add__(self,x):
    if type(x) is tuple and len(x) == 2:
        return self._old___add__(Period(x[0],x[1]))
    else:
        return self._old___add__(x)
def Date_new___sub__(self,x):
    if type(x) is tuple and len(x) == 2:
        return self._old___sub__(Period(x[0],x[1]))
    else:
        return self._old___sub__(x)
Date.__add__ = Date_new___add__
Date.__sub__ = Date_new___sub__
%}

%template(DateVector) std::vector<Date>;

Time daysBetween(const Date&, const Date&);

#endif
