# Multi-Agent Financial Advisory System

A base project demonstrating a **multi-agent architecture** for financial
advisory. Specialized agents independently analyze different facets of a
client's profile, then a synthesis agent combines their outputs into one
coherent report. Runs fully standalone (rule-based logic, mock market data)
— no external API keys required.

## Architecture

```
                     ClientProfile
                          │
      ┌───────────────────┴───────────────────┐
      │              Stage 1 (parallel)         │
      │  RiskProfilingAgent   MarketAnalysisAgent│
      └───────────────────┬───────────────────┘
                          │  (context)
      ┌───────────────────┴───────────────────┐
      │              Stage 2 (parallel)         │
      │ PortfolioStrategyAgent  TaxPlanningAgent │
      └───────────────────┬───────────────────┘
                          │
                  SynthesisAgent
                          │
                   AdvisoryReport
```

- **RiskProfilingAgent** — scores risk tolerance from age, time horizon, debt-to-income, savings cushion, and self-reported comfort.
- **MarketAnalysisAgent** — produces a market outlook from a mock market snapshot (equity trend, rates, inflation, volatility, sector momentum).
- **PortfolioStrategyAgent** — builds an asset allocation using the risk profile + market outlook, projects portfolio value at the client's time horizon.
- **TaxPlanningAgent** — surfaces simplified, illustrative tax-planning notes (NOT real tax advice).
- **SynthesisAgent** — aggregates all of the above into a final `AdvisoryReport` with concrete action items.

The orchestrator (`core/orchestrator.py`) runs independent agents concurrently with `asyncio.gather`, then runs agents that depend on earlier results, mirroring how a production multi-agent system coordinates work.

## Project Structure

```
financial-advisory-system/
├── agents/
│   ├── __init__.py
│   ├── base_agent.py
│   ├── risk_profiling_agent.py
│   ├── market_analysis_agent.py
│   ├── portfolio_strategy_agent.py
│   ├── tax_planning_agent.py
│   └── synthesis_agent.py
├── core/
│   ├── __init__.py
│   ├── models.py            # ClientProfile, AgentRecommendation, AdvisoryReport
│   ├── market_data.py        # Mock market data provider
│   └── orchestrator.py       # Multi-agent coordinator
├── api/
│   ├── __init__.py
│   └── main.py                # FastAPI app
├── cli.py                      # CLI runner (sample or interactive)
├── requirements.txt
└── README.md
```

## Setup

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Run via CLI

```bash
# Quick run with a built-in sample client
python cli.py --sample

# Interactive prompt for a real client profile
python cli.py
```

## Run via API

```bash
uvicorn api.main:app --reload
```

Visit http://127.0.0.1:8000/docs for interactive API documentation.

### Example request

```bash
curl -X POST http://127.0.0.1:8000/api/advisory-report \
  -H "Content-Type: application/json" \
  -d '{
        "name": "Rahul Verma",
        "age": 29,
        "annual_income": 900000,
        "current_savings": 150000,
        "monthly_investment_capacity": 15000,
        "investment_goal": "RETIREMENT",
        "time_horizon_years": 25,
        "existing_debt": 50000,
        "dependents": 0,
        "self_reported_risk_comfort": "high"
      }'
```

## Extending This Base Project

- **Plug in a real LLM per agent** — each agent's `analyze()` method is the natural place to call the Anthropic API (or another LLM) for richer natural-language reasoning, using the rule-based logic as a fallback/guardrail.
- **Real market data** — replace `core/market_data.py` with a live feed (e.g., a market data API).
- **Persistence** — store `ClientProfile` and `AdvisoryReport` history in a database (SQLite/Postgres).
- **More agents** — e.g., an `InsuranceAgent`, `EstatePlanningAgent`, or `DebtPayoffAgent` — just implement `BaseAgent` and register them in the orchestrator's stages.
- **Human-in-the-loop** — add an approval step before the `SynthesisAgent`'s report is finalized, especially important since this is not licensed financial advice.
- **Frontend** — build a simple Streamlit or React UI on top of the FastAPI endpoints (similar pattern to a dashboard app).

## Disclaimer

This is a demo/educational base project. Tax bands, expected returns, and
allocation logic are simplified and illustrative — they do not constitute
licensed financial or tax advice.
