# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v2.0.25] - 2025-07-04

### Added
- Dynamic release notes generation based on CHANGELOG.md
- Automatic detection of available platform installers
- Build information with version, date, and commit SHA

### Changed
- Release workflow now generates content dynamically
- Improved error handling for missing platform builds
- Enhanced GitHub CLI authentication

### Fixed
- Working directory issues in multi-platform builds
- GitHub CLI authentication problems
- Artifact naming consistency

## [v2.0.24] - 2025-07-04

### Added
- Multi-platform build support (Windows, macOS, Linux)
- Platform-specific artifact names with version numbers
- GitHub CLI integration for reliable file uploads

### Changed
- Updated workflow to build on all three platforms simultaneously
- Improved release process with dynamic file discovery
- Enhanced release notes with platform-specific information

### Fixed
- Artifact naming from generic "electron-build" to platform-specific names
- File upload issues with proper path resolution
- Working directory configuration for all jobs

## [v2.0.23] - 2025-07-04

### Added
- Multi-platform installer support
- Dynamic release body generation
- Build information tracking

### Changed
- Release notes now reflect actual available platforms
- Improved workflow reliability and error handling

## [v2.0.22] - 2025-07-04

### Added
- Windows, macOS, and Linux build jobs
- Separate artifact downloads for each platform
- GitHub CLI for file uploads

### Changed
- Updated workflow structure for multi-platform support
- Enhanced release creation process

## [v2.0.21] - 2025-07-04

### Added
- Electron desktop application
- Windows installer (.exe)

### Changed
- Built with Electron for desktop distribution
- Includes all Python dependencies
- Streamlit web interface wrapped in desktop app 