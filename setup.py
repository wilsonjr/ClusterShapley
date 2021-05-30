# -*- coding: utf-8 -*-
# Author: Wilson Estécio Marcílio Júnior <wilson_jr@outlook.com>
#
# License: BSD 3 clause

from setuptools import setup, Extension, find_packages

from pybind11.setup_helpers import Pybind11Extension, build_ext
from pybind11 import get_cmake_dir

import sys 

__version__ = "0.1.5"

ext_modules = None 

with open('README.md', 'r') as f:
	long_description = f.read()


if sys.platform == 'win32':
    print("Compiling for Windows")
    ext_modules = [
    	Pybind11Extension("_cluster_shapley",
    		["src/cpp/cs.cpp", "src/cpp/cs_bind.cpp"],
    		language='c++',
    		extra_compile_args = [ '/openmp', '/DEIGEN_DONT_PARALLELIZE',  '/DINFO', '-IC:/Eigen'],
            extra_link_args = [ '/openmp', '/DEIGEN_DONT_PARALLELIZE', '/DINFO', '-IC:/Eigen'],
    		define_macros = [('VERSION_INFO', __version__)],
    		),

    ]

else:
    print("Compiling for Linux")
    ext_modules = [
    Pybind11Extension("_cluster_shapley",
        ["src/cpp/cs.cpp", "src/cpp/cs_bind.cpp"],
        language='c++',
        extra_compile_args = ['-O3', '-shared', '-std=c++11', '-fPIC', '-fopenmp',  '-march=native', '-DINFO'],
        extra_link_args = ['-O3', '-shared', '-std=c++11', '-fPIC', '-fopenmp',  '-march=native', '-DINFO'],
        define_macros = [('VERSION_INFO', __version__)],
        ),

    ]



setup(
    name="cluster-shapley",
    version=__version__,
    author="Wilson E. Marcílio-Jr",
    author_email="wilson_jr@outlook.com",
    url="https://github.com/wilsonjr/ClusterShapley",
    description="Explaining dimensionality reduction using SHAP values",
    long_description="",
    ext_modules=ext_modules,
    extras_require={"test": "pytest"},
    # Currently, build_ext only provides an optional "highest supported C++
    # level" feature, but in the future it may provide more features.
    cmdclass={"build_ext": build_ext},
    install_requires=['scipy', 'sklearn', 'numpy', 'shap', 'pybind11'],
    packages=['dr_explainer'],
    zip_safe=False,
)

# setup(
# 	name='cluster-shapley',
# 	packages=['dr_explainer'],#find_packages(include=['dr_explainer']),
# 	version=__version__,
# 	description='Explaining dimensionality reduction using SHAP values',
# 	long_description=long_description,
#     long_description_content_type='text/markdown',
# 	author='Wilson E. Marcílio-Jr',
# 	author_email='wilson_jr@outlook.com',
# 	url='https://github.com/wilsonjr/ClusterShapley',
# 	license='MIT',
# 	ext_modules=ext_modules,
# 	extras_require={"test": "pytest"},
# 	cmdclass={"build_ext": build_ext},
# 	install_requires=['scipy', 'sklearn', 'numpy', 'shap', 'pybind11'],
# 	zip_safe=False,
# 	# setup_requires=['pytest-runner'],
# 	# tests_require=['pytest'],
# 	# test_suite='tests',
# )