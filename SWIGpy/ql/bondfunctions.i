#ifndef ql_bond_functions_i
#define ql_bond_functions_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i

%{
using QuantLib::BondFunctions;
%}

class BondFunctions {
    %rename(bondYield) yield;
  public:
    static Date startDate(const Bond& bond);
    static Date maturityDate(const Bond& bond);
    static bool isTradable(
        const Bond& bond,
        Date settlementDate = Date());
    static Date previousCashFlowDate(
        const Bond& bond,
        Date refDate = Date());
    static Date nextCashFlowDate(
        const Bond& bond,
        Date refDate = Date());
    static Real previousCashFlowAmount(
        const Bond& bond,
        Date refDate = Date());
    static Real nextCashFlowAmount(
        const Bond& bond,
        Date refDate = Date());
    static Rate previousCouponRate(
        const Bond& bond,
        Date settlementDate = Date());
    static Rate nextCouponRate(
        const Bond& bond,
        Date settlementDate = Date());
    static Date accrualStartDate(
        const Bond& bond,
        Date settlementDate = Date());
    static Date accrualEndDate(
        const Bond& bond,
        Date settlementDate = Date());
    static Time accrualPeriod(
        const Bond& bond,
        Date settlementDate = Date());
    static BigInteger accrualDays(
        const Bond& bond,
        Date settlementDate = Date());
    static Time accruedPeriod(
        const Bond& bond,
        Date settlementDate = Date());
    static BigInteger accruedDays(
        const Bond& bond,
        Date settlementDate = Date());
    static Real accruedAmount(
        const Bond& bond,
        Date settlementDate = Date());

    static Real cleanPrice(
        const Bond& bond,
        const YieldTermStructure& discountCurve,
        Date settlementDate = Date());
    static Real bps(
        const Bond& bond,
        const YieldTermStructure& discountCurve,
        Date settlementDate = Date());
    static Rate atmRate(
        const Bond& bond,
        const YieldTermStructure& discountCurve,
        Date settlementDate = Date(),
        Real cleanPrice = Null<Real>());
    static Real cleanPrice(
        const Bond& bond,
        const InterestRate& yield,
        Date settlementDate = Date());
    static Real cleanPrice(
        const Bond& bond,
        Rate yield,
        const DayCounter& dayCounter,
        Compounding compounding,
        Frequency frequency,
        Date settlementDate = Date());
    static Real bps(
        const Bond& bond,
        const InterestRate& yield,
        Date settlementDate = Date());
    static Real bps(
        const Bond& bond,
        Rate yield,
        const DayCounter& dayCounter,
        Compounding compounding,
        Frequency frequency,
        Date settlementDate = Date());
    static Rate yield(
        const Bond& bond,
        Real cleanPrice,
        const DayCounter& dayCounter,
        Compounding compounding,
        Frequency frequency,
        Date settlementDate = Date(),
        Real accuracy = 1.0e-10,
        Size maxIterations = 100,
        Rate guess = 0.05);

    static Time duration(
        const Bond& bond,
        const InterestRate& yield,
        Duration::Type type = Duration::Modified,
        Date settlementDate = Date());
    static Time duration(
        const Bond& bond,
        Rate yield,
        const DayCounter& dayCounter,
        Compounding compounding,
        Frequency frequency,
        Duration::Type type = Duration::Modified,
        Date settlementDate = Date());
    static Real convexity(
        const Bond& bond,
        const InterestRate& yield,
        Date settlementDate = Date());
    static Real convexity(
        const Bond& bond,
        Rate yield,
        const DayCounter& dayCounter,
        Compounding compounding,
        Frequency frequency,
        Date settlementDate = Date());
    static Real basisPointValue(
        const Bond& bond,
        const InterestRate& yield,
        Date settlementDate = Date());
    static Real basisPointValue(
        const Bond& bond,
        Rate yield,
        const DayCounter& dayCounter,
        Compounding compounding,
        Frequency frequency,
        Date settlementDate = Date());
    static Real yieldValueBasisPoint(
        const Bond& bond,
        const InterestRate& yield,
        Date settlementDate = Date());
    static Real yieldValueBasisPoint(
        const Bond& bond,
        Rate yield,
        const DayCounter& dayCounter,
        Compounding compounding,
        Frequency frequency,
        Date settlementDate = Date());
    static Spread zSpread(
        const Bond& bond,
        Real cleanPrice,
        const ext::shared_ptr<YieldTermStructure>& discountCurve,
        const DayCounter& dayCounter,
        Compounding compounding,
        Frequency frequency,
        Date settlementDate = Date(),
        Real accuracy = 1.0e-10,
        Size maxIterations = 100,
        Rate guess = 0.0);
    %extend {
        %define DefineYieldFunctionSolver(SolverType)
        static Rate yield ## SolverType(
            SolverType solver,
            const Bond& bond,
            Real cleanPrice,
            const DayCounter& dayCounter,
            Compounding compounding,
            Frequency frequency,
            Date settlementDate = Date(),
            Real accuracy = 1.0e-10,
            Rate guess = 0.05) {
            return QuantLib::BondFunctions::yield<SolverType>(
                solver,
                bond,
                cleanPrice,
                dayCounter,
                compounding,
                frequency,
                settlementDate,
                accuracy,
                guess);
        }
        %enddef

        // See optimizers.i for solver definitions.
        DefineYieldFunctionSolver(Bisection);
        DefineYieldFunctionSolver(Brent);
        DefineYieldFunctionSolver(FalsePosition);
        DefineYieldFunctionSolver(Newton);
        DefineYieldFunctionSolver(NewtonSafe);
        DefineYieldFunctionSolver(Ridder);
        DefineYieldFunctionSolver(Secant);
    }
};

#endif
