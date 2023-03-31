# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased
### Added
- [Minor] EDriveMotion: Added wait_for_traversing_task_ack method
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
