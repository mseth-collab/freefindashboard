"""Streamlit app: Account Propensity Copilot."""
from __future__ import annotations

import streamlit as st
import pandas as pd

from insights import build_decision_intelligence
from scoring import score_accounts
from utils import load_data, merge_inputs, style_tier

st.set_page_config(page_title="Account Propensity Copilot", page_icon="🎯", layout="wide")

st.title("🎯 Exadel - Account Propensity Copilot")
st.caption("Decision Intelligence for Business Development, AEs, and AMs")

accounts_df, opps_df, external_df = load_data()
model_input = merge_inputs(accounts_df, external_df)
scored_df = build_decision_intelligence(score_accounts(model_input))

# Prefer a wow account at launch: highest score in target industries
wow_candidates = scored_df[scored_df["industry"].isin(["FinTech", "HealthTech", "SaaS", "InsurTech"])]
default_account = (wow_candidates.iloc[0] if not wow_candidates.empty else scored_df.iloc[0])["account_name"]

st.markdown(
    """
    <div style='padding:10px 14px; border-radius:8px; background:#0f3d5e; color:white; margin-bottom:12px;'>
      <b>Decision Intelligence:</b> We go beyond scoring. We provide decision intelligence.
    </div>
    """,
    unsafe_allow_html=True,
)

# Executive Overview
st.subheader("A. Executive Overview")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Accounts Scored", len(scored_df))
with col2:
    st.metric("Hot Accounts", int((scored_df["account_tier"] == "Hot").sum()))
with col3:
    st.metric("Average Total Score", f"{scored_df['total_score'].mean():.1f}")
with col4:
    top_industry = scored_df.groupby("industry")["total_score"].mean().sort_values(ascending=False).index[0]
    st.metric("Top Target Industry", top_industry)

st.divider()

# Filters + Ranked list
st.subheader("B. Ranked Account List")
f1, f2, f3, f4 = st.columns(4)
industries = ["All"] + sorted(scored_df["industry"].unique().tolist())
regions = ["All"] + sorted(scored_df["region"].unique().tolist())
clouds = ["All"] + sorted(scored_df["cloud_provider"].unique().tolist())
tiers = ["All", "Hot", "Warm", "Cold"]

industry_filter = f1.selectbox("Industry", industries)
region_filter = f2.selectbox("Region", regions)
cloud_filter = f3.selectbox("Cloud Provider", clouds)
tier_filter = f4.selectbox("Tier", tiers)

filtered = scored_df.copy()
if industry_filter != "All":
    filtered = filtered[filtered["industry"] == industry_filter]
if region_filter != "All":
    filtered = filtered[filtered["region"] == region_filter]
if cloud_filter != "All":
    filtered = filtered[filtered["cloud_provider"] == cloud_filter]
if tier_filter != "All":
    filtered = filtered[filtered["account_tier"] == tier_filter]

ranked = filtered[
    [
        "account_name",
        "industry",
        "fit_score",
        "propensity_score",
        "total_score",
        "account_tier",
        "top_signal",
    ]
].copy()
ranked["tier_label"] = ranked["account_tier"].map(style_tier)

st.dataframe(
    ranked[
        [
            "account_name",
            "industry",
            "fit_score",
            "propensity_score",
            "total_score",
            "tier_label",
            "top_signal",
        ]
    ].rename(columns={"tier_label": "tier"}),
    use_container_width=True,
    hide_index=True,
)

st.divider()

# Account detail
st.subheader("C. Account Detail View")
account_names = filtered["account_name"].tolist() if not filtered.empty else scored_df["account_name"].tolist()
if default_account in account_names:
    default_index = account_names.index(default_account)
else:
    default_index = 0

selected_account = st.selectbox("Select account", account_names, index=default_index)
selected = scored_df[scored_df["account_name"] == selected_account].iloc[0]

c1, c2 = st.columns([1, 2])
with c1:
    st.metric("Total Score", f"{selected['total_score']}/100")
    st.metric("Fit Score", f"{selected['fit_score']}/50")
    st.metric("Propensity Score", f"{selected['propensity_score']}/50")
    st.markdown(f"**Tier:** {style_tier(selected['account_tier'])}")

with c2:
    st.markdown("**Top Score Drivers**")
    for d in selected["top_3_drivers"]:
        st.write(f"- {d}")

    st.markdown("**Why this account**")
    st.info(selected["why_this_account"])

    st.markdown("**Next Best Action**")
    st.success(selected["next_best_action"])

    st.markdown("**Recommended Buyer Persona**")
    st.write(selected["recommended_buyer_persona"])

    st.markdown("**Recommended Exadel Pitch Angle**")
    st.write(selected["recommended_exadel_pitch_angle"].title())

st.markdown("**Raw Signals Used in Scoring**")
raw_cols = [
    "industry",
    "subindustry",
    "revenue_band",
    "employee_band",
    "region",
    "tech_stack",
    "cloud_provider",
    "digital_maturity",
    "modernization_gap",
    "engineering_hiring_trend",
    "funding_stage",
    "product_launch_signal",
    "m_and_a_signal",
    "layoffs_signal",
    "ai_adoption_signal",
    "similarity_to_past_wins",
    "news_velocity",
    "job_postings_change_pct",
    "cloud_spend_growth_pct",
    "ai_initiative_count",
    "intent_signal_strength",
]
st.dataframe(pd.DataFrame(selected[raw_cols]).T.rename(columns={selected.name: "value"}), use_container_width=True)

st.divider()

# Optional comparison view
st.subheader("D. Optional Comparison View")
cmp1, cmp2 = st.columns(2)
left = cmp1.selectbox("Compare account A", scored_df["account_name"].tolist(), index=0)
right = cmp2.selectbox("Compare account B", scored_df["account_name"].tolist(), index=min(1, len(scored_df) - 1))

left_row = scored_df[scored_df["account_name"] == left].iloc[0]
right_row = scored_df[scored_df["account_name"] == right].iloc[0]
comparison = pd.DataFrame(
    {
        "Metric": ["Industry", "Fit Score", "Propensity Score", "Total Score", "Tier", "Top Signal", "Pitch Angle"],
        left: [
            left_row["industry"],
            left_row["fit_score"],
            left_row["propensity_score"],
            left_row["total_score"],
            left_row["account_tier"],
            left_row["top_signal"],
            left_row["recommended_exadel_pitch_angle"],
        ],
        right: [
            right_row["industry"],
            right_row["fit_score"],
            right_row["propensity_score"],
            right_row["total_score"],
            right_row["account_tier"],
            right_row["top_signal"],
            right_row["recommended_exadel_pitch_angle"],
        ],
    }
)
st.dataframe(comparison, use_container_width=True, hide_index=True)

st.markdown("---")
st.caption("Demo uses synthetic data modeled on Salesforce and external account intelligence.")
