#ifndef ql_callability_i
#define ql_callability_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i

%{
using QuantLib::Callability;
using QuantLib::SoftCallability;
using QuantLib::CallabilitySchedule;
%}

%shared_ptr(Callability)
class Callability : public Event {
  public:
    enum Type { Call, Put };
    Callability(const BondPrice& price,
                Type type,
                const Date& date);
    const BondPrice& price() const;
    Type type() const;
};

%shared_ptr(SoftCallability)
class SoftCallability : public Callability {
  public:
    SoftCallability(const BondPrice& price,
                    const Date& date,
                    Real trigger);
    Real trigger() const;
};

%template(CallabilitySchedule) std::vector<ext::shared_ptr<Callability>>;
typedef std::vector<ext::shared_ptr<Callability>> CallabilitySchedule;

#endif
