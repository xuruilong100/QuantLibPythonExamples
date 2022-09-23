#ifndef ql_legacy_lmmodels_i
#define ql_legacy_lmmodels_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i

%{
using QuantLib::LmCorrelationModel;
using QuantLib::LmExponentialCorrelationModel;
using QuantLib::LmLinearExponentialCorrelationModel;
using QuantLib::LmVolatilityModel;
using QuantLib::LmFixedVolatilityModel;
using QuantLib::LmLinearExponentialVolatilityModel;
using QuantLib::LmExtLinearExponentialVolModel;
using QuantLib::LiborForwardModel;
using QuantLib::LfmCovarianceParameterization;
using QuantLib::LfmCovarianceProxy;
using QuantLib::LfmHullWhiteParameterization;
%}

%shared_ptr(LmCorrelationModel)
class LmCorrelationModel {
  private:
    LmCorrelationModel();
  public:
    Size size() const;
    Size factors() const;
    std::vector<Parameter>& params();
    void setParams(const std::vector<Parameter>& arguments);
    Matrix correlation(
        Time t, const Array& x = Null<Array>()) const;
    Matrix pseudoSqrt(
        Time t, const Array& x = Null<Array>()) const;
    Real correlation(
        Size i, Size j, Time t, const Array& x = Null<Array>()) const;
    bool isTimeIndependent() const;
};

%shared_ptr(LmExponentialCorrelationModel)
class LmExponentialCorrelationModel : public LmCorrelationModel {
  public:
    LmExponentialCorrelationModel(
        Size size, 
        Real rho);
};

%shared_ptr(LmLinearExponentialCorrelationModel)
class LmLinearExponentialCorrelationModel : public LmCorrelationModel {
  public:
    LmLinearExponentialCorrelationModel(
        Size size, 
        Real rho, 
        Real beta,
        Size factors = Null<Size>());
};

%shared_ptr(LmVolatilityModel)
class LmVolatilityModel {
  private:
    LmVolatilityModel();
  public:
    Size size() const;
    std::vector<Parameter>& params();
    void setParams(const std::vector<Parameter>& arguments);
    Array volatility(
         Time t, const Array& x = Null<Array>()) const;
    Volatility volatility(
         Size i, Time t, const Array& x = Null<Array>()) const;
    Real integratedVariance(
        Size i, Size j, Time u,
        const Array& x = Null<Array>()) const;
};

%shared_ptr(LmFixedVolatilityModel)
class LmFixedVolatilityModel : public LmVolatilityModel {
  public:
    LmFixedVolatilityModel(
        Array volatilities, 
        const std::vector<Time>& startTimes);
};

%shared_ptr(LmLinearExponentialVolatilityModel)
class LmLinearExponentialVolatilityModel : public LmVolatilityModel {
  public:
    LmLinearExponentialVolatilityModel(
        const std::vector<Time>& fixingTimes,
        Real a, 
        Real b, 
        Real c, 
        Real d);
};

%shared_ptr(LmExtLinearExponentialVolModel)
class LmExtLinearExponentialVolModel : public LmLinearExponentialVolatilityModel {
  public:
    LmExtLinearExponentialVolModel(
        const std::vector<Time>& fixingTimes,
        Real a, 
        Real b, 
        Real c, 
        Real d);
};

%shared_ptr(LiborForwardModel)
class LiborForwardModel : public CalibratedModel, public AffineModel {
  public:
    LiborForwardModel(
        const ext::shared_ptr<LiborForwardModelProcess>& process,
        const ext::shared_ptr<LmVolatilityModel>& volaModel,
        const ext::shared_ptr<LmCorrelationModel>& corrModel);

    Rate S_0(Size alpha, Size beta) const;
    ext::shared_ptr<SwaptionVolatilityMatrix>
        getSwaptionVolatilityMatrix() const;
};

%shared_ptr(LfmCovarianceParameterization)
class LfmCovarianceParameterization {
  private:
    LfmCovarianceParameterization();
  public:
    Size size() const;
    Size factors() const;
    Matrix diffusion(
        Time t, const Array& x = Null<Array>()) const;
    Matrix covariance(
        Time t, const Array& x = Null<Array>()) const;
    Matrix integratedCovariance(
        Time t, const Array& x = Null<Array>()) const;
};

%shared_ptr(LfmCovarianceProxy)
class LfmCovarianceProxy : public LfmCovarianceParameterization {
  public:
    LfmCovarianceProxy(
        ext::shared_ptr<LmVolatilityModel> volaModel,
        const ext::shared_ptr<LmCorrelationModel>& corrModel);

    ext::shared_ptr<LmVolatilityModel>  volatilityModel() const;
    ext::shared_ptr<LmCorrelationModel> correlationModel() const;

    Real integratedCovariance(
        Size i, Size j, Time t, const Array& x = Null<Array>()) const;
};

%shared_ptr(LfmHullWhiteParameterization)
class LfmHullWhiteParameterization : public LfmCovarianceParameterization {
  public:
    LfmHullWhiteParameterization(
        const ext::shared_ptr<LiborForwardModelProcess>& process,
        const ext::shared_ptr<OptionletVolatilityStructure>& capletVol,
        const Matrix& correlation = Matrix(), 
        Size factors = 1);
};

#endif
