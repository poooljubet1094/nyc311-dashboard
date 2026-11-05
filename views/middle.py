"""Middle-level management (Tactical): departmental planning and performance monitoring."""
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

from common import BASE_LAYOUT, C, DIMENSIONS, LIKERT_COLORS, LIKERT_LABELS, analysis, bottom2, kpi_card, load_data, nps_score, top2
from narrative import MIDDLE

MIN_QUARTER_N = 200   # hide noisy quarters in the trend
MIN_SEGMENT_N = 100   # language groups shown in the bubble chart

df_all = load_data()
years = sorted(df_all["year"].unique())

st.markdown("<div class='level-tag'>Middle-level management · Tactical</div>", unsafe_allow_html=True)
st.title("Tactical performance")
st.caption("For call-center operations and quality-assurance managers. Answers: is service quality improving and is any "
           "campaign underperforming; which service drivers are weakest; do language groups experience the service differently.")

yr = st.select_slider("Years", options=years, value=(years[0], years[-1]))
df = df_all[df_all["year"].between(*yr)]
full_range = yr == (years[0], years[-1])
if not full_range:
    st.info("The written analysis describes the full 2020–2025 period. Charts update for the years you pick; "
            "the analysis notes are hidden for other ranges.")


def note(key):
    if full_range:
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

# ------------------------------------------------------------------ Chart 1: trend
st.subheader("1. Trend: CSAT and NPS by quarter")
trend = df.groupby("quarter").agg(n=("nps", "size"), csat=("overall_satisfaction", top2), nps=("nps", nps_score))
trend = trend[trend["n"] >= MIN_QUARTER_N]
fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1,
                    subplot_titles=("CSAT (% favorable)", "Net Promoter Score"))
fig.add_trace(go.Scatter(x=trend.index, y=trend["csat"], mode="lines+markers", name="CSAT",
                         line=dict(color=C["blue"], width=2), marker=dict(size=7), customdata=trend[["n"]],
                         hovertemplate="%{x}<br>CSAT %{y:.1f}%<br>%{customdata[0]:,} responses<extra></extra>"), row=1, col=1)
fig.add_trace(go.Scatter(x=trend.index, y=trend["nps"], mode="lines+markers", name="NPS",
                         line=dict(color=C["orange"], width=2), marker=dict(size=7),
                         hovertemplate="%{x}<br>NPS %{y:+.1f}<extra></extra>"), row=2, col=1)
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
fig.update_xaxes(tickangle=-45)
st.plotly_chart(fig, theme=None)
st.caption(f"Quarters with fewer than {MIN_QUARTER_N} responses are hidden. The lowest and highest quarter on each chart is labelled.")
note("trend")

left, right = st.columns(2, gap="large")
# ------------------------------------------------------------------ Chart 2: driver bars
with left:
    st.subheader("2. Favorable rating by service driver")
    fav = pd.Series({lab: top2(df[col]) for col, lab in DIMENSIONS.items()}).sort_values()
    fig = go.Figure(go.Bar(
        y=fav.index, x=fav.values, orientation="h", text=[f"{v:.1f}%" for v in fav.values], textposition="outside",
        marker_color=[C["orange"] if v == fav.min() else C["blue"] for v in fav.values],
        hovertemplate="%{y}: %{x:.1f}% favorable<extra></extra>"))
    fig.add_vline(x=fav.mean(), line=dict(color=C["muted"], width=1.5, dash="dot"),
                  annotation_text=f"Average {fav.mean():.1f}%", annotation_position="top")
    fig.update_layout(**BASE_LAYOUT, height=380, bargap=0.4)
    fig.update_layout(margin=dict(l=10, r=10, t=40, b=10))
    fig.update_xaxes(range=[0, 105], title_text="% favorable (Agree + Strongly Agree)", gridcolor=C["grid"], showgrid=True)
    st.plotly_chart(fig, theme=None)
    note("drivers")

# ------------------------------------------------------------------ Chart 3: stacked mix by campaign
with right:
    st.subheader("3. Overall satisfaction mix by campaign")
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

# ------------------------------------------------------------------ Chart 4: language bubbles
st.subheader("4. Language segments: answer vs overall satisfaction")
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
fig.update_layout(**BASE_LAYOUT, height=460)
fig.update_xaxes(title_text="Answer satisfaction — % favorable", ticksuffix="%", gridcolor=C["grid"], showgrid=True)
fig.update_yaxes(title_text="Overall satisfaction — % favorable", ticksuffix="%", gridcolor=C["grid"], showgrid=True)
pad_x = (seg["answer"].max() - seg["answer"].min()) * 0.12 + 2
pad_y = (seg["overall"].max() - seg["overall"].min()) * 0.25 + 1
fig.update_xaxes(range=[seg["answer"].min() - pad_x, seg["answer"].max() + pad_x])
fig.update_yaxes(range=[seg["overall"].min() - pad_y, seg["overall"].max() + pad_y * 1.6])
st.plotly_chart(fig, theme=None)
st.caption(f"Languages with at least {MIN_SEGMENT_N} responses. Bubble size = survey volume; darker = higher NPS; "
           "the y-axis is zoomed in, so gaps look larger than they are.")
note("languages")

if full_range and st.session_state.get("show_analysis", True):
    st.subheader("Recommended actions")
    st.markdown("- Make answer quality and first-call resolution the priority for next quarter's plan.\n"
                "- Review Russian-language service, including interpreter quality and the scripts used.\n"
                "- Investigate the English-language “Strongly Disagree” group, using call categories if available.\n"
                "- Keep monitoring quarterly, and treat moves of about ±4 points in CSAT as normal noise.")
