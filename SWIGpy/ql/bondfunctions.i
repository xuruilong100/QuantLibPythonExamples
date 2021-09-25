#ifndef ql_bond_functions_i
#define ql_bond_functions_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i

%{
using QuantLib::BondFunctions;
%}

struct BondFunctions {
    %rename(bondYield) yield;
    static Date startDate(const Bond& bond);
    static Date maturityDate(const Bond& bond);
    static bool isTradable(const Bond& bond,
                           Date settlementDate = Date());

    static Date previousCashFlowDate(const Bond& bond,
                                     Date refDate = Date());
    static Date nextCashFlowDate(const Bond& bond,
                                 Date refDate = Date());
    static Real previousCashFlowAmount(const Bond& bond,
                                       Date refDate = Date());
    static Real nextCashFlowAmount(const Bond& bond,
                                   Date refDate = Date());

    static Rate previousCouponRate(const Bond& bond,
                                   Date settlementDate = Date());
    static Rate nextCouponRate(const Bond& bond,
                               Date settlementDate = Date());
    static Date accrualStartDate(const Bond& bond,
                                 Date settlementDate = Date());
    static Date accrualEndDate(const Bond& bond,
                               Date settlementDate = Date());
    static Date referencePeriodStart(const Bond& bond,
                                     Date settlementDate = Date());
    static Date referencePeriodEnd(const Bond& bond,
                                   Date settlementDate = Date());
    static Time accrualPeriod(const Bond& bond,
                              Date settlementDate = Date());
    static BigInteger accrualDays(const Bond& bond,
                                  Date settlementDate = Date());
    static Time accruedPeriod(const Bond& bond,
                              Date settlementDate = Date());
    static BigInteger accruedDays(const Bond& bond,
                                  Date settlementDate = Date());
    static Real accruedAmount(const Bond& bond,
                              Date settlementDate = Date());

    static Real cleanPrice(const Bond& bond,
                           const YieldTermStructure& discountCurve,
                           Date settlementDate = Date());
    static Real bps(const Bond& bond,
                    const YieldTermStructure& discountCurve,
                    Date settlementDate = Date());
    static Rate atmRate(const Bond& bond,
                        const YieldTermStructure& discountCurve,
                        Date settlementDate = Date(),
                        Real cleanPrice = Null<Real>());

    static Real cleanPrice(const Bond& bond,
                           const InterestRate& yield,
                           Date settlementDate = Date());
    static Real cleanPrice(const Bond& bond,
                           Rate yield,
                           const DayCounter& dayCounter,
                           Compounding compounding,
                           Frequency frequency,
                           Date settlementDate = Date());
    static Real dirtyPrice(const Bond& bond,
                           const InterestRate& yield,
                           Date settlementDate = Date());
    static Real dirtyPrice(const Bond& bond,
                           Rate yield,
                           const DayCounter& dayCounter,
                           Compounding compounding,
                           Frequency frequency,
                           Date settlementDate = Date());
    static Real bps(const Bond& bond,
                    const InterestRate& yield,
                    Date settlementDate = Date());
    static Real bps(const Bond& bond,
                    Rate yield,
                    const DayCounter& dayCounter,
                    Compounding compounding,
                    Frequency frequency,
                    Date settlementDate = Date());
    static Rate yield(const Bond& bond,
                      Real price,
                      const DayCounter& dayCounter,
                      Compounding compounding,
                      Frequency frequency,
                      Date settlementDate = Date(),
                      Real accuracy = 1.0e-10,
                      Size maxIterations = 100,
                      Rate guess = 0.05,
                      Bond::Price::Type priceType = Bond::Price::Clean);

    %extend {
        %define DefineYieldFunctionSolver(SolverType)
        static Rate yield ## SolverType(SolverType solver,
                                        const Bond& bond,
                                        Real cleanPrice,
                                        const DayCounter& dayCounter,
                                        Compounding compounding,
                                        Frequency frequency,
                                        Date settlementDate = Date(),
                                        Real accuracy = 1.0e-10,
                                        Rate guess = 0.05,
                                        Bond::Price::Type priceType = Bond::Price::Clean) {
            return BondFunctions::yield<SolverType>(
                        solver, bond, cleanPrice, dayCounter, compounding,
                        frequency, settlementDate, accuracy, guess);
        }
        %enddef

        // See solvers.i for solver definitions.
        DefineYieldFunctionSolver(Brent);
        DefineYieldFunctionSolver(Bisection);
        DefineYieldFunctionSolver(FalsePosition);
        DefineYieldFunctionSolver(Ridder);
        DefineYieldFunctionSolver(Secant);
        DefineYieldFunctionSolver(Newton);
        DefineYieldFunctionSolver(NewtonSafe);
        DefineYieldFunctionSolver(FiniteDifferenceNewtonSafe);
    }

    static Time duration(const Bond& bond,
                         const InterestRate& yield,
                         Duration::Type type = Duration::Modified,
                         Date settlementDate = Date() );
    static Time duration(const Bond& bond,
                         Rate yield,
                         const DayCounter& dayCounter,
                         Compounding compounding,
                         Frequency frequency,
                         Duration::Type type = Duration::Modified,
                         Date settlementDate = Date() );
    static Real convexity(const Bond& bond,
                          const InterestRate& yield,
                          Date settlementDate = Date());
    static Real convexity(const Bond& bond,
                          Rate yield,
                          const DayCounter& dayCounter,
                          Compounding compounding,
                          Frequency frequency,
                          Date settlementDate = Date());
    static Real basisPointValue(const Bond& bond,
                                const InterestRate& yield,
                                Date settlementDate = Date());
    static Real basisPointValue(const Bond& bond,
                                Rate yield,
                                const DayCounter& dayCounter,
                                Compounding compounding,
                                Frequency frequency,
                                Date settlementDate = Date());
    static Real yieldValueBasisPoint(const Bond& bond,
                                     const InterestRate& yield,
                                     Date settlementDate = Date());
    static Real yieldValueBasisPoint(const Bond& bond,
                                     Rate yield,
                                     const DayCounter& dayCounter,
                                     Compounding compounding,
                                     Frequency frequency,
                                     Date settlementDate = Date());
    static Real cleanPrice(const Bond& bond,
                           const ext::shared_ptr<YieldTermStructure>& discount,
                           Spread zSpread,
                           const DayCounter& dayCounter,
                           Compounding compounding,
                           Frequency frequency,
                           Date settlementDate = Date());
    static Spread zSpread(const Bond& bond,
                          Real cleanPrice,
                          const ext::shared_ptr<YieldTermStructure>&,
                          const DayCounter& dayCounter,
                          Compounding compounding,
                          Frequency frequency,
                          Date settlementDate = Date(),
                          Real accuracy = 1.0e-10,
                          Size maxIterations = 100,
                          Rate guess = 0.0);
};

#endif
