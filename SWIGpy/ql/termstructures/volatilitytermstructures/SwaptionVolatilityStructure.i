#ifndef ql_termstructures_volatilitytermstructures_SwaptionVolatilityStructure_i
#define ql_termstructures_volatilitytermstructures_SwaptionVolatilityStructure_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/termstructures/VolatilityTermStructure.i

%{
using QuantLib::SwaptionVolatilityStructure;
%}

%shared_ptr(SwaptionVolatilityStructure)
class SwaptionVolatilityStructure : public VolatilityTermStructure {
  private:
    SwaptionVolatilityStructure();

  public:
    Volatility volatility(const Period& optionTenor,
                          const Period& swapTenor,
                          Rate strike,
                          bool extrapolate = false) const;
    Volatility volatility(const Date& optionDate,
                          const Period& swapTenor,
                          Rate strike,
                          bool extrapolate = false) const;
    Volatility volatility(Time optionTime,
                          const Period& swapTenor,
                          Rate strike,
                          bool extrapolate = false) const;
    Volatility volatility(const Period& optionTenor,
                          Time swapLength,
                          Rate strike,
                          bool extrapolate = false) const;
    Volatility volatility(const Date& optionDate,
                          Time swapLength,
                          Rate strike,
                          bool extrapolate = false) const;
    Volatility volatility(Time optionTime,
                          Time swapLength,
                          Rate strike,
                          bool extrapolate = false) const;
    Real blackVariance(const Period& optionTenor,
                       const Period& swapTenor,
                       Rate strike,
                       bool extrapolate = false) const;
    Real blackVariance(const Date& optionDate,
                       const Period& swapTenor,
                       Rate strike,
                       bool extrapolate = false) const;
    Real blackVariance(Time optionTime,
                       const Period& swapTenor,
                       Rate strike,
                       bool extrapolate = false) const;
    Real blackVariance(const Period& optionTenor,
                       Time swapLength,
                       Rate strike,
                       bool extrapolate = false) const;
    Real blackVariance(const Date& optionDate,
                       Time swapLength,
                       Rate strike,
                       bool extrapolate = false) const;
    Real blackVariance(Time optionTime,
                       Time swapLength,
                       Rate strike,
                       bool extrapolate = false) const;
    Real shift(const Period& optionTenor,
               const Period& swapTenor,
               bool extrapolate = false) const;
    Real shift(const Date& optionDate,
               const Period& swapTenor,
               bool extrapolate = false) const;
    Real shift(Time optionTime,
               const Period& swapTenor,
               bool extrapolate = false) const;
    Real shift(const Period& optionTenor,
               Time swapLength,
               bool extrapolate = false) const;
    Real shift(const Date& optionDate,
               Time swapLength,
               bool extrapolate = false) const;
    Real shift(Time optionTime,
               Time swapLength,
               bool extrapolate = false) const;
    ext::shared_ptr<SmileSection> smileSection(const Period& optionTenor,
                                               const Period& swapTenor,
                                               bool extr = false) const;
    ext::shared_ptr<SmileSection> smileSection(const Date& optionDate,
                                               const Period& swapTenor,
                                               bool extr = false) const;
    ext::shared_ptr<SmileSection> smileSection(Time optionTime,
                                               const Period& swapTenor,
                                               bool extr = false) const;
    ext::shared_ptr<SmileSection> smileSection(const Period& optionTenor,
                                               Time swapLength,
                                               bool extr = false) const;
    ext::shared_ptr<SmileSection> smileSection(const Date& optionDate,
                                               Time swapLength,
                                               bool extr = false) const;
    ext::shared_ptr<SmileSection> smileSection(Time optionTime,
                                               Time swapLength,
                                               bool extr = false) const;
    const Period& maxSwapTenor() const;
    Time maxSwapLength() const;
    VolatilityType volatilityType() const;
    Time swapLength(const Period& swapTenor) const;
    Time swapLength(const Date& start,
                    const Date& end) const;
};

%template(SwaptionVolatilityStructureHandle) Handle<SwaptionVolatilityStructure>;
%template(RelinkableSwaptionVolatilityStructureHandle) RelinkableHandle<SwaptionVolatilityStructure>;


#endif
