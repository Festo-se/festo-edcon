# Changelog

Please stick to this article: https://keepachangelog.com/de/0.3.0/
Please pick from the following sections when categorizing your entry:
`Added`, `Changed`, `Fixed`, `Removed`
Before every entry put one of these to mark the severity of the change:
`Major`, `Minor` or `Patch`

## Unreleased
### Added
- [Minor] Added sphinx docs.
- [Minor] Added `with` statement support to CmmtPositionFunctionBlock.
### Fixed
- [Patch] Corrected exception upon failing telegram assertion.
- [Patch] Fixed exception caused by reading non-existing DeviceInformationRequest for older CMMT devices.
- [Patch] Fixed bug causing some drives to not start traversing task because of missing delay.
- [Patch] Fixed exception caused when PNU was accessed via Modbus on legacy devices.
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
