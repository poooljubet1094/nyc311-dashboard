"""Middle-level management (Tactical): departmental planning and performance monitoring.

Brief: Which department performs best? What are the monthly trends? What factors influence performance?
"""
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

from common import (BASE_LAYOUT, C, DIMENSIONS, DRIVERS, LIKERT_COLORS, LIKERT_LABELS, TIPS, analysis, bottom2, kpi_card,
                    load_data, nps_score, page_conclusion, top2, trend_fit)
from models import importance_figure, nps_tree, tree_figure, volume_heatmap_figure
from narrative import MIDDLE, PAGE_CONCLUSIONS

MIN_PERIOD_N = 200    # hide noisy periods in the trend
MIN_SEGMENT_N = 100   # language groups shown as departments

df_all = load_data()
years = sorted(df_all["year"].unique())

st.markdown("<div class='level-tag'>Middle-level management · Tactical</div>", unsafe_allow_html=True)
st.title("Tactical performance")
st.caption("For call-center operations and quality-assurance managers. Answers the brief's tactical questions: "
           "which department performs best, what the trends are, and what factors influence performance.")

yr = st.select_slider("Years", options=years, value=(years[0], years[-1]), help="Limit every chart on this page to the years you pick.")
df = df_all[df_all["year"].between(*yr)]
full_range = yr == (years[0], years[-1])
if not full_range:
    st.info("The written analysis describes the full 2020–2025 period. Charts update for the years you pick; "
            "the analysis notes are hidden for other ranges.")


def note(key, show=True):
    if full_range and show:
        analysis(MIDDLE[key])


# ------------------------------------------------------------------ KPI strip
cols = st.columns(4)
with cols[0]:
    kpi_card("Surveys analysed", f"{len(df):,}", "", f"{df['start_datetime'].min():%b %Y} – {df['start_datetime'].max():%b %Y}")
with cols[1]:
    kpi_card("CSAT (% favorable)", f"{top2(df['overall_satisfaction']):.1f}%", "", "Overall Satisfaction 4–5")
with cols[2]:
    kpi_card("Net Promoter Score", f"{nps_score(df['nps']):+.0f}", "", "Promoters − detractors")
with cols[3]:
    kpi_card("% Unfavorable", f"{bottom2(df['overall_satisfaction']):.1f}%", "", "Overall Satisfaction 1–2")
note("kpi")

# ------------------------------------------------------------------ 1. Trend analysis (campaign / quarter / month)
st.subheader("1. What are the trends? CSAT and NPS over time", help="CSAT and NPS per period with a dotted linear trend line. " + TIPS["p_value"])
grain = st.radio("Period", ["Quarter", "Campaign", "Month"], horizontal=True,
                 help="Campaigns are the survey's natural reporting period; months with fewer than 200 responses are hidden.")
if grain == "Quarter":
    key = df["quarter"]
elif grain == "Month":
    key = df["start_datetime"].dt.to_period("M").astype(str)
else:
    key = df["campaign_key"]
trend = (df.assign(_k=key).groupby("_k")
         .agg(n=("nps", "size"), csat=("overall_satisfaction", top2), nps=("nps", nps_score), first=("start_datetime", "median")))
trend = trend[trend["n"] >= MIN_PERIOD_N].sort_values("first")
fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1,
                    subplot_titles=("CSAT (% favorable)", "Net Promoter Score"))
fig.add_trace(go.Scatter(x=trend.index, y=trend["csat"], mode="lines+markers", name="CSAT",
                         line=dict(color=C["blue"], width=2), marker=dict(size=7), customdata=trend[["n"]],
                         hovertemplate="%{x}<br>CSAT %{y:.1f}%<br>%{customdata[0]:,} responses<extra></extra>"), row=1, col=1)
fig.add_trace(go.Scatter(x=trend.index, y=trend["nps"], mode="lines+markers", name="NPS",
                         line=dict(color=C["orange"], width=2), marker=dict(size=7),
                         hovertemplate="%{x}<br>NPS %{y:+.1f}<extra></extra>"), row=2, col=1)
if len(trend) >= 4:
    xq = np.arange(len(trend))
    unit_name = {"Quarter": "quarter", "Campaign": "campaign", "Month": "survey month"}[grain]
    for row, col, color, unit in [(1, "csat", C["blue"], " pt"), (2, "nps", C["orange"], " pts")]:
        fit = trend_fit(xq, trend[col])
        fig.add_trace(go.Scatter(x=trend.index, y=fit["intercept"] + fit["slope"] * xq, mode="lines",
                                 line=dict(color=color, width=1.2, dash="dot"), hoverinfo="skip"), row=row, col=1)
        verdict = "statistically significant" if fit["p"] < 0.05 else "not significant: flat"
        ax = "" if row == 1 else "2"
        fig.add_annotation(xref=f"x{ax} domain", yref=f"y{ax} domain", x=0.995, y=0.03, xanchor="right", yanchor="bottom",
                           text=f"Linear trend {fit['slope']:+.2f}{unit} per {unit_name} · p = {fit['p']:.2f} ({verdict})",
                           showarrow=False, font=dict(size=11, color=color), bgcolor="rgba(255,255,255,.8)")
if len(trend):
    for row, col, fmt in [(1, "csat", "{:.1f}%"), (2, "nps", "{:+.0f}")]:
        for which in ("idxmin", "idxmax"):
            q = getattr(trend[col], which)()
            fig.add_annotation(x=q, y=trend.loc[q, col], text=fmt.format(trend.loc[q, col]), showarrow=False,
                               yshift=-14 if which == "idxmin" else 14, font=dict(size=11, color=C["ink2"]), row=row, col=1)
fig.update_layout(**BASE_LAYOUT, height=480, showlegend=False)
fig.update_layout(margin=dict(l=10, r=10, t=40, b=10))
fig.update_yaxes(gridcolor=C["grid"], showgrid=True)
fig.update_yaxes(ticksuffix="%", row=1, col=1)
fig.update_xaxes(tickangle=-45, type="category")
st.plotly_chart(fig, theme=None)
st.caption(f"Periods with fewer than {MIN_PERIOD_N} responses are hidden. The lowest and highest period on each chart is labelled. "
           "Dotted lines are linear trends; p < 0.05 means the trend is unlikely to be chance.")
note("trend", grain == "Quarter")
if full_range and grain != "Quarter":
    st.caption("The written analysis describes the quarterly view; switch Period to Quarter to read it.")

# ------------------------------------------------------------------ 2. Departmental performance dashboard
st.subheader("2. Which department performs best? Language groups across six KPIs", help="Language groups with at least 100 responses stand in for departments. Cells show each group's value; color shows the gap to the all-caller average (blue above, red below).")
KPI_COLS = {"CSAT": ("overall_satisfaction", top2), "Wait time": ("wait_time", top2),
            "Agent service": ("agent_customer_service", top2), "Job knowledge": ("agent_job_knowledge", top2),
            "Answer": ("answer_satisfaction", top2), "NPS": ("nps", nps_score)}
grp = {g: d for g, d in df.groupby("language_detail") if len(d) >= MIN_SEGMENT_N}
dept = pd.DataFrame({g: {k: f(d[c]) for k, (c, f) in KPI_COLS.items()} for g, d in grp.items()}).T
dept["n"] = [len(grp[g]) for g in dept.index]
dept = dept.sort_values("n", ascending=False)
overall = pd.Series({k: f(df[c]) for k, (c, f) in KPI_COLS.items()})
# One grid: the all-caller average as the first row (difference 0 = neutral), then each group
vals = pd.concat([overall.to_frame("All callers (average)").T, dept[list(KPI_COLS)]])
diff = vals - overall
zmax = max(5, float(np.nanmax(np.abs(diff.values))))
row_labels = ["All callers (average)"] + [f"{g} (n={int(dept.loc[g, 'n']):,})" for g in dept.index]
text = [[(f"{vals.iloc[i][k]:+.1f}" if k == "NPS" else f"{vals.iloc[i][k]:.1f}%") for k in KPI_COLS] for i in range(len(vals))]
fig = go.Figure(go.Heatmap(
    z=diff.values, x=list(KPI_COLS), y=row_labels,
    text=text, texttemplate="%{text}", textfont=dict(size=12), xgap=3, ygap=3, zmid=0, zmin=-zmax, zmax=zmax,
    colorscale=[[0, "#c23a3a"], [0.5, "#f1f0ec"], [1, "#2a78d6"]],
    colorbar=dict(title="vs average<br>(pts)", thickness=10),
    customdata=diff.values, hovertemplate="%{y}<br>%{x}: %{text}<br>%{customdata:+.1f} pts vs all callers<extra></extra>"))
fig.update_layout(**BASE_LAYOUT, height=60 * len(vals) + 70)
fig.update_layout(margin=dict(l=10, r=10, t=20, b=10))
fig.update_yaxes(autorange="reversed", type="category")
fig.update_xaxes(side="top")
st.plotly_chart(fig, theme=None)
st.caption(f"Language groups with at least {MIN_SEGMENT_N} responses stand in for departments (the data has no team field). "
           "Cells show each group's value; blue = above the all-caller average, red = below.")
note("departments")

left, right = st.columns(2, gap="large")
# ------------------------------------------------------------------ 3. Stacked mix by campaign
with left:
    st.subheader("3. Which campaign performs best? Satisfaction mix", help="Share of each Overall Satisfaction rating within each campaign label (Pilot, Campaigns 1–5), all selected years combined.")
    camp_order = [c for c in ["Pilot", "Campaign 1", "Campaign 2", "Campaign 3", "Campaign 4", "Campaign 5"] if c in df["campaign"].unique()]
    mix = (pd.crosstab(df["campaign"], df["overall_satisfaction"], normalize="index") * 100).reindex(camp_order)
    fig = go.Figure()
    for s in [1, 2, 3, 4, 5]:
        vals = mix[s] if s in mix else pd.Series(0, index=mix.index)
        fig.add_trace(go.Bar(
            y=mix.index, x=vals, orientation="h", name=LIKERT_LABELS[s],
            marker=dict(color=LIKERT_COLORS[s], line=dict(color="white", width=1)),
            text=[f"{v:.0f}%" if v >= 8 else "" for v in vals], textposition="inside", insidetextanchor="middle", textangle=0,
            textfont=dict(color="white" if s in (1, 5) else C["ink"]),
            hovertemplate="%{y}<br>" + LIKERT_LABELS[s] + ": %{x:.1f}%<extra></extra>"))
    fig.update_layout(**BASE_LAYOUT, barmode="stack", height=420, bargap=0.3,
                      legend=dict(orientation="h", y=-0.28, x=0.5, xanchor="center", traceorder="normal", font=dict(size=11)))
    fig.update_yaxes(autorange="reversed")
    fig.update_xaxes(range=[0, 100], ticksuffix="%", title_text="% of responses")
    st.plotly_chart(fig, theme=None)
    note("campaigns")

# ------------------------------------------------------------------ 4. Language bubbles (segmentation scatter)
with right:
    st.subheader("4. Segments: answer vs overall satisfaction", help="Each bubble is a language group: x = answer satisfaction, y = overall satisfaction, size = number of responses, color = NPS.")
    seg = df.groupby("language_detail").agg(n=("nps", "size"), overall=("overall_satisfaction", top2),
                                            answer=("answer_satisfaction", top2), nps=("nps", nps_score))
    seg = seg[seg["n"] >= MIN_SEGMENT_N].sort_values("n", ascending=False)
    fig = go.Figure()
    if len(seg) > 2:
        m, b = np.polyfit(seg["answer"], seg["overall"], 1)
        xs = np.linspace(seg["answer"].min(), seg["answer"].max(), 20)
        fig.add_trace(go.Scatter(x=xs, y=m * xs + b, mode="lines", line=dict(color=C["muted"], dash="dash", width=1),
                                 hoverinfo="skip", showlegend=False))
    fig.add_trace(go.Scatter(
        x=seg["answer"], y=seg["overall"], mode="markers+text", text=[f"{i} ({int(r.n):,})" for i, r in seg.iterrows()],
        textposition=[{"Chinese (Trad.)": "top left", "Chinese (Simpl.)": "bottom left"}.get(i, "top center") for i in seg.index],
        textfont=dict(size=12),
        marker=dict(size=np.sqrt(seg["n"]) / 1.6 + 10, color=seg["nps"], colorscale=[[0, "#cde2fb"], [1, "#104281"]],
                    line=dict(color="white", width=1.5), showscale=True, colorbar=dict(title="NPS", thickness=10)),
        customdata=seg[["n", "nps"]],
        hovertemplate="%{text}<br>Answer %{x:.1f}% · Overall %{y:.1f}%<br>NPS %{customdata[1]:+.1f}<extra></extra>",
        showlegend=False))
    fig.update_layout(**BASE_LAYOUT, height=420)
    fig.update_xaxes(title_text="Answer satisfaction — % favorable", ticksuffix="%", gridcolor=C["grid"], showgrid=True)
    fig.update_yaxes(title_text="Overall satisfaction — % favorable", ticksuffix="%", gridcolor=C["grid"], showgrid=True)
    if len(seg):
        pad_x = (seg["answer"].max() - seg["answer"].min()) * 0.12 + 2
        pad_y = (seg["overall"].max() - seg["overall"].min()) * 0.25 + 1
        fig.update_xaxes(range=[seg["answer"].min() - pad_x, seg["answer"].max() + pad_x])
        fig.update_yaxes(range=[seg["overall"].min() - pad_y, seg["overall"].max() + pad_y * 1.6])
    st.plotly_chart(fig, theme=None)
    st.caption(f"Languages with at least {MIN_SEGMENT_N} responses. Bubble size = survey volume; darker = higher NPS; "
               "the y-axis is zoomed in, so gaps look larger than they are.")
    note("languages")

# ------------------------------------------------------------------ 5–7. What factors influence performance?
st.subheader("What factors influence performance?", help="Three views of which parts of the caller experience drive satisfaction and NPS.")
left, right = st.columns(2, gap="large")
with left:
    st.markdown("**5. Fix-first matrix: impact vs performance of each driver**", help="Each driver placed by performance (% favorable) and impact (correlation with Overall Satisfaction). Fix first = high impact, low performance; Protect = high impact, high performance.")
    drv = pd.DataFrame({DIMENSIONS[c]: {"perf": top2(df[c]), "impact": df[c].corr(df["overall_satisfaction"])}
                        for c in DRIVERS}).T
    x_mid, y_mid = drv["perf"].mean(), drv["impact"].mean()
    x_lo, x_hi = min(drv["perf"].min(), x_mid) - 6, max(drv["perf"].max(), x_mid) + 6
    y_lo, y_hi = min(drv["impact"].min(), y_mid) - 0.03, max(drv["impact"].max(), y_mid) + 0.03
    fig = go.Figure()
    for (qx, qy, label, color) in [(x_lo, y_hi, "FIX FIRST", "#b42318"), (x_hi, y_hi, "PROTECT", C["blue"]),
                                   (x_lo, y_lo, "MONITOR", C["muted"]), (x_hi, y_lo, "MAINTAIN", C["muted"])]:
        fig.add_annotation(x=qx, y=qy, text=f"<b>{label}</b>", showarrow=False, font=dict(size=11, color=color),
                           xanchor="left" if qx == x_lo else "right", yanchor="top" if qy == y_hi else "bottom")
    fig.add_vline(x=x_mid, line=dict(color=C["muted"], width=1, dash="dash"))
    fig.add_hline(y=y_mid, line=dict(color=C["muted"], width=1, dash="dash"))
    fix = (drv["perf"] < x_mid) & (drv["impact"] >= y_mid)
    fig.add_trace(go.Scatter(
        x=drv["perf"], y=drv["impact"], mode="markers+text",
        text=[f"{i} ({r.perf:.1f}%)" for i, r in drv.iterrows()],
        textposition=[{"Agent Customer Service": "bottom left", "Wait Time": "bottom center",
                       "Answer Satisfaction": "top right"}.get(i, "top center") for i in drv.index],
        marker=dict(size=16, color=[C["orange"] if f else C["blue"] for f in fix], line=dict(color="white", width=2)),
        hovertemplate="%{text}<br>Impact r = %{y:.2f}<extra></extra>", showlegend=False))
    fig.update_layout(**BASE_LAYOUT, height=380)
    fig.update_layout(margin=dict(l=10, r=10, t=30, b=10))
    fig.update_xaxes(range=[x_lo, x_hi], title_text="Performance: % favorable", ticksuffix="%", gridcolor=C["grid"], showgrid=True)
    fig.update_yaxes(range=[y_lo, y_hi], title_text="Impact (r with Overall)", gridcolor=C["grid"], showgrid=True)
    st.plotly_chart(fig, theme=None)
    st.caption("Dashed lines are the averages of the four drivers. Correlation shows association, not cause.")
    note("matrix")
model, feat_names = nps_tree(df_all)
with right:
    st.markdown("**6. Feature importance: what the NPS model relies on**", help="How much the decision tree relies on each factor when sorting callers into Detractor, Passive and Promoter. Adds up to 100%.")
    st.plotly_chart(importance_figure(model, feat_names), theme=None)
    st.caption("Share of the decision tree's splitting power by factor (all 2020–2025 data).")
st.markdown("**7. Decision tree: the rating thresholds that route callers into each NPS group**", help="A three-level decision tree. Each box shows its split rule, the share of all callers who reach it, and its most common NPS group. Left branch = rule is true.")
st.plotly_chart(tree_figure(model, feat_names), theme=None)
st.caption("Each box: the split rule, the share of all callers who reach it, and its most common NPS group. "
           "Left branch = rule true. Hover a box for the full Detractor / Passive / Promoter mix. Fitted on all years.")
analysis(MIDDLE["tree"])

# ------------------------------------------------------------------ 8. Survey volume by month (planning)
st.subheader("8. When does feedback arrive? Survey responses by month", help="Survey responses per month and year, with each month's share of that year's responses.")
st.plotly_chart(volume_heatmap_figure(df), theme=None)
st.caption("Each cell: responses that month and the share of the year. Use it to plan QA reviews around the campaign months.")
note("volume")

# ------------------------------------------------------------------ Conclusion and recommendations
if full_range:
    page_conclusion(PAGE_CONCLUSIONS["MIDDLE"], "Owner")
