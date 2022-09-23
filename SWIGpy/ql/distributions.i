#ifndef ql_distributions_i
#define ql_distributions_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i

%{
using QuantLib::BinomialDistribution;
using QuantLib::BivariateCumulativeNormalDistribution;
using QuantLib::BivariateCumulativeNormalDistributionDr78;
using QuantLib::BivariateCumulativeNormalDistributionWe04DP;
using QuantLib::CumulativeBinomialDistribution;
using QuantLib::CumulativeChiSquareDistribution;
using QuantLib::CumulativeGammaDistribution;
using QuantLib::CumulativeNormalDistribution;
using QuantLib::CumulativePoissonDistribution;
using QuantLib::CumulativeStudentDistribution;
using QuantLib::GammaFunction;
using QuantLib::InverseCumulativeNormal;
using QuantLib::InverseCumulativePoisson;
using QuantLib::InverseCumulativeStudent;
using QuantLib::InverseNonCentralCumulativeChiSquareDistribution;
using QuantLib::MoroInverseCumulativeNormal;
using QuantLib::NonCentralCumulativeChiSquareDistribution;
using QuantLib::NormalDistribution;
using QuantLib::PoissonDistribution;
using QuantLib::StudentDistribution;
%}

class BinomialDistribution {
  public:
    BinomialDistribution(
        Real p, 
        BigNatural n);
    Real operator()(BigNatural k) const;
};

class BivariateCumulativeNormalDistribution {
  public:
    BivariateCumulativeNormalDistribution(
        Real rho);
    Real operator()(Real x, Real y) const;
};

class BivariateCumulativeNormalDistributionDr78 {
  public:
    BivariateCumulativeNormalDistributionDr78(
        Real rho);
    Real operator()(Real a, Real b) const;
};

class BivariateCumulativeNormalDistributionWe04DP {
  public:
    BivariateCumulativeNormalDistributionWe04DP(
        Real rho);
    Real operator()(Real a, Real b) const;
};

class CumulativeBinomialDistribution {
  public:
    CumulativeBinomialDistribution(
        Real p, 
        BigNatural n);
    Real operator()(BigNatural k) const;
};

class CumulativeChiSquareDistribution {
  public:
    CumulativeChiSquareDistribution(
        Real df);
    Real operator()(Real x) const;
};

class CumulativeGammaDistribution {
  public:
    CumulativeGammaDistribution(
        Real a);
    Real operator()(Real x) const;
};

class CumulativeNormalDistribution {
  public:
    CumulativeNormalDistribution(
        Real average = 0.0, 
        Real sigma = 1.0);
    Real operator()(Real x) const;
    Real derivative(Real x) const;
};

class CumulativePoissonDistribution {
  public:
    CumulativePoissonDistribution(
        Real mu);
    Real operator()(BigNatural k) const;
};

class CumulativeStudentDistribution {
  public:
    CumulativeStudentDistribution(
        Integer n);
    Real operator()(Real x) const;
};

class GammaFunction {
  public:
    Real logValue(Real x) const;
    Real value(Real x) const;
};

class InverseCumulativePoisson {
  public:
    InverseCumulativePoisson(
        Real lambda = 1.0);
    Real operator()(Real x) const;
};

class InverseCumulativeNormal {
  public:
    InverseCumulativeNormal(
        Real average = 0.0, 
        Real sigma = 1.0);
    Real operator()(Real x) const;
    static Real standard_value(Real x);
};

class InverseCumulativeStudent {
  public:
    InverseCumulativeStudent(
        Integer n,
        Real accuracy = 1e-6,
        Size maxIterations = 50);
    Real operator()(Real x) const;
};

class InverseNonCentralCumulativeChiSquareDistribution {
  public:
    InverseNonCentralCumulativeChiSquareDistribution(
        Real df, 
        Real ncp,
        Size maxEvaluations = 10,
        Real accuracy = 1e-8);
    Real operator()(Real x) const;
};

class MoroInverseCumulativeNormal {
  public:
    MoroInverseCumulativeNormal(
        Real average = 0.0, 
        Real sigma = 1.0);
    Real operator()(Real x) const;
};

class NonCentralCumulativeChiSquareDistribution {
  public:
    NonCentralCumulativeChiSquareDistribution(
        Real df, 
        Real ncp);
    Real operator()(Real x) const;
};

class NormalDistribution {
  public:
    NormalDistribution(
        Real average = 0.0, 
        Real sigma = 1.0);
    Real operator()(Real x) const;
    Real derivative(Real x) const;
};

class PoissonDistribution {
  public:
    PoissonDistribution(
        Real mu);
    Real operator()(BigNatural k) const;
};

class StudentDistribution {
  public:
    StudentDistribution(
        Integer n);
    Real operator()(Real x) const;
};

#endif
