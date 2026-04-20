"""Utility helpers for data load and presentation."""
from __future__ import annotations

from pathlib import Path
from typing import Tuple

import pandas as pd

from data_generator import generate_demo_data

DATA_DIR = Path(__file__).resolve().parent / "data"


def ensure_data_files() -> None:
    required = [
        DATA_DIR / "salesforce_accounts.csv",
        DATA_DIR / "salesforce_opportunities.csv",
        DATA_DIR / "external_company_signals.csv",
    ]
    if not all(path.exists() for path in required):
        generate_demo_data()


def load_data() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    ensure_data_files()
    accounts = pd.read_csv(DATA_DIR / "salesforce_accounts.csv")
    opportunities = pd.read_csv(DATA_DIR / "salesforce_opportunities.csv")
    external = pd.read_csv(DATA_DIR / "external_company_signals.csv")
    return accounts, opportunities, external


def merge_inputs(accounts: pd.DataFrame, external: pd.DataFrame) -> pd.DataFrame:
    return accounts.merge(external, on="account_name", how="left")


def style_tier(tier: str) -> str:
    colors = {
        "Hot": "🟢 Hot",
        "Warm": "🟡 Warm",
        "Cold": "🔴 Cold",
    }
    return colors.get(tier, tier)
