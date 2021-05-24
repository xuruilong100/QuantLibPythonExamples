#ifndef ql_grid_i
#define ql_grid_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i
%include stl.i

%{
using QuantLib::TimeGrid;
%}

class TimeGrid {
    %rename(__len__)   size;
  public:
    // empty time-grid
    TimeGrid() {}
    // regularly spaced time-grid
    TimeGrid(Time end, Size steps);
    %extend {
        // time-grid with mandatory time points
        TimeGrid(const std::vector<Time>& times) {
            return new TimeGrid(times.begin(), times.end());
        }
        // time-grid with mandatory time points and steps
        TimeGrid(const std::vector<Time>& times, Size steps) {
            return new TimeGrid(times.begin(), times.end(), steps);
        }
    }
    Size size() const;
    %extend {
        Time __getitem__(Integer i) {
            Integer size_ = static_cast<Integer>(self->size());
            if (i>=0 && i<size_) {
                return (*self)[i];
            } else if (i<0 && -i<=size_) {
                return (*self)[size_+i];
            } else {
                throw std::out_of_range("time-grid index out of range");
            }
        }
        Time dt(Integer i) const {
            Integer size_ = static_cast<Integer>(self->size());
            if (i>=0 && i<size_) {
                return self->dt(i);
            } else if (i<0 && -i<=size_) {
                return self->dt(size_+i);
            } else {
                throw std::out_of_range("time-grid index out of range");
            }
        }
    }
};


#endif
