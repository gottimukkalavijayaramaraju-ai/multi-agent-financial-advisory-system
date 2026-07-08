"""
market_analysis_agent.py
Provides a market outlook based on (mocked) macro indicators. In a real
system this agent would call out to live market data / news sentiment APIs.
"""

import asyncio

from agents.base_agent import BaseAgent
from core.models import ClientProfile, AgentRecommendation
from core.market_data import get_mock_market_snapshot


class MarketAnalysisAgent(BaseAgent):
    name = "MarketAnalysisAgent"

    async def analyze(self, profile: ClientProfile, context: dict) -> AgentRecommendation:
        await asyncio.sleep(0)

        snapshot = get_mock_market_snapshot()

        outlook_parts = []
        if snapshot["equity_trend"] == "BULLISH":
            outlook_parts.append("Equities are showing bullish momentum.")
        elif snapshot["equity_trend"] == "BEARISH":
            outlook_parts.append("Equities are under bearish pressure; consider a defensive tilt.")
        else:
            outlook_parts.append("Equity markets are range-bound with no strong directional signal.")

        if snapshot["interest_rate_environment"] == "RISING":
            outlook_parts.append("Rising rates favor shorter-duration bonds over long-duration debt.")
        elif snapshot["interest_rate_environment"] == "FALLING":
            outlook_parts.append("Falling rates are generally supportive of bond prices and REITs.")
        else:
            outlook_parts.append("Interest rates are stable, providing a predictable fixed-income backdrop.")

        if snapshot["inflation_outlook"] == "HIGH":
            outlook_parts.append("Elevated inflation supports an allocation to gold and real assets.")

        warnings = []
        if snapshot["volatility_index"] > 25:
            warnings.append(f"Elevated volatility index ({snapshot['volatility_index']}) — expect larger price swings.")

        top_sector = max(snapshot["sector_momentum"], key=snapshot["sector_momentum"].get)

        return AgentRecommendation(
            agent_name=self.name,
            summary=" ".join(outlook_parts),
            details={
                "market_snapshot": snapshot,
                "strongest_sector_momentum": top_sector,
            },
            confidence=0.7,  # market views are inherently less certain
            warnings=warnings,
        )
