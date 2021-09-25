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
    explicit FdmLinearOpIterator(
        Size index = 0);
    explicit FdmLinearOpIterator(
        const std::vector<Size>& dim);
    FdmLinearOpIterator(
        std::vector<Size> dim,
        std::vector<Size> coordinates,
        Size index);
    FdmLinearOpIterator(
        const Disposable<FdmLinearOpIterator> & from);

    Size index() const;
    const std::vector<Size>& coordinates() const;
    void swap(FdmLinearOpIterator& iter);
    %extend {
        void increment() {
            ++(*$self);
        }
        bool notEqual(const FdmLinearOpIterator& iterator) {
            return (*self) != iterator;
        }
    }
};

%shared_ptr(FdmLinearOpLayout)
class FdmLinearOpLayout {
  public:
    explicit FdmLinearOpLayout(const std::vector<Size>& dim);

    FdmLinearOpIterator begin() const;
    FdmLinearOpIterator end() const;
    const std::vector<Size>& dim() const;
    const std::vector<Size>& spacing() const;
    Size size() const;
    Size index(const std::vector<Size>& coordinates) const;
    Size neighbourhood(const FdmLinearOpIterator& iterator,
                       Size i, Integer offset) const;
    Size neighbourhood(const FdmLinearOpIterator& iterator,
                       Size i1, Integer offset1,
                       Size i2, Integer offset2) const;

    FdmLinearOpIterator iter_neighbourhood(
        const FdmLinearOpIterator& iterator, Size i, Integer offset) const;
};

%shared_ptr(FdmIndicesOnBoundary)
class FdmIndicesOnBoundary {
  public:
    FdmIndicesOnBoundary(
        const ext::shared_ptr<FdmLinearOpLayout>& l,
        Size direction,
        FdmDirichletBoundary::Side side);

    const std::vector<Size>& getIndices() const;
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

    Rate quantoAdjustment(
        Volatility equityVol, Time t1, Time t2) const;
    Array quantoAdjustment(
        const Array& equityVol, Time t1, Time t2) const;
};

class FdmHestonGreensFct {
  public:
    enum Algorithm {
        ZeroCorrelation,
        Gaussian,
        SemiAnalytical };

    FdmHestonGreensFct(
        ext::shared_ptr<FdmMesher> mesher,
        ext::shared_ptr<HestonProcess> process,
        FdmSquareRootFwdOp::TransformationType trafoType_,
        Real l0 = 1.0);

    Array get(Time t, Algorithm algorithm) const;
};

#endif
