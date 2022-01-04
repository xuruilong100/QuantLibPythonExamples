#ifndef ql_monte_carlo_i
#define ql_monte_carlo_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i

%{
using QuantLib::Path;
using QuantLib::PathGenerator;
using QuantLib::MultiPath;
using QuantLib::MultiPathGenerator;
using QuantLib::BrownianBridge;
%}

class Path {
    %rename(__len__) length;
  public:
    Path(TimeGrid timeGrid, Array values = Array());
    bool empty() const;
    Size length() const;
    Real at(Size i) const;
    Real value(Size i) const;
    Time time(Size i) const;
    Real front() const;
    Real back() const;
    const TimeGrid& timeGrid() const;
    %extend {
        Real __getitem__(Size i) {
            return (*self)[i];
        }
    }
};

%template(SamplePath) Sample<Path>;
//%template(PathVector) std::vector<Path>;

%shared_ptr(PathGenerator<GaussianRandomSequenceGenerator>)
%shared_ptr(PathGenerator<GaussianLowDiscrepancySequenceGenerator>)
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

class MultiPath {
    %rename(__len__) pathSize;
  public:
    MultiPath();
    MultiPath(
        Size nAsset,
        const TimeGrid& timeGrid);
    //MultiPath(std::vector<Path> multiPath);
    Size pathSize() const;
    Size assetNumber() const;
	const Path& at(Size j) const;
    %extend {
        const Path& __getitem__(Size i) {
            return (*self)[i];
        }
    }
};

%template(SampleMultiPath) Sample<MultiPath>;

%shared_ptr(MultiPathGenerator<GaussianRandomSequenceGenerator>)
%shared_ptr(MultiPathGenerator<GaussianLowDiscrepancySequenceGenerator>)
%shared_ptr(MultiPathGenerator<SobolBrownianBridgeRsg>)
template <class GSG>
class MultiPathGenerator {
  public:
    typedef Sample<MultiPath> sample_type;
    MultiPathGenerator(
        const ext::shared_ptr<StochasticProcess>&,
        const TimeGrid& timeGrid,
        const GSG& generator,
        bool brownianBridge = false);
    const sample_type& next() const;
    const sample_type& antithetic() const;
};

%template(GaussianMultiPathGenerator) MultiPathGenerator<GaussianRandomSequenceGenerator>;
%template(GaussianSobolMultiPathGenerator) MultiPathGenerator<GaussianLowDiscrepancySequenceGenerator>;
%template(BrownianBridgeSobolMultiPathGenerator) MultiPathGenerator<SobolBrownianBridgeRsg>;

class BrownianBridge {
  public:
    BrownianBridge(Size steps);
    BrownianBridge(const std::vector<Time>& times);
    BrownianBridge(const TimeGrid& timeGrid);

    Size size() const;
    const std::vector<Time>& times() const;
    const std::vector<Size>& bridgeIndex() const;
    const std::vector<Size>& leftIndex() const;
    const std::vector<Size>& rightIndex() const;
    const std::vector<Real>& leftWeight() const;
    const std::vector<Real>& rightWeight() const;
    const std::vector<Real>& stdDeviation() const;
    %extend {
        std::vector<Real> transform(
            const std::vector<Real>& input) {
            std::vector<Real> outp(input.size());
            self->transform(
                input.begin(), input.end(), outp.begin());
            return outp;
        }
    }
};

#endif
