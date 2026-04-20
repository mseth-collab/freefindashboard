"""Decision intelligence layer for account recommendations."""
from __future__ import annotations

import os
from typing import Dict

import pandas as pd


def _recommended_persona(row: pd.Series) -> str:
    if row["ai_adoption_signal"] == "High":
        return "Chief Digital Officer / VP of AI"
    if row["modernization_gap"] == "High":
        return "CTO / VP Engineering"
    if row["cloud_provider"] in {"AWS", "Azure", "Multi-cloud", "GCP"}:
        return "Head of Platform Engineering"
    return "CIO / IT Transformation Leader"


def _pitch_angle(row: pd.Series) -> str:
    if row["modernization_gap"] == "High" and row["digital_maturity"] in {"Low", "Medium"}:
        return "legacy modernization"
    if row["cloud_provider"] in {"AWS", "Azure", "Multi-cloud"} and row["engineering_hiring_trend"] in {"Growing", "Surging"}:
        return "platform engineering"
    if row["ai_adoption_signal"] in {"Medium", "High"}:
        return "AI enablement"
    if row["product_launch_signal"] == "Yes":
        return "digital product acceleration"
    return "cloud modernization"


def _next_best_action(row: pd.Series, angle: str) -> str:
    if row["account_tier"] == "Hot":
        return f"Target Now: Schedule an executive discovery call in 5 business days with a tailored {angle} POV."
    if row["account_tier"] == "Warm":
        return f"Run a 2-step outreach sequence with industry proof points and a {angle} workshop offer."
    return "Add to nurture stream; monitor buying signals and re-score in the next planning cycle."


def _why_this_account(row: pd.Series, angle: str) -> str:
    return (
        f"{row['account_name']} ranks {row['account_tier']} with a Total Score of {row['total_score']}/100. "
        f"Fit is driven by {row['industry']} alignment and a {row['tech_stack']} delivery footprint. "
        f"Propensity is influenced by {row['engineering_hiring_trend'].lower()} hiring, "
        f"{row['ai_adoption_signal'].lower()} AI adoption, and current market signals. "
        f"This points to a credible near-term conversation around {angle}."
    )


def _optional_llm_enhance(text: str) -> str:
    """Optional enhancement hook when API keys exist.

    This intentionally stays local and deterministic for the demo.
    """
    if os.getenv("OPENAI_API_KEY") or os.getenv("GEMINI_API_KEY"):
        return text + " (LLM enhancement is enabled in this environment.)"
    return text


def build_decision_intelligence(scored_df: pd.DataFrame) -> pd.DataFrame:
    enriched = []

    for _, row in scored_df.iterrows():
        top_drivers = row["drivers"][:3]
        angle = _pitch_angle(row)
        persona = _recommended_persona(row)
        why_text = _optional_llm_enhance(_why_this_account(row, angle))
        nba = _next_best_action(row, angle)

        row_dict: Dict = row.to_dict()
        row_dict.update(
            {
                "top_3_drivers": top_drivers,
                "why_this_account": why_text,
                "next_best_action": nba,
                "recommended_buyer_persona": persona,
                "recommended_exadel_pitch_angle": angle,
            }
        )
        enriched.append(row_dict)

    return pd.DataFrame(enriched)
