#ifndef ql_models_utilities_i
#define ql_models_utilities_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i

%include ../ql/models/evolvers.i
%include ../ql/models/multiproducts.i
%include ../ql/models/dataprovider.i
%include ../ql/models/dataprovider.i

%{
using QuantLib::checkIncreasingTimes;
using QuantLib::checkIncreasingTimesAndCalculateTaus;
using QuantLib::collectNodeData;
using QuantLib::genericLongstaffSchwartzRegression;
%}

%inline {
    void mergeTimes(
        const std::vector<std::vector<Time>>& times,
        std::vector<Time>& mergedTimes,
        std::vector<std::vector<bool>>& isPresent) {
            std::vector<std::valarray<bool>> p(isPresent.size());
            for (Size i = 0; i < p.size(); ++i) {
                p[i].resize(isPresent[i].size());
                std::copy(isPresent[i].begin(), isPresent[i].end(), std::begin(p[i]));
            }

            QuantLib::mergeTimes(times, mergedTimes, p);
            isPresent.resize(p.size());
            for (Size i = 0; i < isPresent.size(); ++i) {
                isPresent[i].resize(p[i].size());
                std::copy(std::begin(p[i]), std::end(p[i]), isPresent[i].begin());
            }
        }

    std::vector<bool> isInSubset(
        const std::vector<Time>& set,
        const std::vector<Time>& subset) {
            std::valarray<bool> s = QuantLib::isInSubset(set, subset);
            std::vector<bool> rst(s.size());
            std::copy(std::begin(s), std::end(s), rst.begin());
            return rst;
        }
}

void checkIncreasingTimes(const std::vector<Time>& times);

void checkIncreasingTimesAndCalculateTaus(
    const std::vector<Time>& times, std::vector<Time>& taus);

void collectNodeData(
    MarketModelEvolver& evolver,
    MarketModelMultiProduct& product,
    MarketModelNodeDataProvider& dataProvider,
    MarketModelExerciseValue& rebate,
    MarketModelExerciseValue& control,
    Size numberOfPaths,
    std::vector<std::vector<NodeData>>& collectedData);

Real genericLongstaffSchwartzRegression(
    std::vector<std::vector<NodeData>>& simulationData,
    std::vector<std::vector<Real>>& basisCoefficients);

#endif
