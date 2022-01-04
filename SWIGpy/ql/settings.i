#ifndef ql_settings_i
#define ql_settings_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i

%{
using QuantLib::Settings;
using QuantLib::SavedSettings;
using QuantLib::SeedGenerator;
%}

class Settings {
  private:
    Settings();
  public:
    static Settings& instance();
    %extend {
        Date getEvaluationDate() {
            return self->evaluationDate();
        }
        void setEvaluationDate(const Date& d) {
            self->evaluationDate() = d;
        }
        void includeReferenceDateEvents(bool b) {
            self->includeReferenceDateEvents() = b;
        }
        void includeTodaysCashFlows(bool b) {
            self->includeTodaysCashFlows() = b;
        }
        void setEnforcesTodaysHistoricFixings(bool b) {
            self->enforcesTodaysHistoricFixings() = b;
        }
        bool getEnforcesTodaysHistoricFixings() {
            return self->enforcesTodaysHistoricFixings();
        }

        ext::shared_ptr<Observable> evaluationDateAsObservable() const {
            return ext::shared_ptr<Observable>(self->evaluationDate());
        }
    }

    %pythoncode %{
        evaluationDate = property(
            getEvaluationDate, setEvaluationDate, None)
        includeReferenceDateCashFlows = property(
            None, includeReferenceDateEvents, None)
        includeReferenceDateEvents = property(
            None, includeReferenceDateEvents, None)
        includeTodaysCashFlows = property(
            None, includeTodaysCashFlows, None)
        enforcesTodaysHistoricFixings = property(
            getEnforcesTodaysHistoricFixings, setEnforcesTodaysHistoricFixings, None)
    %}
};

class SavedSettings {
    public:
    SavedSettings();
};

class SeedGenerator {
  public:
    static SeedGenerator& instance();
    BigNatural get();
  private:
    SeedGenerator();
};

#endif
