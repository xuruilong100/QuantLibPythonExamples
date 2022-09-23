#ifndef ql_defines_i
#define ql_defines_i

// depend on platform

#define QL_MIN_INTEGER         -2147483648              // std::numeric_limits<int>::min()
#define QL_MAX_INTEGER          2147483647              // std::numeric_limits<int>::max()
#define QL_MIN_REAL            -1.797693134862315e+308  // -std::numeric_limits<double>::max()
#define QL_MAX_REAL             1.797693134862315e+308  // std::numeric_limits<double>::max()
#define QL_MIN_POSITIVE_REAL    2.225073858507201e-308  // std::numeric_limits<double>::min()
#define QL_EPSILON              2.220446049250313e-16   // std::numeric_limits<double>::epsilon()
#define QL_NULL_INTEGER         2147483647              // std::numeric_limits<int>::max()
#define QL_NULL_REAL            3.402823e+38            // std::numeric_limits<float>::max()

#define M_E         2.71828182845904523536
#define M_LOG2E     1.44269504088896340736
#define M_LOG10E    0.434294481903251827651
#define M_IVLN10    0.434294481903251827651
#define M_LN2       0.693147180559945309417
#define M_LOG2_E    0.693147180559945309417
#define M_LN10      2.30258509299404568402
#define M_PI        3.141592653589793238462643383280
#define M_TWOPI     (M_PI * 2.0)
#define M_PI_2      1.57079632679489661923
#define M_PI_4      0.785398163397448309616
#define M_3PI_4     2.3561944901923448370E0
#define M_SQRTPI    1.77245385090551602792981
#define M_1_PI      0.318309886183790671538
#define M_2_PI      0.636619772367581343076
#define M_1_SQRTPI  0.564189583547756286948
#define M_2_SQRTPI  1.12837916709551257390
#define M_SQRT2     1.41421356237309504880
#define M_SQRT_2    0.7071067811865475244008443621048490392848359376887
#define M_SQRT1_2   0.7071067811865475244008443621048490392848359376887
#define M_LN2LO     1.9082149292705877000E-10
#define M_LN2HI     6.9314718036912381649E-1
#define M_SQRT3     1.73205080756887719000
#define M_INVLN2    1.4426950408889633870E0

#endif
