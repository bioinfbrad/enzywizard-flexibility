#!/usr/bin/env python
from setuptools import setup, find_packages
import os

# Read the version from version.py without importing the package
version_file = os.path.join(os.path.dirname(__file__), 'src', 'enzywizard_flexibility', 'version.py')
with open(version_file) as f:
    exec(f.read())  # defines __version__

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="enzywizard-flexibility",
    version=__version__,                    # Using the release version
    author="bioinfbrad",
    description="A command-line tool for estimating protein flexibility from a cleaned protein structure",
    long_description=long_description,
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
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering :: Chemistry",
    ],
)
