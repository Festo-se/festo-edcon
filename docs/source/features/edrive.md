# EDrive

There are different communication protocols which transfer telegrams between devices.
The [`ComBase`](edrive.com_base.ComBase) class aims to bundle common parts of the protocol classes.

## ComBase
The [`ComBase`](edrive.com_base.ComBase) class defines interface functions used to handle I/O data and for capable device also PNU accesses.

__`start_io`__: Starts the I/O data operation
__`stop_io`__: Stops the I/O data operation
__`send_io`__: Writes provided `bytes` data to the process data outputs
__`recv_io`__: Reads from process data inputs and returns `bytes` data

For cases where PNU access is available there are also methods

__`read_pnu`__: Reads a PNU of provided index and subindex and interprets with provided datatype
__`write_pnu`__: Writes a provided PNU value to provided index and subindex as provided datatype

## ComEthernetip
Instantiating a [`ComEthernetip`](edrive.com_ethernetip.ComEthernetip) requires an IP address.
Optionally the cycle time can be provided (default is 10 ms).
Be aware that most likely your OS will be a limiting factor here.

```python
edrive = ComEthernetip('192.168.0.1', cycle_time=50)
```

## ComModbus
Instantiating a [`ComModbus`](edrive.com_modbus.ComModbus) requires an IP address.
Optionally the modbus timeout which should be configured on the endpoint can be provided (default is 1000 ms).

```python
edrive = ComModbus('192.168.0.1', timeout_ms=500)
```