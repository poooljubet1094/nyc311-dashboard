"""Lower-level management (Operational): daily monitoring for supervisors and team leads."""
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

from common import (BASE_LAYOUT, C, DIMENSIONS, DRIVERS, LANG_COLORS, LIKERT_COLORS, LIKERT_LABELS, TIPS,
                    analysis, campaign_order, col_help, delta_html, kpi_card, load_data, nps_score, page_conclusion, top2,
                    wilson)
from narrative import LOWER, PAGE_CONCLUSIONS

CSAT_TARGET = 80.0   # working target (historical CSAT is 80.9%)
MIN_DAILY_N = 15     # a day needs this many responses before business-rule flags apply
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


# Last six campaigns (ending at the selected one) for the KPI sparklines
hist_keys = order[max(0, idx - 5): idx + 1]
hist = pd.DataFrame([kpis(df[df["campaign_key"] == k]) for k in hist_keys], index=hist_keys)
spark_note = f"Last {len(hist_keys)} campaigns"

# ------------------------------------------------------------------ V1 KPI cards
k, kp = kpis(cur), (kpis(prev) if len(prev) else {})
st.subheader("Operational scorecard", help="Whole-campaign KPIs for the selected campaign. Arrows compare with the previous campaign; sparklines show the last six campaigns. Hover a card label for its definition.")
st.caption(f"Whole campaign · changes compare with {prev_key or 'no earlier campaign'} · sparklines show the last {len(hist_keys)} campaigns")
row1 = st.columns(3)
row2 = st.columns(3)
with row1[0]:
    kpi_card("Survey responses", f"{k['responses']:,}", delta_html(k["responses"], kp.get("responses"), "", True, 0),
             "Completed surveys", hist["responses"], spark_note)
with row1[1]:
    status = ("<span class='pill pill-good'>✔ On target</span>" if k["csat"] >= CSAT_TARGET
              else "<span class='pill pill-bad'>✖ Below target</span>")
    kpi_card("CSAT (Overall 4–5)", f"{k['csat']:.1f}%", delta_html(k["csat"], kp.get("csat")),
             f"Target {CSAT_TARGET:.0f}% {status}", hist["csat"], spark_note)
with row1[2]:
    kpi_card("Net Promoter Score", f"{k['nps']:+.1f}", delta_html(k["nps"], kp.get("nps"), ""),
             "Promoters − detractors", hist["nps"], spark_note)
with row2[0]:
    kpi_card("Wait time rated OK", f"{k['wait']:.1f}%", delta_html(k["wait"], kp.get("wait")), "Wait Time 4–5",
             hist["wait"], spark_note)
with row2[1]:
    kpi_card("Answer satisfaction", f"{k['answer']:.1f}%", delta_html(k["answer"], kp.get("answer")),
             "Answer Satisfaction 4–5", hist["answer"], spark_note)
with row2[2]:
    kpi_card("Dissatisfied callers", f"{k['dissatisfied']:,}",
             delta_html(k["dissatisfied"], kp.get("dissatisfied"), "", False, 0),
             f"Overall 1–2 · {k['dissatisfied'] / max(k['responses'], 1) * 100:.1f}% of responses",
             hist["dissatisfied"], spark_note)
note("kpi")

# ------------------------------------------------------------------ daily table with control limits
daily = (cur.groupby("start_date")
         .apply(lambda d: pd.Series({
             "responses": len(d), "positive": int((d["overall_satisfaction"] >= 4).sum()),
             "csat": top2(d["overall_satisfaction"]), "answer_ok": top2(d["answer_satisfaction"]),
             "wait_ok": top2(d["wait_time"]), "nps": nps_score(d["nps"]),
             "dissatisfied": int((d["overall_satisfaction"] <= 2).sum())}), include_groups=False)
         .reset_index())
p_bar = daily["positive"].sum() / daily["responses"].sum()
sigma = np.sqrt(p_bar * (1 - p_bar) / daily["responses"])
daily["lcl"] = np.clip(p_bar - 3 * sigma, 0, 1) * 100
daily["ucl"] = np.clip(p_bar + 3 * sigma, 0, 1) * 100
daily["reliable"] = daily["responses"] >= MIN_DAILY_N
daily["below"] = daily["reliable"] & (daily["csat"] < CSAT_TARGET)
daily["out_low"] = daily["csat"] < daily["lcl"]
daily["out_high"] = daily["csat"] > daily["ucl"]
cal = pd.date_range(daily["start_date"].min(), daily["start_date"].max(), freq="D")
roll = daily.set_index("start_date")[["positive", "responses"]].reindex(cal, fill_value=0).rolling(7, min_periods=1).sum()
roll["csat_7d"] = roll["positive"] / roll["responses"] * 100

# ------------------------------------------------------------------ Alerts
runs, run = [], []
for r in daily.itertuples():
    if r.below and run and (r.start_date - run[-1]).days == 1:
        run.append(r.start_date)
    elif r.below:
        if len(run) >= 2:
            runs.append(run)
        run = [r.start_date]
    else:
        if len(run) >= 2:
            runs.append(run)
        run = []
if len(run) >= 2:
    runs.append(run)
out_days = daily[daily["out_low"]]
alerts = []
for rn in runs:
    alerts.append(f"**Escalation rule:** {len(rn)} consecutive days below the {CSAT_TARGET:.0f}% target "
                  f"({rn[0]:%b %d}–{rn[-1]:%b %d}).")
for r in out_days.itertuples():
    alerts.append(f"**Out of control:** {r.start_date:%a %b %d} CSAT {r.csat:.1f}% is below its lower control limit "
                  f"({r.lcl:.1f}%, n = {r.responses}).")
if alerts:
    msg = "  \n".join(alerts)
    if out_days.empty:
        msg += "  \nNo day fell outside its statistical control limits, so treat the run as a pattern to review, not a single-day breakdown."
    (st.error if not out_days.empty else st.warning)(msg, icon=":material/warning:")
else:
    st.success("No alerts: no run of two or more days below target and no day outside its control limits.",
               icon=":material/check_circle:")

# ------------------------------------------------------------------ V2 Control chart (click a day)
st.subheader("What happened each day", help="Daily CSAT on a control chart (top) and survey responses per day (bottom). " + TIPS["control"] + " Click a dot or bar to open that day.")
show_roll = st.toggle("Show 7-day rolling CSAT", value=False, help="Adds a line showing CSAT pooled over the previous 7 days, which smooths out days with few responses.")
fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.09, row_heights=[0.62, 0.38],
                    subplot_titles=("Daily CSAT % with 3-sigma control limits", "Daily survey responses"))
# Control limits drawn as a light vertical range bar per day (wide on small days, narrow on busy ones)
for reliable, alpha, name, show in [(True, 0.28, "Control limits (±3σ)", True), (False, 0.10, "", False)]:
    seg_x, seg_y = [], []
    for r in daily[daily["reliable"] == reliable].itertuples():
        seg_x += [r.start_date, r.start_date, None]
        seg_y += [r.lcl, r.ucl, None]
    fig.add_trace(go.Scatter(x=seg_x, y=seg_y, mode="lines", line=dict(color=f"rgba(42,120,214,{alpha})", width=7),
                             name=name, showlegend=show, hoverinfo="skip"), row=1, col=1)
fig.add_hline(y=p_bar * 100, line=dict(color=C["blue"], width=1), row=1, col=1,
              annotation_text=f"Campaign average {p_bar * 100:.1f}%", annotation_position="top right",
              annotation_font=dict(size=11, color=C["blue"]))
fig.add_hline(y=CSAT_TARGET, line=dict(color=C["ink2"], width=1, dash="dash"), row=1, col=1,
              annotation_text=f"Target {CSAT_TARGET:.0f}%", annotation_position="bottom right",
              annotation_font=dict(size=11))
if show_roll:
    fig.add_trace(go.Scatter(x=roll.index, y=roll["csat_7d"], mode="lines", name="7-day rolling CSAT",
                             line=dict(color=C["navy"], width=2), hovertemplate="7 days to %{x|%b %d}: %{y:.1f}%<extra></extra>"),
                  row=1, col=1)


def point_kind(r):
    if r.out_low:
        return "Below control limit"
    if r.out_high:
        return "Above control limit"
    if not r.reliable:
        return f"Fewer than {MIN_DAILY_N} responses"
    return "Within limits"


daily["kind"] = daily.apply(point_kind, axis=1)
KIND_STYLE = {"Within limits": (C["blue"], 9), "Below control limit": (C["bad"], 11),
              "Above control limit": (C["good"], 11), f"Fewer than {MIN_DAILY_N} responses": ("#b9b8b1", 7)}
for kind, (color, size) in KIND_STYLE.items():
    d = daily[daily["kind"] == kind]
    if d.empty:
        continue
    fig.add_trace(go.Scatter(
        x=d["start_date"], y=d["csat"], mode="markers", name=kind,
        marker=dict(size=size, color=color, line=dict(color="white", width=1.5)),
        customdata=np.stack([d["responses"], d["lcl"], d["ucl"], d["dissatisfied"]], axis=1),
        hovertemplate="%{x|%a %b %d}<br>CSAT %{y:.1f}% (n=%{customdata[0]:.0f})<br>"
                      "Limits %{customdata[1]:.1f}–%{customdata[2]:.1f}%<br>Dissatisfied %{customdata[3]:.0f}"
                      "<br><i>Click to open this day</i><extra></extra>"), row=1, col=1)
fig.add_trace(go.Bar(x=daily["start_date"], y=daily["responses"], name="Responses", marker_color=C["blue"],
                     showlegend=False, hovertemplate="%{x|%a %b %d}<br>Responses %{y}<br><i>Click to open this day</i><extra></extra>"),
              row=2, col=1)
fig.update_layout(**BASE_LAYOUT, height=580, legend=dict(orientation="h", y=-0.1, x=0.5, xanchor="center"),
                  clickmode="event+select")
fig.update_layout(margin=dict(l=10, r=10, t=40, b=10))
fig.update_yaxes(title_text="CSAT %", range=[max(0, daily["csat"].min() - 8), 103],
                 gridcolor=C["grid"], showgrid=True, row=1, col=1)
fig.update_yaxes(title_text="Responses", gridcolor=C["grid"], showgrid=True, row=2, col=1)
fig.update_xaxes(dtick=7 * 86400000, tick0=daily["start_date"].min(), tickformat="%b %d")

nonce = st.session_state.setdefault("daily_nonce", 0)
event = st.plotly_chart(fig, theme=None, on_select="rerun", selection_mode="points", key=f"daily_{campaign}_{nonce}")
sel_day = None
try:
    pts = event.selection.points
except AttributeError:
    pts = []
if pts:
    sel_day = pd.to_datetime(pts[0]["x"]).normalize()
st.caption("The light vertical bar behind each dot is that day's 3-sigma control limits around the campaign average: long on "
           "small days, short on busy ones. A dot outside its bar is statistically unusual. **Click any dot or bar** to open that day.")

# ------------------------------------------------------------------ Day snapshot (cross-filter)
if sel_day is not None:
    day_rows = cur[cur["start_date"] == sel_day]
    head, btn = st.columns([4, 1])
    head.markdown(f"#### Day snapshot · {sel_day:%A, %B %d, %Y}")
    if btn.button("Clear day", icon=":material/close:", help="Remove the day filter and show the latest responses again."):
        st.session_state["daily_nonce"] += 1
        st.rerun()
    if day_rows.empty:
        st.caption("No survey responses arrived on this day.")
    else:
        dk = kpis(day_rows)
        drow = daily[daily["start_date"] == sel_day].iloc[0]
        m = st.columns(5)
        m[0].metric("Responses", f"{dk['responses']:,}", help=TIPS["responses"])
        m[1].metric("CSAT", f"{dk['csat']:.1f}%", f"{dk['csat'] - k['csat']:+.1f} pt vs campaign", help=TIPS["csat"])
        m[2].metric("Answer satisfaction", f"{dk['answer']:.1f}%", f"{dk['answer'] - k['answer']:+.1f} pt vs campaign", help=TIPS["answer"])
        m[3].metric("Wait time OK", f"{dk['wait']:.1f}%", f"{dk['wait'] - k['wait']:+.1f} pt vs campaign", help=TIPS["wait"])
        m[4].metric("Dissatisfied", f"{dk['dissatisfied']:,}", help=TIPS["dissatisfied"])
        verdict = ("**outside** its control limits (statistically unusual)" if drow.out_low or drow.out_high
                   else "**within** its control limits (normal variation for its sample size)")
        st.caption(f"This day's CSAT is {verdict}: limits {drow.lcl:.1f}–{drow.ucl:.1f}% for n = {int(drow.responses)}. "
                   "The follow-up log below is filtered to this day.")
note("daily")

# ------------------------------------------------------------------ Campaign pacing vs same campaign last year
st.subheader("Campaign pacing vs last year", help="Cumulative CSAT by day of campaign compared with the same campaign one year earlier, to judge an in-progress campaign early.")
camp_name = campaign.split(" ", 1)[1]
last_year_key = f"{int(campaign.split(' ')[0]) - 1} {camp_name}"


def pacing(key):
    c = df[df["campaign_key"] == key].sort_values("start_datetime")
    day = (c["start_date"] - c["start_date"].min()).dt.days + 1
    pos = (c["overall_satisfaction"] >= 4).groupby(day).sum().cumsum()
    n = c.groupby(day).size().cumsum()
    return (pos / n * 100), n


fig = go.Figure()
cum, n_cum = pacing(campaign)
if last_year_key in order:
    cum_ly, n_ly = pacing(last_year_key)
    fig.add_trace(go.Scatter(x=cum_ly.index, y=cum_ly.values, mode="lines", name=last_year_key,
                             line=dict(color=C["muted"], width=2), customdata=n_ly.values,
                             hovertemplate="Day %{x}: %{y:.1f}% (%{customdata:,} responses so far)<extra>" + last_year_key + "</extra>"))
fig.add_trace(go.Scatter(x=cum.index, y=cum.values, mode="lines", name=campaign, line=dict(color=C["blue"], width=2.5),
                         customdata=n_cum.values,
                         hovertemplate="Day %{x}: %{y:.1f}% (%{customdata:,} responses so far)<extra>" + campaign + "</extra>"))
fig.add_hline(y=CSAT_TARGET, line=dict(color=C["ink2"], width=1, dash="dash"), annotation_text=f"Target {CSAT_TARGET:.0f}%",
              annotation_position="bottom right")
fig.update_layout(**BASE_LAYOUT, height=320, legend=dict(orientation="h", y=1.12, x=0))
fig.update_xaxes(title_text="Day of campaign", gridcolor=C["grid"])
fig.update_yaxes(title_text="Cumulative CSAT %", gridcolor=C["grid"], showgrid=True)
st.plotly_chart(fig, theme=None)
if last_year_key not in order:
    st.caption(f"No {last_year_key} to compare with.")
note("pacing")

# ------------------------------------------------------------------ V3 Service dimensions + V5 heat map
left, right = st.columns(2, gap="large")
with left:
    st.subheader("Where callers are unhappy", help="Rating mix for each survey question: negative ratings (1–2) left of centre, positive (4–5) right, Neutral split across the centre.")
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
    st.subheader("Weekly problem map", help="% of callers rating each service area 1–2, week by week (Monday start). Darker red = more negative.")
    cur["week_start"] = cur["start_date"].dt.to_period("W-SUN").dt.start_time
    wk = cur.groupby("week_start")[list(DIMENSIONS)].apply(lambda d: (d <= 2).mean() * 100)
    wn = cur.groupby("week_start").size()
    wk.columns = ["Overall", "Wait time", "Agent service", "Knowledge", "Answer"]
    z = wk.T
    fig = go.Figure(go.Heatmap(
        z=z.values, x=[f"{w:%b %d}<br>n={wn[w]:,}" for w in z.columns], y=z.index, xgap=2, ygap=2,
        colorscale=[[0, "#fcf4f3"], [0.5, "#ec9a9a"], [1, "#a32626"]], zmin=0, zmax=max(25, float(np.nanmax(z.values))),
        text=np.vectorize(lambda v: f"{v:.0f}%")(z.values), texttemplate="%{text}", textfont=dict(size=11),
        showscale=False, hovertemplate="%{y}<br>Week of %{x}<br>Negative %{z:.1f}%<extra></extra>"))
    fig.update_layout(**BASE_LAYOUT, height=400)
    fig.update_yaxes(autorange="reversed")
    fig.update_xaxes(tickangle=0, tickfont=dict(size=10), side="bottom")
    st.plotly_chart(fig, theme=None)
    st.caption("% of callers rating each area 1–2, by week (Monday start). Darker = more negative; small weeks swing more.")
    note("heatmap")

# ------------------------------------------------------------------ V4 Language queues with confidence intervals
st.subheader("Language queue performance", help="Each survey language stands in for the queue that served the caller. " + TIPS["ci"])
LANG_ORDER = ["English", "Spanish", "Chinese", "Others"]
qrows = []
for lg in LANG_ORDER:
    d = cur[cur["language_queue"] == lg]
    if d.empty:
        continue
    n = len(d)
    k_csat, k_ans = int((d["overall_satisfaction"] >= 4).sum()), int((d["answer_satisfaction"] >= 4).sum())
    c_lo, c_hi = wilson(k_csat, n)
    a_lo, a_hi = wilson(k_ans, n)
    qrows.append(dict(queue=lg, n=n, csat=k_csat / n * 100, csat_lo=c_lo, csat_hi=c_hi, answer=k_ans / n * 100,
                      ans_lo=a_lo, ans_hi=a_hi, wait=top2(d["wait_time"]), agent=top2(d["agent_customer_service"]),
                      nps=nps_score(d["nps"]), dissatisfied=int((d["overall_satisfaction"] <= 2).sum())))
q = pd.DataFrame(qrows)
q["label"] = q["queue"] + " (n=" + q["n"].map("{:,}".format) + ")"
fig = make_subplots(rows=1, cols=2, shared_yaxes=True, horizontal_spacing=0.06,
                    subplot_titles=("CSAT (Overall 4–5)", "Answer Satisfaction (4–5)"))
for col_i, (val, lo, hi) in enumerate([("csat", "csat_lo", "csat_hi"), ("answer", "ans_lo", "ans_hi")], start=1):
    for r in q.itertuples():
        v, l, h = getattr(r, val), getattr(r, lo), getattr(r, hi)
        fig.add_trace(go.Scatter(
            x=[v], y=[r.label], mode="markers", marker=dict(size=12, color=LANG_COLORS[r.queue], line=dict(color="white", width=1.5)),
            error_x=dict(type="data", symmetric=False, array=[h - v], arrayminus=[v - l], color=LANG_COLORS[r.queue], thickness=2, width=6),
            showlegend=False, hovertemplate=f"{r.queue}: {v:.1f}%<br>95% CI {l:.1f}–{h:.1f}%<br>n = {r.n:,}<extra></extra>"),
            row=1, col=col_i)
        fig.add_annotation(x=h, y=r.label, text=f"{v:.1f}%", showarrow=False, xanchor="left", xshift=8,
                           font=dict(size=11, color=C["ink2"]), row=1, col=col_i)
fig.add_vline(x=CSAT_TARGET, line=dict(color=C["ink2"], width=1, dash="dash"), row=1, col=1)
fig.update_layout(**BASE_LAYOUT, height=320)
fig.update_layout(margin=dict(l=10, r=10, t=40, b=10))
fig.update_xaxes(range=[0, 108], ticksuffix="%", gridcolor=C["grid"], showgrid=True)
fig.update_yaxes(autorange="reversed")
st.plotly_chart(fig, theme=None)
st.caption("Dot = % positive; whisker = 95% confidence interval (Wilson). Wide whiskers mean few responses, so "
           "overlapping whiskers are not a real difference. Dashed line = CSAT target. No agent or team IDs are "
           "published, so the survey language stands in for the queue (Others = Russian, Korean, Arabic, Polish, French and other languages).")
t = q.set_index("queue")[["n", "csat", "answer", "wait", "agent", "nps", "dissatisfied"]]
t["share"] = t["n"] / t["n"].sum() * 100
t = t[["n", "share", "csat", "wait", "agent", "answer", "nps", "dissatisfied"]].rename(columns={
    "n": "Responses", "share": "Share of volume %", "csat": "CSAT %", "wait": "Wait OK %", "agent": "Agent Service OK %",
    "answer": "Answer %", "nps": "NPS", "dissatisfied": "Dissatisfied"})
t.index.name = "Language queue"
st.dataframe(t.style.format({"Responses": "{:,.0f}", "Share of volume %": "{:.1f}", "CSAT %": "{:.1f}", "Wait OK %": "{:.1f}",
                             "Agent Service OK %": "{:.1f}", "Answer %": "{:.1f}", "NPS": "{:+.1f}", "Dissatisfied": "{:,.0f}"}),
             width="stretch", column_config=col_help({
                 "Responses": TIPS["responses"], "Share of volume %": "This queue's share of all responses in the campaign.",
                 "CSAT %": TIPS["csat"], "Wait OK %": TIPS["wait"], "Agent Service OK %": TIPS["agent"],
                 "Answer %": TIPS["answer"], "NPS": TIPS["nps"], "Dissatisfied": TIPS["dissatisfied"]}))
note("queues")

# ------------------------------------------------------------------ V6 Exceptions report
st.subheader("Daily exceptions report", help="Days with at least 15 responses, flagged by business rules (Critical / Warning / OK) and checked against statistical control limits.")


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
rep["Control check"] = np.where(rep["out_low"], "Below limit", np.where(rep["out_high"], "Above limit", "Within limits"))
counts = rep["Status"].value_counts()
st.caption(f"Days with ≥{MIN_DAILY_N} responses. Business rules: Critical = CSAT < 70% or Answer < 55%; Warning = CSAT < target, "
           f"Answer < 60% or Wait OK < 75%. Control check = whether the day was also statistically unusual. This campaign: "
           f"{counts.get('✖ Critical', 0)} critical, {counts.get('▲ Warning', 0)} warning, {counts.get('✔ OK', 0)} OK; "
           f"{int((~daily['reliable']).sum())} days had too few responses to rate.")
rep = rep.rename(columns={"start_date": "Date", "responses": "Responses", "csat": "CSAT %", "lcl": "Lower limit %",
                          "answer_ok": "Answer %", "wait_ok": "Wait OK %", "nps": "NPS", "dissatisfied": "Dissatisfied"})
rep["Date"] = rep["Date"].dt.strftime("%a %b %d")
rep = rep[["Date", "Responses", "CSAT %", "Lower limit %", "Control check", "Answer %", "Wait OK %", "NPS",
           "Dissatisfied", "Status", "Reason"]]
STATUS_STYLE = {"✖ Critical": "background-color:#fdecec;color:#b42318;font-weight:600",
                "▲ Warning": "background-color:#fff4dc;color:#8a5a00;font-weight:600",
                "✔ OK": "background-color:#e7f6e7;color:#0b7a0b;font-weight:600",
                "Below limit": "color:#b42318;font-weight:600", "Above limit": "color:#0b7a0b;font-weight:600",
                "Within limits": "color:#52514e"}
st.dataframe(rep.style.format({"CSAT %": "{:.1f}", "Lower limit %": "{:.1f}", "Answer %": "{:.1f}", "Wait OK %": "{:.1f}",
                               "NPS": "{:+.1f}", "Responses": "{:,.0f}", "Dissatisfied": "{:,.0f}"})
             .map(lambda v: STATUS_STYLE.get(v, ""), subset=["Status", "Control check"])
             .bar(subset=["Responses"], color="#cde2fb", vmin=0),
             hide_index=True, width="stretch", height=36 * (len(rep) + 1) + 4, column_config=col_help({
                 "Responses": TIPS["responses"], "CSAT %": TIPS["csat"],
                 "Lower limit %": "The lowest CSAT this day could show from normal variation alone, given its number of responses (3-sigma).",
                 "Control check": "Within limits = normal variation. Below or above limit = statistically unusual day.",
                 "Answer %": TIPS["answer"], "Wait OK %": TIPS["wait"], "NPS": TIPS["nps"], "Dissatisfied": TIPS["dissatisfied"],
                 "Status": "Business rules. Critical: CSAT < 70% or Answer < 55%. Warning: CSAT < 80%, Answer < 60% or Wait OK < 75%.",
                 "Reason": "Which business rule(s) the day broke."}))
note("exceptions")

# ------------------------------------------------------------------ V7 Follow-up log
st.subheader("Customer follow-up log", help="Individual low-score responses to review and follow up, newest first. " + TIPS["low_score"])
flag = cur[(cur["overall_satisfaction"] <= 2) | (cur["nps"] <= 6)].copy()
flag["Priority"] = np.where((flag["overall_satisfaction"] == 1) | (flag["nps"] <= 3), "High", "Medium")


def weakest(r):
    vals = r[DRIVERS]
    if vals.nunique() == 1:
        return "All equal"
    return " / ".join(DIMENSIONS[c] for c in DRIVERS if vals[c] == vals.min())


flag["Weakest area"] = flag.apply(weakest, axis=1)
fc1, fc2, fc3 = st.columns([1.4, 1.2, 1])
if sel_day is not None:
    fc1.markdown(f"<div style='padding-top:1.9rem'>Day: <b>{sel_day:%a %b %d, %Y}</b> (selected on the chart)</div>",
                 unsafe_allow_html=True)
    day_filter = sel_day
else:
    days = sorted(flag["start_date"].dt.date.unique(), reverse=True)
    pick = fc1.selectbox("Show", ["Latest 15 responses"] + [f"All on {d:%a %b %d, %Y}" for d in days], index=0)
    day_filter = pd.to_datetime(pick.replace("All on ", ""), format="%a %b %d, %Y") if pick.startswith("All on") else None
queues_pick = fc2.multiselect("Queue", LANG_ORDER, default=[], placeholder="All queues", help="Show only responses from these language queues.")
prio_pick = fc3.multiselect("Priority", ["High", "Medium"], default=[], placeholder="All", help=TIPS["priority"])
shown = flag
if day_filter is not None:
    shown = shown[shown["start_date"] == day_filter]
if queues_pick:
    shown = shown[shown["language_queue"].isin(queues_pick)]
if prio_pick:
    shown = shown[shown["Priority"].isin(prio_pick)]
shown = shown.sort_values("start_datetime", ascending=False)
if day_filter is None:
    shown = shown.head(FOLLOW_UP_ROWS)
st.caption(f"Low-score responses: Overall 1–2 or NPS 0–6. {len(flag):,} in this campaign "
           f"({(flag['Priority'] == 'High').sum():,} High priority: Overall 1 or NPS 0–3). Showing {len(shown):,}. "
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
             hide_index=True, width="stretch", height=min(36 * (len(log) + 1) + 4, 760), column_config=col_help({
                 "Response ID": "Row number in the source CSV. The public data holds no personal details.",
                 "Responded": "When the caller started the survey (sent after the call).",
                 "Queue": "Survey language, standing in for the queue that served the caller.",
                 "Overall": "Overall Satisfaction rating, 1 (Strongly Disagree) to 5 (Strongly Agree).",
                 "Wait": "Wait Time rating, 1–5.", "Agent": "Agent Customer Service rating, 1–5.",
                 "Knowledge": "Agent Job Knowledge rating, 1–5.", "Answer": "Answer Satisfaction rating, 1–5.",
                 "NPS": "Recommend score, 0–10. 0–6 = detractor, 7–8 = passive, 9–10 = promoter.",
                 "Weakest area": TIPS["weakest"], "Priority": TIPS["priority"]}))
full = flag.sort_values("start_datetime", ascending=False)
export = pd.DataFrame({
    "response_id": full["row_id"].map(lambda i: f"R-{i:05d}"), "responded_at": full["start_datetime"],
    "queue": full["language_queue"], "overall": full["overall_satisfaction"], "wait_time": full["wait_time"],
    "agent_service": full["agent_customer_service"], "job_knowledge": full["agent_job_knowledge"],
    "answer": full["answer_satisfaction"], "nps": full["nps"], "weakest_area": full["Weakest area"], "priority": full["Priority"]})
st.download_button("Download all low-score responses (CSV)", export.to_csv(index=False).encode("utf-8"),
                   file_name=f"follow_up_{campaign.replace(' ', '_')}.csv", mime="text/csv", icon=":material/download:",
                   help="Downloads every low-score response in this campaign, not only the rows shown.")
note("followup")

# ------------------------------------------------------------------ Conclusion and recommendations
if is_default:
    page_conclusion(PAGE_CONCLUSIONS["LOWER"], "Owner")
