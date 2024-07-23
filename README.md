# festo-edcon
`festo-edcon` is a python package which bundles modules to facilitate operation of Festo electric drives (currently via EtherNet/IP and Modbus) using PROFIDRIVE. Documentation can be found [here](https://festo-research.gitlab.io/electric-automation/festo-edcon) and in the [examples](./examples) directory

## Installation
### Release
The latest release is available in the public PyPi repo. 
Install via pip:
```
pip install festo-edcon
```

To install with GUI support:
```
pip install 'festo-edcon[gui]'
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
### [MotionHandler](https://festo-research.gitlab.io/electric-automation/festo-edcon/features/edrive.html#edrive-motionhandler) - [`edrive.motion.MotionHandler`](https://festo-research.gitlab.io/electric-automation/festo-edcon/edcon.edrive.html#module-edcon.edrive.motion_handler)
The motion module which aims to replicate the function set of the Siemens SinaPos function block (both using telegram 111).

### [ComModbus](https://festo-research.gitlab.io/electric-automation/festo-edcon/features/edrive.html#commodbus) - [`edrive.com_modbus.ComModbus`](https://festo-research.gitlab.io/electric-automation/festo-edcon/edcon.edrive.html#module-edcon.edrive.com_modbus)
The Modbus/TCP communication driver used for transmitting modbus traffic between host and drive.

### [ComEthernetip](https://festo-research.gitlab.io/electric-automation/festo-edcon/features/edrive.html#comethernetip) - [`edrive.com_modbus.ComEthernetip`](https://festo-research.gitlab.io/electric-automation/festo-edcon/edcon.edrive.html#module-edcon.edrive.com_ethernetip)
The EtherNet/IP communication driver used for transmitting EtherNet/IP traffic between host and drive.

### [Profidrive](https://festo-research.gitlab.io/electric-automation/festo-edcon/features/profidrive.html) - [`profidrive`](https://festo-research.gitlab.io/electric-automation/festo-edcon/edcon.profidrive.html#module-edcon.profidrive)
Contains telegram definitions that are currently supported by EDrives running PROFIDRIVE via Modbus/TCP and EtherNet/IP:
   1. Telegram 1
   2. Telegram 9
   3. Telegram 102
   4. Telegram 111

### [CLI](https://festo-research.gitlab.io/electric-automation/festo-edcon/features/cli.html) - [`cli`](https://festo-research.gitlab.io/electric-automation/festo-edcon/edcon.cli.html#module-edcon.cli)

#### `festo-edcon`
Main entry point to the CLI.
```
usage: festo-edcon [-h] [-i IP_ADDRESS] [-q] [--ethernetip] {position,pnu,parameter-set-load,tg1,tg9,tg102,tg111} ...

options:
  -h, --help            show this help message and exit
  -i IP_ADDRESS, --ip-address IP_ADDRESS
                        IP address to connect to (default: 192.168.0.1).
  -q, --quiet           suppress output verbosity
  --ethernetip          use EtherNet/IP (instead of ModbusTCP) as underlying communication.

subcommands:
  {position,pnu,parameter-set-load,tg1,tg9,tg102,tg111}
                        Subcommand that should be called
```

| Subcommand | Description |
| -------- | ------- |
| `position`  | execute very basic positioning tasks.    |
| `pnu` | read or write PNUs.     |
| `parameter-set-load`  | load a complete parameter set to a drive.    |
| `tg1`  | run a test sequence using telegram 1.    |
| `tg9`  | run a test sequence using telegram 9.    |
| `tg102`  | run a test sequence using telegram 102.    |
| `tg111`  | run a test sequence using telegram 111.    |

For more information use the help flag  (`festo-edcon [subcommand] -h`).

#### `festo-edcon-gui`
Entry point to the GUI.
```
usage: festo-edcon-gui [-h] [-i IP_ADDRESS] [-q]

options:
  -h, --help            show this help message and exit
  -i IP_ADDRESS, --ip-address IP_ADDRESS
                        IP address to connect to (default: 192.168.0.1).
  -q, --quiet           suppress output verbosity
```

For more information use the help flag  (`festo-edcon-gui -h`).
