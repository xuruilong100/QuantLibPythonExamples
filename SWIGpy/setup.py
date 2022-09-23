"""
setup.py file for QuantLib
"""

from distutils.core import setup, Extension

ql_module = Extension(
    name='QuantLib._QuantLib',
    sources=[
        'QuantLib/ql_wrap.cpp',
        'qlex/cashflows/ChinaFixingRepoCoupon.cpp',
        'qlex/cashflows/ChinaFixingRepoLeg.cpp',
        'qlex/cashflows/ChinaFixingRepoCouponPricer.cpp',
        'qlex/indexes/ChinaFixingRepo.cpp',
        'qlex/instruments/MakeChinaFixingRepoSwap.cpp',
        'qlex/instruments/ChinaFixingRepoSwap.cpp',
        'qlex/math/CubicSpline.cpp',
        'qlex/math/QuadraticSpline.cpp',
        'qlex/termstructures/yield/AdjustedSvenssonFitting.cpp',
        'qlex/termstructures/yield/CubicSplinesFitting.cpp',
        'qlex/termstructures/yield/BjorkChristensenFitting.cpp',
        'qlex/termstructures/yield/DieboldLiFitting.cpp',
        'qlex/termstructures/yield/BlissFitting.cpp',
        'qlex/termstructures/yield/QuadraticSplinesFitting.cpp',
        'qlex/termstructures/yield/ChinaFixingRepoSwapRateHelper.cpp',
        'qlex/time/daycounters/Actual365_25.cpp'],
    include_dirs=['/usr/include/', './'],
    library_dirs=['/usr/lib/'],
    libraries=[
        'QuantLib',
        'svml'  # for intel oneapi compiler
    ],
    # config extra_compile_args by yourself
    extra_compile_args=[
        '-w',
        '-ferror-limit=0'
    ])

setup(
    name='QuantLib',
    version='1.27',
    author="xrl",
    author_email="xuruilong100@hotmail.com",
    description="Python bindings for the QuantLib",
    ext_modules=[ql_module],
    py_modules=['QuantLib.__init__', 'QuantLib.QuantLib'],
    url="https://github.com/xuruilong100",
    license="follows QuantLib's license")
