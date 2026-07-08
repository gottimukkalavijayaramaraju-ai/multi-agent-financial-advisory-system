"""
main.py
FastAPI backend for the Multi-Agent Financial Advisory System.

Run:
    uvicorn api.main:app --reload
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

from core.models import ClientProfile, InvestmentGoal
from core.orchestrator import FinancialAdvisoryOrchestrator

app = FastAPI(
    title="Multi-Agent Financial Advisory System",
    description=(
        "A base multi-agent system where specialized agents (risk, market, "
        "portfolio, tax) collaborate to produce a financial advisory report."
    ),
    version="1.0.0",
)

orchestrator = FinancialAdvisoryOrchestrator()


class ClientProfileRequest(BaseModel):
    name: str
    age: int = Field(..., ge=18, le=100)
    annual_income: float = Field(..., gt=0)
    current_savings: float = Field(..., ge=0)
    monthly_investment_capacity: float = Field(..., ge=0)
    investment_goal: InvestmentGoal
    time_horizon_years: int = Field(..., ge=1, le=50)
    existing_debt: float = Field(0.0, ge=0)
    dependents: int = Field(0, ge=0)
    self_reported_risk_comfort: Optional[str] = None  # "low" | "medium" | "high"


@app.get("/")
def root():
    return {"status": "ok", "service": "Multi-Agent Financial Advisory System"}


@app.post("/api/advisory-report")
async def generate_advisory_report(request: ClientProfileRequest):
    try:
        profile = ClientProfile(
            name=request.name,
            age=request.age,
            annual_income=request.annual_income,
            current_savings=request.current_savings,
            monthly_investment_capacity=request.monthly_investment_capacity,
            investment_goal=request.investment_goal,
            time_horizon_years=request.time_horizon_years,
            existing_debt=request.existing_debt,
            dependents=request.dependents,
            self_reported_risk_comfort=request.self_reported_risk_comfort,
        )
        report = await orchestrator.run(profile)
        return report.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/investment-goals")
def list_investment_goals():
    return [goal.value for goal in InvestmentGoal]
