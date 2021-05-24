#ifndef ql_statistics_i
#define ql_statistics_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include stl.i

%{
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

%template(MultipleStatistics) GenericSequenceStatistics<Statistics>;
%template(SequenceStatistics) GenericSequenceStatistics<RiskStatistics>;
%template(MultipleIncrementalStatistics) GenericSequenceStatistics<IncrementalStatistics>;

#endif
