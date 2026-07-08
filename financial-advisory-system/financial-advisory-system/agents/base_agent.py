"""
base_agent.py
Abstract base class that every specialized agent implements.
Using asyncio so the orchestrator can run agents concurrently.
"""

from abc import ABC, abstractmethod
from core.models import ClientProfile, AgentRecommendation


class BaseAgent(ABC):
    name: str = "BaseAgent"

    @abstractmethod
    async def analyze(self, profile: ClientProfile, context: dict) -> AgentRecommendation:
        """
        Analyze the client profile (and any shared context produced by
        earlier agents) and return a structured recommendation.
        """
        raise NotImplementedError
