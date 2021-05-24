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
    CashFlows(const CashFlows&);

  public:
    static Date startDate(const Leg&);
    static Date maturityDate(const Leg&);
    static Date
    previousCashFlowDate(
        const Leg& leg,
        bool includeSettlementDateFlows,
        Date settlementDate = Date());
    static Date nextCashFlowDate(
        const Leg& leg,
        bool includeSettlementDateFlows,
        Date settlementDate = Date());

    static Real npv(
        const Leg&,
        const InterestRate&,
        bool includeSettlementDateFlows,
        Date settlementDate = Date(),
        Date npvDate = Date());

    static Real npv(
        const Leg&,
        Rate yield,
        const DayCounter& dayCounter,
        Compounding compounding,
        Frequency frequency,
        bool includeSettlementDateFlows,
        Date settlementDate = Date(),
        Date npvDate = Date());
    static Real bps(
        const Leg&,
        const InterestRate&,
        bool includeSettlementDateFlows,
        Date settlementDate = Date(),
        Date npvDate = Date());
    static Real bps(
        const Leg&,
        Rate yield,
        const DayCounter& dayCounter,
        Compounding compounding,
        Frequency frequency,
        bool includeSettlementDateFlows,
        Date settlementDate = Date(),
        Date npvDate = Date());
    static Rate yield(
        const Leg&,
        Real npv,
        const DayCounter& dayCounter,
        Compounding compounding,
        Frequency frequency,
        bool includeSettlementDateFlows,
        Date settlementDate = Date(),
        Date npvDate = Date(),
        Real accuracy = 1.0e-10,
        Size maxIterations = 10000,
        Rate guess = 0.05);
    static Time duration(
        const Leg&,
        const InterestRate&,
        Duration::Type type,
        bool includeSettlementDateFlows,
        Date settlementDate = Date());

    static Time duration(
        const Leg&,
        Rate yield,
        const DayCounter& dayCounter,
        Compounding compounding,
        Frequency frequency,
        Duration::Type type,
        bool includeSettlementDateFlows,
        Date settlementDate = Date(),
        Date npvDate = Date());

    static Real convexity(
        const Leg&,
        const InterestRate&,
        bool includeSettlementDateFlows,
        Date settlementDate = Date(),
        Date npvDate = Date());

    static Real convexity(
        const Leg&,
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

    static Spread zSpread(
        const Leg& leg,
        Real npv,
        const ext::shared_ptr<YieldTermStructure>&,
        const DayCounter& dayCounter,
        Compounding compounding,
        Frequency frequency,
        bool includeSettlementDateFlows,
        Date settlementDate = Date(),
        Date npvDate = Date(),
        Real accuracy = 1.0e-10,
        Size maxIterations = 100,
        Rate guess = 0.0);
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

        static Real npv(
            const Leg& leg,
            const ext::shared_ptr<YieldTermStructure>& discountCurve,
            Spread zSpread,
            const DayCounter& dayCounter,
            Compounding compounding,
            Frequency frequency,
            bool includeSettlementDateFlows,
            const Date& settlementDate = Date(),
            const Date& npvDate = Date()) {
            return QuantLib::CashFlows::npv(
                leg, discountCurve,
                zSpread,
                dayCounter,
                compounding,
                frequency,
                includeSettlementDateFlows,
                settlementDate,
                npvDate);
        }
        static Real npv(
            const Leg& leg,
            const Handle<YieldTermStructure>& discountCurve,
            bool includeSettlementDateFlows,
            const Date& settlementDate = Date(),
            const Date& npvDate = Date()) {
            return QuantLib::CashFlows::npv(
                leg, **discountCurve,
                includeSettlementDateFlows,
                settlementDate, npvDate);
        }

        static Real bps(
            const Leg& leg,
            const ext::shared_ptr<YieldTermStructure>& discountCurve,
            bool includeSettlementDateFlows,
            const Date& settlementDate = Date(),
            const Date& npvDate = Date()) {
            return QuantLib::CashFlows::bps(
                leg, *discountCurve,
                includeSettlementDateFlows,
                settlementDate, npvDate);
        }
        static Real bps(
            const Leg& leg,
            const Handle<YieldTermStructure>& discountCurve,
            bool includeSettlementDateFlows,
            const Date& settlementDate = Date(),
            const Date& npvDate = Date()) {
            return QuantLib::CashFlows::bps(
                leg, **discountCurve,
                includeSettlementDateFlows,
                settlementDate, npvDate);
        }

        static Rate atmRate(
            const Leg& leg,
            const ext::shared_ptr<YieldTermStructure>& discountCurve,
            bool includeSettlementDateFlows,
            const Date& settlementDate = Date(),
            const Date& npvDate = Date(),
            Real npv = Null<Real>()) {
            return QuantLib::CashFlows::atmRate(
                leg, *discountCurve,
                includeSettlementDateFlows,
                settlementDate, npvDate,
                npv);
        }
    }
};


#endif
