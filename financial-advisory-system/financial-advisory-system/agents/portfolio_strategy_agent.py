"""
portfolio_strategy_agent.py
Builds an asset allocation recommendation. Depends on the RiskProfilingAgent
and MarketAnalysisAgent having already run — their outputs are passed in via
`context`.
"""

import asyncio

from agents.base_agent import BaseAgent
from core.models import ClientProfile, AgentRecommendation, RiskTolerance
from core.market_data import get_asset_class_returns

# Base allocation templates by risk tolerance (percent of portfolio)
BASE_ALLOCATIONS = {
    RiskTolerance.CONSERVATIVE: {
        "Equity": 20, "International Equity": 5, "Bonds": 45,
        "Gold": 10, "REITs": 5, "Cash/Money Market": 15,
    },
    RiskTolerance.MODERATE: {
        "Equity": 40, "International Equity": 10, "Bonds": 25,
        "Gold": 10, "REITs": 10, "Cash/Money Market": 5,
    },
    RiskTolerance.AGGRESSIVE: {
        "Equity": 55, "International Equity": 20, "Bonds": 10,
        "Gold": 5, "REITs": 8, "Cash/Money Market": 2,
    },
}


class PortfolioStrategyAgent(BaseAgent):
    name = "PortfolioStrategyAgent"

    async def analyze(self, profile: ClientProfile, context: dict) -> AgentRecommendation:
        await asyncio.sleep(0)

        risk_rec = context.get("RiskProfilingAgent")
        market_rec = context.get("MarketAnalysisAgent")

        risk_tolerance = RiskTolerance(
            risk_rec.details["risk_tolerance"] if risk_rec else RiskTolerance.MODERATE.value
        )
        allocation = dict(BASE_ALLOCATIONS[risk_tolerance])

        warnings = []

        # Tilt allocation slightly based on market outlook
        if market_rec:
            snapshot = market_rec.details.get("market_snapshot", {})
            if snapshot.get("equity_trend") == "BEARISH":
                shift = min(10, allocation["Equity"])
                allocation["Equity"] -= shift
                allocation["Bonds"] += shift
                warnings.append("Equity allocation trimmed due to bearish market signal.")
            elif snapshot.get("equity_trend") == "BULLISH" and risk_tolerance != RiskTolerance.CONSERVATIVE:
                shift = min(5, allocation["Cash/Money Market"])
                allocation["Equity"] += shift
                allocation["Cash/Money Market"] -= shift

            if snapshot.get("inflation_outlook") == "HIGH":
                shift = min(5, allocation["Cash/Money Market"])
                allocation["Gold"] += shift
                allocation["Cash/Money Market"] -= shift

        # Normalize to ensure allocation sums to 100
        total = sum(allocation.values())
        allocation = {k: round(v / total * 100, 1) for k, v in allocation.items()}

        # Estimate blended expected return
        returns = get_asset_class_returns()
        expected_return = sum(
            (allocation[asset] / 100) * returns.get(asset, 0) for asset in allocation
        )

        # Monthly investment projection (simple compound growth, no contributions escalation)
        monthly = profile.monthly_investment_capacity
        years = profile.time_horizon_years
        annual_rate = expected_return / 100
        months = years * 12
        monthly_rate = annual_rate / 12
        if monthly_rate > 0:
            projected_value = monthly * (((1 + monthly_rate) ** months - 1) / monthly_rate)
        else:
            projected_value = monthly * months
        projected_value += profile.current_savings * ((1 + annual_rate) ** years)

        if profile.monthly_investment_capacity <= 0:
            warnings.append("No monthly investment capacity provided — projections rely on lump-sum savings only.")

        return AgentRecommendation(
            agent_name=self.name,
            summary=(
                f"Recommended a {risk_tolerance.value.lower()}-oriented portfolio with an estimated "
                f"blended annual return of {expected_return:.1f}%."
            ),
            details={
                "allocation_percent": allocation,
                "expected_annual_return_percent": round(expected_return, 2),
                "projected_value_at_horizon": round(projected_value, 2),
                "time_horizon_years": years,
            },
            confidence=0.75,
            warnings=warnings,
        )
