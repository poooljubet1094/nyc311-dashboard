"""Top-level management (Strategic).

Brief: Is the organization meeting its goals? Are results increasing? What are the future opportunities and risks?
"""
import html

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

from common import (BASE_LAYOUT, C, TIPS, analysis, bottom2, col_help, load_data, nps_score, page_conclusion, sparkline_svg,
                    tip, top2, trend_fit)
from models import SEG_COLORS, nps_rules
from narrative import PAGE_CONCLUSIONS, TOP

df = load_data()
LAW_MIN_CAMPAIGNS = 5   # NYC Local Law 26 of 2021: at least five survey campaigns a year

st.markdown("<div class='level-tag'>Top-level management · Strategic</div>", unsafe_allow_html=True)
st.title("Executive CSAT & NPS")
st.caption("For NYC311 leadership. Answers the brief's strategic questions: is the organization meeting its goals, "
           "are results increasing, and what are the future opportunities and risks.")

# ------------------------------------------------------------------ Summary indicators (latest year)
last_y = int(df["year"].max())
cy, py_ = df[df["year"] == last_y], df[df["year"] == last_y - 1]
st.subheader(f"Summary indicators · {last_y}", help=f"Headline results for the latest full year ({last_y}), compared with {last_y - 1}.")
k = st.columns(4)
k[0].metric("CSAT (% favorable)", f"{top2(cy['overall_satisfaction']):.1f}%",
            f"{top2(cy['overall_satisfaction']) - top2(py_['overall_satisfaction']):+.1f} pt vs {last_y - 1}", help=TIPS["csat"])
k[1].metric("Net Promoter Score", f"{nps_score(cy['nps']):+.1f}", f"{nps_score(cy['nps']) - nps_score(py_['nps']):+.1f} vs {last_y - 1}", help=TIPS["nps"])
k[2].metric("Answer satisfaction", f"{top2(cy['answer_satisfaction']):.1f}%",
            f"{top2(cy['answer_satisfaction']) - top2(py_['answer_satisfaction']):+.1f} pt vs {last_y - 1}", help=TIPS["answer"])
k[3].metric("Respondents", f"{len(cy):,}", f"{len(cy) - len(py_):+,} vs {last_y - 1}",
            help=TIPS["responses"] + f" All years: {len(df):,} respondents after removing 26 incomplete records.")
p_pro, p_pas, p_det = (cy["nps"] >= 9).mean() * 100, cy["nps"].between(7, 8).mean() * 100, (cy["nps"] <= 6).mean() * 100
segs = [("Promoters (9–10)", p_pro, SEG_COLORS["Promoter"]), ("Passives (7–8)", p_pas, SEG_COLORS["Passive"]),
        ("Detractors (0–6)", p_det, SEG_COLORS["Detractor"])]
seg_tips = [TIPS["promoters"], TIPS["passives"], TIPS["detractors"]]
labels = "".join(f"<span style='color:{c};font-weight:600'>{tip(f'{lab}: {v:.1f}%', t, right=(i == 2))}</span>"
                 for i, ((lab, v, c), t) in enumerate(zip(segs, seg_tips)))
bar = "".join(f"<div title='{lab}: {v:.1f}%' style='width:{v}%;background:{c}'></div>" for lab, v, c in segs)
st.markdown(f"<div style='padding:.2rem 0 .4rem'><div style='font-size:.8rem;opacity:.7;margin-bottom:4px'>{last_y} NPS mix</div>"
            f"<div style='display:flex;justify-content:space-between;flex-wrap:wrap;gap:8px;font-size:.85rem;margin-bottom:6px'>{labels}</div>"
            f"<div style='display:flex;height:12px;border-radius:6px;overflow:hidden'>{bar}</div></div>", unsafe_allow_html=True)
analysis(TOP["summary"])

# ------------------------------------------------------------------ Strategic scorecard vs targets
st.subheader("Strategic scorecard: are we meeting our goals?", help="Five executive KPIs against their targets, with the change from last year and a 2020–2025 trend line. Hover a KPI name for its definition.")
yearly_k = df.groupby("year").agg(csat=("overall_satisfaction", top2), nps=("nps", nps_score),
                                  answer=("answer_satisfaction", top2), unfav=("overall_satisfaction", bottom2),
                                  answer1=("answer_satisfaction", lambda s: (s == 1).mean() * 100))
prev_y = yearly_k.index[-2]
# Targets come from the group's recommendations; NPS and unfavorable targets are illustrative
SCORECARD = [
    ("CSAT (% favorable)", "csat", 85.0, True, "{:.1f}%", "Middle-level recommendation (above 85%)"),
    ("Net Promoter Score", "nps", 60.0, True, "{:+.1f}", "Illustrative target"),
    ("Answer Satisfaction (% favorable)", "answer", 75.0, True, "{:.1f}%", "Middle-level recommendation (75% or higher)"),
    ("% Unfavorable (Overall 1–2)", "unfav", 10.0, False, "{:.1f}%", "Illustrative target"),
    ("Answer rated 1/5 (% of callers)", "answer1", None, False, "{:.1f}%", "Top-level recommendation: eliminate, so it must fall every year"),
]
rows_html = []
for label, col, target, higher, fmt, basis in SCORECARD:
    now, before = yearly_k.loc[last_y, col], yearly_k.loc[prev_y, col]
    diff = now - before
    good_move = (diff > 0) == higher
    delta = f"<span class='{'good' if good_move else 'bad'}'>{'▲' if diff > 0 else '▼'} {diff:+.1f}</span>"
    if target is None:
        ok = diff < 0
        status = "<span class='pill pill-good'>✔ Falling</span>" if ok else "<span class='pill pill-bad'>✖ Not falling</span>"
        tgt = "Falling"
    else:
        ok = now >= target if higher else now <= target
        gap = abs(now - target)
        status = ("<span class='pill pill-good'>✔ On target</span>" if ok
                  else f"<span class='pill pill-bad'>✖ {gap:.1f} {'pts' if col == 'nps' else 'pt'} off</span>")
        tgt = ("≥ " if higher else "≤ ") + fmt.format(target).replace("+", "")
    kpi_tip = {"csat": TIPS["csat"], "nps": TIPS["nps"], "answer": TIPS["answer"], "unfav": TIPS["unfavorable"],
               "answer1": "Share of callers who rated Answer Satisfaction 1 (Strongly Disagree): the most severe pain point."}[col]
    rows_html.append(f"<tr><td><b>{tip(label, kpi_tip)}</b><div class='kpi-note'>{basis}</div></td><td class='num'>{fmt.format(now)}</td>"
                     f"<td class='num'>{delta}</td><td class='num'>{tgt}</td><td>{status}</td>"
                     f"<td>{sparkline_svg(yearly_k[col].values, width=140, color=C['blue'] if ok else C['bad'])}</td></tr>")
st.markdown(
    "<style>.sc{width:100%;border-collapse:collapse;font-size:.9rem}.sc th{text-align:left;font-size:.72rem;text-transform:uppercase;"
    "letter-spacing:.05em;opacity:.65;padding:6px 10px;border-bottom:1px solid rgba(20,33,61,.15)}.sc td{padding:8px 10px;"
    "border-bottom:1px solid rgba(20,33,61,.08);vertical-align:middle}.sc .num{font-variant-numeric:tabular-nums;white-space:nowrap}</style>"
    f"<table class='sc'><tr><th>KPI</th><th>{last_y}</th><th>{tip(f'vs {prev_y}', 'Change from the previous year, in points.')}</th>"
    f"<th>{tip('Target', 'The goal for this KPI; see the note under each KPI for where it comes from.')}</th>"
    f"<th>{tip('Status', 'On target, or how far off target the latest year is.')}</th>"
    f"<th>{yearly_k.index[0]}–{last_y}</th></tr>{''.join(rows_html)}</table>", unsafe_allow_html=True)
st.caption("Targets for CSAT, Answer Satisfaction and Answer 1/5 come from the group's middle- and top-level recommendations; "
           "the NPS and % Unfavorable targets are illustrative and can be changed in the code. 2020 is the pilot year.")
analysis(TOP["scorecard"])

# ------------------------------------------------------------------ Yearly growth
st.subheader("Are results increasing? Year-over-year growth", help="CSAT and NPS for each year; the label above each bar is the change from the previous year.")
yr_k = df.groupby("year").agg(csat=("overall_satisfaction", top2), nps=("nps", nps_score))
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.08, subplot_titles=("CSAT (% favorable) by year", "Net Promoter Score by year"))
for col_i, (col, color, unit) in enumerate([("csat", C["blue"], " pt"), ("nps", C["orange"], "")], start=1):
    vals = yr_k[col]
    yoy = vals.diff()
    labels = [("Pilot" if i == 0 else f"{d:+.1f}{unit}") for i, d in enumerate(yoy)]
    fig.add_trace(go.Bar(x=vals.index.astype(str), y=vals.values, marker_color=[("#b9b8b1" if y == vals.index[0] else color) for y in vals.index],
                         text=[f"{v:.1f}" for v in vals.values], textposition="inside", insidetextanchor="end",
                         textfont=dict(color="white"), showlegend=False,
                         hovertemplate="%{x}: %{y:.1f}<extra></extra>"), row=1, col=col_i)
    for xi, (v, lab, d) in enumerate(zip(vals.values, labels, yoy)):
        fig.add_annotation(x=xi, y=v, text=lab, showarrow=False, yshift=12, row=1, col=col_i,
                           font=dict(size=11, color=(C["muted"] if lab == "Pilot" else ("#0b7a0b" if d > 0 else "#b42318"))))
    lo = vals.min()
    fig.update_yaxes(range=[lo - (12 if col == "csat" else 15), vals.max() + (3 if col == "csat" else 6)], row=1, col=col_i)
fig.update_layout(**BASE_LAYOUT, height=360, bargap=0.35)
fig.update_xaxes(type="category")
fig.update_layout(margin=dict(l=10, r=10, t=40, b=10))
fig.update_yaxes(gridcolor=C["grid"], showgrid=True)
fig.update_yaxes(ticksuffix="%", row=1, col=1)
st.plotly_chart(fig, theme=None)
st.caption("Labels above the bars are the change from the previous year (green = up, red = down). 2020 is the pilot "
           "(one campaign). Axes start above zero to show year-to-year change; read the labels for exact differences.")
analysis(TOP["growth"])

# ------------------------------------------------------------------ Forecast with prediction intervals
st.subheader("Forecast: CSAT and NPS for the five 2026 campaigns", help="Linear-trend projection of campaign results for the five expected 2026 campaigns. The grey band is the 95% prediction interval: the range a single campaign is likely to fall in. " + TIPS["p_value"])
camp = (df.groupby("campaign_key").agg(mid=("start_datetime", "median"), n=("nps", "size"),
                                       csat=("overall_satisfaction", top2), nps=("nps", nps_score))
        .sort_values("mid"))
camp["t"] = (camp["mid"] - pd.Timestamp("2020-01-01")).dt.days / 365.25
# Expected 2026 campaign mid-points follow the anchor months the survey settled into (Jan, May, Jul, Sep, Nov)
future = pd.to_datetime(["2026-01-10", "2026-05-09", "2026-07-09", "2026-09-12", "2026-11-10"])
future_t = (future - pd.Timestamp("2020-01-01")).days / 365.25
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.08, subplot_titles=("CSAT (% favorable)", "Net Promoter Score"))
fc = {}
for col_i, (col, target, color) in enumerate([("csat", 85.0, C["blue"]), ("nps", 60.0, C["orange"])], start=1):
    fit = trend_fit(camp["t"], camp[col], future_t)
    fc[col] = fit
    fig.add_trace(go.Scatter(x=camp["mid"], y=camp[col], mode="lines+markers", line=dict(color=color, width=2),
                             marker=dict(size=6), customdata=np.stack([camp.index, camp["n"]], axis=1), showlegend=False,
                             hovertemplate="%{customdata[0]}<br>%{y:.1f} (n=%{customdata[1]:,})<extra></extra>"), row=1, col=col_i)
    xs = list(future) + list(future[::-1])
    fig.add_trace(go.Scatter(x=xs, y=list(fit["hi"]) + list(fit["lo"][::-1]), fill="toself", fillcolor="rgba(137,135,129,.22)",
                             mode="lines", line=dict(width=0), hoverinfo="skip", showlegend=False), row=1, col=col_i)
    fig.add_trace(go.Scatter(x=[camp["mid"].iloc[-1]] + list(future), y=[camp[col].iloc[-1]] + list(fit["pred"]),
                             mode="lines+markers", line=dict(color=color, width=2, dash="dash"), marker=dict(size=6, symbol="circle-open"),
                             showlegend=False, customdata=np.r_[[np.nan], fit["lo"]], text=np.r_[[np.nan], fit["hi"]],
                             hovertemplate="Forecast %{x|%b %Y}: %{y:.1f}<br>95% range %{customdata:.1f}–%{text:.1f}<extra></extra>"),
                  row=1, col=col_i)
    fig.add_hline(y=target, line=dict(color=C["ink2"], width=1, dash="dot"), row=1, col=col_i,
                  annotation_text=f"Target {target:.0f}", annotation_position="top left", annotation_font=dict(size=11))
    verdict = "significant" if fit["p"] < 0.05 else "not significant"
    ax = "" if col_i == 1 else "2"
    fig.add_annotation(xref=f"x{ax} domain", yref=f"y{ax} domain", x=0.01, y=0.02, xanchor="left", yanchor="bottom",
                       text=f"Trend {fit['slope']:+.2f} per year · p = {fit['p']:.2f} ({verdict})", showarrow=False,
                       font=dict(size=11, color=color), bgcolor="rgba(255,255,255,.8)")
fig.add_vrect(x0=future[0] - pd.Timedelta(days=20), x1=future[-1] + pd.Timedelta(days=20), fillcolor="rgba(137,135,129,.06)",
              line_width=0, row=1, col="all")
fig.update_layout(**BASE_LAYOUT, height=400)
fig.update_layout(margin=dict(l=10, r=10, t=40, b=10))
fig.update_yaxes(gridcolor=C["grid"], showgrid=True)
fig.update_yaxes(ticksuffix="%", row=1, col=1)
st.plotly_chart(fig, theme=None)
st.caption("Each point is one survey campaign (26 campaigns, 2020–2025). Dashed line = linear-trend forecast for the five expected "
           "2026 campaigns; grey band = 95% prediction interval, the range a single campaign is likely to fall in.")
analysis(TOP["forecast"])

# ------------------------------------------------------------------ Survey mandate compliance
st.subheader("Is the survey mandate being met? Local Law 26 compliance", help="NYC Local Law 26 of 2021 requires at least five customer-satisfaction survey campaigns a year.")
camps = df.groupby("year")["campaign"].nunique()
resp = df["year"].value_counts().sort_index()
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.08,
                    subplot_titles=("Survey campaigns per year", "Survey responses per year"))
fig.add_trace(go.Bar(x=camps.index.astype(str), y=camps.values, text=camps.values, textposition="outside",
                     marker_color=[(C["good"] if v >= LAW_MIN_CAMPAIGNS else ("#b9b8b1" if y == camps.index[0] else C["bad"]))
                                   for y, v in camps.items()], showlegend=False,
                     hovertemplate="%{x}: %{y} campaigns<extra></extra>"), row=1, col=1)
fig.add_hline(y=LAW_MIN_CAMPAIGNS, line=dict(color=C["ink2"], width=1, dash="dash"), row=1, col=1,
              annotation_text=f"Legal minimum: {LAW_MIN_CAMPAIGNS}", annotation_position="top left", annotation_font=dict(size=11))
fig.add_trace(go.Scatter(x=resp.index.astype(str), y=resp.values, mode="lines+markers+text", text=[f"{v:,}" for v in resp.values],
                         textposition="top center", line=dict(color=C["blue"], width=2.5), marker=dict(size=9), showlegend=False,
                         hovertemplate="%{x}: %{y:,} responses<extra></extra>"), row=1, col=2)
fig.update_layout(**BASE_LAYOUT, height=340)
fig.update_xaxes(type="category")
fig.update_layout(margin=dict(l=10, r=10, t=40, b=10))
fig.update_yaxes(range=[0, 7], dtick=1, row=1, col=1)
fig.update_yaxes(range=[0, resp.max() * 1.2], tickformat=",", gridcolor=C["grid"], showgrid=True, row=1, col=2)
st.plotly_chart(fig, theme=None)
st.caption("NYC Local Law 26 of 2021 requires at least five customer-satisfaction survey campaigns a year. 2020 was a single "
           "pilot campaign, before the law. The month-by-month view is on the Tactical page.")
analysis(TOP["compliance"])

# ------------------------------------------------------------------ Visualization 1 (Apriori): driver cards
st.subheader("Future opportunities & risks: what turns callers into promoters or detractors", help="Rating combinations that predict each NPS group, found with Apriori association rules. Hover Reliability, Customer share and Impact on a card for their definitions.")
rules = nps_rules(df)


def cards(segment, title, subtitle, k=3):
    color = SEG_COLORS[segment]
    seg_tip = {"Promoter": TIPS["promoters"], "Passive": TIPS["passives"], "Detractor": TIPS["detractors"]}[segment]
    st.markdown(f"<div style='color:{color};font-weight:700;letter-spacing:.03em;margin:4px 0 8px'>{tip(title, seg_tip)}</div>"
                f"<div style='font-size:.8rem;opacity:.7;margin:-6px 0 8px'>{subtitle}</div>", unsafe_allow_html=True)
    top = rules[rules["segment"] == segment].head(k)
    if top.empty:
        st.caption("No rule met the thresholds.")
    for _, r in top.iterrows():
        st.markdown(
            f"<div class='rule-card' style='border-left-color:{color}'>"
            f"<div class='rule-title'>{html.escape(r['combination'])}</div>"
            f"<div class='rule-meta'><span><b>{tip('Reliability', TIPS['reliability'])}</b> {r['confidence'] * 100:.2f}%</span>"
            f"<span><b>{tip('Customer share', TIPS['share'])}</b> {r['support'] * 100:.2f}%</span>"
            f"<span><b>{tip('Impact', TIPS['impact'], right=True)}</b> <span style='color:{color};font-weight:700'>{r['lift']:.2f}× higher</span></span></div></div>",
            unsafe_allow_html=True)


left, right = st.columns(2, gap="large")
with left:
    cards("Promoter", "TOP PROMOTER DRIVERS", "Positive association")
with right:
    cards("Passive", "TOP PASSIVE DRIVERS", "Opportunities: callers who could be converted")
    cards("Detractor", "TOP DETRACTOR DRIVERS", "Risks: the pain points that create detractors")
st.caption("Apriori association rules (support ≥ 5%, confidence ≥ 30%). Reliability = confidence (chance the combination "
           "produces that NPS group). Customer share = support (% of all callers with the combination). Impact = lift (how many "
           "times more likely than average). The decision tree behind these drivers is on the Tactical page.")
with st.expander("All mined rules"):
    st.dataframe(rules.rename(columns={"segment": "NPS group", "combination": "Rating combination", "confidence": "Reliability",
                                       "support": "Customer share", "lift": "Impact (×)"})
                 .style.format({"Reliability": "{:.2%}", "Customer share": "{:.2%}", "Impact (×)": "{:.2f}"}),
                 hide_index=True, width="stretch", column_config=col_help({
                     "NPS group": "The NPS segment the rating combination predicts.",
                     "Rating combination": "Ratings that occur together (all must be true).",
                     "Reliability": TIPS["reliability"], "Customer share": TIPS["share"], "Impact (×)": TIPS["impact"]}))
analysis(TOP["apriori"])

# ------------------------------------------------------------------ Conclusion and recommendations
page_conclusion(PAGE_CONCLUSIONS["TOP"], "Owner")
