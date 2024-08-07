from Cython.Distutils import build_ext
from Cython.Build import cythonize
from distutils.extension import Extension
from distutils.core import setup
import sys
import numpy as np

A = sys.path.insert(0, "..")

setup(
    ext_modules=cythonize('./cpu_nms.pyx'),
    include_dirs=[np.get_include()]
)
