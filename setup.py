#!/bin/python3
# ccash_python_client - ccash python client
# Copyright (C) 2021 FearlessDoggo21
# see LICENCE file for licensing information

# python3 setup.py sdist; twine upload dist/*
from setuptools import setup

with open("README", "r") as file:
    desc = file.read()

setup(
    name             = "ccash_python_client",
    packages         = ["ccash_python_client"],
    version          = "1.0.1",
    license          = "MIT",
    description      = "Python client for CCash servers",
    long_description = desc,
    long_description_content_type = "text/plain",
    author           = "FearlessDoggo21",
    author_email     = "fearlessdoggo21@vivaldi.net",

    install_requires = [
        "requests"
    ],

    classifiers      = [
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3"
    ],
)
