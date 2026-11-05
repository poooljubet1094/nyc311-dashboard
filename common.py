"""Shared data loading, cleaning, KPI helpers and chart styling for every page."""
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st

DATA_PATH = Path(__file__).parent / "data" / "311_Customer_Satisfaction_Survey.csv"

LIKERT = {"Strongly Disagree": 1, "Disagree": 2, "Neutral": 3, "Agree": 4, "Strongly Agree": 5}
LIKERT_LABELS = {v: k for k, v in LIKERT.items()}

# Display names for the five survey questions
DIMENSIONS = {
    "overall_satisfaction": "Overall Satisfaction",
    "wait_time": "Wait Time",
    "agent_customer_service": "Agent Customer Service",
    "agent_job_knowledge": "Agent Job Knowledge",
    "answer_satisfaction": "Answer Satisfaction",
}
DRIVERS = ["wait_time", "agent_customer_service", "agent_job_knowledge", "answer_satisfaction"]

# Detailed language labels (middle level) — invisible marks stripped first
LANG_DETAIL = {
    "English (United States)": "English", "Español (España, alfabetización internacional)": "Spanish",
    "中文（简体）": "Chinese (Simpl.)", "中文（繁體）": "Chinese (Trad.)", "Pусский": "Russian",
    "한국어": "Korean", "ht": "Haitian Creole", "العربية": "Arabic", "Polski": "Polish",
    "Français (France)": "French", "bn": "Bengali", "ur": "Urdu",
}
# Language queues (lower level): top three languages, everything else grouped
QUEUE = {"English": "English", "Spanish": "Spanish", "Chinese (Simpl.)": "Chinese", "Chinese (Trad.)": "Chinese"}

# ---- Colours (colour-blind-checked categorical order, diverging Likert scale, status) ----
C = {
    "blue": "#2a78d6", "orange": "#eb6834", "aqua": "#1baf7a", "yellow": "#eda100",
    "ink": "#1d2433", "ink2": "#52514e", "muted": "#898781", "grid": "#e6e5df",
    "good": "#0ca30c", "warn": "#d99100", "bad": "#d03b3b", "navy": "#14213d",
}
SERIES = [C["blue"], C["orange"], C["aqua"], C["yellow"]]
LIKERT_COLORS = {1: "#c23a3a", 2: "#ec9a9a", 3: "#d6d5cf", 4: "#86b6ef", 5: "#2a78d6"}
LANG_COLORS = {"English": C["blue"], "Spanish": C["orange"], "Chinese": C["aqua"], "Others": C["yellow"]}

BASE_LAYOUT = dict(
    template="simple_white",
    font=dict(family="Inter, Segoe UI, system-ui, sans-serif", size=13, color=C["ink"]),
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=10, r=10, t=30, b=10),
    hoverlabel=dict(bgcolor="white", font_size=12),
)


@st.cache_data(show_spinner="Loading survey data…")
def load_data() -> pd.DataFrame:
    """Load the NYC Open Data export and apply the group's cleaning rules.

    * Column names to snake_case.
    * Likert text to 1–5; 'Agree+I1030' → Agree, 'SATISFACTORIO' → Neutral.
    * Drop the one record with a blank Job Knowledge rating and the 25 with no NPS
      (28,816 → 28,790 rows).
    """
    raw = pd.read_csv(DATA_PATH)
    df = raw.copy()
    df.columns = (df.columns.str.lower().str.replace(r"[^\w\s]", "", regex=True)
                  .str.strip().str.replace(r"\s+", "_", regex=True))

    df["agent_customer_service"] = df["agent_customer_service"].replace("Agree+I1030", "Agree")
    df["agent_job_knowledge"] = df["agent_job_knowledge"].replace("SATISFACTORIO", "Neutral")
    df = df.dropna(subset=["agent_job_knowledge", "nps"])
    for col in DIMENSIONS:
        df[col] = df[col].map(LIKERT).astype(int)
    df["nps"] = df["nps"].astype(int)

    fmt = "%Y %b %d %I:%M:%S %p"
    df["start_datetime"] = pd.to_datetime(df["start_time"], format=fmt)
    df["completion_datetime"] = pd.to_datetime(df["completion_time"], format=fmt)
    df["turnaround_minutes"] = (df["completion_datetime"] - df["start_datetime"]).dt.total_seconds() / 60
    df["start_date"] = df["start_datetime"].dt.normalize()
    df["year"] = df["start_datetime"].dt.year
    df["month"] = df["start_datetime"].dt.month
    df["quarter"] = df["start_datetime"].dt.to_period("Q").astype(str)
    df["campaign_key"] = df["year"].astype(str) + " " + df["campaign"]

    lang = df["survey_language"].str.replace("‎", "", regex=False).str.strip()
    df["language_detail"] = lang.map(LANG_DETAIL).fillna("Other")
    df["language_queue"] = df["language_detail"].map(QUEUE).fillna("Others")

    df["nps_group"] = pd.cut(df["nps"], [-1, 6, 8, 10], labels=["Detractor", "Passive", "Promoter"])
    df["row_id"] = df.index
    return df.reset_index(drop=True)


def campaign_order(df: pd.DataFrame) -> list:
    """Campaign keys ordered by first response."""
    return df.groupby("campaign_key")["start_datetime"].min().sort_values().index.tolist()


# ---- KPI helpers ----
def top2(s) -> float:
    """% rated 4–5 (Agree / Strongly Agree)."""
    return float((s >= 4).mean() * 100) if len(s) else np.nan


def bottom2(s) -> float:
    """% rated 1–2 (Disagree / Strongly Disagree)."""
    return float((s <= 2).mean() * 100) if len(s) else np.nan


def nps_score(s) -> float:
    """% promoters (9–10) − % detractors (0–6)."""
    return float(((s >= 9).mean() - (s <= 6).mean()) * 100) if len(s) else np.nan


# ---- Page furniture ----
CSS = """
<style>
  .block-container, [data-testid="stMainBlockContainer"] {padding-top: 4.5rem !important; max-width: 1280px;}
  h1, h2, h3 {letter-spacing: -0.01em;}
  .kpi {border: 1px solid rgba(20,33,61,.12); border-radius: 10px; padding: 14px 16px; background: rgba(255,255,255,.6);}
  .kpi-label {font-size: .74rem; text-transform: uppercase; letter-spacing: .06em; opacity: .7;}
  .kpi-value {font-size: 1.9rem; font-weight: 600; line-height: 1.15; margin-top: 2px;}
  .kpi-delta {font-size: .8rem; font-weight: 600; margin-top: 2px;}
  .kpi-note {font-size: .74rem; opacity: .65; margin-top: 4px;}
  .good {color: #0b7a0b;} .bad {color: #b42318;} .flat {opacity: .6;}
  .pill {display:inline-block; border-radius: 999px; padding: 1px 9px; font-size: .72rem; font-weight: 600;}
  .pill-good {background:#e7f6e7; color:#0b7a0b;} .pill-bad {background:#fdecec; color:#b42318;}
  .pill-warn {background:#fff4dc; color:#8a5a00;}
  .level-tag {font-size: .75rem; text-transform: uppercase; letter-spacing: .08em; opacity: .65; margin-bottom: -6px;}
  .rule-card {border-left: 5px solid; border-radius: 6px; padding: 12px 16px; margin-bottom: 10px;
              background: rgba(255,255,255,.65); box-shadow: 0 1px 3px rgba(0,0,0,.07);}
  .rule-title {font-weight: 600; font-size: .95rem; margin-bottom: 6px;}
  .rule-meta {font-size: .82rem; opacity: .85; display: flex; flex-wrap: wrap; gap: 16px;}
  @media (prefers-color-scheme: dark) {
    .kpi, .rule-card {background: rgba(255,255,255,.04); border-color: rgba(255,255,255,.14);}
    .good {color: #3ccf3c;} .bad {color: #ff7b72;}
  }
</style>
"""


def page_setup():
    st.markdown(CSS, unsafe_allow_html=True)


def kpi_card(label, value, delta_html="", note=""):
    st.markdown(
        f"<div class='kpi'><div class='kpi-label'>{label}</div><div class='kpi-value'>{value}</div>"
        f"<div class='kpi-delta'>{delta_html}</div><div class='kpi-note'>{note}</div></div>",
        unsafe_allow_html=True,
    )


def delta_html(now, before, unit=" pt", higher_is_better=True, digits=1):
    if before is None or pd.isna(before):
        return "<span class='flat'>no earlier campaign</span>"
    d = now - before
    cls = "flat" if d == 0 else ("good" if (d > 0) == higher_is_better else "bad")
    arrow = "▲" if d > 0 else ("▼" if d < 0 else "■")
    return f"<span class='{cls}'>{arrow} {d:+,.{digits}f}{unit}</span>"


def analysis(block: dict):
    """Render the four-part analysis required by the project brief."""
    if not st.session_state.get("show_analysis", True):
        return
    with st.expander("Analysis — description, insight, interpretation, recommendation", expanded=False):
        for key, title in [("description", "1. Description"), ("insight", "2. Insight"),
                           ("interpretation", "3. Interpretation"), ("recommendation", "4. Recommendation")]:
            st.markdown(f"**{title}** — {block[key]}")
