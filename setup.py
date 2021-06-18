## To publish:
## python3 setup.py sdist
## twine upload dist/*

from distutils.core import setup

setup(
    name                = "CCashPythonClient",
    packages            = ["CCashPythonClient"],
    version             = "0.1.0",
    license             = "MIT",
    description         = "A web-client to query CCash servers, providing ease of development.",
    long_description    = open("README.md", "r").read(),
    author              = "FearlessDoggo21",
    author_email        = "fearlessdoggo21@vivaldi.net",
    url                 = "https://GitHub.com/FearlessDoggo21/CCashPythonClient",
    
    install_requires    = [
        "requests"
    ],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ],
)
