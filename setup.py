#!/usr/bin/python3
# python3 setup.py sdist; twine upload dist/*
from setuptools import setup

with open("README", "r") as file:
    desc = file.read()

setup(
    name             = "ccash-python-client",
    packages         = ["ccash-python-client"],
    version          = "1.0.1",
    license          = "MIT",
    description      = "A web-client to query CCash servers, providing ease of development.",
    long_description = desc,
    long_description_content_type = "text/plain",
    author           = "FearlessDoggo21",
    author_email     = "fearlessdoggo21@vivaldi.net",

    install_requires = [
        "requests"
    ],

    classifiers      = [
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ],
)
