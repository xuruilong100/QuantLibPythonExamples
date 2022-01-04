#ifndef ql_interpolation_SafeInterpolation2D_i
#define ql_interpolation_SafeInterpolation2D_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/interpolation/Interpolation2D.i

%{
class SafeInterpolation2D : public Interpolation2D {
  public:
    SafeInterpolation2D(
        const Array& x, const Array& y,
        const Matrix& z) : x_(x), y_(y), z_(z) {}
    ~SafeInterpolation2D() override = default;

    void enableExtrapolation(bool b = true) {
        i_->enableExtrapolation(b);
    }
    void disableExtrapolation(bool b = true) {
        i_->disableExtrapolation(b);
    }
    bool allowsExtrapolation() const {
        return i_->allowsExtrapolation();
    }

    Real xMin() const {return i_->xMin();}
    Real xMax() const {return i_->xMax();}
    std::vector<Real> xValues() const {return i_->xValues();}
    Size locateX(Real x) const {return i_->locateX(x);}
    Real yMin() const {return i_->yMin();}
    Real yMax() const {return i_->yMax();}
    std::vector<Real> yValues() const {return i_->yValues();}
    Size locateY(Real y) const {return i_->locateY(y);}
    const Matrix& zData() const {return i_->zData();}
    bool isInRange(Real x, Real y) const {return i_->isInRange(x, y);}
    void update() {i_->update();}
    Real operator()(
        Real x, Real y,
        bool allowExtrapolation = false) const {
        return (*i_)(x, y, allowExtrapolation);
    }
  protected:
    ext::shared_ptr<Interpolation2D> i_;
    Array x_, y_;
    Matrix z_;
};
%}

%shared_ptr(SafeInterpolation2D)
class SafeInterpolation2D : public Interpolation2D {
  private:
    SafeInterpolation2D();
  public:
    void enableExtrapolation(bool b = true);
    void disableExtrapolation(bool b = true);
    bool allowsExtrapolation() const;

    Real xMin() const;
    Real xMax() const;
    std::vector<Real> xValues() const;
    Size locateX(Real x) const;
    Real yMin() const;
    Real yMax() const;
    std::vector<Real> yValues() const;
    Size locateY(Real y) const;
    const Matrix& zData() const;
    bool isInRange(Real x, Real y) const;
    void update();
    Real operator()(
        Real x, Real y,
        bool allowExtrapolation = false) const;
};

#endif
