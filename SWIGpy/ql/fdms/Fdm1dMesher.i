#ifndef ql_fdms_Fdm1dMesher_i
#define ql_fdms_Fdm1dMesher_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i

%{
using QuantLib::Fdm1dMesher;
%}

%shared_ptr(Fdm1dMesher)
class Fdm1dMesher {
  public:
    explicit Fdm1dMesher(Size size);

    Size size() const;
    Real dplus(Size index) const;
    Real dminus(Size index) const;
    Real location(Size index) const;
    const std::vector<Real>& locations();
};

%template(Fdm1dMesherVector) std::vector<ext::shared_ptr<Fdm1dMesher>>;

#endif
