#ifndef ql_instruments_Option_i
#define ql_instruments_Option_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i

%{
using QuantLib::Option;
%}

%shared_ptr(Option)
class Option : public Instrument {
  public:
    enum Type {
        Put = -1,
        Call = 1
    };
    ext::shared_ptr<Payoff> payoff();
    ext::shared_ptr<Exercise> exercise();
  private:
    Option();
};

#endif
