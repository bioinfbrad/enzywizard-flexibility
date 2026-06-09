#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name="enzywizard-flexibility",
    version="1.0.1",                     # Using the release version
    author="bioinfbrad",
    description="A command-line tool for estimating protein flexibility from a cleaned protein structure",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/bioinfbrad/enzywizard-flexibility",
    package_dir={"": "src"},             # The package is under the src/ directory
    packages=find_packages(where="src"),
    python_requires=">=3.10",
    install_requires=[
        "biopython>=1.86",
        "prody>=2.6.1",
        "numpy>=1.23.5",
        "scipy>=1.15.2",
        "requests>=2.33.1",
        "packaging",
        "pyparsing",
    ],
    entry_points={
        "console_scripts": [
            "enzywizard-flexibility = enzywizard_flexibility.cli:main",
        ],
    },
    include_package_data=True,
    license="MIT",
)
