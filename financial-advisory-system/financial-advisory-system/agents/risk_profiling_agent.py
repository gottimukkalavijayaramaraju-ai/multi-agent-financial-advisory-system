"""
risk_profiling_agent.py
Assesses the client's risk tolerance using a scoring model that blends
objective factors (age, time horizon, income stability proxy, debt) with
the client's self-reported comfort level.
"""

import asyncio

from agents.base_agent import BaseAgent
from core.models import ClientProfile, AgentRecommendation, RiskTolerance


class RiskProfilingAgent(BaseAgent):
    name = "RiskProfilingAgent"

    async def analyze(self, profile: ClientProfile, context: dict) -> AgentRecommendation:
        await asyncio.sleep(0)  # yield control point (placeholder for real async I/O)

        score = 0

        # Age: younger clients can typically absorb more risk
        if profile.age < 30:
            score += 3
        elif profile.age < 45:
            score += 2
        elif profile.age < 60:
            score += 1
        else:
            score += 0

        # Time horizon
        if profile.time_horizon_years >= 15:
            score += 3
        elif profile.time_horizon_years >= 7:
            score += 2
        elif profile.time_horizon_years >= 3:
            score += 1

        # Debt-to-income ratio (lower debt -> more risk capacity)
        dti = profile.existing_debt / max(profile.annual_income, 1)
        if dti < 0.1:
            score += 2
        elif dti < 0.3:
            score += 1

        # Savings cushion relative to income
        savings_ratio = profile.current_savings / max(profile.annual_income, 1)
        if savings_ratio > 1.0:
            score += 2
        elif savings_ratio > 0.3:
            score += 1

        # Dependents reduce risk capacity slightly
        score -= min(profile.dependents, 3)

        # Self-reported comfort adjusts the score
        comfort_map = {"low": -2, "medium": 0, "high": 2}
        if profile.self_reported_risk_comfort:
            score += comfort_map.get(profile.self_reported_risk_comfort.lower(), 0)

        # Map score to a risk tolerance bucket
        if score >= 7:
            risk = RiskTolerance.AGGRESSIVE
        elif score >= 3:
            risk = RiskTolerance.MODERATE
        else:
            risk = RiskTolerance.CONSERVATIVE

        warnings = []
        if dti > 0.4:
            warnings.append("High debt-to-income ratio — consider debt reduction before aggressive investing.")
        if savings_ratio < 0.15:
            warnings.append("Low emergency savings cushion relative to income.")

        return AgentRecommendation(
            agent_name=self.name,
            summary=f"Risk tolerance assessed as {risk.value} (score: {score}).",
            details={
                "risk_score": score,
                "risk_tolerance": risk.value,
                "debt_to_income_ratio": round(dti, 2),
                "savings_to_income_ratio": round(savings_ratio, 2),
            },
            confidence=0.85,
            warnings=warnings,
        )
