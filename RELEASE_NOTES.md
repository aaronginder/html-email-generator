# Release Notes

## v1.0.1

### Features / Fixes

- :bug: Fixed relative import for generator module in the cli

## v1.0.0

### Features / Fixes

- :rocket: First stable release of the HTML Email Generator
- :new: Added command-line interface for generating emails
- :new: Implemented support for custom buttons with rounded corners
- :new: Added support for positioning logos in different locations
- :hammer_and_wrench: Improved error handling for missing image files
- :hammer_and_wrench: Enhanced styling options for all email elements
- :bug: Fixed import issues when installing package from GitHub
- :bug: Corrected module imports in CLI component

### Docs

- :memo: Updated installation instructions for pip installation
- :memo: Added comprehensive usage examples for all email components
- :memo: Improved documentation on styling parameters
- :memo: Added sample templates for common email types

### DevOps

- :gear: Finalized semantic-release configuration
- :gear: Implemented branch-based release strategy
- :gear: Added GitHub Actions workflow for automated testing and releases

## v1.0.0-alpha.5

### Features / Fixes

- :new: Added Poetry build system for package management
- :new: Implemented CLI entry point for easier command-line usage
- :hammer_and_wrench: Fixed package structure for proper installation
- :bug: Fixed import path issues in CLI module

### Docs

- :memo: Added instructions for using the CLI tool
- :memo: Updated installation instructions

## v1.0.0-alpha.2

### Features / Fixes

- :new: Created semantic versioning pipeline for automated releases
- :new: Added GitHub Actions workflow for CI/CD with alpha, beta, and stable - release channels
- :new: Configured project structure as an installable Python package
- :hammer_and_wrench: Restructured project to use Poetry for dependency - management
- :hammer_and_wrench: Updated package configuration in pyproject.toml for - proper installation
- :hammer_and_wrench: Improved configuration loading with better error handling
- :bug: Fixed import issues when installing package from GitHub

### Docs

- :memo: Added installation instructions for installing directly from GitHub
- :memo: Updated documentation with usage examples for the package
- :memo: Added release process documentation for contributors
- :memo: Included semantic versioning guidelines for future development
- DevOps
- :gear: Added semantic-release configuration in pyproject.toml
- :gear: Implemented automated versioning based on conventional commits
- :gear: Created branch-based release channels (alpha, beta, stable)

## v1.0.0-alpha.1

### Features / Fixes

- :new: Created the `EmailHTMLGenerator` class
- :new: Added unit tests for `EmailHTMLGenerator` class.
- :new: Added fixtures for mock configuration and YAML file.
- :new: Added property-based tests using Hypothesis for generating HTML with random titles, alt text, and image paths.
- :hammer_and_wrench: Updated `EmailHTMLGenerator` class to correctly load YAML configuration using `yaml.safe_load`.
- :hammer_and_wrench: Refactored test functions to use `mock.patch` for simulating file system interactions.
- :hammer_and_wrench: Add error handling in `EmailHTMLGenerator`
- :hammer_and_wrench: add logging functionality and removed print statements for robust logging for processing purposes
- :hammer_and_wrench: removed unused images from assets folder
- :bug: Fixed `AttributeError: 'str' object has no attribute 'get'` by ensuring the configuration is loaded as a dictionary.
- :bug: Fixed `TypeError: missing required positional arguments` by correctly passing fixtures to test functions.

### Docs

- :memo: Created initial documentation for the HTML Email Generator.
- :memo: Added details on how to run tests and use the `EmailHTMLGenerator` class.
- :memo: Add sample config to see how to configure YAML files used by the generator
- :memo: Add sample images to README
- :memo: Add markdown lint configuration file for linting README file
