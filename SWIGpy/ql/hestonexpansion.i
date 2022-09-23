#ifndef ql_heston_expansion_i
#define ql_heston_expansion_i

%include ../ql/types.i

%{
using QuantLib::HestonExpansion;
using QuantLib::LPP2HestonExpansion;
using QuantLib::LPP3HestonExpansion;
using QuantLib::FordeHestonExpansion;
%}

class HestonExpansion {
  private:
    HestonExpansion(){}
  public:
    Real impliedVolatility(
        Real strike, Real forward) const;
};

class LPP2HestonExpansion : public HestonExpansion {
  public:
    LPP2HestonExpansion(
        Real kappa, 
        Real theta, 
        Real sigma,
        Real v0, 
        Real rho, 
        Real term);
};

class LPP3HestonExpansion : public HestonExpansion{
  public:
    LPP3HestonExpansion(
        Real kappa, 
        Real theta, 
        Real sigma,
        Real v0, 
        Real rho, 
        Real term);
};

class FordeHestonExpansion : public HestonExpansion {
  public:
    FordeHestonExpansion(
        Real kappa, 
        Real theta, 
        Real sigma,
        Real v0, 
        Real rho, 
        Real term);
};

#endif
