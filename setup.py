from setuptools import find_packages, setup 

with open('README.md', 'r') as f:
	long_description = f.read()

setup(
	name='cluster-shapley',
	packages=find_packages(include=['dr_explainer']),
	version='0.1.0',
	description='Explaining dimensionality reduction using SHAP values',
	long_description=long_description,
    long_description_content_type='text/markdown',
	author='Wilson Estecio Marcilio Junior',
	author_email='wilson_jr@outlook.com',
	url='https://github.com/wilsonjr/ClusterShapley',
	license='MIT',
	install_requires=['scipy', 'sklearn', 'numpy', 'shap'],
	setup_requires=['pytest-runner'],
	tests_require=['pytest'],
	test_suite='tests',
)