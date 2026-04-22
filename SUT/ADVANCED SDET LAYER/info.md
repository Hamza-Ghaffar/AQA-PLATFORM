Test Design Principles
✔ Risk-Based Testing
Auth system = HIGH RISK
Prioritize login failure scenarios
✔ Test Pyramid Alignment
70% Functional (UI/API)
20% Negative tests
10% Edge cases
🔁 Data-Driven Testing Strategy

Instead of writing single tests:

Test Matrix:
- Admin / valid password
- Admin / wrong password
- empty / empty
- random / random
🧩 Test Independence Rule
Every test must run independently
No dependency on previous test state
Fresh session per test
🧪 Observability Requirements

Each test must capture:

screenshots on failure
logs of actions
request/response trace (future API layer)
execution time
🔐 Security Awareness Layer

Even in UI testing, include:

brute-force attempt simulation
input sanitization checks
session hijack simulation (later advanced)
⚙️ CI/CD Readiness Criteria

Tests must be:

deterministic
parallelizable
environment-agnostic
CI-safe (no headless issues)