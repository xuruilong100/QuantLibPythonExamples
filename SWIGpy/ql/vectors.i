#ifndef ql_vectors_i
#define ql_vectors_i

%include ../ql/alltypes.i
%include common.i
%include date.i

%template(SizeVector) std::vector<size_t>;
%template(IntVector) std::vector<int>;
%template(UnsignedIntVector) std::vector<unsigned int>;
%template(DoubleVector) std::vector<double>;
%template(StrVector) std::vector<std::string>;
%template(BoolVector) std::vector<bool>;

%template(DoublePair) std::pair<double, double>;
%template(DoublePairVector) std::vector<std::pair<double, double> >;
%template(PairDoubleVector) std::pair<std::vector<double>, std::vector<double> >;

%template(NodePair) std::pair<Date, double>;
%template(NodeVector) std::vector<std::pair<Date, double> >;

%template(DoubleVectorVector) std::vector<std::vector<Real> >;

namespace std {
    %template(QuoteVector) vector<ext::shared_ptr<Quote> >;
    %template(QuoteVectorVector) vector<vector<ext::shared_ptr<Quote> > >;
    %template(QuoteHandleVector) vector<Handle<Quote> >;
    %template(QuoteHandleVectorVector) vector<vector<Handle<Quote> > >;
    %template(RelinkableQuoteHandleVector) vector<RelinkableHandle<Quote> >;
    %template(RelinkableQuoteHandleVectorVector) vector<vector<RelinkableHandle<Quote> > >;
}

%{
template <class T, class U>
std::vector<T> to_vector(const std::vector<U>& v) {
    std::vector<T> out(v.size());
    std::copy(v.begin(), v.end(), out.begin());
    return out;
}
%}

#endif
