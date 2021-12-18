#ifndef qlex_indexes_all
#define qlex_indexes_all

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i
%include ../ql/indexes/all.i

%{
using QuantLib::ChinaFixingRepo;
%}

%shared_ptr(ChinaFixingRepo)
class ChinaFixingRepo : public IborIndex {
  public:
    ChinaFixingRepo(
        const Period& tenor,
        Natural fixingDays,
        const Handle<YieldTermStructure>& h = Handle<YieldTermStructure>());
};

#endif
