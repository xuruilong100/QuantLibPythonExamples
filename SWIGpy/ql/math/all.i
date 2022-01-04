#ifndef ql_math_all_i
#define ql_math_all_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i

%{
using QuantLib::convolutions;
using QuantLib::autocovariances;
using QuantLib::autocorrelations;
%}
%{
using QuantLib::getCovariance;
using QuantLib::pseudoSqrt;
using QuantLib::rankReducedSqrt;
using QuantLib::CovarianceDecomposition;
%}
%{
using QuantLib::CreditRiskPlus;
%}
%{
using QuantLib::MaddockInverseCumulativeNormal;
using QuantLib::BivariateCumulativeStudentDistribution;
using QuantLib::StochasticCollocationInvCDF;
using QuantLib::NonCentralCumulativeChiSquareSankaranApprox;
%}
%{
using QuantLib::FastFourierTransform;
%}
%{
using QuantLib::Factorial;
using QuantLib::modifiedBesselFunction_i;
using QuantLib::modifiedBesselFunction_k;
using QuantLib::modifiedBesselFunction_i_exponentiallyWeighted;
using QuantLib::modifiedBesselFunction_k_exponentiallyWeighted;
%}

%{
using QuantLib::TwoDimensionalIntegral;
using QuantLib::ExponentialIntegral::Si;
using QuantLib::ExponentialIntegral::Ci;
using QuantLib::ExponentialIntegral::E1;
using QuantLib::ExponentialIntegral::Ei;
using QuantLib::AbcdMathFunction;
using QuantLib::AbcdFunction;
using QuantLib::AbcdSquared;
using QuantLib::abcdBlackVolatility;
%}

%{
using QuantLib::FaureRsg;
using QuantLib::LatticeRsg;
using QuantLib::RandomizedLDS;
using QuantLib::LatticeRule;
%}

%{
using QuantLib::SymmetricSchurDecomposition;
using QuantLib::qrDecomposition;
using QuantLib::qrSolve;
using QuantLib::determinant;
using QuantLib::OrthogonalProjections;
using QuantLib::CholeskyDecomposition;
using QuantLib::moorePenroseInverse;
%}

%{
using QuantLib::NumericalDifferentiation;
%}

%{
using QuantLib::TqrEigenDecomposition;
%}

%{
using QuantLib::BSpline;
%}

%{
using QuantLib::CenteredGrid;
using QuantLib::BoundedGrid;
using QuantLib::BoundedLogGrid;
%}

%{
using QuantLib::TransformedGrid;
using QuantLib::LogGrid;
%}

%{
Array convolutions(const Array& forward, Size maxLag) {
    Array out(forward.size() - maxLag + 1);
    convolutions(
        forward.begin(), forward.end(), out.begin(), maxLag);
    return out;
}

Array autocovariances(const Array& forward, Size maxLag) {
    Array out(forward.size() - maxLag + 1);
    autocovariances(
        forward.begin(), forward.end(), out.begin(), maxLag);
    return out;
}

std::pair<Real, Array> autocovariances(Array& forward, Size maxLag, bool reuse) {
    Array out(forward.size() - maxLag + 1);
    Real mean = autocovariances(
        forward.begin(), forward.end(), out.begin(), maxLag, reuse);
    return std::make_pair(mean, out);
}

Array autocorrelations(const Array& forward, Size maxLag) {
    Array out(forward.size() - maxLag + 1);
    autocorrelations(
        forward.begin(), forward.end(), out.begin(), maxLag);
    return out;
}

std::pair<Real, Array> autocorrelations(Array& forward, Size maxLag, bool reuse) {
    Array out(forward.size() - maxLag + 1);
    Real mean = autocorrelations(
        forward.begin(), forward.end(), out.begin(), maxLag, reuse);
    return std::make_pair(mean, out);
}
%}

Array convolutions(const Array& forward, Size maxLag);
Array autocovariances(const Array& forward, Size maxLag);
std::pair<Real, Array> autocovariances(Array& forward, Size maxLag, bool reuse);
Array autocorrelations(const Array& forward, Size maxLag);
std::pair<Real, Array> autocorrelations(Array& forward, Size maxLag, bool reuse);

%template(DoubleArray) std::pair<Real, Array>;

//---------

%inline %{
Matrix getCovariance(
    const Array& volatilities,
    const Matrix& correlations,
    Real tolerance = 1.0e-12) {
    return QuantLib::getCovariance(
        volatilities.begin(),
        volatilities.end(),
        correlations,
        tolerance);
}
%}

Matrix pseudoSqrt(
    const Matrix&,
    SalvagingAlgorithm::Type = SalvagingAlgorithm::None);

Matrix rankReducedSqrt(
    const Matrix&,
    Size maxRank,
    Real componentRetainedPercentage,
    SalvagingAlgorithm::Type);

class CovarianceDecomposition {
  public:
    CovarianceDecomposition(
        const Matrix& covarianceMatrix,
        Real tolerance = 1.0e-12);
    const Array& variances() const;
    const Array& standardDeviations() const;
    const Matrix& correlationMatrix() const;
};

//------

class CreditRiskPlus {
  public:
    CreditRiskPlus(
        std::vector<Real> exposure,
        std::vector<Real> defaultProbability,
        std::vector<Size> sector,
        std::vector<Real> relativeDefaultVariance,
        Matrix correlation,
        Real unit);

    const std::vector<Real>& loss();
    const std::vector<Real>& marginalLoss();

    Real exposure() const;
    Real expectedLoss() const;
    Real unexpectedLoss() const;
    Real relativeDefaultVariance() const;
    const std::vector<Real>& sectorExposures() const;
    const std::vector<Real>& sectorExpectedLoss() const;
    const std::vector<Real>& sectorUnexpectedLoss() const;
    Real lossQuantile(Real p);
};

//------

class MaddockInverseCumulativeNormal {
  public:
    MaddockInverseCumulativeNormal(
        Real average = 0.0,
        Real sigma   = 1.0);
    Real operator()(Real x) const;
};

class BivariateCumulativeStudentDistribution {
  public:
    BivariateCumulativeStudentDistribution(
        Natural n,
        Real rho);
    Real operator()(Real x, Real y) const;
};

class StochasticCollocationInvCDF {
  public:
    %extend {
        StochasticCollocationInvCDF(
            PyObject* invCDF,
            Size lagrangeOrder,
            Real pMax = Null<Real>(),
            Real pMin = Null<Real>()) {
                return new StochasticCollocationInvCDF(
                    UnaryFunction(invCDF),
                    lagrangeOrder, pMax, pMin);
            }
    }
    Real value(Real x) const;
    Real operator()(Real u) const;
};

class NonCentralCumulativeChiSquareSankaranApprox {
  public:
    NonCentralCumulativeChiSquareSankaranApprox(
        Real df, Real ncp);
    Real operator()(Real x) const;
};

//-----------

class FastFourierTransform {
  public:
    static Size min_order(Size inputSize);
    FastFourierTransform(Size order);
    Size output_size() const;

    %extend {
        std::vector<std::complex<Real>> transform(
            const std::vector<std::complex<Real>>& in) const {
            std::vector<std::complex<Real>> out(in.size());
            self->transform(in.begin(), in.end(), out.begin());
            return out;
        }
        std::vector<std::complex<Real>> inverse_transform(
            const std::vector<std::complex<Real>>& in) const {
            Size outSize = static_cast<Size>(1) << in.size();
            std::vector<std::complex<Real>> out(outSize);
            self->inverse_transform(in.begin(), in.end(), out.begin());
            return out;
        }
    }
};

%template(ComplexVector) std::vector<std::complex<Real>>;

class Factorial {
  public:
    static Real get(Natural n);
    static Real ln(Natural n);
  private:
    Factorial();
};

Real modifiedBesselFunction_i(Real nu, Real x);
Real modifiedBesselFunction_k(Real nu, Real x);
Real modifiedBesselFunction_i_exponentiallyWeighted(Real nu, Real x);
Real modifiedBesselFunction_k_exponentiallyWeighted(Real nu, Real x);

std::complex<Real> modifiedBesselFunction_i(
    Real nu, const std::complex<Real>& z);
std::complex<Real> modifiedBesselFunction_k(
    Real nu, const std::complex<Real>& z);
std::complex<Real> modifiedBesselFunction_i_exponentiallyWeighted(
    Real nu, const std::complex<Real> &z);
std::complex<Real> modifiedBesselFunction_k_exponentiallyWeighted(
    Real nu, const std::complex<Real> &z);

class TwoDimensionalIntegral {
  public:
    TwoDimensionalIntegral(
        ext::shared_ptr<Integrator> integratorX,
        ext::shared_ptr<Integrator> integratorY);
    %extend {
        Real operator()(
            PyObject* f,
            const std::pair<Real, Real>& a,
            const std::pair<Real, Real>& b) const {
                return (*self)(
                    BinaryFunction(f), a, b);
            }
    }
};

Real Si(Real x);
Real Ci(Real x);
std::complex<Real> E1(std::complex<Real> z);
std::complex<Real> Ei(std::complex<Real> z);
std::complex<Real> Si(std::complex<Real> z);
std::complex<Real> Ci(std::complex<Real> z);

class AbcdMathFunction {
  public:
    AbcdMathFunction(Real a = 0.002,
                     Real b = 0.001,
                     Real c = 0.16,
                     Real d = 0.0005);
    AbcdMathFunction(std::vector<Real> abcd);

    Real operator()(Time t) const;
    Time maximumLocation() const;
    Real maximumValue() const;
    Real longTermValue() const { return d_; }
    Real derivative(Time t) const;
    Real primitive(Time t) const;
    Real definiteIntegral(Time t1, Time t2) const;
    Real a() const;
    Real b() const;
    Real c() const;
    Real d() const;
    const std::vector<Real>& coefficients() { return abcd_; }
    const std::vector<Real>& derivativeCoefficients() { return dabcd_; }
    std::vector<Real> definiteIntegralCoefficients(
        Time t, Time t2) const;
    std::vector<Real> definiteDerivativeCoefficients(
        Time t, Time t2) const;
    static void validate(Real a, Real b, Real c, Real d);
};

class AbcdFunction : public AbcdMathFunction {
  public:
    AbcdFunction(Real a = -0.06,
                 Real b =  0.17,
                 Real c =  0.54,
                 Real d =  0.17);

    Real maximumVolatility() const;
    Real shortTermVolatility() const;
    Real longTermVolatility() const;
    Real covariance(Time t, Time T, Time S) const;
    Real covariance(Time t1, Time t2, Time T, Time S) const;
    Real volatility(Time tMin, Time tMax, Time T) const;
    Real variance(Time tMin, Time tMax, Time T) const;
    Real instantaneousVolatility(Time t, Time T) const;
    Real instantaneousVariance(Time t, Time T) const;
    Real instantaneousCovariance(Time u, Time T, Time S) const;
    Real primitive(Time t, Time T, Time S) const;
};

class AbcdSquared {
  public:
    AbcdSquared(Real a, Real b, Real c, Real d, Time T, Time S);
    Real operator()(Time t) const;
};

Real abcdBlackVolatility(Time u, Real a, Real b, Real c, Real d);

%inline %{
    long primitivePolynomials(Size i, Size j) {
        return PrimitivePolynomials[i][j];
    }
%}

class FaureRsg {
  public:
    typedef Sample<std::vector<Real> > sample_type;
    FaureRsg(Size dimensionality);
    const std::vector<long int>& nextIntSequence() const;
    const std::vector<long int>& lastIntSequence() const;
    const sample_type& nextSequence() const;
    const sample_type& lastSequence() const;
    Size dimension() const;
};

class LatticeRsg {
  public:
    typedef Sample<std::vector<Real> > sample_type;
    LatticeRsg(Size dimensionality, std::vector<Real> z, Size N);

    void skipTo(unsigned long n);
    const sample_type& nextSequence();
    Size dimension() const;
    const sample_type& lastSequence() const;
};

template <class LDS,
          class PRS = RandomSequenceGenerator<MersenneTwisterUniformRng> >
class RandomizedLDS {
  public:
    typedef Sample<std::vector<Real> > sample_type;
    RandomizedLDS(const LDS& ldsg, PRS prsg);
    RandomizedLDS(const LDS& ldsg);
    RandomizedLDS(Size dimensionality,
                  BigNatural ldsSeed = 0,
                  BigNatural prsSeed = 0);
    const sample_type& nextSequence() const;
    const sample_type& lastSequence() const;
    void nextRandomizer();
    Size dimension() const;
};

template <>
class RandomizedLDS<LatticeRsg, RandomSequenceGenerator<MersenneTwisterUniformRng>> {
  public:
    typedef Sample<std::vector<Real> > sample_type;
    RandomizedLDS(const LatticeRsg& ldsg, RandomSequenceGenerator<MersenneTwisterUniformRng> prsg);
    RandomizedLDS(const LatticeRsg& ldsg);
    const sample_type& nextSequence() const;
    const sample_type& lastSequence() const;
    void nextRandomizer();
    Size dimension() const;
};

%template(RandomizedSobolLDS) RandomizedLDS<SobolRsg>;
%template(RandomizedLatticeLDS) RandomizedLDS<LatticeRsg>;

class LatticeRule {
public:
    enum type {
        A, B , C , D};
    %extend {
        static std::vector<Real> getRule(
            type name, Integer N) {
                std::vector<Real> z;
                LatticeRule::getRule(name, z, N);
                return z;
            }
    }
    /* static void getRule(
        type name, std::vector<Real>& Z, Integer N); */
};

class SymmetricSchurDecomposition {
  public:
    SymmetricSchurDecomposition(const Matrix &s);
    const Array& eigenvalues() const;
    const Matrix& eigenvectors() const;
};

std::vector<Size> qrDecomposition(
    const Matrix& M, Matrix& q, Matrix& r, bool pivot = true);

Array qrSolve(
    const Matrix& a, const Array& b,
    bool pivot, const Array& d = Array());

Real determinant(const Matrix& m);

class OrthogonalProjections {
public:
    OrthogonalProjections(
        const Matrix& originalVectors,
        Real multiplierCutOff,
        Real tolerance);
    /* const std::valarray<bool>& validVectors() const; */
    %extend {
        std::vector<bool> validVectors() const {
            const std::valarray<bool>& v=self->validVectors();
            std::vector<bool> rst(std::begin(v), std::end(v));
            return rst;
        }
    }
    const std::vector<Real>& GetVector(Size index) const;
    Size numberValidVectors() const;
};

Matrix CholeskyDecomposition(
    const Matrix& S, bool flexible);

Matrix moorePenroseInverse(
    const Matrix &A, const Real tol = Null<Real>());

class NumericalDifferentiation {
  public:
    enum Scheme {
        Central, Backward, Forward };
    %extend {
        NumericalDifferentiation(
            PyObject* f,
            Size orderOfDerivative,
            Array x_offsets) {
                return new NumericalDifferentiation(
                    UnaryFunction(f), orderOfDerivative, x_offsets);
            }
        NumericalDifferentiation(
            PyObject* f,
            Size orderOfDerivative,
            Real stepSize,
            Size steps,
            Scheme scheme) {
                return new NumericalDifferentiation(
                    UnaryFunction(f),
                    orderOfDerivative, stepSize, steps, scheme);
            }
    }

    Real operator()(Real x) const;
    const Array& offsets() const;
    const Array& weights() const;
};

class TqrEigenDecomposition {
  public:
    enum EigenVectorCalculation {
        WithEigenVector,
        WithoutEigenVector,
        OnlyFirstRowEigenVector };

    enum ShiftStrategy {
        NoShift,
        Overrelaxation,
        CloseEigenValue };

    TqrEigenDecomposition(
        const Array& diag,
        const Array& sub,
        EigenVectorCalculation calc = WithEigenVector,
        ShiftStrategy strategy = CloseEigenValue);

    const Array& eigenvalues() const;
    const Matrix& eigenvectors() const;
    Size iterations() const;
};

class BSpline {
  public:
    BSpline(Natural p,
            Natural n,
            const std::vector<Real>& knots);
    Real operator()(Natural i, Real x) const;
};

Array CenteredGrid(Real center, Real dx, Size steps);
Array BoundedGrid(Real xMin, Real xMax, Size steps);
Array BoundedLogGrid(Real xMin, Real xMax, Size steps);

class TransformedGrid {
public:
    TransformedGrid (const Array& grid);
    %extend {
        TransformedGrid(const Array& grid, PyObject* func) {
            return new TransformedGrid(grid, UnaryFunction(func));
        }
    }

    const Array& gridArray() const;
    const Array& transformedGridArray() const;
    const Array& dxmArray() const;
    const Array& dxpArray() const;
    const Array& dxArray() const;

    Real grid(Size i) const;
    Real transformedGrid(Size i) const;
    Real dxm(Size i) const;
    Real dxp(Size i) const;
    Real dx(Size i) const;
    Size size() const;
};

class LogGrid : public TransformedGrid {
public:
    LogGrid(const Array& grid);
    const Array& logGridArray() const;
    Real logGrid(Size i) const;
};

#endif
