#ifndef ql_exp_mcm_i
#define ql_exp_mcm_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include ../ql/montecarlo.i

%{
using QuantLib::Path;
using QuantLib::PathPricer;
using QuantLib::SingleVariate;
using QuantLib::MultiVariate;
using QuantLib::MonteCarloModel;
%}

%{
typedef MonteCarloModel<SingleVariate, PseudoRandom> SingleVariatePRMonteCarloModel;
typedef MonteCarloModel<SingleVariate, LowDiscrepancy> SingleVariateLDMonteCarloModel;
typedef MonteCarloModel<MultiVariate, PseudoRandom> MultiVariatePRMonteCarloModel;
typedef MonteCarloModel<MultiVariate, LowDiscrepancy> MultiVariateLDMonteCarloModel;
%}

%shared_ptr(PathPricer<Path>)
%shared_ptr(PathPricer<MultiPath>)
template<class PathType>
class PathPricer {
  private:
    PathPricer();
  public:
    Real operator()(const PathType& path) const;
};

%template(SinglePathPricer) PathPricer<Path>;
%template(MultiPathPricer) PathPricer<MultiPath>;

%{
class PathFunction {
  public:
    PathFunction(PyObject* function) : function_(function) {
        Py_XINCREF(function_);
    }
    PathFunction(const PathFunction& f)
        : function_(f.function_) {
        Py_XINCREF(function_);
    }
    PathFunction& operator=(const PathFunction& f) {
        if ((this != &f) && (function_ != f.function_)) {
            Py_XDECREF(function_);
            function_ = f.function_;
            Py_XINCREF(function_);
        }
        return *this;
    }
    ~PathFunction() {
        Py_XDECREF(function_);
    }
    Real operator()(const Path& x) const {
        PyObject* path = PyTuple_New(x.length());
        for (Size i = 0; i < x.length(); ++i) {
            PyTuple_SetItem(
                path, static_cast<Py_ssize_t>(i), PyFloat_FromDouble(x[i]));
        }

        PyObject* arg = PyTuple_New(1);
        PyTuple_SetItem(arg, 0, path);

        PyObject* pyResult = PyObject_CallObject(function_, arg);

        Py_XDECREF(path);
        Py_XDECREF(arg);

        QL_ENSURE(
            pyResult != NULL,
            "failed to call Python function");

        Real result = PyFloat_AsDouble(pyResult);
        Py_XDECREF(pyResult);
        return result;
    }

  private:
    PyObject* function_;
};

class CustomPathPricer : public PathPricer<Path> {
  public:
    CustomPathPricer(PyObject* function):
        function_(function) {}
    ~CustomPathPricer() {}
    Real operator()(const Path& path) const {
        return function_(path);
    }
  private:
    PathFunction function_;
};
%}

%shared_ptr(CustomPathPricer)
class CustomPathPricer : public PathPricer<Path> {
  public:
    CustomPathPricer(PyObject* function);
    Real operator()(const Path& path) const;
};

%{
class MultiPathFunction {
  public:
    MultiPathFunction(PyObject* function) : function_(function) {
        Py_XINCREF(function_);
    }
    MultiPathFunction(const MultiPathFunction& f)
        : function_(f.function_) {
        Py_XINCREF(function_);
    }
    MultiPathFunction& operator=(const MultiPathFunction& f) {
        if ((this != &f) && (function_ != f.function_)) {
            Py_XDECREF(function_);
            function_ = f.function_;
            Py_XINCREF(function_);
        }
        return *this;
    }
    ~MultiPathFunction() {
        Py_XDECREF(function_);
    }
    Real operator()(const MultiPath& x) const {
        PyObject* multiPath = PyTuple_New(x.assetNumber());
        for (Size i = 0; i < x.assetNumber(); ++i) {
            PyObject* path = PyTuple_New(x.pathSize());
            for (Size j = 0; j < x.pathSize(); ++j){
                PyTuple_SetItem(
                    path, static_cast<Py_ssize_t>(j), PyFloat_FromDouble(x[i][j]));
            }
            PyList_SetItem(
                multiPath, static_cast<Py_ssize_t>(i), path);
            Py_XDECREF(path);
        }

        PyObject* arg = PyTuple_New(1);
        PyTuple_SetItem(arg, 0, multiPath);

        PyObject* pyResult = PyObject_CallObject(function_, arg);

        Py_XDECREF(multiPath);
        Py_XDECREF(arg);

        QL_ENSURE(
            pyResult != NULL,
            "failed to call Python function");

        Real result = PyFloat_AsDouble(pyResult);
        Py_XDECREF(pyResult);
        return result;
    }

  private:
    PyObject* function_;
};

class CustomMultiPathPricer : public PathPricer<MultiPath> {
  public:
    CustomMultiPathPricer(PyObject* function):
        function_(function) {}
    ~CustomMultiPathPricer() {}
    Real operator()(const MultiPath& path) const {
        return function_(path);
    }
  private:
    MultiPathFunction function_;
};
%}

class SingleVariatePRMonteCarloModel {
  public:
    SingleVariatePRMonteCarloModel(
        ext::shared_ptr<PathGenerator<GaussianRandomSequenceGenerator>> pathGenerator,
        ext::shared_ptr<PathPricer<Path>> pathPricer,
        Statistics sampleAccumulator,
        bool antitheticVariate,
        ext::shared_ptr<PathPricer<Path>> cvPathPricer = ext::shared_ptr<PathPricer<Path>>(),
        Real cvOptionValue = Real(),
        ext::shared_ptr<PathGenerator<GaussianRandomSequenceGenerator>> cvPathGenerator =
            ext::shared_ptr<PathGenerator<GaussianRandomSequenceGenerator>>());
    void addSamples(Size samples);
    const Statistics& sampleAccumulator() const;
};

class SingleVariateLDMonteCarloModel {
  public:
    SingleVariateLDMonteCarloModel(
        ext::shared_ptr<PathGenerator<GaussianLowDiscrepancySequenceGenerator>> pathGenerator,
        ext::shared_ptr<PathPricer<Path>> pathPricer,
        Statistics sampleAccumulator,
        bool antitheticVariate,
        ext::shared_ptr<PathPricer<Path>> cvPathPricer = ext::shared_ptr<PathPricer<Path>>(),
        Real cvOptionValue = Real(),
        ext::shared_ptr<PathGenerator<GaussianLowDiscrepancySequenceGenerator>> cvPathGenerator =
            ext::shared_ptr<PathGenerator<GaussianLowDiscrepancySequenceGenerator>>());
    void addSamples(Size samples);
    const Statistics& sampleAccumulator() const;
};

class MultiVariatePRMonteCarloModel {
  public:
    MultiVariatePRMonteCarloModel(
        ext::shared_ptr<MultiPathGenerator<GaussianRandomSequenceGenerator>> pathGenerator,
        ext::shared_ptr<PathPricer<MultiPath>> pathPricer,
        Statistics sampleAccumulator,
        bool antitheticVariate,
        ext::shared_ptr<PathPricer<MultiPath>> cvPathPricer = ext::shared_ptr<PathPricer<MultiPath>>(),
        Real cvOptionValue = Real(),
        ext::shared_ptr<MultiPathGenerator<GaussianRandomSequenceGenerator>> cvPathGenerator =
            ext::shared_ptr<MultiPathGenerator<GaussianRandomSequenceGenerator>>());
    void addSamples(Size samples);
    const Statistics& sampleAccumulator() const;
};

class MultiVariateLDMonteCarloModel {
  public:
    MultiVariateLDMonteCarloModel(
        ext::shared_ptr<MultiPathGenerator<GaussianLowDiscrepancySequenceGenerator>> pathGenerator,
        ext::shared_ptr<PathPricer<MultiPath>> pathPricer,
        Statistics sampleAccumulator,
        bool antitheticVariate,
        ext::shared_ptr<PathPricer<MultiPath>> cvPathPricer = ext::shared_ptr<PathPricer<MultiPath>>(),
        Real cvOptionValue = Real(),
        ext::shared_ptr<MultiPathGenerator<GaussianLowDiscrepancySequenceGenerator>> cvPathGenerator =
            ext::shared_ptr<MultiPathGenerator<GaussianLowDiscrepancySequenceGenerator>>());
    void addSamples(Size samples);
    const Statistics& sampleAccumulator() const;
};

#endif
