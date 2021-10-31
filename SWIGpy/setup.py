"""
setup.py file for QuantLib
"""

from distutils.core import setup, Extension

ql_module = Extension(
    name='QuantLib._QuantLib',
    sources=[
        'QuantLib/ql_wrap.cpp'],
    include_dirs=['/usr/include/'],
    library_dirs=['/usr/lib/'],
    libraries=['QuantLib'],
    extra_compile_args=['-fopenmp', '-Wno-unused', '-w', '-ferror-limit=0'],
    extra_link_args=['-fopenmp'])

setup(
    name='QuantLib',
    version='1.24',
    author="xrl",
    author_email="xuruilong100@hotmail.com",
    description="Python bindings for the QuantLib",
    ext_modules=[ql_module],
    py_modules=['QuantLib.__init__', 'QuantLib.QuantLib'],
    url="https://github.com/xuruilong100",
    license="follows QuantLib's license")
