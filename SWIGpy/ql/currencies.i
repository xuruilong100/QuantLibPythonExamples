#ifndef ql_currencies_i
#define ql_currencies_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i

%{
using QuantLib::Currency;
%}

class Currency {
  public:
    const std::string& name() const;
    const std::string& code() const;
    Integer numericCode() const;
    const std::string& symbol() const;
    const std::string& fractionSymbol() const;
    Integer fractionsPerUnit() const;
    const Rounding& rounding() const;
    std::string format() const;
    bool empty() const;
    const Currency& triangulationCurrency() const;
    %extend {
        std::string __str__() {
            return self->name();
        }
        bool __eq__(const Currency& other) {
            return (*self) == other;
        }
        bool __ne__(const Currency& other) {
            return (*self) != other;
        }
        Money operator*(Decimal x) {
            return *self*x;
        }
        Money __rmul__(Decimal x) {
            return *self*x;
        }
        bool __nonzero__() {
            return !self->empty();
        }
        bool __bool__() {
            return !self->empty();
        }
    }
    %pythoncode %{
    def __hash__(self):
        return hash(self.name())
    %}
};

namespace QuantLib {
class ARSCurrency : public Currency {};
class ATSCurrency : public Currency {};
class AUDCurrency : public Currency {};
class BDTCurrency : public Currency {};
class BEFCurrency : public Currency {};
class BGLCurrency : public Currency {};
class BRLCurrency : public Currency {};
class BYRCurrency : public Currency {};
class CADCurrency : public Currency {};
class CHFCurrency : public Currency {};
class CLPCurrency : public Currency {};
class CNYCurrency : public Currency {};
class COPCurrency : public Currency {};
class CYPCurrency : public Currency {};
class CZKCurrency : public Currency {};
class DEMCurrency : public Currency {};
class DKKCurrency : public Currency {};
class EEKCurrency : public Currency {};
class ESPCurrency : public Currency {};
class EURCurrency : public Currency {};
class FIMCurrency : public Currency {};
class FRFCurrency : public Currency {};
class GBPCurrency : public Currency {};
class GRDCurrency : public Currency {};
class HKDCurrency : public Currency {};
class HUFCurrency : public Currency {};
class IDRCurrency : public Currency {};
class IEPCurrency : public Currency {};
class ILSCurrency : public Currency {};
class INRCurrency : public Currency {};
class IQDCurrency : public Currency {};
class IRRCurrency : public Currency {};
class ISKCurrency : public Currency {};
class ITLCurrency : public Currency {};
class JPYCurrency : public Currency {};
class KRWCurrency : public Currency {};
class KWDCurrency : public Currency {};
class LTLCurrency : public Currency {};
class LUFCurrency : public Currency {};
class LVLCurrency : public Currency {};
class MTLCurrency : public Currency {};
class MXNCurrency : public Currency {};
class MYRCurrency : public Currency {};
class NLGCurrency : public Currency {};
class NOKCurrency : public Currency {};
class NPRCurrency : public Currency {};
class NZDCurrency : public Currency {};
class PEHCurrency : public Currency {};
class PEICurrency : public Currency {};
class PENCurrency : public Currency {};
class PKRCurrency : public Currency {};
class PLNCurrency : public Currency {};
class PTECurrency : public Currency {};
class ROLCurrency : public Currency {};
class RONCurrency : public Currency {};
class RUBCurrency : public Currency {};
class SARCurrency : public Currency {};
class SEKCurrency : public Currency {};
class SGDCurrency : public Currency {};
class SITCurrency : public Currency {};
class SKKCurrency : public Currency {};
class THBCurrency : public Currency {};
class TRLCurrency : public Currency {};
class TRYCurrency : public Currency {};
class TTDCurrency : public Currency {};
class TWDCurrency : public Currency {};
class USDCurrency : public Currency {};
class VEBCurrency : public Currency {};
class VNDCurrency : public Currency {};
class ZARCurrency : public Currency {};
}

#endif
