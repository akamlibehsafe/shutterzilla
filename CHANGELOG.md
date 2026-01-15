# Changelog

All notable changes to ShutterZilla will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

- Keep short notes here as you work; move to a release section when you tag

## 0.2.0 - 2026-01-13

### Added
- Mobile-responsive mockups (v2) for all 26 pages
- Comprehensive tech stack documentation (tech-stack-guide.md, tech-stack-final.md)
- Implementation planning documents with 10-phase plan
- Validation plan for scraping feasibility testing
- Project structure reorganization with clear separation (apps/, infrastructure/, docs/)
- Folder structure documentation

### Changed
- Reorganized documentation: consolidated `documentation/` into `docs/` folder
- Renamed `mockups/` to `mockupsv1/` for clarity
- Moved all specification markdown files to `docs/specification/`
- Updated root README with comprehensive project overview
- Fixed logo distortion issues on authentication pages
- Made `resize_logo.py` script portable (removed hardcoded paths)

### Fixed
- Logo horizontal compression on all authentication pages
- Incorrect active tab state on collection detail page

## 0.1.0 - 2026-01-12

### Added
- Initial design and documentation handoff
- 26 interactive HTML/CSS mockups covering all platform pages
- Complete documentation package:
  - Design system (colors, typography, spacing)
  - Functional requirements
  - Component library
  - Data models
  - Key decisions log
- Live presentation and project homepage
- Comprehensive page inventory with sitemap
