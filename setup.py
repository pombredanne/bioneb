#! /usr/bin/env python

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name = "BioNEB",
    version = "1",
    description = "BioNEB - Bioinformatics utilities",
    long_description = "BioNEB - Bioinformatics utilities developed at New England Biolabs",
    author = "Paul Joseph Davis",
    author_email = "davisp@neb.com",
    license = "Apache 2.0",
    url = "http://github.com/davisp/bioneb",
    zip_safe = False,
    
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    
    packages = [
        "bioneb",
        "bioneb.bin",
        "bioneb.bin.couchdb",
        "bioneb.parsers",
        "bioneb.utils"
    ],
    
    entry_points = {
        "console_scripts": [
            "bioneb-taxonomy = neb.bin.couchdb.taxonomy:main",
            "bioneb-genbank = neb.bin.couchdb.genbank:main",
        ]
    }
)
        
        
    
