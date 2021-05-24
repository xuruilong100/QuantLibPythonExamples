#ifndef ql_settings_i
#define ql_settings_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i

%{
using QuantLib::Settings;
using QuantLib::SavedSettings;
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

#endif
