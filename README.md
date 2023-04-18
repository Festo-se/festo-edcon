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

### [CLI](https://festo-research.gitlab.io/electric-automation/festo-edcon/features/cli.html) - [`edcon_cli`](https://festo-research.gitlab.io/electric-automation/festo-edcon/edcon_cli.html#module-edcon_cli)
`festo-edcon` is the main entry point to the CLI.
It supports various subcommands which execute some basic functions.
For more information use the help flag  (`festo-edcon -h`).
#### Subcommands
- `position` is a subcommand to execute very basic positioning tasks.
- `pnu` is subcommnad to read or write PNUs.
- `tg1` is subcommnad to run a test sequence using telegram 1.
- `tg9` is subcommnad to run a test sequence using telegram 9.
- `tg102` is subcommnad to run a test sequence using telegram 102.
- `tg111` is subcommnad to run a test sequence using telegram 111.



