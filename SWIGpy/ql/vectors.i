#ifndef ql_vectors_i
#define ql_vectors_i

%include ../ql/alltypes.i
%include common.i
%include date.i

// %template(SizeVector) std::vector<Size>;    // comment this line if on ubuntu
%template(IntVector) std::vector<int>;
%template(NaturalVector) std::vector<Natural>;
%template(BigNaturalVector) std::vector<BigNatural>;
%template(DoubleVector) std::vector<double>;
%template(StrVector) std::vector<std::string>;
%template(BoolVector) std::vector<bool>;

%template(SizeSizePair) std::pair<Size, Size>;
%template(SizeSizePairVector) std::vector<std::pair<Size, Size>>;

%template(DoubleDoublePair) std::pair<double, double>;
%template(DoubleDoublePairVector) std::vector<std::pair<double, double>>;
%template(DoubleVectorDoubleVectorPair) std::pair<std::vector<double>, std::vector<double>>;

%template(DateDoublePair) std::pair<Date, double>;
%template(DateDoublePairVector) std::vector<std::pair<Date, double>>;
%template(DateVectorDoubleVectorPair) std::pair<std::vector<Date>, std::vector<Rate>>;

%template(DoubleVectorVector) std::vector<std::vector<Real>>;
%template(DoubleVectorVectorVector) std::vector<std::vector<std::vector<Real>>>;

%template(QuoteVector) std::vector<ext::shared_ptr<Quote>>;
%template(QuoteVectorVector) std::vector<std::vector<ext::shared_ptr<Quote>>>;
%template(QuoteHandleVector) std::vector<Handle<Quote>>;
%template(QuoteHandleVectorVector) std::vector<std::vector<Handle<Quote>>>;
%template(RelinkableQuoteHandleVector) std::vector<RelinkableHandle<Quote>>;
%template(RelinkableQuoteHandleVectorVector) std::vector<std::vector<RelinkableHandle<Quote>>>;

%{
template <class T, class U>
std::vector<T> to_vector(const std::vector<U>& v) {
    std::vector<T> out(v.size());
    std::copy(v.begin(), v.end(), out.begin());
    return out;
}
%}

%pythoncode %{
Shape = DoubleDoublePairVector
%}

#endif
