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


# ---- Glossary used for hover tooltips ----
TIPS = {
    "responses": "Completed survey responses. Each response is one caller who answered the survey after a 311 call.",
    "csat": "Customer satisfaction: the % of callers who rated Overall Satisfaction 4 or 5 (Agree or Strongly Agree) on the 1–5 scale.",
    "nps": "Net Promoter Score: % of promoters (rated 9–10 on 'would you recommend 311?') minus % of detractors (0–6). Ranges from −100 to +100.",
    "wait": "% of callers who rated Wait Time 4 or 5: they agreed the wait to reach an agent was acceptable.",
    "answer": "% of callers who rated Answer Satisfaction 4 or 5: they were satisfied with the answer or outcome they received.",
    "agent": "% of callers who rated Agent Customer Service 4 or 5: the agent was courteous and helpful.",
    "knowledge": "% of callers who rated Agent Job Knowledge 4 or 5: the agent knew how to handle the request.",
    "dissatisfied": "Callers who rated Overall Satisfaction 1 or 2 (Strongly Disagree or Disagree).",
    "unfavorable": "% of callers who rated Overall Satisfaction 1 or 2.",
    "promoters": "Callers who scored 9–10 on the recommend question: likely to speak well of 311.",
    "passives": "Callers who scored 7–8: satisfied but not enthusiastic. They count in neither side of NPS.",
    "detractors": "Callers who scored 0–6: unlikely to recommend 311.",
    "target": "Working CSAT target for this dashboard (80%), close to the 80.9% historical average. Not an official NYC311 figure.",
    "control": "3-sigma control limits: the range a day's CSAT would normally fall in given its number of responses. Outside the range = statistically unusual.",
    "ci": "95% confidence interval: the range the true value very likely falls in. Wide when a group has few responses.",
    "low_score": "A response with Overall Satisfaction 1–2 or an NPS score of 0–6. These callers are candidates for follow-up.",
    "priority": "High = Overall Satisfaction 1 or NPS 0–3. Medium = any other low-score response.",
    "weakest": "The lowest-rated of the four service drivers (Wait, Agent service, Job knowledge, Answer) in that response.",
    "reliability": "Confidence: when callers have this rating combination, the chance they end up in this NPS group.",
    "share": "Support: the % of all callers who have this rating combination.",
    "impact": "Lift: how many times more likely this NPS group is for callers with the combination than for callers overall. Above 1 = positive link.",
    "p_value": "The chance of seeing a trend this strong if there were really no trend. Below 0.05 = statistically significant.",
}

# ---- Page furniture ----
CSS = """
<style>
  .tip {position: relative; cursor: help; border-bottom: 1px dotted currentColor;}
  .tip:hover::after {content: attr(data-tip); position: absolute; left: 0; top: 100%; margin-top: 6px; z-index: 9999;
       background: #1d2433; color: #fff; padding: 8px 10px; border-radius: 6px; font-size: .78rem; line-height: 1.4;
       width: max-content; max-width: 280px; white-space: normal; text-transform: none; letter-spacing: 0; font-weight: 400;
       box-shadow: 0 4px 14px rgba(0,0,0,.18);}
  .tip-r:hover::after {left: auto; right: 0;}
  [data-testid="stMarkdownContainer"], [data-testid="stElementContainer"] {overflow: visible !important;}
  .block-container, [data-testid="stMainBlockContainer"] {padding-top: 4.5rem !important; max-width: 1280px;}
  h1, h2, h3 {letter-spacing: -0.01em;}
  .kpi {border: 1px solid rgba(20,33,61,.12); border-radius: 10px; padding: 14px 16px; background: rgba(255,255,255,.6);}
  .kpi-label {font-size: .74rem; text-transform: uppercase; letter-spacing: .06em; color: #5b6170;}
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
  .rule-meta {font-size: .82rem; color: #3a4152; display: flex; flex-wrap: wrap; gap: 16px;}
  @media (prefers-color-scheme: dark) {
    .kpi, .rule-card {background: rgba(255,255,255,.04); border-color: rgba(255,255,255,.14);}
    .good {color: #3ccf3c;} .bad {color: #ff7b72;}
  }
</style>
"""


def page_setup():
    st.markdown(CSS, unsafe_allow_html=True)


def tip(label, text, right=False):
    """Inline label with a hover tooltip (dotted underline)."""
    import html as _html
    if not text:
        return label
    return f"<span class='tip{' tip-r' if right else ''}' data-tip='{_html.escape(text, quote=True)}'>{label}</span>"


KPI_LABEL_TIPS = {
    "Survey responses": "responses", "Surveys analysed": "responses", "Respondents": "responses",
    "CSAT (Overall 4–5)": "csat", "CSAT (% favorable)": "csat", "Net Promoter Score": "nps",
    "Wait time rated OK": "wait", "Answer satisfaction": "answer", "Dissatisfied callers": "dissatisfied",
    "% Unfavorable": "unfavorable",
}


def col_help(mapping):
    """column_config entries that show a tooltip when hovering a table header."""
    return {name: st.column_config.Column(help=text) for name, text in mapping.items()}


def kpi_card(label, value, delta_html="", note="", spark=None, spark_note="", help=None, tip_right=False):
    help = help or TIPS.get(KPI_LABEL_TIPS.get(label, ""), None)
    label = tip(label, help, tip_right)
    spark_html = ""
    if spark is not None and len(spark) > 1:
        spark_html = sparkline_svg(spark) + (f"<div class='kpi-note' style='margin-top:0'>{spark_note}</div>" if spark_note else "")
    st.markdown(
        f"<div class='kpi'><div class='kpi-label'>{label}</div><div class='kpi-value'>{value}</div>"
        f"<div class='kpi-delta'>{delta_html}</div><div class='kpi-note'>{note}</div>{spark_html}</div>",
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
    """Render the written analysis in research-paper style, without part labels.

    1. A description of the graph.
    2. A conclusion paragraph: the findings, ending in what can be concluded.
    3. A recommendation paragraph.
    """
    if not st.session_state.get("show_analysis", True):
        return
    with st.expander("Analysis", expanded=False, icon=":material/notes:"):
        st.markdown(block["description"])
        st.markdown(block.get("conclusion") or f"{block['insight']} {block['interpretation']}")
        st.markdown(block.get("recommend") or block["recommendation"])


def page_conclusion(entry, owner_label="Responsible"):
    """Closing section: an overall conclusion paragraph and numbered recommendations, as in a research paper."""
    if not st.session_state.get("show_analysis", True):
        return
    conclusion, recs = entry
    st.subheader("Conclusion and recommendations",
                 help="The overall conclusion from this page's charts and the recommended actions, written as in the "
                      "conclusion and recommendation section of a research paper.")
    st.markdown(conclusion)
    st.markdown("Based on these conclusions, the following are recommended:\n\n" +
                "\n".join(f"{i}. {text} *({owner_label}: {owner})*" for i, (text, owner) in enumerate(recs, 1)))


# ---- Advanced helpers ----
def wilson(k, n, z=1.96):
    """95% Wilson score interval for a proportion, returned in percent (low, high)."""
    if n == 0:
        return (np.nan, np.nan)
    p = k / n
    den = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / den
    half = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (centre - half) * 100, (centre + half) * 100


def sparkline_svg(values, width=120, height=28, color="#2a78d6"):
    """Tiny inline SVG trend line with an emphasised last point."""
    v = [float(x) for x in values if pd.notna(x)]
    if len(v) < 2:
        return ""
    lo, hi = min(v), max(v)
    span = (hi - lo) or 1
    xs = [i * (width - 6) / (len(v) - 1) + 3 for i in range(len(v))]
    ys = [height - 4 - (x - lo) / span * (height - 8) for x in v]
    pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in zip(xs, ys))
    return (f"<svg width='{width}' height='{height}' viewBox='0 0 {width} {height}' style='display:block;margin-top:4px'>"
            f"<polyline points='{pts}' fill='none' stroke='{color}' stroke-width='1.6' stroke-linejoin='round' stroke-linecap='round' opacity='.75'/>"
            f"<circle cx='{xs[-1]:.1f}' cy='{ys[-1]:.1f}' r='2.6' fill='{color}'/></svg>")


def trend_fit(x, y, x_new=None, level=0.95):
    """OLS line with slope p-value and prediction interval (for forecasts)."""
    from scipy import stats
    x, y = np.asarray(x, float), np.asarray(y, float)
    n = len(x)
    res = stats.linregress(x, y)
    out = {"slope": res.slope, "intercept": res.intercept, "p": res.pvalue, "r2": res.rvalue ** 2}
    if x_new is not None:
        x_new = np.asarray(x_new, float)
        resid = y - (res.intercept + res.slope * x)
        s = np.sqrt((resid ** 2).sum() / (n - 2))
        t = stats.t.ppf((1 + level) / 2, n - 2)
        se = s * np.sqrt(1 + 1 / n + (x_new - x.mean()) ** 2 / ((x - x.mean()) ** 2).sum())
        pred = res.intercept + res.slope * x_new
        out.update(pred=pred, lo=pred - t * se, hi=pred + t * se)
    return out
