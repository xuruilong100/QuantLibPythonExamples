#ifndef ql_timebasket_i
#define ql_timebasket_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i

%{
using QuantLib::TimeBasket;
%}

class TimeBasket {
    %rename(__len__) size;
  public:
    TimeBasket();
    TimeBasket(const std::vector<Date>&, const std::vector<Real>&);
    Size size();
    TimeBasket rebin(const std::vector<Date>&) const;
    %extend {
        Real __getitem__(const Date& d) {
            return (*self)[d];
        }
        void __setitem__(const Date& d, Real value) {
            (*self)[d] = value;
        }
        PyObject* items() {
            PyObject* itemList = PyList_New(self->size());
            TimeBasket::iterator i;
            Size j;
            for (i = self->begin(), j = 0; i != self->end(); ++i, ++j) {
                Date* d = new Date(i->first);
                PyObject* item = PyTuple_New(2);
                PyTuple_SetItem(
                    item, 0,
                    SWIG_NewPointerObj((void*)d, $descriptor(Date*), 1));
                PyTuple_SetItem(
                    item, 1, PyFloat_FromDouble(i->second));
                PyList_SetItem(
                    itemList, j, item);
            }
            return itemList;
        }
        // Python 2.2 methods
        bool __contains__(const Date& d) {
            return self->hasDate(d);
        }
        PyObject* __iter__() {
            %#if PY_VERSION_HEX >= 0x02020000
            PyObject* keyList = PyList_New(self->size());
            TimeBasket::iterator i;
            Size j;
            for (i = self->begin(), j = 0; i != self->end(); ++i, ++j) {
                Date* d = new Date(i->first);
                PyList_SetItem(
                    keyList, j,
                    SWIG_NewPointerObj((void*)d, $descriptor(Date*), 1));
            }
            PyObject* iter = PyObject_GetIter(keyList);
            Py_DECREF(keyList);
            return iter;
            %#else
            throw std::runtime_error(
                "Python 2.2 or later is needed for iterator support");
            %#endif
        }
    }
};

#endif
