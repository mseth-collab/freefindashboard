# Account Propensity Copilot (Exadel Hackathon Demo)

## What this app does
**Account Propensity Copilot** is an internal AI-assisted sales decision tool for Exadel teams (Business Development, AEs, AMs).

It scores accounts using two transparent dimensions:
- **Fit Score (0–50):** Is this a good IT services client for Exadel?
- **Propensity Score (0–50):** Are they likely to buy now?

These are combined into:
- **Total Score (0–100)** with account tiering (**Hot / Warm / Cold**)

Then the app adds **Decision Intelligence**:
- top 3 score drivers
- “Why this account” narrative
- next best action
- recommended buyer persona
- recommended Exadel pitch angle

The demo uses **synthetic Salesforce-like and external intelligence CSVs** only.

---

## How to run
```bash
pip install -r requirements.txt
streamlit run app.py
```

Open the local URL shown by Streamlit (typically `http://localhost:8501`).

---

## Architecture summary
- `data_generator.py`
  - Generates synthetic account, opportunity, and external signal CSVs under `/data`
  - Creates:
    - `data/salesforce_accounts.csv`
    - `data/salesforce_opportunities.csv`
    - `data/external_company_signals.csv`
- `utils.py`
  - Ensures demo CSVs exist and loads/merges input data
- `scoring.py`
  - Implements transparent Fit and Propensity scoring logic
  - Outputs fit, propensity, total, tier, top signal, and drivers
- `insights.py`
  - Creates decision intelligence outputs (explanations + actions + persona + pitch angle)
  - Optional LLM enhancement if `OPENAI_API_KEY` or `GEMINI_API_KEY` exists
  - Works fully without external APIs
- `app.py`
  - Streamlit enterprise-style interface with executive overview, ranked list, details, and comparison

---

## Scoring summary
### Fit Score (0–50)
Weighted factors:
1. Industry alignment to Exadel target sectors
2. Tech stack match to Exadel strengths
3. Company size sweet spot
4. Digital maturity + modernization opportunity

### Propensity Score (0–50)
Weighted factors:
1. Engineering hiring trend (momentum)
2. Cloud / AI migration signals
3. Funding/growth stage
4. Product launch, M&A, layoffs signals

### Output fields
- `fit_score`
- `propensity_score`
- `total_score`
- `account_tier` (`Hot`, `Warm`, `Cold`)

---

## Why this is innovative
This prototype is not just a lead score dashboard.

It introduces a **Decision Intelligence layer** that translates signals into action:
- **Why this account** in plain English
- **Who to target** (buyer persona)
- **What to sell** (Exadel pitch angle)
- **What to do next** (next best action)

This helps teams move from analytics to execution in one screen.

---

## Suggested 4-minute demo flow
Use this exact path:
1. **open dashboard**
2. **show hot accounts**
3. **explain Fit vs Propensity**
4. **click one top-ranked account**
5. **show "Why this account?"**
6. **show "Next best action"**
7. **end with business value: better targeting, better pipeline quality, less wasted seller time**

---

## Notes & constraints
- Local only
- Synthetic data only
- No external DB
- No auth
- No real CRM integration
- Fast startup
- Demo-ready business framing and explainability
