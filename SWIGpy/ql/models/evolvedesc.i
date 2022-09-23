#ifndef ql_models_evolvedesc_i
#define ql_models_evolvedesc_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i

%{
using QuantLib::EvolutionDescription;
using QuantLib::checkCompatibility;
using QuantLib::isInTerminalMeasure;
using QuantLib::isInMoneyMarketPlusMeasure;
using QuantLib::isInMoneyMarketMeasure;
using QuantLib::terminalMeasure;
using QuantLib::moneyMarketPlusMeasure;
using QuantLib::moneyMarketMeasure;
%}

class EvolutionDescription {
    typedef std::pair<Size,Size> range;
  public:
    EvolutionDescription();
    EvolutionDescription(
        const std::vector<Time>& rateTimes,
        const std::vector<Time>& evolutionTimes = std::vector<Time>(),
        const std::vector<std::pair<Size,Size>>& relevanceRates = std::vector<range>());
    const std::vector<Time>& rateTimes() const;
    const std::vector<Time>& rateTaus() const;
    const std::vector<Time>& evolutionTimes() const;
    const std::vector<Size>& firstAliveRate() const;
    const std::vector<std::pair<Size,Size>>& relevanceRates() const;
    Size numberOfRates() const;
    Size numberOfSteps() const;
};

void checkCompatibility(
    const EvolutionDescription& evolution, 
    const std::vector<Size>& numeraires);
bool isInTerminalMeasure(
    const EvolutionDescription& evolution, 
    const std::vector<Size>& numeraires);
bool isInMoneyMarketPlusMeasure(
    const EvolutionDescription& evolution,
    const std::vector<Size>& numeraires,
    Size offset = 1);
bool isInMoneyMarketMeasure(
    const EvolutionDescription& evolution, 
    const std::vector<Size>& numeraires);
std::vector<Size> terminalMeasure(
    const EvolutionDescription& evolution);
std::vector<Size> moneyMarketPlusMeasure(
    const EvolutionDescription&, 
    Size offset = 1);
std::vector<Size> moneyMarketMeasure(
    const EvolutionDescription&);

#endif
