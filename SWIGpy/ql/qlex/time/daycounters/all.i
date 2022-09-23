#ifndef qlex_time_daycounters_all
#define qlex_time_daycounters_all

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i
%include ../ql/daycounters.i

%{
using QuantLib::Actual365_25;
%}

class Actual365_25 : public DayCounter {
  public:
    enum Convention { Standard,
                      Canadian,
                      NoLeap };
    Actual365_25(
        Convention c = Actual365_25::Standard);
};

#endif
