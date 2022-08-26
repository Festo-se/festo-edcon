# edcon
`edcon` is a python package which bundles modules to facilitate operation of Festo electric drives (currently via EtherNet/IP and Modbus) using PROFIDRIVE. Documentation can be found [here](https://lrsch.gitlab-pages.festo.company/edcon) and in the [examples](./examples) directory
## Modules
There are two main modules which contribute to the package:

1. Generic PROFIDRIVE telegrams (`profidrive`):
   1. Telegram 1
   2. Telegram 9
   3. Telegram 102
   4. Telegram 111

2. Driver modules (`edrive`):
    1. EDrive: EtherNet/IP and Modbus
    2. Motion Module based on Siemens SinaPos functionality (using Telegram 111)

## Tools

- `edcon-position` is a CLI tool to execute very basic positioning tasks.
- `edcon-pnu` is a CLI tool to read or write PNUs.
- `edcon-test-tg1` is a CLI tool to run a test sequence using telegram 1.
- `edcon-test-tg9` is a CLI tool to run a test sequence using telegram 9.
- `edcon-test-tg102` is a CLI tool to run a test sequence using telegram 102.
- `edcon-test-tg111` is a CLI tool to run a test sequence using telegram 111.

## Installation
### Release
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

### From git repo
You can also install directly from the git repo.

1. Clone the repository

```
git clone <git-url> <destination>
```

2. Change into the clone directory
```
cd <destination>
```

3. Install via pip
```
pip install .
```
