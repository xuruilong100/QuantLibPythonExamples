#ifndef ql_fdms_FdmMesher_i
#define ql_fdms_FdmMesher_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i

%{
using QuantLib::FdmMesher;
using QuantLib::FdmMesherComposite;
using QuantLib::FdmMesherIntegral;
%}

%shared_ptr(FdmMesher)
class FdmMesher {
  private:
    FdmMesher();
  public:
    Real dplus(const FdmLinearOpIterator& iter, Size direction)  const;
    Real dminus(const FdmLinearOpIterator& iter, Size direction) const;
    Real location(const FdmLinearOpIterator& iter, Size direction) const;
    Array locations(Size direction) const;
    const ext::shared_ptr<FdmLinearOpLayout>& layout() const;
};

%shared_ptr(FdmMesherComposite)
class FdmMesherComposite : public FdmMesher {
  public:
    FdmMesherComposite(
        const ext::shared_ptr<FdmLinearOpLayout>& layout,
        const std::vector<ext::shared_ptr<Fdm1dMesher>>& mesher);

    // convenient constructors
    explicit FdmMesherComposite(
        const std::vector<ext::shared_ptr<Fdm1dMesher>>& mesher);
    explicit FdmMesherComposite(
        const ext::shared_ptr<Fdm1dMesher>& mesher);
    FdmMesherComposite(
        const ext::shared_ptr<Fdm1dMesher>& m1,
        const ext::shared_ptr<Fdm1dMesher>& m2);
    FdmMesherComposite(
        const ext::shared_ptr<Fdm1dMesher>& m1,
        const ext::shared_ptr<Fdm1dMesher>& m2,
        const ext::shared_ptr<Fdm1dMesher>& m3);
    FdmMesherComposite(
        const ext::shared_ptr<Fdm1dMesher>& m1,
        const ext::shared_ptr<Fdm1dMesher>& m2,
        const ext::shared_ptr<Fdm1dMesher>& m3,
        const ext::shared_ptr<Fdm1dMesher>& m4);

    const std::vector<ext::shared_ptr<Fdm1dMesher>>& getFdm1dMeshers() const;
};

class FdmMesherIntegral {
  public:
    %extend {
        FdmMesherIntegral(
            const ext::shared_ptr<FdmMesherComposite>& mesher,
            const DiscreteTrapezoidIntegral& integrator1d) {
                const ext::function<Real(const Array&, const Array&)> integrator = integrator1d;
                return new FdmMesherIntegral(
                    ext::shared_ptr<FdmMesherComposite>(
                        new FdmMesherComposite(mesher->getFdm1dMeshers())),
                    integrator);
            }
        FdmMesherIntegral(
            const ext::shared_ptr<FdmMesherComposite>& mesher,
            const DiscreteSimpsonIntegral& integrator1d) {
                const ext::function<Real(const Array&, const Array&)> integrator = integrator1d;
                return new FdmMesherIntegral(
                    ext::shared_ptr<FdmMesherComposite>(
                        new FdmMesherComposite(mesher->getFdm1dMeshers())),
                    integrator);
            }
    }
    Real integrate(const Array& f) const;
};

%{
class SafeFdmMesherIntegral {
  public:
    SafeFdmMesherIntegral(
        const ext::shared_ptr<FdmMesherComposite>& mesher,
        const DiscreteTrapezoidIntegral& integrator1d) :
        integrator_(integrator1d) {
            fdmMesherIntegral_ = ext::shared_ptr<FdmMesherIntegral>(
                new FdmMesherIntegral(
                    ext::shared_ptr<FdmMesherComposite>(
                        new FdmMesherComposite(mesher->getFdm1dMeshers())),
                    integrator_));
        }
    SafeFdmMesherIntegral(
        const ext::shared_ptr<FdmMesherComposite>& mesher,
        const DiscreteSimpsonIntegral& integrator1d) :
        integrator_(integrator1d) {
            fdmMesherIntegral_ = ext::shared_ptr<FdmMesherIntegral>(
                new FdmMesherIntegral(
                    ext::shared_ptr<FdmMesherComposite>(
                        new FdmMesherComposite(mesher->getFdm1dMeshers())),
                    integrator_));
        }
    Real integrate(const Array& f) const {
        return fdmMesherIntegral_->integrate(f);
    }
  private:
    ext::function<Real(const Array&, const Array&)> integrator_;
    ext::shared_ptr<FdmMesherIntegral> fdmMesherIntegral_;
};
%}

class SafeFdmMesherIntegral {
  public:
    SafeFdmMesherIntegral(
        const ext::shared_ptr<FdmMesherComposite>& mesher,
        const DiscreteTrapezoidIntegral& integrator1d);
    SafeFdmMesherIntegral(
        const ext::shared_ptr<FdmMesherComposite>& mesher,
        const DiscreteSimpsonIntegral& integrator1d);
    Real integrate(const Array& f) const;
};

#endif
