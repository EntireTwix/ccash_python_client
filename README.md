# CCashPythonClient
A web-client to query CCash servers, providing ease of 
development. \
Uses the requests lib to communicate with a remote server. \
Implements python Exception based errors rather than numbers, and
returns JSON data as dictionaries.

## CCash
CCash repository and set-up information can be found
[here](https://GitHub.com/EntireTwix/CCash).

## Documentation
This project has very simple functions and is not large. Thus, no
external documentation is provided. However, each class and function
has its information written in markdown format beneath the
definition.

## Setup
Because this is a small module, it is safe to clone it into your
working directory. Use the following git commands or download
the source code from GitHub.

`git clone https://GitHub.com/FearlessDoggo21/CCashPythonClient`

You will then be able to import the python module. \
It is requested that the README remains in the directory. The license
must remain.

`import CCashPythonClient as CCash`

To enable VSCode IntelliSense auto-completion and markdown
information, place the following lines in `.vscode/settings.json`:

    "python.autoComplete.extraPaths": [
        "${workspaceFolder}/CCashPythonClient"
    ]
