#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

setup_requirements = ['pytest-runner']
test_requirements = ['pytest>=3', ]

with open('README.md') as readme_file:
    long_desc = readme_file.read()


with open('requirements.txt') as reqs:
    requirements = reqs.read()

setup(
    author="eduardokapp",
    author_email="eduardobkapp@gmail.com",
    python_requires='>=3.6',
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Correlation analysis for categorical features.",
    install_requires=requirements,
    license="MIT license",
    long_description=long_desc,
    include_package_data=True,
    keywords='correlation',
    name="cat_corr",
    packages=find_packages(include=["cat_corr", "cat_corr.*"]),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/eduardokapp/categorical_correlation',
    version='0.1.0',
    zip_safe=False,
)
