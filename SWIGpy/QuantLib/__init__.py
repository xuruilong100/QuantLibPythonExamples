from .QuantLib import *
from .QuantLib import _QuantLib

__author__ = 'xrl'
__email__ = 'xuruilong100@hotmail.com'

if hasattr(_QuantLib,'__version__'):
    __version__ = _QuantLib.__version__
elif hasattr(_QuantLib.cvar,'__version__'):
    __version__ = _QuantLib.cvar.__version__
else:
    print('Could not find __version__ attribute')

if hasattr(_QuantLib,'__hexversion__'):
    __hexversion__ = _QuantLib.__hexversion__
elif hasattr(_QuantLib.cvar,'__hexversion__'):
    __hexversion__ = _QuantLib.cvar.__hexversion__
else:
    print('Could not find __hexversion__ attribute')
