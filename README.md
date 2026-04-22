# 🚀 AQA Platform - AI-Powered QA Engine

**Automated Quality Assurance Platform** - A universal, AI-driven testing engine that automatically generates, executes, and analyzes tests for ANY system using advanced LLM reasoning and MCP-based tool orchestration.

---

## 🎯 Core Concept

Transform QA from manual scripting into **intelligent automation**:

```
SUT (Any System) → LLM Understands → AI Generates Tests → MCP Executes → AI Analyzes Failures
```

No hardcoding. No brittle scripts. Just config + intelligence.

---

## 🥇 Example SUT: Saleor

We chose **Saleor** as our reference implementation because it demonstrates all platform capabilities:

### Why Saleor?

✅ **Modern, Real-World System**
- Production-grade e-commerce platform
- Used in actual deployments

✅ **Rich Testing Surface**
- GraphQL API (perfect for AI schema understanding)
- Complex workflows (auth → cart → checkout → payment)
- State management (edge cases, invalid flows)

✅ **Multi-Layer Coverage**
- **Phase 1**: GraphQL API testing (PyTest)
- **Phase 2**: Workflow orchestration (multi-step flows)
- **Phase 3**: UI testing (Playwright) + Failure injection + Chaos testing

✅ **Docker-Ready**
- Easy local setup
- Cloud deployment ready

---

## 🎯 What Gets Tested

### Phase 1: API Foundation

**Authentication & Tokens**
```graphql
mutation {
  tokenCreate(email: "user@example.com", password: "pass") {
    token
    user { id email }
  }
}
```

**Product Queries**
```graphql
query {
  products(first: 10) {
    edges { node { id name price } }
  }
}
```

**Cart Mutations**
```graphql
mutation {
  cartCreate(input: { lines: [{sku: "PRODUCT-1", quantity: 2}] }) {
    cart { id total }
  }
}
```

**Checkout & Orders**
```graphql
mutation {
  checkoutCreate(input: { lines: [...] }) {
    checkout { id }
  }
}
```

### Phase 2: Workflows & Orchestration

**Multi-Step Flows**
- User registration → Login → Browse products → Add to cart → Checkout → Payment

**State Transitions**
- Order status: pending → processing → shipped → delivered

**Edge Cases**
- Invalid tokens → 401 errors
- Out of stock items → 400 errors
- Concurrent cart modifications → Conflict resolution

### Phase 3: UI & Chaos

**Admin Dashboard** (Playwright)
- Create products
- Manage orders
- View analytics

**Storefront** (Playwright)
- Browse products
- Checkout flow
- Account management

**Failure Injection**
- Simulate payment failures
- Network delays
- Rate limiting
- Database timeouts

---

## 🧠 System Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                  USER / RECRUITER                                     │
│         (Dashboard: Create SUT → View Results → AI Insights)          │
└──────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────────┐
│                    AQA PLATFORM (FastAPI Backend)                    │
│                                                                      │
│  ┌────────────────────┐  ┌────────────────────┐  ┌──────────────┐  │
│  │  SUT MANAGEMENT    │  │  TEST ORCHESTRATION │  │  RESULTS     │  │
│  │  - Register SUT    │  │  - Trigger tests    │  │  - Logs      │  │
│  │  - Store configs   │  │  - Manage flows     │  │  - Metrics   │  │
│  │  - Load GraphQL    │  │  - Aggregate results│  │  - Analysis  │  │
│  └────────────────────┘  └────────────────────┘  └──────────────┘  │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │              SUT ADAPTER LAYER (Click-In Architecture)         │ │
│  │  - API Adapter (REST/GraphQL)                                  │ │
│  │  - Database Adapter (SQL validation)                           │ │
│  │  - UI Adapter (Playwright - Phase 2)                           │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │            MCP LAYER (Tool Orchestration)                      │ │
│  │  - generate_tests(sut, count, types)                           │ │
│  │  - run_tests(scenarios)                                        │ │
│  │  - analyze_failures(results)                                   │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │                 AI LAYER (LLM Integration)                     │ │
│  │  - OpenAI (GPT-4 for reasoning)                                │ │
│  │  - Anthropic (Claude for analysis)                             │ │
│  │                                                                │ │
│  │  Functions:                                                   │ │
│  │  • Test generation from GraphQL schema                        │ │
│  │  • Edge case discovery                                        │ │
│  │  • Failure root cause analysis                                │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │           EXECUTION ENGINE (Test Runners)                      │ │
│  │  - PyTest (GraphQL/API tests)                                  │ │
│  │  - Playwright (UI tests - Phase 2)                             │ │
│  └────────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
        ┌────────────────────────────────────────────┐
        │    SALEOR (System Under Test)              │
        │    Docker Container                        │
        │                                            │
        │  ┌──────────────┐  ┌──────────────┐       │
        │  │ GraphQL API  │  │ Auth System  │       │
        │  └──────────────┘  └──────────────┘       │
        │                                            │
        │  ┌──────────────┐  ┌──────────────┐       │
        │  │ Products     │  │ Cart         │       │
        │  │ Service      │  │ Service      │       │
        │  └──────────────┘  └──────────────┘       │
        │                                            │
        │  ┌──────────────┐  ┌──────────────┐       │
        │  │ Checkout     │  │ Orders       │       │
        │  │ Service      │  │ Service      │       │
        │  └──────────────┘  └──────────────┘       │
        │                                            │
        │  ┌──────────────────────────────────┐     │
        │  │ Database (PostgreSQL)            │     │
        │  │ Payments (Stripe Mock)           │     │
        │  └──────────────────────────────────┘     │
        │                                            │
        └────────────────────────────────────────────┘
```




---

## 🔌 SUT Configuration Format

When you register Saleor (or any system), it looks like this:

```json
{
  "name": "saleor-demo",
  "version": "3.0.0",
  "type": "graphql",
  "base_url": "http://localhost:8000/graphql/",
  
  "auth": {
    "type": "token",
    "login_mutation": "tokenCreate",
    "credentials": {
      "email": "admin@example.com",
      "password": "admin123"
    }
  },
  
  "schema": {
    "type": "graphql",
    "endpoint": "/graphql/",
    "introspection": true
  },
  
  "services": {
    "products": {
      "type": "graphql",
      "queries": ["products", "productById"],
      "mutations": ["productCreate", "productUpdate"]
    },
    "orders": {
      "type": "graphql", 
      "queries": ["orders"],
      "mutations": ["orderCreate"]
    },
    "payments": {
      "type": "webhook",
      "endpoint": "/webhooks/payment"
    }
  },
  
  "tags": ["e-commerce", "graphql", "production"],
  "owner": "QA Team"
}
```

---

## 🧠 How AQA Powers Testing

### 1. **Understand the System**

LLM reads Saleor's GraphQL schema and understands:
- Available queries & mutations
- Data types & relationships
- Authentication flow
- Business workflows

### 2. **Generate Tests**

AI Creates scenarios like:

✅ **Positive Tests**
```
Scenario: Complete purchase flow
1. Create user account
2. Login with credentials
3. Query products
4. Add to cart
5. Checkout
6. Payment confirmation
Expected: Order created with status="pending"
```

✅ **Negative Tests**
```
Scenario: Invalid login
1. Attempt login with wrong password
Expected: 401 Unauthorized
```

✅ **Edge Cases**
```
Scenario: Concurrent cart modifications
1. Add 2 items from browser 1
2. Remove 1 item from browser 2 (simultaneous)
Expected: Cart resolves correctly, no data loss
```

### 3. **Execute Tests**

MCP routes to appropriate executor:
- GraphQL → PyTest runner
- UI → Playwright runner
- Webhooks → HTTP mock server

### 4. **Analyze Failures**

LLM analyzes logs and reports:
```json
{
  "root_cause": "Cart item price mismatch due to concurrent currency conversion",
  "severity": "high",
  "affected_service": "checkout-service",
  "remediation": "Implement optimistic locking on cart updates",
  "similar_issues": 3
}
```

---

## 📊 What You Can Demonstrate

### To Recruiters

> "I built an AI-powered QA platform that automatically generates, executes, and analyzes tests for production systems like Saleor. Using LLMs for intelligent test generation and MCP for agent orchestration, the system discovers edge cases without manual scripting, improving coverage while reducing maintenance overhead."

### Technical Highlights

✅ **Full-Stack QA Innovation**
- GraphQL schema parsing
- AI test generation  
- Workflow orchestration
- Failure analysis

✅ **Enterprise Architecture**
- Microservices ready
- Plugin-based adapters
- Cloud deployable
- Production-proven patterns

✅ **Modern Tech Stack**
- FastAPI + Async
- GraphQL integration
- LLM orchestration (MCP)
- PyTest + Playwright

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- UV package manager
- Docker (for Saleor)
- OpenAI or Anthropic API key

### 1. Setup Project

```bash
# Clone and setup
git clone https://github.com/yourusername/aqa-platform.git
cd aqa-platform

# Install dependencies
uv sync --all-extras

# Activate environment
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate  # Windows
```

### 2. Start Saleor (SUT)

```bash
# Using Docker
docker pull mirumee/saleor:latest
docker run -p 8000:8000 mirumee/saleor:latest

# Or use Docker Compose (recommended)
cd saleor-docker
docker-compose up
```

Saleor dashboard: http://localhost:3000
GraphQL endpoint: http://localhost:8000/graphql/

### 3. Register SUT

```bash
# Start AQA server
uv run python -m backend.api.main
```

Register Saleor:
```bash
curl -X POST http://localhost:8001/api/suts/register \
  -H "Content-Type: application/json" \
  -d @saleor-sut-config.json
```

### 4. Generate & Run Tests

```python
from backend.services import TestService
import asyncio

async def run_tests():
    service = TestService()
    
    # Generate tests
    scenarios = await service.generate_tests(
        sut_id="saleor-demo",
        test_count=10
    )
    
    # Execute
    results = await service.run_tests(
        sut_id="saleor-demo",
        scenario_ids=[s["id"] for s in scenarios]
    )
    
    # Analyze
    analysis = await service.analyze_failures(
        sut_id="saleor-demo",
        failed_results=results["failures"]
    )
    
    print(f"✅ Tests passed: {results['passed']}")
    print(f"❌ Tests failed: {results['failed']}")
    print(f"\n🧠 AI Analysis:\n{analysis}")

asyncio.run(run_tests())
```

---

## 📁 Project Structure

```
aqa-platform/
├── backend/                    # FastAPI Core
│   ├── api/                   # REST endpoints
│   ├── sut/                   # SUT abstraction
│   ├── mcp/                   # Tool routing
│   ├── ai/                    # LLM integration
│   ├── execution/             # Test runners
│   ├── services/              # Business logic
│   └── core/                  # Config, database
│
├── frontend/                  # Next.js Dashboard (Phase 2)
├── tests/                     # Platform tests
├── saleor-config/             # Saleor setup
├── docker/                    # Docker configs
├── .github/workflows/         # CI/CD
├── pyproject.toml             # Dependencies
└── README.md                  # This file
```

---

## 🧪 Development Phases

### Phase 1: Foundation ✅
- [x] FastAPI backend
- [x] SUT abstraction layer
- [x] MCP tool router
- [x] GraphQL adapter
- [x] PyTest runner
- [ ] LLM integration
- [ ] Basic test generation

### Phase 2: AI & UI
- [ ] LLM providers (OpenAI, Anthropic)
- [ ] Test generation engine
- [ ] Playwright UI testing
- [ ] Next.js dashboard
- [ ] Result visualization

### Phase 3: Advanced
- [ ] Failure injection (chaos testing)
- [ ] Performance testing
- [ ] Multi-tenant support
- [ ] CI/CD integration
- [ ] Report generation

---

## 🔧 Key Technologies

| Layer | Tech | Purpose |
|-------|------|---------|
| Backend | FastAPI | REST API, async support |
| SUT Adapter | GraphQL Core | Schema parsing |
| API Testing | PyTest | Test execution |
| UI Testing | Playwright | Browser automation |
| AI | OpenAI/Anthropic | Test generation & analysis |
| MCP | Custom Router | Tool orchestration |
| Database | PostgreSQL | Results storage |
| Frontend | Next.js | User dashboard |

---

## 🎓 Learn More

- API Documentation: http://localhost:8001/docs (Swagger UI)
- Saleor Docs: https://docs.saleor.io/
- GraphQL Docs: https://graphql.org/

---

## 🤝 Contributing

Contributions welcome! Areas to enhance:
- Additional SUT adapters (REST, gRPC, WebSocket)
- More LLM providers
- Performance optimizations
- Documentation

---

## 📄 License

MIT License - See LICENSE file

---

## 🙋 Support

Questions? Open an issue on GitHub or check the documentation.

---

## 🚀 What Makes This Special

Unlike traditional QA frameworks:

❌ **NOT** another automation library (Selenium, Cypress)
❌ **NOT** manual test scripting
❌ **NOT** limited to one app

✅ **IS** AI-powered test generation
✅ **IS** Universal SUT support
✅ **IS** Intelligent failure analysis
✅ **IS** Enterprise-ready architecture

This is a **platform** for QA transformation, not just automation scripting.

---

Built with ❤️ for modern QA teams.
