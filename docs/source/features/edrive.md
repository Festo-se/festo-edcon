# EDrive

## EDrive Communication
There are different communication protocols which transfer telegrams between devices.
The [`EDriveBase`](edrive.edrive_base.EDriveBase) class aims to bundle common parts of the protocol classes.

### EDriveBase
The [`EDriveBase`](edrive.edrive_base.EDriveBase) class defines interface functions used to handle I/O data and for capable device also PNU accesses.

__`start_io`__: Starts the I/O data operation
__`stop_io`__: Stops the I/O data operation
__`send_io`__: Writes provided `bytes` data to the process data outputs
__`recv_io`__: Reads from process data inputs and returns `bytes` data

For cases where PNU access is available there are also methods

__`read_pnu`__: Reads a PNU of provided index and subindex and interprets with provided datatype
__`write_pnu`__: Writes a provided PNU value to provided index and subindex as provided datatype

### EDriveEthernetip
Instantiating a [`EDriveEthernetip`](edrive.edrive_ethernetip.EDriveEthernetip) requires an IP address.
Optionally the cycle time can be provided (default is 10 ms).
Be aware that most likely your OS will be a limiting factor here.

```python
edrive = EDriveEthernetip('192.168.0.1', cycle_time=50)
```

### EDriveModbus
Instantiating a [`EDriveModbus`](edrive.edrive_modbus.EDriveModbus) requires an IP address.
Optionally the modbus timeout which should be configured on the endpoint can be provided (default is 1000 ms).

```python
edrive = EDriveModbus('192.168.0.1', timeout_ms=500)
```

Another option that can be provided optionally is the `flavour` which determines device specific behaviors.
The default `flavour` is `CMMT-AS`.
If the device is supported, the simplest method is to provide the flavour as a device string.

```python
edrive = EDriveModbus('192.168.0.1', flavour='CPX-AP')
```

In case there is no matching flavour built-in, the fastest method to provide a basic info dict.
The dict must at least contain the fields `"pd_in_addr"`,`"pd_out_addr"`, `"timeout_addr"` and `"pd_size"`.
```python
my_flavour = {"pd_in_addr": 0, "pd_out_addr": 160, "timeout_addr": 500, "pd_size": 32}
edrive = EDriveModbus('192.168.0.1', flavour=my_flavour)
```

In order to support more sophisticated  behaviors e.g. reading device information or PNU access
there is the possibility to provide a [`FlavourBase`](edrive.modbus_flavours.flavour_base.FlavourBase) deduced class.
See [ModbusFlavours](edrive_modbus/modbus_flavours.md).

## EDrivePositioning
The [`EDrivePositioning`](edrive.edrive_positioning.EDrivePositioning) class can be used to start different motion tasks.
Under the hood it uses PROFIDRIVE telegram 111.
The intention of the class is to provide an abstraction from telegram 111 to the user, thus providing a simpler interface.

The positioning class is instantiated by providing a edrive communication instance that is used to transfer the telegram (e.g. [`EDriveEthernetip`](edrive.edrive_ethernetip.EDriveEthernetip) or [`EDriveModbus`](edrive.edrive_modbus.EDriveModbus)).

```python
with EDrivePositioning(edrive) as pos:
```

The instance is then able of handling basic setup sequences.

```python
    pos.request_plc_control()
    pos.acknkwoledge_faults()
    pos.enable_powerstage()
```

And start motion tasks:

```python
    pos.position_task(position=1000, velocity=5000)
```


