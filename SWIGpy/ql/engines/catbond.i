#ifndef ql_engines_catbond_i
#define ql_engines_catbond_i

%define QL_TYPECHECK_BOOL                        7220    %enddef

%typemap(in) boost::optional<bool> {
	if($input == Py_None)
		$1 = boost::none;
	else if ($input == Py_True)
		$1 = true;
	else
		$1 = false;
}

%typecheck (QL_TYPECHECK_BOOL) boost::optional<bool> {
    if (PyBool_Check($input) || Py_None == $input)
    	$1 = 1;
    else
    	$1 = 0;
}

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i

%{
using QuantLib::CatSimulation;
using QuantLib::EventSetSimulation;
using QuantLib::BetaRiskSimulation;
using QuantLib::CatRisk;
using QuantLib::EventSet;
using QuantLib::BetaRisk;
using QuantLib::EventPaymentOffset;
using QuantLib::NoOffset;
using QuantLib::NotionalPath;
using QuantLib::NotionalRisk;
using QuantLib::DigitalNotionalRisk;
using QuantLib::ProportionalNotionalRisk;
using QuantLib::MonteCarloCatBondEngine;
%}

%template(BoolDateDoublePairVectorPair) std::pair<bool, std::vector<std::pair<Date, Real>>>;

%shared_ptr(CatSimulation)
class CatSimulation {
  private:
    CatSimulation();
  public:
	%extend {
		std::pair<bool, std::vector<std::pair<Date, Real>>> nextPath() {
			std::vector<std::pair<Date, Real>> path;
			bool b = self->nextPath(path);
			return std::make_pair(b, path);
		}
	}
};

%shared_ptr(EventSetSimulation)
class EventSetSimulation : public CatSimulation {
  public:
	%extend {
		EventSetSimulation(
        const std::vector<std::pair<Date, Real>>& events,
        Date eventsStart,
        Date eventsEnd,
        Date start,
        Date end) {
            ext::shared_ptr<std::vector<std::pair<Date, Real>>> eventsPtr(
					      new std::vector<std::pair<Date, Real>>(events));
            return new EventSetSimulation(
              eventsPtr,
              eventsStart,
              eventsEnd,
              start,
              end);
			}
	}
};

%shared_ptr(BetaRiskSimulation)
class BetaRiskSimulation : public CatSimulation {
  public:
    BetaRiskSimulation(
        Date start,
        Date end,
        Real maxLoss,
        Real lambda,
        Real alpha,
        Real beta);
    Real generateBeta();
};

%shared_ptr(CatRisk)
class CatRisk {
  private:
    CatRisk();
  public:
    ext::shared_ptr<CatSimulation> newSimulation(
        const Date& start, 
        const Date& end) const;
};

%shared_ptr(EventSet)
class EventSet : public CatRisk {
  public:
	%extend {
		EventSet(
			const std::vector<std::pair<Date, Real>>& events,
			Date eventsStart,
			Date eventsEnd) {
          ext::shared_ptr<std::vector<std::pair<Date, Real>>> eventsPtr(
              new std::vector<std::pair<Date, Real>>(events));
          return new EventSet(
              eventsPtr,
              eventsStart,
              eventsEnd);
			}
	}
};

%shared_ptr(BetaRisk)
class BetaRisk : public CatRisk {
  public:
    BetaRisk(
        Real maxLoss,
        Real years,
        Real mean,
        Real stdDev);
};

%shared_ptr(EventPaymentOffset)
class EventPaymentOffset {
  private:
    EventPaymentOffset();
  public:
    Date paymentDate(const Date& eventDate);
};

%shared_ptr(NoOffset)
class NoOffset : public EventPaymentOffset {
  public:
    NoOffset();
};

class NotionalPath {
  public:
    NotionalPath();
    Rate notionalRate(const Date& date) const;
    void reset();
    void addReduction(const Date& date, Rate newRate);
    Real loss();
};

%shared_ptr(NotionalRisk)
class NotionalRisk {
  private:
    NotionalRisk();
  public:
    void updatePath(
        const std::vector<std::pair<Date, Real>>& events,
        NotionalPath& path) const;
};

%shared_ptr(DigitalNotionalRisk)
class DigitalNotionalRisk : public NotionalRisk {
  public:
    DigitalNotionalRisk(
        const ext::shared_ptr<EventPaymentOffset>& paymentOffset,
        Real threshold);
};

%shared_ptr(ProportionalNotionalRisk)
class ProportionalNotionalRisk : public NotionalRisk {
  public:
    ProportionalNotionalRisk(
        const ext::shared_ptr<EventPaymentOffset>& paymentOffset,
        Real attachement,
        Real exhaustion);
};

%shared_ptr(MonteCarloCatBondEngine)
class MonteCarloCatBondEngine : public PricingEngine {
  public:
    MonteCarloCatBondEngine(
        ext::shared_ptr<CatRisk> catRisk,
        Handle<YieldTermStructure> discountCurve = Handle<YieldTermStructure>(),
        boost::optional<bool> includeSettlementDateFlows = boost::none);
    Handle<YieldTermStructure> discountCurve() const;
};

#endif
