# happy-simulator
Simulate event driven systems in a few lines of Python code.

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0) 
![PyPI](https://img.shields.io/pypi/v/happysimulator)

## Quick Start
```sh
pip install happysimulator
```

To configure logging, set your `HS_LOGGING` environment variable to `DEBUG`, `INFO`, `WARNING`, `ERROR`. Default is `INFO`.

## Maintainers
- [AdamCyber1](https://github.com/adamcyber1)

## Tutorials 
See `examples/` folder for examples.

## Development Plan
* Add oX and uX statistics (i.e. over X and under X)
* Add Server lambdas for arbitrarily complex server behavior
* Add Java ExecutorService pipeline simulation components and example
* Load balancer entity
* Retry explosion example 
* Full unit test coverage