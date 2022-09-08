# Changelog

Please stick to this article: https://keepachangelog.com/de/0.3.0/
Please pick from the following sections when categorizing your entry:
`Added`, `Changed`, `Fixed`, `Removed`
Before every entry put one of these to mark the severity of the change:
`Major`, `Minor` or `Patch`

## Unreleased
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

## [v0.6.1] - 01.09.22
### Added
- [Patch] Added CHANGELOG to sphinx page.
### Fixed
- [Patch] Fixed bug that caused a crash if `homing` option of position tool was used. Option is now called `reference`.

## [v0.6.0] - 26.08.22
### Added
- [Minor] Added modbus flavour feature e.g. to specify device specific options.
- [Minor] Added public API methods to EDriveMotion for configuring various options (SINAPOS functionality).
- [Minor] Added non-blocking semantics to motion tasks in EDriveMotion.

### Changed
- [Minor] Renamed EDrivePositioning to EDriveMotion.
- [Minor] EDriveModbus performs I/O data transfer in a separate thread (EDriveEthernetip did this already).

## [v0.5.1] - 10.08.22
### Added
- [Patch] Added proper README, docu and examples.
### Fixed
- [Patch] Fixed bug leading to infinite loop when an fault appears during motion task.

## [v0.5.0] - 02.08.22
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

## [v0.4.0] - 24.06.22
### Added
- [Minor] Added CLI options for edcon-position tool.

## [v0.3.1] - 21.06.22
### Changed
- [Patch] Fixed gitlab-ci job dependencies.

## [v0.3.0] - 15.06.22
### Changed
- [Minor] Changed deploy job to release job CI/CD. Also creates release.
 
## [v0.2.0] - 14.06.22
### Added
- [Minor] Added deploy job to CI/CD

## [v0.1.0] - 13.06.22
- [Minor] Initial release
