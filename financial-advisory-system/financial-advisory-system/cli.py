"""
cli.py
Simple command-line runner for the Multi-Agent Financial Advisory System.
Useful for quick testing without spinning up the API.

Run with a built-in sample profile:
    python cli.py --sample

Run interactively:
    python cli.py
"""

import argparse
import asyncio
import json

from core.models import ClientProfile, InvestmentGoal
from core.orchestrator import FinancialAdvisoryOrchestrator


def build_sample_profile() -> ClientProfile:
    return ClientProfile(
        name="Aditi Sharma",
        age=32,
        annual_income=1_200_000,
        current_savings=500_000,
        monthly_investment_capacity=25_000,
        investment_goal=InvestmentGoal.WEALTH_GROWTH,
        time_horizon_years=15,
        existing_debt=200_000,
        dependents=1,
        self_reported_risk_comfort="medium",
    )


def build_interactive_profile() -> ClientProfile:
    print("Enter client details:")
    name = input("Name: ").strip() or "Client"
    age = int(input("Age: ").strip())
    annual_income = float(input("Annual income: ").strip())
    current_savings = float(input("Current savings: ").strip())
    monthly_capacity = float(input("Monthly investment capacity: ").strip())

    print(f"Investment goals: {[g.value for g in InvestmentGoal]}")
    goal_input = input("Investment goal: ").strip().upper()
    goal = InvestmentGoal(goal_input) if goal_input in InvestmentGoal._value2member_map_ else InvestmentGoal.WEALTH_GROWTH

    horizon = int(input("Time horizon (years): ").strip())
    debt = float(input("Existing debt [0]: ").strip() or 0)
    dependents = int(input("Number of dependents [0]: ").strip() or 0)
    comfort = input("Self-reported risk comfort (low/medium/high) [medium]: ").strip() or "medium"

    return ClientProfile(
        name=name,
        age=age,
        annual_income=annual_income,
        current_savings=current_savings,
        monthly_investment_capacity=monthly_capacity,
        investment_goal=goal,
        time_horizon_years=horizon,
        existing_debt=debt,
        dependents=dependents,
        self_reported_risk_comfort=comfort,
    )


async def main():
    parser = argparse.ArgumentParser(description="Multi-Agent Financial Advisory System CLI")
    parser.add_argument("--sample", action="store_true", help="Run with a built-in sample profile")
    args = parser.parse_args()

    profile = build_sample_profile() if args.sample else build_interactive_profile()

    orchestrator = FinancialAdvisoryOrchestrator()
    report = await orchestrator.run(profile)

    print("\n" + "=" * 70)
    print(f"FINANCIAL ADVISORY REPORT — {report.client_name}")
    print("=" * 70)
    print(json.dumps(report.to_dict(), indent=2))


if __name__ == "__main__":
    asyncio.run(main())
