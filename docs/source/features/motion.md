# EDriveMotion
The [`EDriveMotion`](edrive.edrive_motion.EDriveMotion) class can be used to start different motion tasks.
Under the hood it uses PROFIDRIVE telegram 111.
The intention of the class is to provide an abstraction from telegram 111 to the user, thus providing a simpler interface.

The motion class is instantiated by providing a edrive communication instance that is used to transfer the telegram (e.g. [`EDriveEthernetip`](edrive.edrive_ethernetip.EDriveEthernetip) or [`EDriveModbus`](edrive.edrive_modbus.EDriveModbus)).

```python
with EDriveMotion(edrive) as mot:
```

The instance is then able of handling basic setup sequences.

```python
    mot.acknkwoledge_faults()
    mot.enable_powerstage()
```

And start motion tasks:

```python
    mot.position_task(position=1000, velocity=5000)
```
