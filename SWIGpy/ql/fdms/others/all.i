#ifndef ql_fdms_others_all_i
#define ql_fdms_others_all_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i

%{
using QuantLib::FdmLinearOpIterator;
using QuantLib::FdmLinearOpLayout;
using QuantLib::FdmIndicesOnBoundary;
using QuantLib::FdmSchemeDesc;
using QuantLib::FdmQuantoHelper;
using QuantLib::FdmHestonGreensFct;
%}

class FdmLinearOpIterator {
  public:
    %extend {
        FdmLinearOpIterator(const std::vector<unsigned int>& dim,
                            const std::vector<unsigned int>& coordinates,
                            Size index) {
            return new FdmLinearOpIterator(to_vector<Size>(dim),
                                           to_vector<Size>(coordinates),
                                           index);
        }
        std::vector<unsigned int> coordinates() {
            return to_vector<unsigned int>($self->coordinates());
        }
        void increment() {
            ++(*$self);
        }
        bool notEqual(const FdmLinearOpIterator& iterator) {
            return self->operator!=(iterator);
        }
    }

    Size index() const;
};

%shared_ptr(FdmLinearOpLayout)
class FdmLinearOpLayout {
  public:
    %extend {
        FdmLinearOpLayout(
            const std::vector<unsigned int>& dim) {
            return new FdmLinearOpLayout(to_vector<Size>(dim));
        }
        std::vector<unsigned int> spacing() {
            return to_vector<unsigned int>($self->spacing());
        }
        std::vector<unsigned int> dim() const {
            return to_vector<unsigned int>($self->dim());
        }
        Size index(
            const std::vector<unsigned int>& coordinates) const {
            return $self->index(to_vector<Size>(coordinates));
        }
    }

    FdmLinearOpIterator begin() const;
    FdmLinearOpIterator end() const;

    Size size() const;

    Size neighbourhood(
        const FdmLinearOpIterator& iterator,
        Size i, Integer offset) const;

    Size neighbourhood(
        const FdmLinearOpIterator& iterator,
        Size i1, Integer offset1,
        Size i2, Integer offset2) const;

    FdmLinearOpIterator iter_neighbourhood(
        const FdmLinearOpIterator& iterator,
        Size i, Integer offset) const;
};

%shared_ptr(FdmIndicesOnBoundary)
class FdmIndicesOnBoundary {
  public:
    FdmIndicesOnBoundary(
        const ext::shared_ptr<FdmLinearOpLayout>& l,
        Size direction,
        FdmDirichletBoundary::Side side);

    %extend {
        std::vector<unsigned int> getIndices() const {
            return to_vector<unsigned int>($self->getIndices());
        }
    }
};

struct FdmSchemeDesc {
    enum FdmSchemeType {
        HundsdorferType,
        DouglasType,
        CraigSneydType,
        ModifiedCraigSneydType,
        ImplicitEulerType,
        ExplicitEulerType,
        MethodOfLinesType,
        TrBDF2Type,
        CrankNicolsonType
    };

    FdmSchemeDesc(
        FdmSchemeType type, Real theta, Real mu);

    const FdmSchemeType type;
    const Real theta, mu;

    // some default scheme descriptions
    static FdmSchemeDesc Douglas();
    static FdmSchemeDesc CrankNicolson();
    static FdmSchemeDesc ImplicitEuler();
    static FdmSchemeDesc ExplicitEuler();
    static FdmSchemeDesc CraigSneyd();
    static FdmSchemeDesc ModifiedCraigSneyd();
    static FdmSchemeDesc Hundsdorfer();
    static FdmSchemeDesc ModifiedHundsdorfer();
    static FdmSchemeDesc MethodOfLines(
        Real eps = 0.001, Real relInitStepSize = 0.01);
    static FdmSchemeDesc TrBDF2();
};

%shared_ptr(FdmQuantoHelper)
class FdmQuantoHelper {
  public:
    FdmQuantoHelper(
        const ext::shared_ptr<YieldTermStructure>& rTS,
        const ext::shared_ptr<YieldTermStructure>& fTS,
        const ext::shared_ptr<BlackVolTermStructure>& fxVolTS,
        Real equityFxCorrelation,
        Real exchRateATMlevel);
};

struct FdmHestonGreensFct {
    enum Algorithm { ZeroCorrelation, Gaussian, SemiAnalytical };
  private:
    FdmHestonGreensFct();
};

#endif
