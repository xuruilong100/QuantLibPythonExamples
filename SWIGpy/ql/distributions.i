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
    BinomialDistribution(Real p, BigNatural n);
    Real operator()(BigNatural k);
};

class BivariateCumulativeNormalDistribution {
  public:
    BivariateCumulativeNormalDistribution(Real rho);
    Real operator()(Real x, Real y);
};

class BivariateCumulativeNormalDistributionDr78 {
  public:
    BivariateCumulativeNormalDistributionDr78(Real rho);
    Real operator()(Real a, Real b);
};

class BivariateCumulativeNormalDistributionWe04DP {
  public:
    BivariateCumulativeNormalDistributionWe04DP(Real rho);
    Real operator()(Real a, Real b);
};

class CumulativeBinomialDistribution {
  public:
    CumulativeBinomialDistribution(
        Real p, BigNatural n);
    Real operator()(BigNatural k);
};

class CumulativeChiSquareDistribution {
  public:
    CumulativeChiSquareDistribution(Real df);
    Real operator()(Real x);
};

class CumulativeGammaDistribution {
  public:
    CumulativeGammaDistribution(Real a);
    Real operator()(Real x);
};

class CumulativeNormalDistribution {
  public:
    CumulativeNormalDistribution(
        Real average = 0.0, Real sigma = 1.0);
    Real operator()(Real x);
    Real derivative(Real x);
};

class CumulativePoissonDistribution {
  public:
    CumulativePoissonDistribution(Real mu);
    Real operator()(BigNatural k);
};

class CumulativeStudentDistribution {
  public:
    CumulativeStudentDistribution(Integer n);
    Real operator()(Real x);
};

class GammaFunction {
  public:
    Real logValue(Real x);
};

class InverseCumulativePoisson {
  public:
    InverseCumulativePoisson(Real lambda);
    Real operator()(Real x);
};

class InverseCumulativeNormal {
  public:
    InverseCumulativeNormal(
        Real average = 0.0, Real sigma = 1.0);
    Real operator()(Real x);
};

class InverseCumulativeStudent {
  public:
    InverseCumulativeStudent(
        Integer n, Real accuracy = 1e-6,
        Size maxIterations = 50);
    Real operator()(Real x);
};

class InverseNonCentralCumulativeChiSquareDistribution {
  public:
    InverseNonCentralCumulativeChiSquareDistribution(
        Real df, Real ncp,
        Size maxEvaluations = 10,
        Real accuracy = 1e-8);
    Real operator()(Real x);
};

class MoroInverseCumulativeNormal {
  public:
    MoroInverseCumulativeNormal(
        Real average = 0.0, Real sigma = 1.0);
    Real operator()(Real x);
};

class NonCentralCumulativeChiSquareDistribution {
  public:
    NonCentralCumulativeChiSquareDistribution(
        Real df, Real ncp);
    Real operator()(Real x);
};

class NormalDistribution {
  public:
    NormalDistribution(
        Real average = 0.0, Real sigma = 1.0);
    Real operator()(Real x);
    Real derivative(Real x);
};

class PoissonDistribution {
  public:
    PoissonDistribution(Real mu);
    Real operator()(BigNatural k);
};

class StudentDistribution {
  public:
    StudentDistribution(Integer n);
    Real operator()(Real x);
};

#endif
