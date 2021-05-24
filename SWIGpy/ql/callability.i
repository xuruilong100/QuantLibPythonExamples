#ifndef ql_callability_i
#define ql_callability_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i

%{
using QuantLib::Callability;
using QuantLib::SoftCallability;
using QuantLib::CallabilitySchedule;
typedef Callability::Price CallabilityPrice;
%}

class CallabilityPrice {
  public:
    enum Type { Dirty, Clean };
    CallabilityPrice(Real amount, Type type);
    Real amount() const;
    Type type() const;
};

%shared_ptr(Callability)
class Callability {
  public:
    enum Type { Call, Put };
    Callability(const CallabilityPrice& price,
                Type type,
                const Date& date);
    const CallabilityPrice& price() const;
    Type type() const;
    Date date() const;
};

%shared_ptr(SoftCallability)
class SoftCallability : public Callability {
  public:
    SoftCallability(const CallabilityPrice& price,
                    const Date& date,
                    Real trigger);
};

%template(CallabilitySchedule) std::vector<ext::shared_ptr<Callability> >;

#endif
