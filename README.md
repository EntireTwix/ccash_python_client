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
Assuming `pip` is installed, run the following command in a terminal:
`python3 -m pip install CCashPythonClient`

You may then import the server class as follows:
`from CCashPythonClient import CCash`

The exceptions may be found in `CCashPythonClient.ex`.
The configurations may be found in `CCashPythonClient.conf`.
