"""Synthetic data generation for Account Propensity Copilot demo."""
from __future__ import annotations

import csv
from dataclasses import asdict, dataclass
from pathlib import Path
import random
from typing import Dict, List

DATA_DIR = Path(__file__).resolve().parent / "data"


@dataclass
class AccountRecord:
    account_name: str
    industry: str
    subindustry: str
    revenue_band: str
    employee_band: str
    region: str
    tech_stack: str
    cloud_provider: str
    digital_maturity: str
    modernization_gap: str
    engineering_hiring_trend: str
    funding_stage: str
    product_launch_signal: str
    m_and_a_signal: str
    layoffs_signal: str
    ai_adoption_signal: str
    historical_outcome: str
    similarity_to_past_wins: float


def _generate_company_name(rng: random.Random) -> str:
    prefixes = [
        "Nova", "Blue", "Quantum", "Vertex", "Apex", "Core", "Sky", "Pulse", "Nimbus", "Forge",
        "Opti", "Helio", "Bright", "North", "Next", "Prime", "Lumen", "Terra", "Cyber", "Delta",
    ]
    suffixes = [
        "Soft", "Systems", "Cloud", "Labs", "Dynamics", "Works", "Logic", "Platform", "Tech", "Flow",
        "Matrix", "Edge", "One", "Solutions", "Digital", "Vista", "Bridge", "Stack", "Scale", "Grid",
    ]
    return f"{rng.choice(prefixes)} {rng.choice(suffixes)}"


def _pick_tech_stack(rng: random.Random) -> str:
    stacks = [
        "Java, Spring, React",
        "Python, Django, React",
        "Node.js, TypeScript, React",
        "Java, Kotlin, Angular",
        "C#, .NET, Azure DevOps",
        "Go, Kubernetes, React",
        "PHP, Laravel, Vue",
        "Legacy .NET, jQuery, SQL Server",
        "Java, Kafka, Microservices",
    ]
    return rng.choice(stacks)


def _weighted_choice(rng: random.Random, choices: List[str], weights: List[int]) -> str:
    return rng.choices(choices, weights=weights, k=1)[0]


def _generate_accounts(count: int, historical: bool, rng: random.Random) -> List[Dict]:
    industries = [
        "FinTech", "HealthTech", "Retail & eCommerce", "Manufacturing", "Media & Entertainment",
        "Travel & Hospitality", "SaaS", "Logistics", "EdTech", "InsurTech",
    ]
    subindustries = {
        "FinTech": ["Payments", "Lending", "Digital Banking"],
        "HealthTech": ["Provider Platforms", "Care Coordination", "Health Analytics"],
        "Retail & eCommerce": ["Marketplace", "D2C", "Omnichannel Retail"],
        "Manufacturing": ["Industrial IoT", "Supply Chain", "Smart Factory"],
        "Media & Entertainment": ["Streaming", "AdTech", "Gaming Platforms"],
        "Travel & Hospitality": ["Booking Platforms", "Loyalty Tech", "Travel Operations"],
        "SaaS": ["Developer Tools", "B2B Productivity", "Workflow Automation"],
        "Logistics": ["Fleet Tech", "Warehouse Automation", "Routing Platforms"],
        "EdTech": ["Learning Platforms", "Assessment Tech", "Student Success"],
        "InsurTech": ["Claims Automation", "Policy Admin", "Risk Analytics"],
    }

    rows: list[AccountRecord] = []
    used_names = set()

    for _ in range(count):
        name = _generate_company_name(rng)
        while name in used_names:
            name = _generate_company_name(rng)
        used_names.add(name)

        industry = _weighted_choice(rng, industries, [14, 12, 10, 8, 8, 7, 15, 8, 7, 11])
        subindustry = rng.choice(subindustries[industry])
        revenue = _weighted_choice(rng, ["$50M-$200M", "$200M-$1B", "$1B-$5B", "$5B+"], [30, 35, 25, 10])
        employees = _weighted_choice(rng, ["200-500", "500-2000", "2000-10000", "10000+"], [25, 45, 23, 7])
        region = _weighted_choice(rng, ["North America", "EMEA", "APAC", "LATAM"], [40, 25, 25, 10])
        cloud = _weighted_choice(rng, ["AWS", "Azure", "GCP", "Multi-cloud", "On-prem heavy"], [30, 24, 14, 24, 8])
        digital = _weighted_choice(rng, ["Low", "Medium", "High"], [25, 50, 25])
        mod_gap = _weighted_choice(rng, ["Low", "Medium", "High"], [20, 45, 35])
        hiring = _weighted_choice(rng, ["Declining", "Stable", "Growing", "Surging"], [12, 35, 35, 18])
        funding = _weighted_choice(rng, ["Bootstrapped", "Series B", "Series C", "Series D+", "Public"], [10, 15, 20, 25, 30])
        launch = _weighted_choice(rng, ["Yes", "No"], [35, 65])
        mna = _weighted_choice(rng, ["Yes", "No"], [20, 80])
        layoffs = _weighted_choice(rng, ["Yes", "No"], [18, 82])
        ai = _weighted_choice(rng, ["Low", "Medium", "High"], [20, 45, 35])
        sim = round(rng.uniform(0.3, 0.95), 2)

        outcome = "N/A"
        if historical:
            score_proxy = 0
            if industry in {"FinTech", "HealthTech", "Retail & eCommerce", "SaaS", "InsurTech"}:
                score_proxy += 2
            if cloud in {"AWS", "Azure", "Multi-cloud"}:
                score_proxy += 1
            if hiring in {"Growing", "Surging"}:
                score_proxy += 1
            if layoffs == "Yes":
                score_proxy -= 2
            if mod_gap in {"Medium", "High"}:
                score_proxy += 1
            if ai in {"Medium", "High"}:
                score_proxy += 1
            if sim > 0.7:
                score_proxy += 2
            outcome = "Won" if score_proxy >= 4 else "Lost"

        rows.append(
            AccountRecord(
                account_name=name,
                industry=industry,
                subindustry=subindustry,
                revenue_band=revenue,
                employee_band=employees,
                region=region,
                tech_stack=_pick_tech_stack(rng),
                cloud_provider=cloud,
                digital_maturity=digital,
                modernization_gap=mod_gap,
                engineering_hiring_trend=hiring,
                funding_stage=funding,
                product_launch_signal=launch,
                m_and_a_signal=mna,
                layoffs_signal=layoffs,
                ai_adoption_signal=ai,
                historical_outcome=outcome,
                similarity_to_past_wins=sim,
            )
        )

    return [asdict(r) for r in rows]


def _build_opportunities(accounts: List[Dict], rng: random.Random) -> List[Dict]:
    rows: List[Dict] = []
    service_lines = ["Cloud Modernization", "Platform Engineering", "AI Enablement", "Digital Product", "Legacy Modernization"]

    for row in accounts:
        if row["historical_outcome"] in {"Won", "Lost"}:
            rows.append(
                {
                    "account_name": row["account_name"],
                    "opportunity_name": f"{row['account_name']} - {rng.choice(service_lines)}",
                    "stage": "Closed Won" if row["historical_outcome"] == "Won" else "Closed Lost",
                    "amount_usd": rng.randint(200_000, 4_500_000),
                    "service_line": rng.choice(service_lines),
                    "close_quarter": rng.choice(["2024-Q4", "2025-Q1", "2025-Q2", "2025-Q3", "2025-Q4"]),
                }
            )

    prospects = [a for a in accounts if a["historical_outcome"] == "N/A"]
    rng.shuffle(prospects)
    for row in prospects[:18]:
        rows.append(
            {
                "account_name": row["account_name"],
                "opportunity_name": f"{row['account_name']} - Growth Initiative",
                "stage": rng.choice(["Discovery", "Scoping", "Proposal", "Negotiation"]),
                "amount_usd": rng.randint(150_000, 3_200_000),
                "service_line": rng.choice(service_lines),
                "close_quarter": rng.choice(["2026-Q1", "2026-Q2", "2026-Q3"]),
            }
        )
    return rows


def _build_external_signals(accounts: List[Dict], rng: random.Random) -> List[Dict]:
    rows: List[Dict] = []
    for row in accounts:
        rows.append(
            {
                "account_name": row["account_name"],
                "news_velocity": rng.choice(["Low", "Medium", "High"]),
                "job_postings_change_pct": rng.randint(-20, 55),
                "cloud_spend_growth_pct": rng.randint(-10, 45),
                "ai_initiative_count": rng.randint(0, 8),
                "intent_signal_strength": rng.choice(["Weak", "Moderate", "Strong"]),
            }
        )
    return rows


def _write_csv(path: Path, rows: List[Dict]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def generate_demo_data(seed: int = 21) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    rng = random.Random(seed)

    historical = _generate_accounts(count=25, historical=True, rng=rng)
    prospects = _generate_accounts(count=60, historical=False, rng=rng)
    accounts = historical + prospects

    opportunities = _build_opportunities(accounts, rng)
    external = _build_external_signals(accounts, rng)

    _write_csv(DATA_DIR / "salesforce_accounts.csv", accounts)
    _write_csv(DATA_DIR / "salesforce_opportunities.csv", opportunities)
    _write_csv(DATA_DIR / "external_company_signals.csv", external)


if __name__ == "__main__":
    generate_demo_data()
    print("Synthetic demo data generated under ./data")
