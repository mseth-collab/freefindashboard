"""Interpretable scoring logic for Account Propensity Copilot."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple

import pandas as pd

TARGET_INDUSTRIES = {"FinTech", "HealthTech", "Retail & eCommerce", "SaaS", "InsurTech"}
EXADEL_STRENGTH_KEYWORDS = {
    "Java", "Spring", "React", "Node.js", "TypeScript", "Kubernetes", "Microservices", "Azure", "Python",
}


@dataclass
class ScoreResult:
    fit_score: int
    propensity_score: int
    total_score: int
    account_tier: str
    top_signal: str
    drivers: List[str]


def _clamp(value: int, low: int, high: int) -> int:
    return max(low, min(high, value))


def _fit_score_breakdown(row: pd.Series) -> Tuple[int, Dict[str, int], List[str]]:
    breakdown = {
        "industry_alignment": 0,
        "tech_stack_match": 0,
        "size_sweet_spot": 0,
        "modernization_opportunity": 0,
    }
    drivers: list[str] = []

    if row["industry"] in TARGET_INDUSTRIES:
        breakdown["industry_alignment"] = 14
        drivers.append(f"Strong sector fit in {row['industry']}")
    else:
        breakdown["industry_alignment"] = 6

    tech_tokens = {t.strip() for t in row["tech_stack"].replace(".", "").split(",")}
    matched = len(tech_tokens.intersection(EXADEL_STRENGTH_KEYWORDS))
    breakdown["tech_stack_match"] = _clamp(4 + matched * 3, 4, 14)
    if breakdown["tech_stack_match"] >= 10:
        drivers.append("Tech stack aligns with Exadel delivery strengths")

    size_points = {
        "200-500": 8,
        "500-2000": 12,
        "2000-10000": 10,
        "10000+": 6,
    }
    breakdown["size_sweet_spot"] = size_points.get(row["employee_band"], 8)

    maturity_gap = (row["digital_maturity"], row["modernization_gap"])
    gap_matrix = {
        ("Low", "High"): 10,
        ("Medium", "High"): 10,
        ("Low", "Medium"): 8,
        ("Medium", "Medium"): 7,
        ("High", "High"): 6,
        ("High", "Medium"): 5,
        ("Medium", "Low"): 4,
        ("Low", "Low"): 5,
        ("High", "Low"): 3,
    }
    breakdown["modernization_opportunity"] = gap_matrix.get(maturity_gap, 5)
    if breakdown["modernization_opportunity"] >= 8:
        drivers.append("Visible modernization gap indicates transformation potential")

    fit_score = _clamp(sum(breakdown.values()), 0, 50)
    return fit_score, breakdown, drivers


def _propensity_score_breakdown(row: pd.Series) -> Tuple[int, Dict[str, int], List[str]]:
    breakdown = {
        "engineering_hiring": 0,
        "cloud_ai_signals": 0,
        "funding_growth": 0,
        "market_activity": 0,
    }
    drivers: list[str] = []

    hiring_scores = {"Declining": 2, "Stable": 6, "Growing": 10, "Surging": 14}
    breakdown["engineering_hiring"] = hiring_scores.get(row["engineering_hiring_trend"], 6)
    if breakdown["engineering_hiring"] >= 10:
        drivers.append("Engineering hiring momentum suggests active investment")

    cloud_points = 5 if row["cloud_provider"] in {"AWS", "Azure", "Multi-cloud", "GCP"} else 2
    ai_points = {"Low": 2, "Medium": 5, "High": 8}.get(row["ai_adoption_signal"], 4)
    breakdown["cloud_ai_signals"] = _clamp(cloud_points + ai_points, 0, 14)
    if breakdown["cloud_ai_signals"] >= 10:
        drivers.append("Cloud and AI trajectory supports near-term transformation buying")

    funding_scores = {"Bootstrapped": 4, "Series B": 8, "Series C": 10, "Series D+": 12, "Public": 11}
    breakdown["funding_growth"] = funding_scores.get(row["funding_stage"], 7)

    activity = 0
    if row["product_launch_signal"] == "Yes":
        activity += 5
    if row["m_and_a_signal"] == "Yes":
        activity += 4
    if row["layoffs_signal"] == "Yes":
        activity -= 4
    breakdown["market_activity"] = _clamp(activity + 5, 0, 10)
    if breakdown["market_activity"] >= 8:
        drivers.append("Recent launch / M&A activity creates urgency for execution support")

    propensity_score = _clamp(sum(breakdown.values()), 0, 50)
    return propensity_score, breakdown, drivers


def _tier(total_score: int) -> str:
    if total_score >= 75:
        return "Hot"
    if total_score >= 55:
        return "Warm"
    return "Cold"


def score_accounts(accounts_df: pd.DataFrame) -> pd.DataFrame:
    scored_rows = []

    for _, row in accounts_df.iterrows():
        fit, fit_breakdown, fit_drivers = _fit_score_breakdown(row)
        prop, prop_breakdown, prop_drivers = _propensity_score_breakdown(row)
        total = fit + prop
        tier = _tier(total)

        all_drivers = fit_drivers + prop_drivers
        if not all_drivers:
            all_drivers = ["Balanced profile with no extreme drivers"]

        top_signal = max(
            {
                "Industry Fit": fit_breakdown["industry_alignment"],
                "Tech Match": fit_breakdown["tech_stack_match"],
                "Hiring Momentum": prop_breakdown["engineering_hiring"],
                "Cloud/AI Signals": prop_breakdown["cloud_ai_signals"],
                "Market Activity": prop_breakdown["market_activity"],
            }.items(),
            key=lambda x: x[1],
        )[0]

        scored = row.to_dict()
        scored.update(
            {
                "fit_score": fit,
                "propensity_score": prop,
                "total_score": total,
                "account_tier": tier,
                "top_signal": top_signal,
                "fit_breakdown": fit_breakdown,
                "propensity_breakdown": prop_breakdown,
                "drivers": all_drivers,
            }
        )
        scored_rows.append(scored)

    scored_df = pd.DataFrame(scored_rows).sort_values("total_score", ascending=False).reset_index(drop=True)
    return scored_df
