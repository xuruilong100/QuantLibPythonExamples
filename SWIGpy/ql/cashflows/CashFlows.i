#ifndef ql_cashflows_CashFlows_i
#define ql_cashflows_CashFlows_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i

%{
using QuantLib::CashFlows;
%}

class CashFlows {
    %rename("yieldRate") yield;
  private:
    CashFlows();
  public:
    static Date startDate(const Leg&);
    static Date maturityDate(const Leg&);
    static bool isExpired(
        const Leg& leg,
        bool includeSettlementDateFlows,
        Date settlementDate = Date());
    %extend {
        static ext::shared_ptr<CashFlow> previousCashFlow(
            const Leg& leg,
            bool includeSettlementDateFlows,
            Date settlementDate = Date()) {
            Leg::const_reverse_iterator i = QuantLib::CashFlows::previousCashFlow(
                leg, includeSettlementDateFlows, settlementDate);

            if (i == leg.rend())
                return ext::shared_ptr<CashFlow>();
            else
                return *i;
        }
        static ext::shared_ptr<CashFlow> nextCashFlow(
            const Leg& leg,
            bool includeSettlementDateFlows,
            Date settlementDate = Date()) {
            Leg::const_iterator i = QuantLib::CashFlows::nextCashFlow(
                leg, includeSettlementDateFlows, settlementDate);

            if (i == leg.end())
                return ext::shared_ptr<CashFlow>();
            else
                return *i;
        }
    }

    static Date previousCashFlowDate(
        const Leg& leg,
        bool includeSettlementDateFlows,
        Date settlementDate = Date());
    static Date nextCashFlowDate(
        const Leg& leg,
        bool includeSettlementDateFlows,
        Date settlementDate = Date());
    static Real previousCashFlowAmount(
        const Leg& leg,
        bool includeSettlementDateFlows, Date settlementDate = Date());
    static Real nextCashFlowAmount(
        const Leg& leg,
        bool includeSettlementDateFlows, Date settlementDate = Date());
    static Rate previousCouponRate(
        const Leg& leg,
        bool includeSettlementDateFlows,
        Date settlementDate = Date());
    static Rate nextCouponRate(
        const Leg& leg,
        bool includeSettlementDateFlows,
        Date settlementDate = Date());
    static Real nominal(
        const Leg& leg,
        bool includeSettlementDateFlows,
        Date settlDate = Date());
    static Date accrualStartDate(
        const Leg& leg,
        bool includeSettlementDateFlows,
        Date settlDate = Date());
    static Date accrualEndDate(
        const Leg& leg,
        bool includeSettlementDateFlows,
        Date settlementDate = Date());
    static Date referencePeriodStart(
        const Leg& leg,
        bool includeSettlementDateFlows,
        Date settlDate = Date());
    static Date referencePeriodEnd(
        const Leg& leg,
        bool includeSettlementDateFlows,
        Date settlDate = Date());
    static Time accrualPeriod(
        const Leg& leg,
        bool includeSettlementDateFlows,
        Date settlementDate = Date());
    static BigInteger accrualDays(
        const Leg& leg,
        bool includeSettlementDateFlows,
        Date settlementDate = Date());
    static BigInteger accruedDays(
        const Leg& leg,
        bool includeSettlementDateFlows,
        Date settlementDate = Date());
    static Time accruedPeriod(
        const Leg& leg,
        bool includeSettlementDateFlows,
        Date settlementDate = Date());
    static Real accruedAmount(
        const Leg& leg,
        bool includeSettlementDateFlows,
        Date settlementDate = Date());
    static Real npv(
        const Leg& leg,
        const YieldTermStructure& discountCurve,
        bool includeSettlementDateFlows,
        Date settlementDate = Date(),
        Date npvDate = Date());
    static Real bps(
        const Leg& leg,
        const YieldTermStructure& discountCurve,
        bool includeSettlementDateFlows,
        Date settlementDate = Date(),
        Date npvDate = Date());
 	static void npvbps(
        const Leg& leg,
        const YieldTermStructure& discountCurve,
        bool includeSettlementDateFlows,
        Date settlementDate,
        Date npvDate,
        Real& npv,
        Real& bps);
 	static Rate atmRate(
        const Leg& leg,
        const YieldTermStructure& discountCurve,
        bool includeSettlementDateFlows,
        Date settlementDate = Date(),
        Date npvDate = Date(),
        Real npv=Null<Real>());
    static Real npv(
        const Leg& leg,
        const InterestRate& yield,
        bool includeSettlementDateFlows,
        Date settlementDate = Date(),
        Date npvDate = Date());
 	static Real npv(
        const Leg& leg,
        Rate yield,
        const DayCounter& dayCounter,
        Compounding compounding,
        Frequency frequency,
        bool includeSettlementDateFlows,
        Date settlementDate = Date(),
        Date npvDate = Date());
    static Real bps(
        const Leg& leg,
        const InterestRate& yield,
        bool includeSettlementDateFlows,
        Date settlementDate = Date(),
        Date npvDate = Date());
 	static Real bps(
        const Leg& leg,
        Rate yield,
        const DayCounter& dayCounter,
        Compounding compounding,
        Frequency frequency,
        bool includeSettlementDateFlows,
        Date settlementDate = Date(),
        Date npvDate = Date());
    static Rate yield(
        const Leg& leg,
        Real npv,
        const DayCounter& dayCounter,
        Compounding compounding,
        Frequency frequency,
        bool includeSettlementDateFlows,
        Date settlementDate = Date(),
        Date npvDate = Date(),
        Real accuracy = 1.0e-10,
        Size maxIterations = 100,
        Rate guess = 0.05);
    static Time duration(
        const Leg& leg,
        const InterestRate& yield,
        Duration::Type type,
        bool includeSettlementDateFlows,
        Date settlementDate = Date(),
        Date npvDate = Date());
 	static Time duration(
        const Leg& leg,
        Rate yield,
        const DayCounter& dayCounter,
        Compounding compounding,
        Frequency frequency,
        Duration::Type type,
        bool includeSettlementDateFlows,
        Date settlementDate = Date(),
        Date npvDate = Date());
    static Real convexity(
        const Leg& leg,
        const InterestRate& yield,
        bool includeSettlementDateFlows,
        Date settlementDate = Date(),
        Date npvDate = Date());
 	static Real convexity(
        const Leg& leg,
        Rate yield,
        const DayCounter& dayCounter,
        Compounding compounding,
        Frequency frequency,
        bool includeSettlementDateFlows,
        Date settlementDate = Date(),
        Date npvDate = Date());
    static Real basisPointValue(
        const Leg& leg,
        const InterestRate& yield,
        bool includeSettlementDateFlows,
        Date settlementDate = Date(),
        Date npvDate = Date());
 	static Real basisPointValue(
        const Leg& leg,
        Rate yield,
        const DayCounter& dayCounter,
        Compounding compounding,
        Frequency frequency,
        bool includeSettlementDateFlows,
        Date settlementDate = Date(),
        Date npvDate = Date());
    static Real yieldValueBasisPoint(
        const Leg& leg,
        const InterestRate& yield,
        bool includeSettlementDateFlows,
        Date settlementDate = Date(),
        Date npvDate = Date());
 	static Real yieldValueBasisPoint(
        const Leg& leg,
        Rate yield,
        const DayCounter& dayCounter,
        Compounding compounding,
        Frequency frequency,
        bool includeSettlementDateFlows,
        Date settlementDate = Date(),
        Date npvDate = Date());
    static Real npv(
        const Leg& leg,
        const ext::shared_ptr<YieldTermStructure>& discount,
        Spread zSpread,
        const DayCounter& dayCounter,
        Compounding compounding,
        Frequency frequency,
        bool includeSettlementDateFlows,
        Date settlementDate = Date(),
        Date npvDate = Date());
 	static Spread zSpread(
        const Leg& leg,
        Real npv,
        const ext::shared_ptr<YieldTermStructure>& ,
        const DayCounter& dayCounter,
        Compounding compounding,
        Frequency frequency,
        bool includeSettlementDateFlows,
        Date settlementDate = Date(),
        Date npvDate = Date(),
        Real accuracy = 1.0e-10,
        Size maxIterations = 100,
        Rate guess = 0.0);
 	static Spread zSpread(
        const Leg& leg,
        const ext::shared_ptr<YieldTermStructure>& d,
        Real npv,
        const DayCounter& dayCounter,
        Compounding compounding,
        Frequency frequency,
        bool includeSettlementDateFlows,
        Date settlementDate = Date(),
        Date npvDate = Date(),
        Real accuracy = 1.0e-10,
        Size maxIterations = 100,
        Rate guess = 0.0);
};


#endif
