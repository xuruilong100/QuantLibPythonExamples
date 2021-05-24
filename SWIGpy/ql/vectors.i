#ifndef ql_vectors_i
#define ql_vectors_i

%include ../ql/alltypes.i
%include stl.i
%include common.i
%include date.i
%include std_vector.i
%include std_pair.i

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

%{
template <class T, class U>
std::vector<T> to_vector(const std::vector<U>& v) {
    std::vector<T> out(v.size());
    std::copy(v.begin(), v.end(), out.begin());
    return out;
}
%}

#endif
