# edcon
`edcon` is a python package which bundles modules to facilitate operation of Festo electric drives (currently via EtherNet/IP and Modbus). Documentation can be found here and in the [examples](./examples) directory
## Modules
There are two main modules which contribute to the package:

1. Generic PROFIDRIVE telegrams:
   1. Telegram 1
   2. Telegram 9
   3. Telegram 102
   4. Telegram 111

2. Drive specific driver modules:
    1. CMMT: EtherNet/IP and Modbus
    2. Position Function Block based on Siemens SinaPos (using Telegram 111)

## Tools
### edcon-position
`edcon-position` is a CLI tool to execute very basic positioning tasks
### edcon-pnu
`edcon-position` is a CLI tool to read or write PNUs 

### edcon-test-tg1
`edcon-position` is a CLI tool to run a test sequence using telegram 1

### edcon-test-tg9
`edcon-position` is a CLI tool to run a test sequence using telegram 9

### edcon-test-tg102
`edcon-position` is a CLI tool to run a test sequence using telegram 102

### edcon-test-tg111
`edcon-position` is a CLI tool to run a test sequence using telegram 111

## Installation
The latest release is available in a non-public PyPi repo. 
The URL can be added to your pip.ini in order to make it known to your pip instance.

1. Find your `pip.ini`:
```
pip config debug
```
2. Add the following line:
```
extra-index-url = https://adeartifactory1.de.festo.net/artifactory/api/pypi/electricdrives-python-dev-local/simple
```
3. Install via pip:
```
pip install edcon
```