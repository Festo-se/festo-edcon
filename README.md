# festo-edcon
`festo-edcon` is a python package which bundles modules to facilitate operation of Festo electric drives (currently via EtherNet/IP and Modbus) using PROFIDRIVE. Documentation can be found [here](https://festo-research.gitlab.io/electric-automation/festo-edcon) and in the [examples](./examples) directory

## Installation
### Release
The latest release is available in the public PyPi repo. 
Install via pip:
```
pip install festo-edcon
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
## Usage
### [EDriveMotion](https://festo-research.gitlab.io/electric-automation/festo-edcon/features/motion.html) - [`edrive.edrive_motion.EDriveMotion`](https://festo-research.gitlab.io/electric-automation/festo-edcon/edrive.html#module-edrive.edrive_motion)
The motion module which aims to replicate the function set of the Siemens SinaPos function block (both using telegram 111).

### [EDriveModbus](https://festo-research.gitlab.io/electric-automation/festo-edcon/features/edrive.html#edrivemodbus) - [`edrive.edrive_modbus.EDriveModbus`)](https://festo-research.gitlab.io/electric-automation/festo-edcon/edrive.html#module-edrive.edrive_modbus)
The Modbus/TCP communication driver used for transmitting modbus traffic between host and drive.

### [EDriveEthernetip](https://festo-research.gitlab.io/electric-automation/festo-edcon/features/edrive.html#edriveethernetip) - [`edrive.edrive_modbus.EDriveEthernetip`](https://festo-research.gitlab.io/electric-automation/festo-edcon/edrive.html#module-edrive.edrive_ethernetip)
The EtherNet/IP communication driver used for transmitting EtherNet/IP traffic between host and drive.

### [Profidrive](https://festo-research.gitlab.io/electric-automation/festo-edcon/features/profidrive.html) - [`profidrive`](https://festo-research.gitlab.io/electric-automation/festo-edcon/profidrive.html#module-profidrive)
Contains telegram definitions that are currently supported by EDrives running PROFIDRIVE via Modbus/TCP and EtherNet/IP:
   1. Telegram 1
   2. Telegram 9
   3. Telegram 102
   4. Telegram 111

### [CLI-Tools](https://festo-research.gitlab.io/electric-automation/festo-edcon/features/cli-tools.html) - [`edcon_tools`](https://festo-research.gitlab.io/electric-automation/festo-edcon/edcon_tools.html#module-edcon_tools)

- `festo-edcon-position` is a CLI tool to execute very basic positioning tasks.
- `festo-edcon-pnu` is a CLI tool to read or write PNUs.
- `festo-edcon-test-tg1` is a CLI tool to run a test sequence using telegram 1.
- `festo-edcon-test-tg9` is a CLI tool to run a test sequence using telegram 9.
- `festo-edcon-test-tg102` is a CLI tool to run a test sequence using telegram 102.
- `festo-edcon-test-tg111` is a CLI tool to run a test sequence using telegram 111.



