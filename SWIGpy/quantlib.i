%module QuantLib

%include exception.i

%exception {
    try {
        $action
    } catch (std::out_of_range& e) {
        SWIG_exception(SWIG_IndexError,const_cast<char*>(e.what()));
    } catch (std::exception& e) {
        SWIG_exception(SWIG_RuntimeError,const_cast<char*>(e.what()));
    } catch (...) {
        SWIG_exception(SWIG_UnknownError,"unknown error");
    }
}

%{
#include <ql/version.hpp>
const int    __hexversion__ = QL_HEX_VERSION;
const char* __version__     = QL_VERSION;
%}

const int __hexversion__;
%immutable;
const char* __version__;
%mutable;

%include ./ql/ql.i
