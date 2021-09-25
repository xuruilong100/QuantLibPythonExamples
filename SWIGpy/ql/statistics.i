#ifndef ql_statistics_i
#define ql_statistics_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i

%{
using QuantLib::Statistics;
using QuantLib::IncrementalStatistics;
using QuantLib::RiskStatistics;
using QuantLib::GenericSequenceStatistics;
using QuantLib::GeneralStatistics;
using QuantLib::GenericGaussianStatistics;
using QuantLib::GenericRiskStatistics;
using QuantLib::GaussianStatistics;
using QuantLib::SequenceStatistics;
using QuantLib::SequenceStatisticsInc;
%}

class GeneralStatistics {
  public:
    GeneralStatistics();
    Size samples() const;
    const std::vector<std::pair<Real,Real> >& data() const;
    Real weightSum() const;
    Real mean() const;
    Real variance() const;
    Real standardDeviation() const;
    Real errorEstimate() const;
    Real skewness() const;
    Real kurtosis() const;
    Real min() const;
    Real max() const;
    /* template <class Func, class Predicate>
    std::pair<Real,Size> expectationValue(
        const Func& f,
        const Predicate& inRange) const */
    Real percentile(Real y) const;
    Real topPercentile(Real y) const;
    void add(Real value, Real weight = 1.0);
    %extend {
        void addSequence(const std::vector<Real>& data) {
            self->addSequence(data.begin(), data.end());
        }
        void addSequence(
            const std::vector<Real>& data,
            const std::vector<Real>& weight) {
            self->addSequence(
                data.begin(), data.end(),
                weight.begin());
        }
    }
    void reset();
    void reserve(Size n) const;
    void sort() const;
};

template<class Stat>
class GenericGaussianStatistics : public Stat {
  public:
    GenericGaussianStatistics();
    explicit GenericGaussianStatistics(const GeneralStatistics& s);

    Real gaussianDownsideVariance() const;
    Real gaussianDownsideDeviation() const;
    Real gaussianRegret(Real target) const;
    Real gaussianPercentile(Real percentile) const;
    Real gaussianTopPercentile(Real percentile) const;
    Real gaussianPotentialUpside(Real percentile) const;
    Real gaussianValueAtRisk(Real percentile) const;
    Real gaussianExpectedShortfall(Real percentile) const;
    Real gaussianShortfall(Real target) const;
    Real gaussianAverageShortfall(Real target) const;
};

%template(GaussianStatistics) GenericGaussianStatistics<GeneralStatistics>;
typedef GenericGaussianStatistics<GeneralStatistics> GaussianStatistics;

template<class S>
class GenericRiskStatistics : public S {
  public:
    Real semiVariance() const;
    Real semiDeviation() const;
    Real downsideVariance() const;
    Real downsideDeviation() const;
    Real regret(Real target) const;
    Real potentialUpside(Real percentile) const;
    Real valueAtRisk(Real percentile) const;
    Real expectedShortfall(Real percentile) const;
    Real shortfall(Real target) const;
    Real averageShortfall(Real target) const;
};

%template(RiskStatistics) GenericRiskStatistics<GaussianStatistics>;
typedef RiskStatistics Statistics;

class IncrementalStatistics {
  public:
    Size samples() const;
    Real weightSum() const;
    Real mean() const;
    Real variance() const;
    Real standardDeviation() const;
    Real errorEstimate() const;
    Real skewness() const;
    Real kurtosis() const;
    Real min() const;
    Real max() const;
    // Modifiers
    void reset();
    void add(Real value, Real weight = 1.0);
    %extend {
        void add(const std::vector<Real>& values) {
            self->addSequence(values.begin(), values.end());
        }
        void add(const std::vector<Real>& values,
                 const std::vector<Real>& weights) {
            self->addSequence(values.begin(), values.end(), weights.begin());
        }
    }
};

template <class StatisticsType>
class GenericSequenceStatistics {
  public:
    GenericSequenceStatistics(Size dimension = 0);
    Size size() const { return dimension_; }
    Matrix covariance() const;
    Matrix correlation() const;
    Size samples() const;
    Real weightSum() const;
    std::vector<Real> mean() const;
    std::vector<Real> variance() const;
    std::vector<Real> standardDeviation() const;
    std::vector<Real> downsideVariance() const;
    std::vector<Real> downsideDeviation() const;
    std::vector<Real> semiVariance() const;
    std::vector<Real> semiDeviation() const;
    std::vector<Real> errorEstimate() const;
    std::vector<Real> skewness() const;
    std::vector<Real> kurtosis() const;
    std::vector<Real> min() const;
    std::vector<Real> max() const;
    std::vector<Real> gaussianPercentile(Real y) const;
    std::vector<Real> percentile(Real y) const;
    std::vector<Real> gaussianPotentialUpside(Real percentile) const;
    std::vector<Real> potentialUpside(Real percentile) const;
    std::vector<Real> gaussianValueAtRisk(Real percentile) const;
    std::vector<Real> valueAtRisk(Real percentile) const;
    std::vector<Real> gaussianExpectedShortfall(Real percentile) const;
    std::vector<Real> expectedShortfall(Real percentile) const;
    std::vector<Real> regret(Real target) const;
    std::vector<Real> gaussianShortfall(Real target) const;
    std::vector<Real> shortfall(Real target) const;
    std::vector<Real> gaussianAverageShortfall(Real target) const;
    std::vector<Real> averageShortfall(Real target) const;
    void reset(Size dimension = 0);
    %extend {
        void add(
            const std::vector<Real>& sample,
            Real weight = 1.0) {
                self->add(sample, weight);
            }
    }
};

%template(SequenceStatistics) GenericSequenceStatistics<Statistics>;
//%template(SequenceStatisticsInc) GenericSequenceStatistics<IncrementalStatistics>;

//-----------------------------------------------------------

/* %{
using QuantLib::Statistics;
using QuantLib::IncrementalStatistics;
using QuantLib::RiskStatistics;
using QuantLib::GenericSequenceStatistics;
%}

class Statistics {
  public:
    Size samples() const;
    Real weightSum() const;
    Real mean() const;
    Real variance() const;
    Real standardDeviation() const;
    Real errorEstimate() const;
    Real skewness() const;
    Real kurtosis() const;
    Real min() const;
    Real max() const;
    // Modifiers
    void reset();
    void add(Real value, Real weight = 1.0);
    %extend {
        void add(const std::vector<Real>& values) {
            self->addSequence(values.begin(), values.end());
        }
        void add(const std::vector<Real>& values,
                 const std::vector<Real>& weights) {
            self->addSequence(values.begin(), values.end(), weights.begin());
        }
    }
};

class RiskStatistics : public Statistics {
  public:
    Real semiVariance() const;
    Real semiDeviation() const;
    Real downsideVariance() const;
    Real downsideDeviation() const;
    Real regret(Real target) const;
    Real potentialUpside(Real percentile) const;
    Real valueAtRisk(Real percentile) const;
    Real expectedShortfall(Real percentile) const;
    Real shortfall(Real target) const;
    Real averageShortfall(Real target) const;
};

template <class S>
class GenericSequenceStatistics {
  public:
    GenericSequenceStatistics(Size dimension);
    Size size() const;
    Size samples() const;
    Real weightSum() const;
    std::vector<Real> mean() const;
    std::vector<Real> variance() const;
    std::vector<Real> standardDeviation() const;
    std::vector<Real> errorEstimate() const;
    std::vector<Real> skewness() const;
    std::vector<Real> kurtosis() const;
    std::vector<Real> min() const;
    std::vector<Real> max() const;
    Matrix covariance() const;
    Matrix correlation() const;
    // Modifiers
    void reset();
    void add(const std::vector<Real>& value, Real weight = 1.0);
    void add(const Array& value, Real weight = 1.0);
};

%template(MultipleStatistics) GenericSequenceStatistics<Statistics>;
%template(SequenceStatistics) GenericSequenceStatistics<RiskStatistics>;
%template(MultipleIncrementalStatistics) GenericSequenceStatistics<IncrementalStatistics>; */

#endif
