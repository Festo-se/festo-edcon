# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased
## v0.13.3 - 19.04.24
### Fixed
- Fix reset() method of telegram

### Changed
- Apply black formatting
- Update gitlab-ci (added black format check)
- TelegramHandler does update_io() after construction
- Telegram*Handler: Rename `validation` parameter to `config_mode`
- CLI: Replaced `verbose` option with `quiet`

## v0.13.2 - 17.04.24
### Fixed
- Validation mode not used by MotionHandler.

## v0.13.1 - 15.04.24
### Fixed
- Fix occasional exception when closing IOThread which is not active anymore.

## v0.13.0 - 15.04.24
### Changed
- Added inputs()/outputs() method to retrieve input/output words from Telegram.

## v0.12.2 - 07.03.24
### Fixed
- Fixed pos_stw1.activate_setup bit not being resetted on position task preparation.

## v0.12.1 - 23.02.24
### Fixed
- Fixed Festo logo.

## v0.12.0 - 23.02.24
### Added
- Added first version of GUI.

### Changed
- Added .pylintrc containing pylint config.

## v0.11.0 - 11.12.23
### Added
- Parameter: Added new class Parameter as representation of a EDrive parameter.
- ParameterHandler: Added write and read methods for Parameter objects.
### Changed
- Ported setup.py to pyproject.toml.

## v0.10.11 - 05.12.23
### Added
- Added connected() method to ComBase.
### Changed
- Updated pnu_map.csv and icp_map.csv.
- Enforce ethernetip package version 1.1.1.
### Fixed
- Added conditional toggle for activate_traversing_task bit when continuous_update is not active.

## v0.10.10 - 26.10.23
### Fixed
- Fixed bug where setup of ComModbus would crash for CMMT-xx-EP devices.

### Added
- Added job to create gitlab release entry.

## v0.10.9 - 17.10.23
### Changed
- Changes to enable backport to python3.9.

## v0.10.8 - 13.10.23
### Added
- Added error handling to parameter-set-load for missing parameter mappings.

### Changed
- Upgraded package dependencies to pymodbus3.
- Run branch pipeline only if no MR pipeline exists.
- Upgraded pnu_map.csv.
- ComEthernetip: increased waiting time for send_io to ensure that data is sent reliably.
- Using dedicated logger instead of generic root logger for edcon logs.

## v0.10.7 - 21.07.23
### Added
- Enabled possibility to create multiple ComEthernetip instances.

### Fixed
- Fixed shutdown behavior of ComEthernetip.
- Fixed log output of error string when timeout occurs (e.g. acknowlege_faults).

## v0.10.6 - 19.07.23
### Fixed
- Improved shutdown behavior of TelegramHandler.

## v0.10.5 - 18.07.23
### Fixed
- Fixed exception on exit when using python-3.11.

## v0.10.4 - 18.07.23
### Fixed
- Increased timeout for enabling the powerstage from 1 to 5 seconds.
- Fixed return value of TelegramHandler: disable_powerstage().

### Changed
- Updated logging info output strings.

## v0.10.3 - 21.06.23
### Fixed
- Fixed issue causing an error when reading 8-bit wide PNUs.

## v0.10.2 - 10.05.23
### Added
- Added CLI tool to load complete parameter set files.
  
### Changed
- MotionHandler: Changed semantics of current_velocity.

## v0.10.1 - 02.05.23
### Fixed
- Fixed typo in help message causing CLI to crash.

 ### Changed
- Changed default IP adress from `192.168.0.51` to `192.168.0.1`
  
## v0.10.0 - 28.04.23
### Added
- Added LUT for ICP names to skip manual search for fault names and remedies in manual.
 ### Changed
- Overhauled complete project structure to recommended pattern.
- Separated EDriveMotion into subclasses also used for other telegam modes.
- Updated examples/multi_position_nonblock.py.
- Changed CLI tools to use a central entry point with subcommands.
### Fixed
- Fixed not updating telegram bits during condition monitoring.

## v0.9.0 - 05.04.23
### Added
- EDriveMotion: Added function to disable powerstage.
- Added LUT for PNU types to skip manual search for data types in manual.
- Added example for PNU access.
- Added missing data types to  `festo-edcon-pnu` tool.
### Changed
- Restructured README.md and sphinx docs.
### Removed
- Removed modbus flavour feature due to simplification reasons.

## v0.8.0 - 31.03.23
### Added
- EDriveMotion: Added wait_for_traversing_task_ack method.
### Changed
- Moved to python version 3.10
- EDriveModbus/EDriveEthernetip: added nonblocking/blocking behavior to I/O methods.
- EDriveMotion: enhanced wait_for_condition and adapted motion tasks to new behavior.
- EDriveMotion: referencing task now uses homing method as per default.
- Updated unit tests.
- Updated examples.
### Fixed
- Raise error when no EIP connection is possible.

## v0.7.6 - 03.11.22
### Added
- EDriveMotion: Added methods to check if fix stop and/or clamping torque has been reached.
### Fixed
- Fixed setup.py.

## v0.7.5 - 20.10.22
### Fixed
- Fixed LICENSE.

## v0.7.4 - 18.10.22
### Added
- Updated URLs to new project location.
### Fixed
- Fixed issue where position tool would continue operation after error instead of exiting.

## v0.7.3 - 17.10.22
### Added
- Added LICENSE file.

## v0.7.2 - 11.10.22
### Added
- Added a EDriveLogging class to enable easy logging. 
### Changed
- Moved correct telegram assertion from constructor to separate method.
## v0.7.1 - 13.09.22
### Added
- Added a few status checking functions. 
- Added example for multiple axes.
- Added examples to docu page.
### Fixed
- Fixed return type of pnu_write/read_raw methods.
  
## v0.7.0 - 08.09.22
### Added
- EDriveMotion: Added methods for pausing and resuming motion tasks.
- EDriveMotion: Added methods for waiting on specific conditions.
- EDriveMotion: Added `timeout` parameter to `acknowledge_faults`.
### Changed
- EDriveMotion: Removed `request_plc_control()` which is now done implicit.
- Replaced standard logging format handler with `Rich` logging handler.
### Fixed
- EDriveMotion: Fixed incorrect scaling of velocity.
- EDriveMotion: Checking correct bit after enabling of powerstage.

## v0.6.1 - 01.09.22
### Added
- Added CHANGELOG to sphinx page.
### Fixed
- Fixed bug that caused a crash if `homing` option of position tool was used. Option is now called `reference`.

## v0.6.0 - 26.08.22
### Added
- Added modbus flavour feature e.g. to specify device specific options.
- Added public API methods to EDriveMotion for configuring various options (SINAPOS functionality).
- Added non-blocking semantics to motion tasks in EDriveMotion.

### Changed
- Renamed EDrivePositioning to EDriveMotion.
- EDriveModbus performs I/O data transfer in a separate thread (EDriveEthernetip did this already).

## v0.5.1 - 10.08.22
### Added
- Added proper README, docu and examples.
### Fixed
- Fixed bug leading to infinite loop when an fault appears during motion task.

## v0.5.0 - 02.08.22
### Added
- Added sphinx docs.
- Added `with` statement support to EDrivePositioning.
- Added method to `EDriveModbus` to configure the modbus timeout.
- Added method to update I/O data.
- Added methods for reading current position and velocity.
- Added ready_for_motion method to check if motion tasks are allowed.
- Added graceful closing of ethernetip/modbus session when driver is destructed.
### Changed
- Renamed `CMMT` occurences to `EDrive`
### Fixed
- Corrected exception upon failing telegram assertion.
- Fixed exception caused by reading non-existing DeviceInformationRequest for older EDrive devices.
- Fixed bug causing some drives to not start traversing task because of missing delay.
- Fixed exception caused when PNU was accessed via Modbus on legacy devices.
- Fixed bug that sometimes caused infinite waiting for (homing, position, record) tasks to be finished.
- Fixed bug causing a failing powerstage enable in case it has already been enabled once.

## v0.4.0 - 24.06.22
### Added
- Added CLI options for edcon-position tool.

## v0.3.1 - 21.06.22
### Changed
- Fixed gitlab-ci job dependencies.

## v0.3.0 - 15.06.22
### Changed
- Changed deploy job to release job CI/CD. Also creates release.
 
## v0.2.0 - 14.06.22
### Added
- Added deploy job to CI/CD

## v0.1.0 - 13.06.22
- Initial release
