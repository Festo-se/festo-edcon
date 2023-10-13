# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased
### Added
- [Patch] Added error handling to parameter-set-load for missing parameter mappings.

### Changed
- [Minor] Upgraded package dependencies to pymodbus3.
- [Patch] Run branch pipeline only if no MR pipeline exists.
- [Patch] Upgraded pnu_map.csv.
- [Patch] ComEthernetip: increased waiting time for send_io to ensure that data is sent reliably.
- [Patch] Using dedicated logger instead of generic root logger for edcon logs.

## v0.10.7 - 21.07.23
### Added
- [Patch] Enabled possibility to create multiple ComEthernetip instances.

### Fixed
- [Patch] Fixed shutdown behavior of ComEthernetip.
- [Patch] Fixed log output of error string when timeout occurs (e.g. acknowlege_faults).

## v0.10.6 - 19.07.23
### Fixed
- [Patch] Improved shutdown behavior of TelegramHandler.

## v0.10.5 - 18.07.23
### Fixed
- [Patch] Fixed exception on exit when using python-3.11.

## v0.10.4 - 18.07.23
### Fixed
- [Patch] Increased timeout for enabling the powerstage from 1 to 5 seconds.
- [Patch] Fixed return value of TelegramHandler: disable_powerstage().

### Changed
- [Patch] Updated logging info output strings.

## v0.10.3 - 21.06.23
### Fixed
- [Patch] Fixed issue causing an error when reading 8-bit wide PNUs.

## v0.10.2 - 10.05.23
### Added
- [Patch] Added CLI tool to load complete parameter set files.
  
### Changed
- [Patch] MotionHandler: Changed semantics of current_velocity.

## v0.10.1 - 02.05.23
### Fixed
- [Patch] Fixed typo in help message causing CLI to crash.

 ### Changed
- [Patch] Changed default IP adress from `192.168.0.51` to `192.168.0.1`
  
## v0.10.0 - 28.04.23
### Added
- [Minor] Added LUT for ICP names to skip manual search for fault names and remedies in manual.
 ### Changed
- [Minor] Overhauled complete project structure to recommended pattern.
- [Minor] Separated EDriveMotion into subclasses also used for other telegam modes.
- [Patch] Updated examples/multi_position_nonblock.py.
- [Patch] Changed CLI tools to use a central entry point with subcommands.
### Fixed
- [Patch] Fixed not updating telegram bits during condition monitoring.

## v0.9.0 - 05.04.23
### Added
- [Minor] EDriveMotion: Added function to disable powerstage.
- [Minor] Added LUT for PNU types to skip manual search for data types in manual.
- [Patch] Added example for PNU access.
- [Patch] Added missing data types to  `festo-edcon-pnu` tool.
### Changed
- [Patch] Restructured README.md and sphinx docs.
### Removed
- [Minor] Removed modbus flavour feature due to simplification reasons.

## v0.8.0 - 31.03.23
### Added
- [Minor] EDriveMotion: Added wait_for_traversing_task_ack method.
### Changed
- [Minor] Moved to python version 3.10
- [Minor] EDriveModbus/EDriveEthernetip: added nonblocking/blocking behavior to I/O methods.
- [Minor] EDriveMotion: enhanced wait_for_condition and adapted motion tasks to new behavior.
- [Patch] EDriveMotion: referencing task now uses homing method as per default.
- [Patch] Updated unit tests.
- [Patch] Updated examples.
### Fixed
- [Patch] Raise error when no EIP connection is possible.

## v0.7.6 - 03.11.22
### Added
- [Patch] EDriveMotion: Added methods to check if fix stop and/or clamping torque has been reached.
### Fixed
- [Patch] Fixed setup.py.

## v0.7.5 - 20.10.22
### Fixed
- [Patch] Fixed LICENSE.

## v0.7.4 - 18.10.22
### Added
- [Patch] Updated URLs to new project location.
### Fixed
- [Patch] Fixed issue where position tool would continue operation after error instead of exiting.

## v0.7.3 - 17.10.22
### Added
- [Patch] Added LICENSE file.

## v0.7.2 - 11.10.22
### Added
- [Patch] Added a EDriveLogging class to enable easy logging. 
### Changed
- [Patch] Moved correct telegram assertion from constructor to separate method.
## v0.7.1 - 13.09.22
### Added
- [Patch] Added a few status checking functions. 
- [Patch] Added example for multiple axes.
- [Patch] Added examples to docu page.
### Fixed
- [Patch] Fixed return type of pnu_write/read_raw methods.
  
## v0.7.0 - 08.09.22
### Added
- [Minor] EDriveMotion: Added methods for pausing and resuming motion tasks.
- [Minor] EDriveMotion: Added methods for waiting on specific conditions.
- [Patch] EDriveMotion: Added `timeout` parameter to `acknowledge_faults`.
### Changed
- [Minor] EDriveMotion: Removed `request_plc_control()` which is now done implicit.
- [Minor] Replaced standard logging format handler with `Rich` logging handler.
### Fixed
- [Patch] EDriveMotion: Fixed incorrect scaling of velocity.
- [Patch] EDriveMotion: Checking correct bit after enabling of powerstage.

## v0.6.1 - 01.09.22
### Added
- [Patch] Added CHANGELOG to sphinx page.
### Fixed
- [Patch] Fixed bug that caused a crash if `homing` option of position tool was used. Option is now called `reference`.

## v0.6.0 - 26.08.22
### Added
- [Minor] Added modbus flavour feature e.g. to specify device specific options.
- [Minor] Added public API methods to EDriveMotion for configuring various options (SINAPOS functionality).
- [Minor] Added non-blocking semantics to motion tasks in EDriveMotion.

### Changed
- [Minor] Renamed EDrivePositioning to EDriveMotion.
- [Minor] EDriveModbus performs I/O data transfer in a separate thread (EDriveEthernetip did this already).

## v0.5.1 - 10.08.22
### Added
- [Patch] Added proper README, docu and examples.
### Fixed
- [Patch] Fixed bug leading to infinite loop when an fault appears during motion task.

## v0.5.0 - 02.08.22
### Added
- [Minor] Added sphinx docs.
- [Minor] Added `with` statement support to EDrivePositioning.
- [Minor] Added method to `EDriveModbus` to configure the modbus timeout.
- [Minor] Added method to update I/O data.
- [Minor] Added methods for reading current position and velocity.
- [Minor] Added ready_for_motion method to check if motion tasks are allowed.
- [Patch] Added graceful closing of ethernetip/modbus session when driver is destructed.
### Changed
- [Minor] Renamed `CMMT` occurences to `EDrive`
### Fixed
- [Patch] Corrected exception upon failing telegram assertion.
- [Patch] Fixed exception caused by reading non-existing DeviceInformationRequest for older EDrive devices.
- [Patch] Fixed bug causing some drives to not start traversing task because of missing delay.
- [Patch] Fixed exception caused when PNU was accessed via Modbus on legacy devices.
- [Patch] Fixed bug that sometimes caused infinite waiting for (homing, position, record) tasks to be finished.
- [Patch] Fixed bug causing a failing powerstage enable in case it has already been enabled once.

## v0.4.0 - 24.06.22
### Added
- [Minor] Added CLI options for edcon-position tool.

## v0.3.1 - 21.06.22
### Changed
- [Patch] Fixed gitlab-ci job dependencies.

## v0.3.0 - 15.06.22
### Changed
- [Minor] Changed deploy job to release job CI/CD. Also creates release.
 
## v0.2.0 - 14.06.22
### Added
- [Minor] Added deploy job to CI/CD

## v0.1.0 - 13.06.22
- [Minor] Initial release
