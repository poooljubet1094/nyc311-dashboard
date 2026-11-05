"""Top-level management (Strategic): is the organization meeting its goals, and what drives NPS?"""
import calendar
import html

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from mlxtend.frequent_patterns import apriori, association_rules
from sklearn.tree import DecisionTreeClassifier

from common import BASE_LAYOUT, C, analysis, load_data, nps_score, top2
from narrative import TOP

df = load_data()

RULE_NAMES = {"overall_satisfaction": "Overall Satisfaction", "wait_time": "Wait Time Rating",
              "agent_customer_service": "Agent Customer Service", "agent_job_knowledge": "Agent Job Knowledge",
              "answer_satisfaction": "Answer Satisfaction"}
SEGMENTS = {"Detractor": "Detractor (Score 0-6)", "Passive": "Passive (Score 7-8)", "Promoter": "Promoter (Score 9-10)"}
SEG_COLORS = {"Promoter": "#2e7d32", "Passive": "#c77700", "Detractor": "#c62828"}


@st.cache_data(show_spinner="Mining NPS driver rules…")
def nps_rules(data: pd.DataFrame) -> pd.DataFrame:
    """Target-oriented Apriori: rating combinations → NPS segment (support ≥ 5%, confidence ≥ 30%, lift > 1)."""
    onehot = {}
    for col, name in RULE_NAMES.items():
        for v in range(1, 6):
            onehot[f"{name}: {v}/5"] = data[col].eq(v)
    for short, label in SEGMENTS.items():
        onehot[f"NPS Outcome: {label}"] = data["nps_group"].astype(str).eq(short)
    enc = pd.DataFrame(onehot)
    enc = enc.loc[:, enc.any()]
    items = apriori(enc, min_support=0.05, use_colnames=True)
    rules = association_rules(items, metric="confidence", min_threshold=0.30)
    targets = {f"NPS Outcome: {v}" for v in SEGMENTS.values()}
    rules = rules[rules["consequents"].apply(lambda c: len(c) == 1 and next(iter(c)) in targets)]
    rules = rules[rules["lift"] > 1.0].copy()
    rules["combination"] = rules["antecedents"].apply(lambda a: " AND ".join(sorted(a)))
    rules["segment"] = rules["consequents"].apply(lambda c: next(iter(c)).split(": ")[1].split(" ")[0])
    rules = rules.sort_values(["lift", "confidence", "support"], ascending=False)
    return rules[["segment", "combination", "confidence", "support", "lift"]].reset_index(drop=True)


@st.cache_resource(show_spinner="Fitting decision tree…")
def nps_tree(data: pd.DataFrame):
    features = {"overall_satisfaction": "Overall Satisfaction", "answer_satisfaction": "Answer Satisfaction",
                "agent_customer_service": "Agent Customer Service", "turnaround_minutes": "Turnaround (Minutes)",
                "agent_job_knowledge": "Agent Job Knowledge", "wait_time": "Wait Time Rating"}
    X, y = data[list(features)], data["nps_group"].astype(str)
    model = DecisionTreeClassifier(max_depth=3, random_state=42).fit(X, y)
    return model, list(features.values())


st.markdown("<div class='level-tag'>Top-level management · Strategic</div>", unsafe_allow_html=True)
st.title("Executive CSAT & NPS")
st.caption("For NYC311 leadership. Answers: is the organization meeting its goals, how has survey coverage grown, "
           "and which parts of the caller experience actually decide NPS.")

# ------------------------------------------------------------------ KPI banner
n = len(df)
p_pro, p_pas, p_det = (df["nps"] >= 9).mean() * 100, df["nps"].between(7, 8).mean() * 100, (df["nps"] <= 6).mean() * 100
k1, k2, k3 = st.columns([1, 1, 2.2])
k1.metric("Overall NPS", f"{p_pro - p_det:+.2f}")
k2.metric("Total respondents", f"{n:,}", help="After cleaning: 26 incomplete records removed from 28,816.")
with k3:
    segs = [("Promoters (9–10)", p_pro, SEG_COLORS["Promoter"]), ("Passives (7–8)", p_pas, SEG_COLORS["Passive"]),
            ("Detractors (0–6)", p_det, SEG_COLORS["Detractor"])]
    labels = "".join(f"<span style='color:{c};font-weight:600'>{lab}: {v:.2f}%</span>" for lab, v, c in segs)
    bar = "".join(f"<div title='{lab}: {v:.2f}%' style='width:{v}%;background:{c}'></div>" for lab, v, c in segs)
    st.markdown(f"<div style='padding-top:.4rem'><div style='display:flex;justify-content:space-between;flex-wrap:wrap;"
                f"gap:8px;font-size:.85rem;margin-bottom:6px'>{labels}</div><div style='display:flex;height:12px;"
                f"border-radius:6px;overflow:hidden'>{bar}</div></div>", unsafe_allow_html=True)

# ------------------------------------------------------------------ Visualization 1: volumes & growth
st.subheader("Campaign volumes & historic trends (2020–2025)")
left, right = st.columns([3, 2], gap="large")
with left:
    piv = df.groupby(["month", "year"]).size().unstack(fill_value=0).reindex(range(1, 13), fill_value=0)
    pct = piv / piv.sum() * 100
    text = [[f"{piv.iloc[i, j]:,}<br>({pct.iloc[i, j]:.1f}%)" for j in range(piv.shape[1])] for i in range(12)]
    fig = go.Figure(go.Heatmap(
        z=piv.values, x=[str(y) for y in piv.columns], y=[calendar.month_name[m] for m in piv.index],
        text=text, texttemplate="%{text}", textfont=dict(size=11), xgap=2, ygap=2,
        colorscale=[[0, "#f7fbf2"], [0.5, "#86c48a"], [1, "#1f6b35"]], colorbar=dict(title="Responses", thickness=10),
        hovertemplate="%{y} %{x}<br>%{z:,} responses<extra></extra>"))
    fig.update_layout(**BASE_LAYOUT, height=520, title=dict(text="Responses by month (count and % of the year)", x=0, font=dict(size=14)))
    fig.update_layout(margin=dict(l=10, r=10, t=40, b=10))
    fig.update_yaxes(autorange="reversed")
    st.plotly_chart(fig, theme=None)
with right:
    yearly = df["year"].value_counts().sort_index()
    fig = go.Figure(go.Scatter(x=yearly.index.astype(str), y=yearly.values, mode="lines+markers+text",
                               text=[f"{v:,}" for v in yearly.values], textposition="top center",
                               line=dict(color=C["blue"], width=2.5), marker=dict(size=9),
                               hovertemplate="%{x}: %{y:,} responses<extra></extra>"))
    fig.update_layout(**BASE_LAYOUT, height=520, title=dict(text="Survey responses per year", x=0, font=dict(size=14)))
    fig.update_layout(margin=dict(l=10, r=10, t=40, b=10))
    fig.update_yaxes(range=[0, yearly.max() * 1.18], gridcolor=C["grid"], showgrid=True, tickformat=",")
    st.plotly_chart(fig, theme=None)
analysis(TOP["volume"])

# ------------------------------------------------------------------ Visualization 2 & 3: importance & tree
st.subheader("Operational tipping points & key decision drivers")
model, feat_names = nps_tree(df)
imp = pd.Series(model.feature_importances_, index=feat_names).sort_values()
left, right = st.container(), st.container()
with left:
    fig = go.Figure(go.Bar(y=imp.index, x=imp.values * 100, orientation="h", text=[f"{v * 100:.1f}%" for v in imp.values],
                           textposition="outside", cliponaxis=False,
                           marker_color=[C["blue"] if v > 0.05 else "#9ec5f4" for v in imp.values],
                           hovertemplate="%{y}: %{x:.1f}%<extra></extra>"))
    fig.update_layout(**BASE_LAYOUT, height=300, bargap=0.35,
                      title=dict(text="Feature importance (share of the model)", x=0, font=dict(size=14)))
    fig.update_layout(margin=dict(l=10, r=40, t=40, b=10))
    fig.update_xaxes(range=[0, 100], ticksuffix="%", gridcolor=C["grid"], showgrid=True)
    st.plotly_chart(fig, theme=None)
with right:
    t = model.tree_
    classes = list(model.classes_)
    order_cls = ["Detractor", "Passive", "Promoter"]
    fill = {"Detractor": "#f6c9c4", "Passive": "#ffe1a8", "Promoter": "#cde2fb"}
    edge = {"Detractor": "#c62828", "Passive": "#c77700", "Promoter": "#2a78d6"}
    pos, depth = {}, {}
    leaves = []

    def walk(node, d):
        depth[node] = d
        if t.children_left[node] == -1:
            leaves.append(node)
            pos[node] = len(leaves) - 1
            return
        walk(t.children_left[node], d + 1)
        walk(t.children_right[node], d + 1)
        pos[node] = (pos[t.children_left[node]] + pos[t.children_right[node]]) / 2

    walk(0, 0)
    fig = go.Figure()
    for node in pos:
        for child, lab in [(t.children_left[node], "Yes"), (t.children_right[node], "No")]:
            if child != -1:
                fig.add_trace(go.Scatter(x=[pos[node], pos[child]], y=[-depth[node], -depth[child]], mode="lines",
                                         line=dict(color="#b8b7b0", width=1), hoverinfo="skip", showlegend=False))
                if node == 0:
                    fig.add_annotation(x=(pos[node] + pos[child]) / 2, y=-0.5, text=f"{lab} (≤)" if lab == "Yes" else "No (>)",
                                       showarrow=False, font=dict(size=10, color=C["muted"]), yshift=8)
    hover_x, hover_y, hover_t = [], [], []
    total = t.weighted_n_node_samples[0]
    for node in pos:
        vals = t.value[node][0] / t.value[node][0].sum()
        mix = dict(zip(classes, vals))
        cls = max(mix, key=mix.get)
        share = t.weighted_n_node_samples[node] / total * 100
        is_leaf = t.children_left[node] == -1
        split = "" if is_leaf else f"<b>{feat_names[t.feature[node]]} ≤ {t.threshold[node]:.1f}</b><br>"
        body = f"{split}{share:.1f}% of callers<br>{cls} {mix[cls] * 100:.0f}%"
        fig.add_annotation(x=pos[node], y=-depth[node], text=body, showarrow=False, align="center",
                           font=dict(size=10 if is_leaf else 11, color=C["ink"]), bgcolor=fill[cls],
                           bordercolor=edge[cls], borderwidth=1, borderpad=4)
        hover_x.append(pos[node]); hover_y.append(-depth[node])
        hover_t.append(f"{share:.1f}% of callers<br>" + "<br>".join(f"{c}: {mix.get(c, 0) * 100:.1f}%" for c in order_cls))
    fig.add_trace(go.Scatter(x=hover_x, y=hover_y, mode="markers", marker=dict(size=40, opacity=0),
                             hovertext=hover_t, hoverinfo="text", showlegend=False))
    fig.update_layout(**BASE_LAYOUT, height=480, title=dict(text="Decision tree: which ratings route callers into each NPS group", x=0, font=dict(size=14)))
    fig.update_layout(margin=dict(l=10, r=10, t=40, b=10))
    fig.update_xaxes(visible=False, range=[-0.6, len(leaves) - 0.4])
    fig.update_yaxes(visible=False, range=[-3.45, 0.45])
    st.plotly_chart(fig, theme=None)
    st.caption("Each box: the split rule, the share of all callers who reach it, and its most common NPS group. "
               "Left branch = rule true. Hover a box for the full Detractor / Passive / Promoter mix.")
analysis(TOP["tree"])

# ------------------------------------------------------------------ Visualization 1 (Apriori): driver cards
st.subheader("Apriori driver analysis: rating combinations & their NPS impact")
rules = nps_rules(df)


def cards(segment, title, subtitle, k=3):
    color = SEG_COLORS[segment]
    st.markdown(f"<div style='color:{color};font-weight:700;letter-spacing:.03em;margin:4px 0 8px'>{title}</div>"
                f"<div style='font-size:.8rem;opacity:.7;margin:-6px 0 8px'>{subtitle}</div>", unsafe_allow_html=True)
    top = rules[rules["segment"] == segment].head(k)
    if top.empty:
        st.caption("No rule met the thresholds.")
    for _, r in top.iterrows():
        st.markdown(
            f"<div class='rule-card' style='border-left-color:{color}'>"
            f"<div class='rule-title'>{html.escape(r['combination'])}</div>"
            f"<div class='rule-meta'><span><b>Reliability</b> {r['confidence'] * 100:.2f}%</span>"
            f"<span><b>Customer share</b> {r['support'] * 100:.2f}%</span>"
            f"<span><b>Impact</b> <span style='color:{color};font-weight:700'>{r['lift']:.2f}× higher</span></span></div></div>",
            unsafe_allow_html=True)


left, right = st.columns(2, gap="large")
with left:
    cards("Promoter", "TOP PROMOTER DRIVERS", "Positive association")
with right:
    cards("Passive", "TOP PASSIVE DRIVERS", "Conversion opportunities")
    cards("Detractor", "TOP DETRACTOR DRIVERS", "Key pain points")
st.caption("Reliability = confidence (chance the combination produces that NPS group). Customer share = support "
           "(% of all callers with the combination). Impact = lift (how many times more likely than average).")
with st.expander("All mined rules"):
    st.dataframe(rules.rename(columns={"segment": "NPS group", "combination": "Rating combination", "confidence": "Reliability",
                                       "support": "Customer share", "lift": "Impact (×)"})
                 .style.format({"Reliability": "{:.2%}", "Customer share": "{:.2%}", "Impact (×)": "{:.2f}"}),
                 hide_index=True, width="stretch")
analysis(TOP["apriori"])
