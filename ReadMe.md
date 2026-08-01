https://github.com/mwinteringham/restful-booker-platform/tree/trunk
https://automationintesting.online/api/auth/swagger-ui/index.html

# Python QA Automation Framework

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-Framework-0A9EDC?logo=pytest)
![Playwright](https://img.shields.io/badge/Playwright-UI%20Automation-2EAD33?logo=playwright)
![Allure](https://img.shields.io/badge/Allure-Reporting-EE6C4D)
![Pydantic](https://img.shields.io/badge/Pydantic-Validation-E92063)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-CI-2088FF?logo=githubactions)
![Ruff](https://img.shields.io/badge/Ruff-Linter-D7FF64)
![MyPy](https://img.shields.io/badge/MyPy-Type%20Checking-2A6DB2)

Production-style UI & API automation framework built with **Python**, **Pytest** and **Playwright**.

The project demonstrates my vision and implementation of modern QA Automation practices, scalable architecture, clean
code principles, and maintainable test design. It combines UI automation, API testing, reporting, continuous
integration, and reusable framework components into a single repository.

The framework is intended as a portfolio project showcasing modern QA Automation practices.

---

# Project Overview

The project contains automated tests for Customer UI, Admin UI, and API of booking platform:

https://automationintesting.online

The framework is designed with maintainability and scalability in mind and separates UI, API, configuration and test
utilities into independent modules.

[Last Allure test report
](https://anastasiiakravets.github.io/TAF-Restfull-booker-platform/)
---

# Tech Stack

## Core

- Python
- Pytest
- Playwright
- HTTPX

## Supporting Libraries

- Pydantic
- Faker
- Allure
- pytest-xdist
- python-dotenv

## Code Quality

- Ruff
- MyPy

## CI

- GitHub Actions

---

# Current Features

## UI Framework

- Page Object Model
- Reusable UI Components
- Base Page implementation
- Customer and Admin page separation
- Playwright browser manager
- Custom fixtures
- Playwright trace generation on failure
- Multi-browser support
- Headed and Headless execution

---

## API Framework

- HTTPX based API client
- Dedicated clients for different endpoints
- Authentication manager
- Typed Pydantic models
- Request/Response validation
- Shared API fixtures
- Retry policy
- Request info logging

---

## Test Infrastructure

- Environment configuration
- Centralized settings
- Test data generation
- Shared fixtures
- HTML Report
- Allure Report
- Parallel execution support
- GitHub Actions workflow

---

# Architecture

The framework follows a layered architecture.

```
Tests

        ↓

Page Objects / API Clients

        ↓

Components / BaseClient

        ↓

Playwright / HTTPX

        ↓

Application
```

The goal is to keep business logic separated from framework implementation, making tests readable, reusable, and easy to
maintain.

---

# Project Structure

```text
.
├── .github/
│   └── workflows/
│
├── config/
│
├── src/
│   ├── api/
│   │   ├── clients/
│   │   └── models/
│   │
│   ├── ui/
│   │   ├── customer/
│   │   ├── admin/
│   │   ├── components/
│   │   ├── browser/
│   │   └── pages/
│   │
│   ├── data/
│   │
│   └── helpers/
│
├── tests/
│   ├── fixtures/
│   ├── api/
│   └── ui/
│
├── README.md
└── pyproject.toml
```

---

# Reports

The framework currently supports

- Allure Report
- HTML Report
- Playwright Trace on failures integrated into Allure Report

---

# Run Locally

## Clone repository

```bash
git clone <repository-url>

cd <repository-folder>
```

---

## Create virtual environment

Windows

```bash
python -m venv .venv

.venv\Scripts\activate
```

Linux / macOS

```bash
python3 -m venv .venv

source .venv/bin/activate
```

---

## Install dependencies

```bash
pip install -r requirements.txt
```

---

## Install Playwright browsers

```bash
playwright install
```

---

## Configure environment

Create an environment file

```
.env.local
```

using

```
.env.example
```

---

# Running Tests

Run all tests

```bash
pytest
```

Run UI tests

```bash
pytest tests/ui
```

or

```bash
pytest -m ui
```

For headed mode set HEADED = True variable in configuration file.

Run API tests

```bash
pytest tests/api
```

or

```bash
pytest -m api
```

Run tests in parallel

```bash
pytest -n auto
```

Run tests on debug mode

```bash
$env:PWDEBUG=1
pytest -s -k test_name
```
---

# Generate Allure Report

Install Allure according to official documents.

```bash
allure generate allure-results
```

and following

```bash
allure open allure-report
```

View trace

```bash
playwright show-trace trace.zip
```

---

# Continuous Integration

GitHub Actions is configured to automatically:

- install dependencies
- run tests
- generate reports
- perform static code analysis

---

# Planned Improvements

The following improvements are planned for future versions of the framework:

### Framework

- Retry mechanism for unstable operations
- Custom framework exceptions
- Additional CLI options
- Better assertion messages
- Response time assertions

### API

- Retry policy

### Testing

- Integration UI + API scenarios
- Multi-browser execution
- Additional boundary value tests

### Documentation

- Architecture diagram
- Example Allure Report screenshots
- Contributing guide
- Testing strategy improvements

---

# Project Goals

This repository demonstrates:

- scalable automation framework architecture
- maintainable Page Object Model
- reusable API client design
- typed request/response models
- modern Python development practices
- CI integration
- clean project organization
- production-oriented QA Automation approach