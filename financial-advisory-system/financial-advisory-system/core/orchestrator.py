"""
orchestrator.py
Coordinates the multi-agent pipeline:

  Stage 1 (parallel):  RiskProfilingAgent, MarketAnalysisAgent
  Stage 2 (parallel):  PortfolioStrategyAgent, TaxPlanningAgent
                        (both depend on Stage 1 outputs)
  Stage 3 (final):     SynthesisAgent aggregates everything

This staged-parallel pattern mirrors how a real multi-agent system would
run independent analyses concurrently, then combine dependent results.
"""

import asyncio
from typing import List

from core.models import ClientProfile, AdvisoryReport
from agents.risk_profiling_agent import RiskProfilingAgent
from agents.market_analysis_agent import MarketAnalysisAgent
from agents.portfolio_strategy_agent import PortfolioStrategyAgent
from agents.tax_planning_agent import TaxPlanningAgent
from agents.synthesis_agent import SynthesisAgent


class FinancialAdvisoryOrchestrator:
    def __init__(self):
        self.stage1_agents = [RiskProfilingAgent(), MarketAnalysisAgent()]
        self.stage2_agents = [PortfolioStrategyAgent(), TaxPlanningAgent()]
        self.synthesis_agent = SynthesisAgent()

    async def _run_stage(self, agents: List, profile: ClientProfile, context: dict):
        results = await asyncio.gather(*[agent.analyze(profile, context) for agent in agents])
        for rec in results:
            context[rec.agent_name] = rec
        return results

    async def run(self, profile: ClientProfile) -> AdvisoryReport:
        context: dict = {}

        await self._run_stage(self.stage1_agents, profile, context)
        await self._run_stage(self.stage2_agents, profile, context)
        await self.synthesis_agent.analyze(profile, context)

        return context["final_report"]

    def run_sync(self, profile: ClientProfile) -> AdvisoryReport:
        """Convenience wrapper for non-async callers (e.g. simple scripts)."""
        return asyncio.run(self.run(profile))
