#ifndef ql_random_numbers_i
#define ql_random_numbers_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i

%{
using QuantLib::LecuyerUniformRng;
using QuantLib::KnuthUniformRng;
using QuantLib::MersenneTwisterUniformRng;
using QuantLib::CLGaussianRng;
using QuantLib::BoxMullerGaussianRng;
using QuantLib::InverseCumulativeRng;
using QuantLib::HaltonRsg;
using QuantLib::SobolRsg;
using QuantLib::SobolBrownianBridgeRsg;
using QuantLib::InverseCumulativeRsg;
using QuantLib::RandomSequenceGenerator;
typedef QuantLib::LowDiscrepancy::rsg_type GaussianLowDiscrepancySequenceGenerator;
typedef QuantLib::LowDiscrepancy::ursg_type UniformLowDiscrepancySequenceGenerator;
typedef QuantLib::PseudoRandom::rsg_type GaussianRandomSequenceGenerator;
typedef QuantLib::PseudoRandom::rng_type GaussianRandomGenerator;
typedef QuantLib::PseudoRandom::urng_type UniformRandomGenerator;
typedef QuantLib::PseudoRandom::ursg_type UniformRandomSequenceGenerator;
%}

/************* Uniform number generators *************/

class LecuyerUniformRng {
  public:
    LecuyerUniformRng(BigInteger seed=0);
    Sample<Real> next() const;
};

class KnuthUniformRng {
  public:
    KnuthUniformRng(BigInteger seed=0);
    Sample<Real> next() const;
};

class MersenneTwisterUniformRng {
  public:
    MersenneTwisterUniformRng(BigInteger seed = 0);
    Sample<Real> next() const;
};

class UniformRandomGenerator {
  public:
    UniformRandomGenerator(BigInteger seed=0);
    Sample<Real> next() const;

	%extend {
		// improve performance for direct access. faster version
		Real nextValue() const {
			return (*self).next().value;
		}
	}
};

/************* Gaussian number generators *************/

template<class RNG>
class CLGaussianRng {
  public:
    CLGaussianRng(const RNG& rng);
    Sample<Real> next() const;
};

%template(CentralLimitLecuyerGaussianRng) CLGaussianRng<LecuyerUniformRng>;
%template(CentralLimitKnuthGaussianRng) CLGaussianRng<KnuthUniformRng>;
%template(CentralLimitMersenneTwisterGaussianRng) CLGaussianRng<MersenneTwisterUniformRng>;

template<class RNG>
class BoxMullerGaussianRng {
  public:
    BoxMullerGaussianRng(const RNG& rng);
    Sample<Real> next() const;
};

%template(BoxMullerLecuyerGaussianRng) BoxMullerGaussianRng<LecuyerUniformRng>;
%template(BoxMullerKnuthGaussianRng) BoxMullerGaussianRng<KnuthUniformRng>;
%template(BoxMullerMersenneTwisterGaussianRng) BoxMullerGaussianRng<MersenneTwisterUniformRng>;

template<class RNG, class F>
class InverseCumulativeRng {
  public:
    InverseCumulativeRng(const RNG& rng);
    Sample<Real> next() const;
};

%template(MoroInvCumulativeLecuyerGaussianRng) InverseCumulativeRng<LecuyerUniformRng,MoroInverseCumulativeNormal>;
%template(MoroInvCumulativeKnuthGaussianRng) InverseCumulativeRng<KnuthUniformRng,MoroInverseCumulativeNormal>;
%template(MoroInvCumulativeMersenneTwisterGaussianRng) InverseCumulativeRng<MersenneTwisterUniformRng, MoroInverseCumulativeNormal>;
%template(InvCumulativeLecuyerGaussianRng) InverseCumulativeRng<LecuyerUniformRng,InverseCumulativeNormal>;
%template(InvCumulativeKnuthGaussianRng) InverseCumulativeRng<KnuthUniformRng,InverseCumulativeNormal>;
%template(InvCumulativeMersenneTwisterGaussianRng) InverseCumulativeRng<MersenneTwisterUniformRng, InverseCumulativeNormal>;

class GaussianRandomGenerator {
  public:
    GaussianRandomGenerator(
        const UniformRandomGenerator& rng);
    Sample<Real> next() const;

	%extend {
		// improve performance for direct access, faster version
		Real nextValue() const {
			return (*self).next().value;
		}
	}
};

/************* Uniform sequence generators *************/

class HaltonRsg {
  public:
    HaltonRsg(
        Size dimensionality,
        unsigned long seed = 0,
        bool randomStart = true,
        bool randomShift = false);
    const Sample<std::vector<Real>>& nextSequence() const;
    const Sample<std::vector<Real>>& lastSequence() const;
    Size dimension() const;
};

class SobolRsg {
  public:
    enum DirectionIntegers {
        Unit,
        Jaeckel,
        SobolLevitan,
        SobolLevitanLemieux,
        JoeKuoD5,
        JoeKuoD6,
        JoeKuoD7,
        Kuo,
        Kuo2,
        Kuo3
    };
    SobolRsg(
        Size dimensionality,
        BigInteger seed = 0,
        DirectionIntegers directionIntegers = QuantLib::SobolRsg::Jaeckel);
    const Sample<std::vector<Real>>& nextSequence() const;
    const Sample<std::vector<Real>>& lastSequence() const;
    Size dimension() const;
    void skipTo(Size n);
    %extend {
        std::vector<unsigned int> nextInt32Sequence() {
            return to_vector<unsigned int>(
                self->nextInt32Sequence());
        }
    }
};

class SobolBrownianBridgeRsg {
  public:
    SobolBrownianBridgeRsg(
        Size factors,
        Size steps,
        SobolBrownianGenerator::Ordering ordering = SobolBrownianGenerator::Diagonal,
        unsigned long seed = 0,
        SobolRsg::DirectionIntegers directionIntegers = SobolRsg::JoeKuoD7);
    const Sample<std::vector<Real>>& nextSequence() const;
    const Sample<std::vector<Real>>& lastSequence() const;
    Size dimension() const;
};

template <class RNG>
class RandomSequenceGenerator {
  public:
    RandomSequenceGenerator(
        Size dimensionality,
        const RNG& rng);
    RandomSequenceGenerator(
        Size dimensionality,
        BigNatural seed = 0);
    const Sample<std::vector<Real>>& nextSequence() const;
    const Sample<std::vector<Real>>& lastSequence() const;
    Size dimension() const;
};

%template(LecuyerUniformRsg) RandomSequenceGenerator<LecuyerUniformRng>;
%template(KnuthUniformRsg) RandomSequenceGenerator<KnuthUniformRng>;
%template(MersenneTwisterUniformRsg) RandomSequenceGenerator<MersenneTwisterUniformRng>;

class UniformRandomSequenceGenerator {
  public:
    UniformRandomSequenceGenerator(
        Size dimensionality,
        const UniformRandomGenerator& rng);
    const Sample<std::vector<Real>>& nextSequence() const;
    const Sample<std::vector<Real>>& lastSequence() const;
    Size dimension() const;
};

class UniformLowDiscrepancySequenceGenerator {
  public:
    UniformLowDiscrepancySequenceGenerator(
        Size dimensionality,
        BigInteger seed=0,
        SobolRsg::DirectionIntegers directionIntegers = QuantLib::SobolRsg::Jaeckel);
    const Sample<std::vector<Real>>& nextSequence() const;
    const Sample<std::vector<Real>>& lastSequence() const;
    Size dimension() const;
};

/************* Gaussian sequence generators *************/

template <class U, class I>
class InverseCumulativeRsg {
  public:
    InverseCumulativeRsg(
        const U& uniformSequenceGenerator);
    InverseCumulativeRsg(
        const U& uniformSequenceGenerator,
        const I& inverseCumulative);
    const Sample<std::vector<Real>>& nextSequence() const;
    const Sample<std::vector<Real>>& lastSequence() const;
    Size dimension() const;
};


%template(MoroInvCumulativeLecuyerGaussianRsg) InverseCumulativeRsg<RandomSequenceGenerator<LecuyerUniformRng>, MoroInverseCumulativeNormal>;
%template(MoroInvCumulativeKnuthGaussianRsg) InverseCumulativeRsg<RandomSequenceGenerator<KnuthUniformRng>, MoroInverseCumulativeNormal>;
%template(MoroInvCumulativeMersenneTwisterGaussianRsg) InverseCumulativeRsg<RandomSequenceGenerator<MersenneTwisterUniformRng>, MoroInverseCumulativeNormal>;
%template(MoroInvCumulativeHaltonGaussianRsg) InverseCumulativeRsg<HaltonRsg, MoroInverseCumulativeNormal>;
%template(MoroInvCumulativeSobolGaussianRsg) InverseCumulativeRsg<SobolRsg, MoroInverseCumulativeNormal>;
%template(InvCumulativeLecuyerGaussianRsg) InverseCumulativeRsg<RandomSequenceGenerator<LecuyerUniformRng>, InverseCumulativeNormal>;
%template(InvCumulativeKnuthGaussianRsg) InverseCumulativeRsg<RandomSequenceGenerator<KnuthUniformRng>, InverseCumulativeNormal>;
%template(InvCumulativeMersenneTwisterGaussianRsg) InverseCumulativeRsg<RandomSequenceGenerator<MersenneTwisterUniformRng>, InverseCumulativeNormal>;
%template(InvCumulativeHaltonGaussianRsg) InverseCumulativeRsg<HaltonRsg,InverseCumulativeNormal>;
%template(InvCumulativeSobolGaussianRsg) InverseCumulativeRsg<SobolRsg,InverseCumulativeNormal>;

class GaussianRandomSequenceGenerator {
  public:
    GaussianRandomSequenceGenerator(
        const UniformRandomSequenceGenerator& uniformSequenceGenerator);
    const Sample<std::vector<Real>>& nextSequence() const;
    const Sample<std::vector<Real>>& lastSequence() const;
    Size dimension() const;
};

class GaussianLowDiscrepancySequenceGenerator {
  public:
    GaussianLowDiscrepancySequenceGenerator(
        const UniformLowDiscrepancySequenceGenerator& u);
    const Sample<std::vector<Real>>& nextSequence() const;
    const Sample<std::vector<Real>>& lastSequence() const;
    Size dimension() const;
};

#endif
