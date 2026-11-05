"""Lower-level management (Operational): daily monitoring for supervisors and team leads."""
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

from common import (BASE_LAYOUT, C, DIMENSIONS, DRIVERS, LANG_COLORS, LIKERT_COLORS, LIKERT_LABELS,
                    analysis, bottom2, campaign_order, delta_html, kpi_card, load_data, nps_score, top2)
from narrative import LOWER, LOWER_SUMMARY

CSAT_TARGET = 80.0   # working target (historical CSAT is 80.9%)
MIN_DAILY_N = 15     # a day needs this many responses before it can be flagged
FOLLOW_UP_ROWS = 15

df = load_data()
order = campaign_order(df)
latest = order[-1]

st.markdown("<div class='level-tag'>Lower-level management · Operational</div>", unsafe_allow_html=True)
st.title("Daily operations")
st.caption("For call-center floor supervisors, team leads and QA leads. Answers: what happened each day, "
           "which transactions need action, which service areas were rated poorly, and which queues performed poorly.")

f1, f2 = st.columns([1, 2])
campaign = f1.selectbox("Campaign", order[::-1], index=0, help="The latest campaign is selected by default.")
is_default = campaign == latest
idx = order.index(campaign)
prev_key = order[idx - 1] if idx > 0 else None
cur = df[df["campaign_key"] == campaign].copy()
prev = df[df["campaign_key"] == prev_key] if prev_key else df.iloc[0:0]
period = f"{cur['start_date'].min():%b %d, %Y} – {cur['start_date'].max():%b %d, %Y}"
f2.markdown(f"<div style='padding-top:1.9rem;opacity:.75'>{period} · {len(cur):,} responses · "
            f"{cur['start_date'].nunique()} active days · CSAT target {CSAT_TARGET:.0f}%</div>", unsafe_allow_html=True)
if not is_default:
    st.info(f"The written analysis describes {latest}. Charts and tables update for {campaign}; "
            "the analysis notes are hidden for other campaigns.")


def note(key):
    if is_default:
        analysis(LOWER[key])


def kpis(d):
    return dict(responses=len(d), csat=top2(d["overall_satisfaction"]), nps=nps_score(d["nps"]),
                wait=top2(d["wait_time"]), answer=top2(d["answer_satisfaction"]),
                dissatisfied=int((d["overall_satisfaction"] <= 2).sum()))


# ------------------------------------------------------------------ V1 KPI cards
k, kp = kpis(cur), (kpis(prev) if len(prev) else {})
st.subheader("Operational scorecard")
st.caption(f"Whole campaign · changes compare with {prev_key or 'no earlier campaign'}")
row1 = st.columns(3)
row2 = st.columns(3)
with row1[0]:
    kpi_card("Survey responses", f"{k['responses']:,}", delta_html(k["responses"], kp.get("responses"), "", True, 0),
             "Completed surveys")
with row1[1]:
    status = ("<span class='pill pill-good'>✔ On target</span>" if k["csat"] >= CSAT_TARGET
              else "<span class='pill pill-bad'>✖ Below target</span>")
    kpi_card("CSAT (Overall 4–5)", f"{k['csat']:.1f}%", delta_html(k["csat"], kp.get("csat")), f"Target {CSAT_TARGET:.0f}% {status}")
with row1[2]:
    kpi_card("Net Promoter Score", f"{k['nps']:+.1f}", delta_html(k["nps"], kp.get("nps"), ""), "Promoters − detractors")
with row2[0]:
    kpi_card("Wait time rated OK", f"{k['wait']:.1f}%", delta_html(k["wait"], kp.get("wait")), "Wait Time 4–5")
with row2[1]:
    kpi_card("Answer satisfaction", f"{k['answer']:.1f}%", delta_html(k["answer"], kp.get("answer")), "Answer Satisfaction 4–5")
with row2[2]:
    kpi_card("Dissatisfied callers", f"{k['dissatisfied']:,}",
             delta_html(k["dissatisfied"], kp.get("dissatisfied"), "", False, 0),
             f"Overall 1–2 · {k['dissatisfied'] / max(k['responses'], 1) * 100:.1f}% of responses")
note("kpi")

# ------------------------------------------------------------------ daily table used by V2 and V6
daily = (cur.groupby("start_date")
         .apply(lambda d: pd.Series({
             "responses": len(d), "positive": int((d["overall_satisfaction"] >= 4).sum()),
             "csat": top2(d["overall_satisfaction"]), "answer_ok": top2(d["answer_satisfaction"]),
             "wait_ok": top2(d["wait_time"]), "nps": nps_score(d["nps"]),
             "dissatisfied": int((d["overall_satisfaction"] <= 2).sum())}), include_groups=False)
         .reset_index())
daily["reliable"] = daily["responses"] >= MIN_DAILY_N
daily["below"] = daily["reliable"] & (daily["csat"] < CSAT_TARGET)
cal = pd.date_range(daily["start_date"].min(), daily["start_date"].max(), freq="D")
roll = daily.set_index("start_date")[["positive", "responses"]].reindex(cal, fill_value=0).rolling(7, min_periods=1).sum()
roll["csat_7d"] = roll["positive"] / roll["responses"] * 100

# ------------------------------------------------------------------ V2 Daily trend
st.subheader("What happened each day")
fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.09, row_heights=[0.6, 0.4],
                    subplot_titles=("Daily CSAT % (Overall Satisfaction 4–5)", "Daily survey responses"))
fig.add_trace(go.Scatter(x=roll.index, y=roll["csat_7d"], mode="lines", name="7-day rolling CSAT",
                         line=dict(color=C["blue"], width=2), customdata=roll[["responses"]],
                         hovertemplate="7 days to %{x|%b %d}<br>Rolling CSAT %{y:.1f}%<br>"
                                       "Responses in window %{customdata[0]:,.0f}<extra></extra>"), row=1, col=1)
for label, mask, color, size in [(f"Day on target (≥{MIN_DAILY_N} responses)", daily["reliable"] & ~daily["below"], C["blue"], 9),
                                 ("Day below target", daily["below"], C["bad"], 10),
                                 (f"Too few responses (<{MIN_DAILY_N})", ~daily["reliable"], "#c3c2b7", 7)]:
    d = daily[mask]
    fig.add_trace(go.Scatter(x=d["start_date"], y=d["csat"], mode="markers", name=label,
                             marker=dict(size=size, color=color, line=dict(color="white", width=1.5)),
                             customdata=d[["responses", "dissatisfied"]],
                             hovertemplate="%{x|%a %b %d}<br>Day CSAT %{y:.1f}%<br>Responses %{customdata[0]}"
                                           "<br>Dissatisfied %{customdata[1]}<extra></extra>"), row=1, col=1)
fig.add_hline(y=CSAT_TARGET, line=dict(color=C["ink2"], width=1, dash="dash"), row=1, col=1,
              annotation_text=f"Target {CSAT_TARGET:.0f}%", annotation_position="top left")
fig.add_trace(go.Bar(x=daily["start_date"], y=daily["responses"], name="Responses", marker_color=C["blue"],
                     hovertemplate="%{x|%a %b %d}<br>Responses %{y}<extra></extra>"), row=2, col=1)
fig.update_layout(**BASE_LAYOUT, height=560, legend=dict(orientation="h", y=-0.1, x=0.5, xanchor="center"))
fig.update_layout(margin=dict(l=10, r=10, t=40, b=10))
fig.update_yaxes(title_text="CSAT %", range=[min(20, daily["csat"].min() - 5), 105], gridcolor=C["grid"], showgrid=True, row=1, col=1)
fig.update_yaxes(title_text="Responses", gridcolor=C["grid"], showgrid=True, row=2, col=1)
fig.update_xaxes(dtick=7 * 86400000, tick0=daily["start_date"].min(), tickformat="%b %d")
st.plotly_chart(fig, theme=None)
st.caption("Line = CSAT over the last 7 days, pooled across responses so small days cannot swing it. "
           "Dots = single days; grey dots have too few responses to judge.")
note("daily")

# ------------------------------------------------------------------ V3 Service dimensions + V5 heat map
left, right = st.columns(2, gap="large")
with left:
    st.subheader("Where callers are unhappy")
    dist = pd.DataFrame({lab: cur[col].value_counts(normalize=True).reindex([1, 2, 3, 4, 5], fill_value=0) * 100
                         for col, lab in DIMENSIONS.items()}).T
    dist["positive"], dist["negative"] = dist[4] + dist[5], dist[1] + dist[2]
    dist = dist.sort_values("positive", ascending=False)
    half = dist[3] / 2
    segs = {1: (-(half + dist[2] + dist[1]), dist[1]), 2: (-(half + dist[2]), dist[2]), 3: (-half, dist[3]),
            4: (half, dist[4]), 5: (half + dist[4], dist[5])}
    fig = go.Figure()
    for s, (start, width) in segs.items():
        fig.add_trace(go.Bar(y=dist.index, x=width, base=start, orientation="h", name=LIKERT_LABELS[s],
                             marker=dict(color=LIKERT_COLORS[s], line=dict(color="white", width=1)), customdata=width,
                             hovertemplate="%{y}<br>" + LIKERT_LABELS[s] + ": %{customdata:.1f}%<extra></extra>"))
    for name, r in dist.iterrows():
        fig.add_annotation(x=r[3] / 2 + r["positive"], y=name, text=f"<b>{r['positive']:.0f}%</b>", showarrow=False,
                           xanchor="left", xshift=5)
        fig.add_annotation(x=-(r[3] / 2 + r["negative"]), y=name, text=f"{r['negative']:.0f}%", showarrow=False,
                           xanchor="right", xshift=-5, font=dict(color="#b42318"))
    fig.update_layout(**BASE_LAYOUT, barmode="overlay", bargap=0.35, height=400,
                      legend=dict(orientation="h", y=-0.12, x=0.5, xanchor="center", font=dict(size=11), traceorder="normal"))
    fig.update_xaxes(range=[-50, 112], tickvals=[-40, -20, 0, 20, 40, 60, 80, 100],
                     ticktext=["40%", "20%", "0", "20%", "40%", "60%", "80%", "100%"], showgrid=True,
                     gridcolor=C["grid"], zeroline=True, zerolinecolor=C["ink2"])
    st.plotly_chart(fig, theme=None)
    st.caption("Negative ratings (1–2) extend left of centre, positive (4–5) right; Neutral is split across the centre.")
    note("dims")
with right:
    st.subheader("Weekly problem map")
    cur["week_start"] = cur["start_date"].dt.to_period("W-SUN").dt.start_time
    wk = cur.groupby("week_start")[list(DIMENSIONS)].apply(lambda d: (d <= 2).mean() * 100)
    wn = cur.groupby("week_start").size()
    wk.columns = ["Overall", "Wait time", "Agent service", "Knowledge", "Answer"]
    z = wk.T
    fig = go.Figure(go.Heatmap(
        z=z.values, x=[f"{w:%b %d}<br>n={wn[w]:,}" for w in z.columns], y=z.index, xgap=2, ygap=2,
        colorscale=[[0, "#fcf4f3"], [0.5, "#ec9a9a"], [1, "#a32626"]], zmin=0, zmax=max(25, float(np.nanmax(z.values))),
        text=np.vectorize(lambda v: f"{v:.0f}%")(z.values), texttemplate="%{text}", textfont=dict(size=11),
        showscale=False,
        hovertemplate="%{y}<br>Week of %{x}<br>Negative %{z:.1f}%<extra></extra>"))
    # (dimension rows: Overall Satisfaction, Wait Time, Agent Customer Service, Agent Job Knowledge, Answer Satisfaction)
    fig.update_layout(**BASE_LAYOUT, height=380)
    fig.update_yaxes(autorange="reversed")
    fig.update_xaxes(tickangle=0, tickfont=dict(size=10), side="bottom")
    st.plotly_chart(fig, theme=None)
    st.caption("% of callers rating each area 1–2, by week (Monday start). Darker = more negative; small weeks swing more.")
    note("heatmap")

# ------------------------------------------------------------------ V4 Language queues
st.subheader("Language queue performance")
LANG_ORDER = ["English", "Spanish", "Chinese", "Others"]
METRICS = {"csat": "CSAT", "wait": "Wait Time OK", "agent": "Agent Service OK", "answer": "Answer Satisfaction"}
lang = pd.DataFrame({lg: {"responses": len(d), "csat": top2(d["overall_satisfaction"]), "wait": top2(d["wait_time"]),
                          "agent": top2(d["agent_customer_service"]), "answer": top2(d["answer_satisfaction"]),
                          "nps": nps_score(d["nps"]), "dissatisfied": int((d["overall_satisfaction"] <= 2).sum())}
                     for lg, d in cur.groupby("language_queue")}).T.reindex(LANG_ORDER).dropna(how="all")
lang["share"] = lang["responses"] / lang["responses"].sum() * 100
c1, c2 = st.container(), st.container()
with c1:
    fig = go.Figure()
    for lg, r in lang.iterrows():
        fig.add_trace(go.Bar(x=list(METRICS.values()), y=[r[m] for m in METRICS], name=f"{lg} (n={int(r.responses):,})",
                             marker=dict(color=LANG_COLORS[lg], line=dict(color="white", width=1.5)),
                             hovertemplate=f"{lg} · %{{x}}: %{{y:.1f}}%<extra></extra>"))
    fig.add_hline(y=CSAT_TARGET, line=dict(color=C["ink2"], width=1, dash="dash"),
                  annotation_text=f"Target {CSAT_TARGET:.0f}%", annotation_position="top right")
    fig.update_layout(**BASE_LAYOUT, barmode="group", height=380, legend=dict(orientation="h", y=1.1, x=0))
    fig.update_yaxes(title_text="% rating 4–5", range=[0, 100], gridcolor=C["grid"], showgrid=True)
    st.plotly_chart(fig, theme=None)
with c2:
    t = lang[["responses", "share", "csat", "wait", "agent", "answer", "nps", "dissatisfied"]].rename(columns={
        "responses": "Responses", "share": "Share of volume %", "csat": "CSAT %", "wait": "Wait OK %",
        "agent": "Agent Service OK %", "answer": "Answer %", "nps": "NPS", "dissatisfied": "Dissatisfied"})
    t.index.name = "Language queue"
    st.dataframe(t.style.format({"Responses": "{:,.0f}", "Share of volume %": "{:.1f}", "CSAT %": "{:.1f}", "Wait OK %": "{:.1f}",
                                 "Agent Service OK %": "{:.1f}", "Answer %": "{:.1f}", "NPS": "{:+.1f}", "Dissatisfied": "{:,.0f}"}), width="stretch")
    st.caption("No agent or team IDs are published, so the survey language stands in for the queue. "
               "Others = Russian, Korean, Arabic, Polish, French and other languages.")
note("queues")

# ------------------------------------------------------------------ V6 Exceptions report
st.subheader("Daily exceptions report")


def status(r):
    if r.csat < 70 or r.answer_ok < 55:
        return "✖ Critical"
    if r.csat < CSAT_TARGET or r.answer_ok < 60 or r.wait_ok < 75:
        return "▲ Warning"
    return "✔ OK"


def reason(r):
    out = []
    if r.csat < CSAT_TARGET: out.append(f"CSAT {r.csat:.0f}% < {CSAT_TARGET:.0f}%")
    if r.answer_ok < 60: out.append(f"Answer {r.answer_ok:.0f}% < 60%")
    if r.wait_ok < 75: out.append(f"Wait {r.wait_ok:.0f}% < 75%")
    return "; ".join(out) or "—"


rep = daily[daily["reliable"]].copy()
rep["Status"] = rep.apply(status, axis=1)
rep["Reason"] = rep.apply(reason, axis=1)
counts = rep["Status"].value_counts()
st.caption(f"Days with ≥{MIN_DAILY_N} responses. Critical: CSAT < 70% or Answer < 55%. Warning: CSAT < target, "
           f"Answer < 60% or Wait OK < 75%. This campaign: {counts.get('✖ Critical', 0)} critical, "
           f"{counts.get('▲ Warning', 0)} warning, {counts.get('✔ OK', 0)} OK; {int((~daily['reliable']).sum())} days had too few responses to rate.")
rep = rep.rename(columns={"start_date": "Date", "responses": "Responses", "csat": "CSAT %", "answer_ok": "Answer %",
                          "wait_ok": "Wait OK %", "nps": "NPS", "dissatisfied": "Dissatisfied"})
rep["Date"] = rep["Date"].dt.strftime("%a %b %d")
rep = rep[["Date", "Responses", "CSAT %", "Answer %", "Wait OK %", "NPS", "Dissatisfied", "Status", "Reason"]]
STATUS_STYLE = {"✖ Critical": "background-color:#fdecec;color:#b42318;font-weight:600",
                "▲ Warning": "background-color:#fff4dc;color:#8a5a00;font-weight:600",
                "✔ OK": "background-color:#e7f6e7;color:#0b7a0b;font-weight:600"}
st.dataframe(rep.style.format({"CSAT %": "{:.1f}", "Answer %": "{:.1f}", "Wait OK %": "{:.1f}", "NPS": "{:+.1f}",
                               "Responses": "{:,.0f}", "Dissatisfied": "{:,.0f}"})
             .map(lambda v: STATUS_STYLE.get(v, ""), subset=["Status"])
             .bar(subset=["Responses"], color="#cde2fb", vmin=0),
             hide_index=True, width="stretch", height=36 * (len(rep) + 1) + 4)
note("exceptions")

# ------------------------------------------------------------------ V7 Follow-up log
st.subheader("Customer follow-up log")
flag = cur[(cur["overall_satisfaction"] <= 2) | (cur["nps"] <= 6)].copy()
flag["Priority"] = np.where((flag["overall_satisfaction"] == 1) | (flag["nps"] <= 3), "High", "Medium")


def weakest(r):
    vals = r[DRIVERS]
    if vals.nunique() == 1:
        return "All equal"
    return " / ".join(DIMENSIONS[c] for c in DRIVERS if vals[c] == vals.min())


flag["Weakest area"] = flag.apply(weakest, axis=1)
days = sorted(flag["start_date"].dt.date.unique(), reverse=True)
pick = st.selectbox("Show", ["Latest 15 responses"] + [f"All on {d:%a %b %d, %Y}" for d in days], index=0)
if pick.startswith("All on"):
    day = pd.to_datetime(pick.replace("All on ", ""), format="%a %b %d, %Y")
    shown = flag[flag["start_date"] == day]
else:
    shown = flag
shown = shown.sort_values("start_datetime", ascending=False)
if not pick.startswith("All on"):
    shown = shown.head(FOLLOW_UP_ROWS)
st.caption(f"Low-score responses: Overall 1–2 or NPS 0–6. {len(flag):,} in this campaign "
           f"({(flag['Priority'] == 'High').sum():,} High priority: Overall 1 or NPS 0–3). "
           "Response ID is the row number in the source CSV; the public data holds no personal details.")
log = pd.DataFrame({
    "Response ID": shown["row_id"].map(lambda i: f"R-{i:05d}"),
    "Responded": shown["start_datetime"].dt.strftime("%b %d %I:%M %p"),
    "Queue": shown["language_queue"], "Overall": shown["overall_satisfaction"], "Wait": shown["wait_time"],
    "Agent": shown["agent_customer_service"], "Knowledge": shown["agent_job_knowledge"],
    "Answer": shown["answer_satisfaction"], "NPS": shown["nps"], "Weakest area": shown["Weakest area"],
    "Priority": shown["Priority"]})
SCORE_STYLE = {1: "background-color:#f6d3d3", 2: "background-color:#fbe7e7", 3: "background-color:#f0efec"}
st.dataframe(log.style.map(lambda v: SCORE_STYLE.get(v, ""), subset=["Overall", "Wait", "Agent", "Knowledge", "Answer"])
             .map(lambda v: "color:#b42318;font-weight:600" if v == "High" else "color:#8a5a00;font-weight:600",
                  subset=["Priority"]),
             hide_index=True, width="stretch", height=min(36 * (len(log) + 1) + 4, 760))
note("followup")

# ------------------------------------------------------------------ Summary
if is_default and st.session_state.get("show_analysis", True):
    st.subheader("Key findings & recommended actions")
    st.markdown("| # | Key finding | Recommended operational action | Owner |\n|---|---|---|---|\n" +
                "\n".join(f"| {i} | {a} | {b} | {c} |" for i, (a, b, c) in enumerate(LOWER_SUMMARY, 1)))
