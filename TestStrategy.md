# Test Automation Strategy

## Purpose of the project

This repository represents a **portfolio project**, not a complete regression suite.

Its primary goal is to demonstrate the design and implementation of Python UI/API automation framework using realistic business scenarios.

The selected test cases were intentionally chosen to showcase different automation techniques, architecture decisions, and testing approaches rather than duplicate similar CRUD operations.

---

# Test Selection and Coverage Philosophy

This project is **not intended to achieve 100% functional coverage**.

The selected test cases were intentionally chosen to demonstrate framework design, automation architecture, and different testing techniques rather than achieve full functional coverage.

**If this were a real commercial project**, I would build the automation strategy according to the **Test Pyramid** and business priorities.

---

### API Layer

The API layer would serve as the foundation of the automation suite.

Most business logic would be validated here because API tests are faster, more stable, easier to maintain, and provide more deterministic results than UI automation.

The API test suite would typically include:

- Complete CRUD operations for all business entities
- Positive and negative scenarios
- Boundary value analysis
- Missing and invalid data validation
- Authentication and authorization scenarios
- Requests without authentication
- Response schema validation
- Complete business workflows executed entirely through the API

Whenever possible, end-to-end business flows would also be implemented on the API layer to achieve fast and reliable verification without UI-related instability and slowness.

For projects with database access, integration tests would additionally verify that the data existed in the database matches the data returned by the API.

---

### UI Layer

UI automation would focus on validating the application's user experience rather than repeating API verification.

Most UI tests would:

- prepare test data through the API or database;
- execute a single business scenario through the user interface;
- verify one logical workflow covering one or two screens;
- remain independent from other UI tests.

This approach keeps UI automation:

- stable;
- fast;
- deterministic;
- easy to maintain.

UI tests should validate that the interface correctly interacts with the backend, rather than duplicate business logic already covered at the API level.

---

### End-to-End UI Scenarios

Long UI end-to-end scenarios would be implemented only when they provide clear business value.

Such tests are typically slower, more fragile, and more expensive to maintain, therefore they should cover only the most critical user journeys.

The decision to automate large end-to-end scenarios should always be aligned with the team, project priorities, and stakeholder expectations.

---

## Portfolio Scope

Since this project is intended to demonstrate automation engineering skills rather than provide complete regression coverage, the implemented test suite focuses on representative scenarios that showcase:

- framework architecture;
- API automation;
- UI automation;
- integration between application layers;
- reusable test design;
- maintainability and scalability.

### What Is Intentionally Not Covered

The following scenarios were intentionally excluded:

- Duplicate CRUD combinations
- Repetitive validation tests
- Browser compatibility matrix
- Full regression suite
- Performance testing
- Full Security testing
- Accessibility testing

These areas are outside the scope of this portfolio project.

---

## Coverage Matrix

| Feature         |   API   | Customer UI | Admin UI  | Integration | Reason                                                                                |
|-----------------|:-------:|:-----------:|:---------:|:-----------:|---------------------------------------------------------------------------------------|
| Authentication  |    ✅    |      —      | Partially |      —      | Authentication is a critical business feature and demonstrates authorization testing. |
| Room Management | Partial |    Read     |     —     |      —      | Covers business entities and data synchronization across application layers.          |
| Booking         | Partial |   Create    |  Manage   |      —      | Core business functionality of the application.                                       |
| Branding        |    —    |   Display   |     —     |      —      | Demonstrate data visibility from API.                                                 |
| Messages        |    —    |      —      |  Display  |      ✅      | Covers asynchronous business flow.                                                    |
| Reporting       |    —    |      —      |  Display  |      ✅      | Verifies that reporting reflects backend data correctly.                              |
---

## Layer Responsibilities

### API Tests

Purpose:

- Business logic
- CRUD operations
- Response validation
- Authentication
- Negative scenarios
- Schema validation
- 
---

### Customer UI Tests

Purpose:

- End-user workflows
- Form validation
- Content rendering
- Navigation

API is used only for:

- test data preparation
- data verification

Customer UI never depends on Admin UI.

---

### Admin UI Tests

Purpose:

- Administrative workflows
- Data management
- Validation
- Reporting

API is used only for:

- preparing test data
- verifying persisted changes

Admin UI never depends on Customer UI.

---

### Integration Tests

Integration tests verify synchronization between application layers.

Only the following directions are used:

API → Customer UI

API → Admin UI

These scenarios are stable, deterministic, and easy to maintain.

The opposite direction (UI → API → Admin) was intentionally avoided because it introduces multiple failure points while providing little additional testing value.
