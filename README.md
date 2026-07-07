# Vehicle Validation Framework

A Python-based validation framework for testing simulated vehicle software systems.

I started this project to learn more about the kind of software infrastructure used behind the scenes in the automotive industry. As vehicles become increasingly software-defined, a huge amount of engineering goes into validating that every system behaves correctly before software is released. This project is my attempt to build a simplified version of that tooling from the ground up.

Rather than focusing on building the vehicle itself, the goal is to build the framework around it—automated tests, logging, reporting, and eventually fault injection and AI-assisted debugging.

---

## Current Features

### Vehicle Simulator

The simulator currently includes several core vehicle subsystems:

- Battery
- Door locks
- Climate control
- Sleep / Wake state

Each subsystem is implemented independently and managed through a central `Vehicle` class.

---

### Validation Framework

Current functionality includes:

- Automated test execution with `pytest`
- HTML test report generation
- Structured logging
- Custom exception hierarchy
- Reusable testing framework
- Configurable project settings

The framework is designed so that adding a new subsystem only requires implementing the subsystem itself and writing the corresponding validation tests.

---

## Current Test Coverage

The project currently validates functionality including:

- Door locking and unlocking
- Battery state management
- Charging behavior
- Climate control
- Vehicle sleep/wake transitions
- Invalid operating conditions
- Battery safety checks

More tests are continually being added as new vehicle functionality is implemented.

---

## Project Structure

```
Vehicle Validation Framework
│
├── api/
├── framework/
├── simulator/
├── tests/
├── reports/
├── requirements.txt
└── README.md
```

---

## Technologies

- Python
- FastAPI
- pytest
- pytest-html
- Requests
- Pydantic
- Git

---

## Running the Project

Install dependencies

```bash
pip install -r requirements.txt
```

Start the API

```bash
uvicorn api.app:app --reload
```

Run the validation suite

```bash
python framework/test_runner.py
```

or

```bash
pytest tests
```

Generated reports are saved in the `reports/` directory.

---

## Why I Built This

I'm interested in pursuing software automation within the automotive industry, particularly around vehicle software validation and testing. Most personal projects focus on building applications for end users, but I wanted to build something that more closely resembles an internal engineering tool.

This project has been a way to explore topics like software architecture, automated testing, API development, logging, and validation infrastructure while creating something that's directly related to the kind of work I'd like to do professionally.

---

## Roadmap

There are still a lot of features I'd like to add, including:

- Fault injection for testing failure scenarios
- Scenario-based testing
- More comprehensive validation coverage
- AI-assisted log analysis
- Improved reporting and test metrics

The long-term goal is to continue expanding the project into something that resembles a real internal vehicle software validation platform.

---

## Author

**Carson Apple**
Northwestern University

Computer Engineering & Economics
