"""
synthesis_agent.py
Final agent in the pipeline — synthesizes all upstream agent outputs into
a single coherent AdvisoryReport with concrete action items.
"""

import asyncio

from agents.base_agent import BaseAgent
from core.models import ClientProfile, AgentRecommendation, AdvisoryReport


class SynthesisAgent(BaseAgent):
    name = "SynthesisAgent"

    async def analyze(self, profile: ClientProfile, context: dict) -> AgentRecommendation:
        await asyncio.sleep(0)

        risk_rec: AgentRecommendation = context.get("RiskProfilingAgent")
        market_rec: AgentRecommendation = context.get("MarketAnalysisAgent")
        portfolio_rec: AgentRecommendation = context.get("PortfolioStrategyAgent")
        tax_rec: AgentRecommendation = context.get("TaxPlanningAgent")

        action_items = []

        if risk_rec:
            action_items.append(f"Confirmed risk tolerance: {risk_rec.details.get('risk_tolerance')}.")
            action_items.extend(risk_rec.warnings)

        if portfolio_rec:
            alloc = portfolio_rec.details.get("allocation_percent", {})
            alloc_str = ", ".join(f"{k}: {v}%" for k, v in alloc.items())
            action_items.append(f"Target allocation — {alloc_str}.")
            projected = portfolio_rec.details.get("projected_value_at_horizon")
            if projected:
                action_items.append(
                    f"Projected portfolio value in {portfolio_rec.details.get('time_horizon_years')} years: "
                    f"~₹{projected:,.0f} (illustrative, not guaranteed)."
                )
            action_items.extend(portfolio_rec.warnings)

        if tax_rec:
            action_items.extend(tax_rec.details.get("notes", []))
            action_items.extend(tax_rec.warnings)

        if market_rec:
            action_items.extend(market_rec.warnings)

        report = AdvisoryReport(
            client_name=profile.name,
            risk_profile=risk_rec.details.get("risk_tolerance") if risk_rec else "UNKNOWN",
            recommended_allocation=portfolio_rec.details.get("allocation_percent", {}) if portfolio_rec else {},
            market_outlook=market_rec.summary if market_rec else "No market data available.",
            tax_notes=tax_rec.details.get("notes", []) if tax_rec else [],
            action_items=action_items,
            agent_breakdown=[
                r.to_dict() for r in [risk_rec, market_rec, portfolio_rec, tax_rec] if r
            ],
        )

        context["final_report"] = report

        return AgentRecommendation(
            agent_name=self.name,
            summary=f"Synthesized advisory report for {profile.name} combining {len(report.agent_breakdown)} agent inputs.",
            details={"report": report.to_dict()},
            confidence=0.9,
        )
