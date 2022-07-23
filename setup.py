# -*- coding: utf-8 -*-
"""
Created on Sat Jul 11 15:03:16 2020

@author: oisin
"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ustreasurycurve",
    version="0.0.6",
    author="Oisin Kenny",
    author_email="oisinkenn@gmail.com",
    description="Pulls the real and nominal yield curves from the US Treasury's website for a date range (inclusive)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/oisinkenny/ustreasurycurve",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)