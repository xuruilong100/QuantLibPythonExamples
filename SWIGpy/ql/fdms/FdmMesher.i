#ifndef ql_fdms_FdmMesher_i
#define ql_fdms_FdmMesher_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i

%{
using QuantLib::FdmMesher;
using QuantLib::FdmMesherComposite;
%}

%shared_ptr(FdmMesher)
class FdmMesher {
  private:
    FdmMesher();
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

    Real dplus(const FdmLinearOpIterator& iter, Size direction) const;
    Real dminus(const FdmLinearOpIterator& iter, Size direction) const;
    Real location(const FdmLinearOpIterator& iter, Size direction) const;
    %extend {
        Array locations(Size direction) const {
            return self->locations(direction);
        }

        ext::shared_ptr<FdmLinearOpLayout> layout() {
            const std::vector<ext::shared_ptr<Fdm1dMesher>>& meshers = self->getFdm1dMeshers();

            std::vector<Size> dim(meshers.size());

            for (Size i = 0; i < dim.size(); ++i)
                dim[i] = meshers[i]->size();

            return ext::make_shared<FdmLinearOpLayout>(dim);
        }
    }

    const std::vector<ext::shared_ptr<Fdm1dMesher>>& getFdm1dMeshers() const;
};

#endif
