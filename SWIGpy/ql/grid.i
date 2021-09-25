#ifndef ql_grid_i
#define ql_grid_i

%include ../ql/types.i
%include ../ql/common.i
%include ../ql/alltypes.i

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

    Size index(Time t) const;
    Size closestIndex(Time t) const;
    Time closestTime(Time t) const;
    const std::vector<Time>& mandatoryTimes() const;
    Time dt(Size i) const;
    Time at(Size i) const;
    Size size() const;
    bool empty() const;
    Time front() const;
    Time back() const;
    %extend {
        Time __getitem__(Size i) {
            return (*self)[i];
        }
    }
};


#endif
