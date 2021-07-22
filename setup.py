## python3 setup.py sdist
## twine upload dist/*

from setuptools import setup

with open("README.md", "r") as file:
    desc = file.read()

setup(
    name             = "CCashPythonClient",
    packages         = ["CCashPythonClient"],
    version          = "1.0.0",
    license          = "MIT",
    description      = "A web-client to query CCash servers, providing ease of development.",
    long_description = desc,
    long_description_content_type = "text/markdown",
    author           = "FearlessDoggo21",
    author_email     = "fearlessdoggo21@vivaldi.net",
    url              = "https://GitHub.com/FearlessDoggo21/CCashPythonClient/",

    install_requires = [
        "requests"
    ],

    classifiers      = [
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ],
)
