# v1.0.0-alpha

## Features / Fixes

- :new: Created the `EmailHTMLGenerator` class
- :new: Added unit tests for `EmailHTMLGenerator` class.
- :new: Added fixtures for mock configuration and YAML file.
- :new: Added property-based tests using Hypothesis for generating HTML with random titles, alt text, and image paths.
- :hammer_and_wrench: Updated `EmailHTMLGenerator` class to correctly load YAML configuration using `yaml.safe_load`.
- :hammer_and_wrench: Refactored test functions to use `mock.patch` for simulating file system interactions.
- :bug: Fixed `AttributeError: 'str' object has no attribute 'get'` by ensuring the configuration is loaded as a dictionary.
- :bug: Fixed `TypeError: missing required positional arguments` by correctly passing fixtures to test functions.

## Docs

- :memo: Created initial documentation for the HTML Email Generator.
- :memo: Added details on how to run tests and use the `EmailHTMLGenerator` class.
