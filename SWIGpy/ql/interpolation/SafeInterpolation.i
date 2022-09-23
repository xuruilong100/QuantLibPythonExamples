#ifndef ql_interpolation_SafeInterpolation_i
#define ql_interpolation_SafeInterpolation_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/interpolation/Interpolation.i

%{
class SafeInterpolation : public Interpolation {
  public:
    SafeInterpolation(
        const Array& x, 
        const Array& y) : x_(x), y_(y) {}
    ~SafeInterpolation() override = default;

    void enableExtrapolation(bool b = true) {
        i_->enableExtrapolation(b);
    }
    void disableExtrapolation(bool b = true) {
        i_->disableExtrapolation(b);
    }
    bool allowsExtrapolation() const {
        return i_->allowsExtrapolation();
    }

    bool empty() const { return i_->empty(); }
    Real operator()(Real x, bool allowExtrapolation = false) const {
        return (*i_)(x, allowExtrapolation);
    }
    Real primitive(Real x, bool allowExtrapolation = false) const {
        return i_->primitive(x, allowExtrapolation);
    }
    Real derivative(Real x, bool allowExtrapolation = false) const {
        return i_->derivative(x, allowExtrapolation);
    }
    Real secondDerivative(Real x, bool allowExtrapolation = false) const {
        return i_->secondDerivative(x, allowExtrapolation);
    }
    Real xMin() const {
        return i_->xMin();
    }
    Real xMax() const {
        return i_->xMax();
    }
    bool isInRange(Real x) const {
        return i_->isInRange(x);
    }
    void update() {
        i_->update();
    }
  protected:
    ext::shared_ptr<Interpolation> i_;
    Array x_, y_;
};
%}

%shared_ptr(SafeInterpolation)
class SafeInterpolation : public Interpolation {
  private:
    SafeInterpolation();
  public:
    void enableExtrapolation(bool b = true);
    void disableExtrapolation(bool b = true);
    bool allowsExtrapolation() const;

    bool empty() const;
    Real primitive(Real x, bool allowExtrapolation = false) const;
    Real derivative(Real x, bool allowExtrapolation = false) const;
    Real secondDerivative(Real x, bool allowExtrapolation = false) const;
    Real xMin() const;
    Real xMax() const;
    bool isInRange(Real x) const;
    void update();
    Real operator()(
        Real x,
        bool allowExtrapolation = false) const;
};

#endif
