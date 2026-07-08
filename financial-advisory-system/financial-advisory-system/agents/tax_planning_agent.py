"""
tax_planning_agent.py
Surfaces general tax-efficiency considerations based on income level and
investment goal. Uses simplified illustrative tax bands — NOT real tax advice.
"""

import asyncio

from agents.base_agent import BaseAgent
from core.models import ClientProfile, AgentRecommendation, InvestmentGoal


class TaxPlanningAgent(BaseAgent):
    name = "TaxPlanningAgent"

    async def analyze(self, profile: ClientProfile, context: dict) -> AgentRecommendation:
        await asyncio.sleep(0)

        notes = []
        warnings = []

        # Simplified illustrative income bands (NOT real tax law)
        if profile.annual_income > 1_500_000:
            bracket = "Highest illustrative bracket"
            notes.append("Prioritize tax-advantaged retirement accounts and long-term capital gains holding periods.")
        elif profile.annual_income > 700_000:
            bracket = "Mid-to-high illustrative bracket"
            notes.append("Consider tax-saving investment instruments eligible for deductions.")
        else:
            bracket = "Lower illustrative bracket"
            notes.append("Standard tax-advantaged accounts are likely sufficient; focus on growth over tax optimization.")

        if profile.investment_goal == InvestmentGoal.RETIREMENT:
            notes.append("Retirement-focused goal — prioritize accounts with long-term tax deferral benefits.")
        elif profile.investment_goal == InvestmentGoal.SHORT_TERM_SAVINGS:
            notes.append("Short-term goal — be mindful of short-term capital gains tax on early withdrawals.")
            warnings.append("Short time horizon combined with equity-heavy allocations may trigger higher short-term tax exposure.")

        if profile.time_horizon_years < 3 and profile.investment_goal != InvestmentGoal.SHORT_TERM_SAVINGS:
            warnings.append("Short time horizon increases the chance of realizing gains at higher short-term tax rates.")

        return AgentRecommendation(
            agent_name=self.name,
            summary=f"Illustrative tax bracket: {bracket}. {len(notes)} planning note(s) generated.",
            details={
                "illustrative_bracket": bracket,
                "notes": notes,
            },
            confidence=0.6,  # explicitly lower — this is simplified, not real tax advice
            warnings=warnings,
        )
