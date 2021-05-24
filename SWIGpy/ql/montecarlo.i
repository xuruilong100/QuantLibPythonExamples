#ifndef ql_montecarlo_i
#define ql_montecarlo_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i

%inline %{
Matrix getCovariance(
    const Array& volatilities,
    const Matrix& correlations) {
    return QuantLib::getCovariance(
        volatilities.begin(),
        volatilities.end(),
        correlations);
}
%}

%{
using QuantLib::Path;
using QuantLib::PathGenerator;
using QuantLib::MultiPath;
using QuantLib::MultiPathGenerator;
using QuantLib::BrownianBridge;
%}

class Path {
    %rename(__len__) length;
  private:
    Path();
  public:
    Size length() const;
    Real value(Size i) const;
    Real front() const;
    Real back() const;
    Time time(Size i) const;
    %extend {
        Real __getitem__(Integer i) {
            Integer size_ = Integer(self->length());
            if (i>=0 && i<size_) {
                return (*self)[i];
            } else if (i<0 && -i<=size_) {
                return (*self)[size_+i];
            } else {
                throw std::out_of_range("path index out of range");
            }
        }

    }
};

%template(SamplePath) Sample<Path>;

template <class GSG>
class PathGenerator {
  public:
    typedef Sample<Path> sample_type;
    PathGenerator(
        const ext::shared_ptr<StochasticProcess>& process,
        Time length,
        Size timeSteps,
        const GSG& generator,
        bool brownianBridge);
    PathGenerator(
        const ext::shared_ptr<StochasticProcess>& process,
        const TimeGrid& timeGrid,
        const GSG& generator,
        bool brownianBridge);
    const sample_type& next() const;
    const sample_type& antithetic() const;
    Size size() const;
    const TimeGrid& timeGrid() const;
};

%template(GaussianPathGenerator) PathGenerator<GaussianRandomSequenceGenerator>;
%template(GaussianSobolPathGenerator) PathGenerator<GaussianLowDiscrepancySequenceGenerator>;
%template(InvCumulativeMersenneTwisterPathGenerator) PathGenerator<InverseCumulativeRsg<RandomSequenceGenerator<MersenneTwisterUniformRng>, InverseCumulativeNormal> >;

class MultiPath {
    %rename(__len__) pathSize;
  private:
    MultiPath();
  public:
    Size pathSize() const;
    Size assetNumber() const;
	Path& at(Size j);

    %extend {
        const Path& __getitem__(Integer i) {
            Integer assets_ = Integer(self->assetNumber());
            if (i>=0 && i<assets_) {
                return (*self)[i];
            } else if (i<0 && -i<=assets_) {
                return (*self)[assets_+i];
            } else {
                throw std::out_of_range("multi-path index out of range");
            }
        }
    }
};

%template(SampleMultiPath) Sample<MultiPath>;

template <class GSG>
class MultiPathGenerator {
  public:
    typedef Sample<MultiPath> sample_type;
    MultiPathGenerator(
        const ext::shared_ptr<StochasticProcess>&,
        const TimeGrid& timeGrid,
        const GSG& generator,
        bool brownianBridge = false);
    %extend {
        MultiPathGenerator(
            const ext::shared_ptr<StochasticProcess>& process,
            const std::vector<Time>& times,
            const GSG& generator,
            bool brownianBridge = false) {
            return new MultiPathGenerator<GSG>(
                process,
                TimeGrid(times.begin(), times.end()),
                generator,
                brownianBridge);
        }
    }
    const sample_type& next() const;
    const sample_type& antithetic() const;
};

%template(GaussianMultiPathGenerator) MultiPathGenerator<GaussianRandomSequenceGenerator>;
%template(GaussianSobolMultiPathGenerator) MultiPathGenerator<GaussianLowDiscrepancySequenceGenerator>;

class BrownianBridge {
  public:
    BrownianBridge(Size steps);
    BrownianBridge(const std::vector<Time>& times);
    BrownianBridge(const TimeGrid& timeGrid);

    Size size() const;
    std::vector<Time> times() const;
    std::vector<Real> leftWeight() const;
    std::vector<Real> rightWeight() const;
    std::vector<Real> stdDeviation() const;
    %extend {
        std::vector<Real> transform(
            const std::vector<Real>& input) {
            std::vector<Real> outp(input.size());
            $self->transform(
                input.begin(), input.end(), outp.begin());
            return outp;
        }
        std::vector<unsigned int> bridgeIndex() const {
            return to_vector<unsigned int>($self->bridgeIndex());
        }
        std::vector<unsigned int> leftIndex() const {
            return to_vector<unsigned int>($self->leftIndex());
        }
        std::vector<unsigned int> rightIndex() const {
            return to_vector<unsigned int>($self->rightIndex());
        }
    }
};

#endif
