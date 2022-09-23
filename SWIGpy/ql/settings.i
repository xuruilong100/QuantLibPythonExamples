#ifndef ql_settings_i
#define ql_settings_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i

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

%typemap(out) boost::optional<bool> {
    if ($1 == boost::none) {
        Py_INCREF(Py_None);
        $result = Py_None;
    } else {
		if ($1 == true)
        	$result = Py_True;
		else
			$result = Py_False;
    }
}

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
        void setEvaluationDate(const Date& d) {
            self->evaluationDate() = d;
        }
        Date getEvaluationDate() const {
            return self->evaluationDate();
        }
        void setIncludeReferenceDateEvents(bool b) {
            self->includeReferenceDateEvents() = b;
        }
        bool getIncludeReferenceDateEvents() const {
            return self->includeReferenceDateEvents();
        }
		void setIncludeTodaysCashFlows(boost::optional<bool> b) {
            self->includeTodaysCashFlows() = b;
        }
        boost::optional<bool> getIncludeTodaysCashFlows() const {
			boost::optional<bool> result = self->includeTodaysCashFlows();
            if (result)
                return *result;
            else
                return boost::none;
        }
        void setEnforcesTodaysHistoricFixings(bool b) {
            self->enforcesTodaysHistoricFixings() = b;
        }
        bool getEnforcesTodaysHistoricFixings() const {
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
            getIncludeReferenceDateEvents, setIncludeReferenceDateEvents, None)
        includeReferenceDateEvents = property(
            getIncludeReferenceDateEvents, setIncludeReferenceDateEvents, None)
        includeTodaysCashFlows = property(
            getIncludeTodaysCashFlows, setIncludeTodaysCashFlows, None)
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
