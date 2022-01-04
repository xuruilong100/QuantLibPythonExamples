#ifndef ql_unit_all_i
#define ql_unit_all_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/base.i

%{
using QuantLib::UnitOfMeasureConversionManager;
using QuantLib::UnitOfMeasureConversion;
using QuantLib::CommodityType;
using QuantLib::NullCommodityType;
%}

%{
using QuantLib::UnitOfMeasure;
using QuantLib::BarrelUnitOfMeasure;
using QuantLib::MTUnitOfMeasure;
using QuantLib::MBUnitOfMeasure;
using QuantLib::GallonUnitOfMeasure;
using QuantLib::LitreUnitOfMeasure;
using QuantLib::LotUnitOfMeasure;
using QuantLib::KilolitreUnitOfMeasure;
using QuantLib::TokyoKilolitreUnitOfMeasure;
%}

%{
using QuantLib::Quantity;
%}

class UnitOfMeasureConversionManager {
  private:
    UnitOfMeasureConversionManager();
  public:
    static UnitOfMeasureConversionManager& instance();
    UnitOfMeasureConversion lookup(
        const CommodityType& commodityType,
        const UnitOfMeasure&,
        const UnitOfMeasure&,
        UnitOfMeasureConversion::Type type = UnitOfMeasureConversion::Derived) const;
    void add(const UnitOfMeasureConversion&);
    void clear();
};

class UnitOfMeasureConversion {
  public:
    enum Type {
        Direct,
        Derived
    };
    UnitOfMeasureConversion() = default;
    UnitOfMeasureConversion(const CommodityType& commodityType,
                            const UnitOfMeasure& source,
                            const UnitOfMeasure& target,
                            Real conversionFactor);
    const UnitOfMeasure& source() const;
    const UnitOfMeasure& target() const;
    const CommodityType& commodityType() const;
    Type type() const;
    Real conversionFactor() const;
    const std::string& code() const;
    Quantity convert(const Quantity& quantity) const;
    static UnitOfMeasureConversion chain(
        const UnitOfMeasureConversion& r1,
        const UnitOfMeasureConversion& r2);
};

class CommodityType {
  public:
    CommodityType() = default;
    CommodityType(const std::string& code, const std::string& name);

    const std::string& code() const;
    const std::string& name() const;
    bool empty() const;
    %extend {
        bool __eq__(const CommodityType& c) const {
            return *self == c;
        }
        bool __ne__(const CommodityType& c) const {
            return *self != c;
        }
        std::string __str__() const {
            std::ostringstream out;
            out << *self;
            return out.str();
        }
        std::string __repr__() const {
            std::ostringstream out;
            out << *self;
            return out.str();
        }
    }
};

class NullCommodityType : public CommodityType {
  public:
    NullCommodityType();
};

class UnitOfMeasure {
  public:
    enum Type { Mass, Volume, Energy, Quantity };
    UnitOfMeasure() = default;
    UnitOfMeasure(const std::string& name,
                  const std::string& code,
                  Type unitType);
    const std::string& name() const;
    const std::string& code() const;
    Type unitType() const;
    bool empty() const;
    const Rounding& rounding() const;
    const UnitOfMeasure& triangulationUnitOfMeasure() const;
    %extend {
        bool __eq__(const UnitOfMeasure& c) const {
            return *self == c;
        }
        bool __ne__(const UnitOfMeasure& c) const {
            return *self != c;
        }
        std::string __str__() const {
            std::ostringstream out;
            out << *self;
            return out.str();
        }
        std::string __repr__() const {
            std::ostringstream out;
            out << *self;
            return out.str();
        }
    }
};

class BarrelUnitOfMeasure : public UnitOfMeasure {
  public:
    BarrelUnitOfMeasure();
};

class MTUnitOfMeasure : public UnitOfMeasure {
  public:
    MTUnitOfMeasure();
};

class MBUnitOfMeasure : public UnitOfMeasure {
  public:
    MBUnitOfMeasure();
};

class GallonUnitOfMeasure : public UnitOfMeasure {
  public:
    GallonUnitOfMeasure();
};

class LitreUnitOfMeasure : public UnitOfMeasure {
  public:
    LitreUnitOfMeasure();
};

class LotUnitOfMeasure : public UnitOfMeasure {
  public:
    LotUnitOfMeasure();
};

class KilolitreUnitOfMeasure : public UnitOfMeasure {
  public:
    KilolitreUnitOfMeasure();
};

class TokyoKilolitreUnitOfMeasure : public UnitOfMeasure {
  public:
    TokyoKilolitreUnitOfMeasure();
};

class Quantity {
  public:
    Quantity() = default;
    Quantity(CommodityType commodityType, UnitOfMeasure unitOfMeasure, Real amount);
    const CommodityType& commodityType() const;
    const UnitOfMeasure& unitOfMeasure() const;
    Real amount() const;
    Quantity rounded() const;

    Quantity operator+() const;
    Quantity operator-() const;
    Quantity& operator+=(const Quantity&);
    Quantity& operator-=(const Quantity&);
    Quantity& operator*=(Real);
    Quantity& operator/=(Real);

    enum ConversionType {
        NoConversion,
        BaseUnitOfMeasureConversion,
        AutomatedConversion
    };
    static ConversionType conversionType;
    static UnitOfMeasure baseUnitOfMeasure;

    %extend {
        Quantity __add__(const Quantity& q) const {
            return *self + q;
        }

        Quantity __sub__(const Quantity& q) const {
            return *self - q;
        }
        Quantity __mul__(Real q) const {
            return *self * q;
        }
        Quantity __rmul__(Real q) const {
            return *self * q;
        }
        Quantity __truediv__(Real q) const {
            return *self / q;
        }
        Real __truediv__(const Quantity& q) const {
            return *self / q;
        }

        bool __eq__(const Quantity& q) const {
            return *self == q;
        }
        bool __ne__(const Quantity& q) const {
            return *self != q;
        }
        bool __lt__(const Quantity& q) const {
            return *self < q;
        }
        bool __le__(const Quantity& q) const {
            return *self <= q;
        }
        bool __gt__(const Quantity& q) const {
            return *self > q;
        }
        bool __ge__(const Quantity& q) const {
            return *self >= q;
        }
    }
};

bool close(const Quantity&, const Quantity&, Size n = 42);
bool close_enough(const Quantity&, const Quantity&, Size n = 42);

#endif
