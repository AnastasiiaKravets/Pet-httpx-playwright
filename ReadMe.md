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
[Project Overview](#project-overview)

[Tech Stack](#tech-stack)

[Current Features](#current-features)

[Architecture](#architecture)

[Architectural Trade-offs & Design Decisions](#architectural-trade-offs--design-decisions)

[How to run](#run-locally)

[CI](#continuous-integration)

[Reports](#reports)

[Planned Improvements](#planned-improvements)


# Project Overview

The project contains automated tests for Customer UI, Admin UI, and API of booking platform:

https://automationintesting.online

The framework is designed with maintainability and scalability in mind and separates UI, API, configuration and test
utilities into independent modules.

---

# Project Goals

This repository demonstrates:

- scalable automation framework architecture
- maintainable Page Object Model
- reusable API client design
- typed request/response models
- CI integration
- clean project organization
- production-oriented QA Automation approach

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
- Request info logging with recursive reduction strategy

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

# Architectural Trade-offs & Design Decisions

- **Explicit API Tests vs. Encapsulated Test Setup:**  
  * **No High-Level Domain Wrappers for API Tests:** Tests interact directly via `API_Client` methods (e.g., `api_client.post("/booking", json=payload)`). This keeps API interactions fully visible, making the exact HTTP method, URI, and payload fully transparent right in the test body.
  * **In UI Tests & Fixtures:** Dedicated domain clients (e.g., `BookingClient`, `RoomClient`) are used exclusively for data preparation, pre-conditions, and cleanup. This encapsulates setup logic, keeps UI tests clean, and speeds up test execution.

- **In-Line Schema Validation over Separate Contract Suites:**  
  Schema validation for both requests and responses is embedded directly into each functional API test via strict Pydantic models. Separate contract testing suites were intentionally avoided to eliminate test duplication: every functional test execution automatically acts as a contract check, ensuring payload and response integrity.

- **Custom retry policies for API:**
   Retries only for 429, 502, 503, 504 (Too Many Requests, Bad Gateway, Service Unavailable, Gateway Timeout) status codes. No retry for POST method to prevent possible data inconsistency.

- **Embedded Playwright Trace over Screenshots/Video:**  
  Instead of static screenshots or heavy video overhead, `trace.zip` is automatically generated on test failure and attached directly to the Allure Report. This provides complete DOM state inspection, console logs, and network interception capabilities during debugging.

- **Zero-Tolerance for Flaky Tests (No Auto-Retries):**  
  Automatic test retries are deliberately disabled. Masking test failures with retries degrades confidence in the test suite and hides underlying race conditions or infrastructure instability. Every failure is treated as an actionable defect.

- **Direct Database Layer (Enterprise Approach):**
   In enterprise environments, database-level setup and validation may be preferred for speed and reliability. This framework currently relies on public APIs to remain environment-independent.

- **Strict Environment-Based Configuration:**  
  CLI options were intentionally skipped in favor of centralized `.env` and Environment Variable management, streamlining deployment across local runs and CI/CD runners (GitHub Actions).
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

GitHub Actions is configured to perform automatically:

- install dependencies
- run tests
- generate reports
- perform static code analysis

---

# Reports

The framework currently supports

- Allure Report
- HTML Report
- Playwright Trace on failures integrated into Allure Report

[Last Allure test report
](https://anastasiiakravets.github.io/TAF-Restfull-booker-platform/)

---

# Planned Improvements

The following improvements are planned for future versions of the framework:

### Framework

- Retry mechanism for unstable operations
- Custom framework exceptions
- Better assertion messages
- Response time assertions

### Testing

- Integration UI + API scenarios
- Multi-browser execution
- Additional boundary value tests

### Documentation

- Architecture diagram
- Example Allure Report screenshots
- Contributing guide
- Testing strategy improvements
