# EDrive

## EDrive Communication
There are different communication protocols which transfer telegrams between devices.
The `EDriveBase` class aims to bundle common parts of the protocol classes.

### EDriveBase
The `EDriveBase` class defines interface functions used to handle I/O data and for capable device also PNU accesses.

__`start_io`__: Starts the I/O data operation
__`stop_io`__: Stops the I/O data operation
__`send_io`__: Writes provided `bytes` data to the process data outputs
__`recv_io`__: Reads from process data inputs and returns `bytes` data

For cases where PNU access is available there are also methods

__`read_pnu`__: Reads a PNU of provided index and subindex and interprets with provided datatype
__`write_pnu`__: Writes a provided PNU value to provided index and subindex as provided datatype

### EDriveEthernetip
Instantiating a `EDriveEthernetip` requires an IP address.
Optionally the cycle time can be provided (default is 10 ms).
Be aware that most likely your OS will be a limiting factor here.

```
edrive = EDriveEthernetip('192.168.0.1', cycle_time=50)
```

### EDriveModbus
Instantiating a `EDriveModbus` requires an IP address.
Optionally the modbus timeout which should be configured on the endpoint can be provided (default is 1000 ms).

```
edrive = EDriveModbus('192.168.0.1', timeout_ms=500)
```

Another option that can be provided optionally is the `flavour` which determines device specific behaviors.
The default `flavour` is `CMMT-AS`.
If the device is supported, the simplest method is to provide the flavour as a device string.

```
edrive = EDriveModbus('192.168.0.1', flavour='CPX-AP')
```

In case there is no matching flavour, a custom flavour dict can be provided.
```
my_flavour = {"registers": {"pd_in": 0, "pd_out": 160, "timeout": 500}}
edrive = EDriveModbus('192.168.0.1', flavour=my_flavour)
```

The dict should contain a field `"registers"` which contains a dict with register addresses (`"pd_in"`,`"pd_out"` and `"timeout"`).


## EDrivePositioning
The `EDrivePositioning` class can be used to start different motion tasks.
Under the hood it uses PROFIDRIVE telegram 111.
The intention of the class is to provide an abstraction from telegram 111 to the user, thus providing a simpler interface.

The positioning class is instantiated by providing a edrive communication instance that is used to transfer the telegram (e.g. `EDriveEthernetip` or `EDriveModbus`).

```
with EDrivePositioning(edrive) as pos:
```

The instance is then able of handling basic setup sequences.

```
    pos.request_plc_control()
    pos.acknkwoledge_faults()
    pos.enable_powerstage()
```

And start motion tasks:

```
    pos.position_task(position=1000, velocity=5000)
```


