"""Models and figure builders shared by the tactical and strategic pages."""
import calendar

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from mlxtend.frequent_patterns import apriori, association_rules
from sklearn.tree import DecisionTreeClassifier

from common import BASE_LAYOUT, C

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
    """Depth-3 decision tree classifying callers into NPS groups from their ratings and survey turnaround."""
    features = {"overall_satisfaction": "Overall Satisfaction", "answer_satisfaction": "Answer Satisfaction",
                "agent_customer_service": "Agent Customer Service", "turnaround_minutes": "Turnaround (Minutes)",
                "agent_job_knowledge": "Agent Job Knowledge", "wait_time": "Wait Time Rating"}
    X, y = data[list(features)], data["nps_group"].astype(str)
    model = DecisionTreeClassifier(max_depth=3, random_state=42).fit(X, y)
    return model, list(features.values())


def importance_figure(model, feat_names):
    imp = pd.Series(model.feature_importances_, index=feat_names).sort_values()
    fig = go.Figure(go.Bar(y=imp.index, x=imp.values * 100, orientation="h", text=[f"{v * 100:.1f}%" for v in imp.values],
                           textposition="outside", cliponaxis=False,
                           marker_color=[C["blue"] if v > 0.05 else "#9ec5f4" for v in imp.values],
                           hovertemplate="%{y}: %{x:.1f}%<extra></extra>"))
    fig.update_layout(**BASE_LAYOUT, height=380, bargap=0.35)
    fig.update_layout(margin=dict(l=10, r=40, t=30, b=10))
    fig.update_xaxes(range=[0, 100], ticksuffix="%", title_text="Share of the model's decisions", gridcolor=C["grid"], showgrid=True)
    return fig


def tree_figure(model, feat_names):
    t = model.tree_
    classes = list(model.classes_)
    order_cls = ["Detractor", "Passive", "Promoter"]
    fill = {"Detractor": "#f6c9c4", "Passive": "#ffe1a8", "Promoter": "#cde2fb"}
    edge = {"Detractor": "#c62828", "Passive": "#c77700", "Promoter": "#2a78d6"}
    pos, depth, leaves = {}, {}, []

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
                    fig.add_annotation(x=(pos[node] + pos[child]) / 2, y=-0.5, text="Yes (≤)" if lab == "Yes" else "No (>)",
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
        fig.add_annotation(x=pos[node], y=-depth[node], text=f"{split}{share:.1f}% of callers<br>{cls} {mix[cls] * 100:.0f}%",
                           showarrow=False, align="center", font=dict(size=10 if is_leaf else 11, color=C["ink"]),
                           bgcolor=fill[cls], bordercolor=edge[cls], borderwidth=1, borderpad=4)
        hover_x.append(pos[node]); hover_y.append(-depth[node])
        hover_t.append(f"{share:.1f}% of callers<br>" + "<br>".join(f"{c}: {mix.get(c, 0) * 100:.1f}%" for c in order_cls))
    fig.add_trace(go.Scatter(x=hover_x, y=hover_y, mode="markers", marker=dict(size=40, opacity=0),
                             hovertext=hover_t, hoverinfo="text", showlegend=False))
    fig.update_layout(**BASE_LAYOUT, height=460)
    fig.update_layout(margin=dict(l=10, r=10, t=20, b=10))
    fig.update_xaxes(visible=False, range=[-0.6, len(leaves) - 0.4])
    fig.update_yaxes(visible=False, range=[-3.45, 0.45])
    return fig


def volume_heatmap_figure(df):
    piv = df.groupby(["month", "year"]).size().unstack(fill_value=0).reindex(range(1, 13), fill_value=0)
    pct = piv / piv.sum() * 100
    text = [[f"{piv.iloc[i, j]:,}<br>({pct.iloc[i, j]:.1f}%)" for j in range(piv.shape[1])] for i in range(12)]
    fig = go.Figure(go.Heatmap(
        z=piv.values, x=[str(y) for y in piv.columns], y=[calendar.month_name[m] for m in piv.index],
        text=text, texttemplate="%{text}", textfont=dict(size=11), xgap=2, ygap=2,
        colorscale=[[0, "#f7fbf2"], [0.5, "#86c48a"], [1, "#1f6b35"]], colorbar=dict(title="Responses", thickness=10),
        hovertemplate="%{y} %{x}<br>%{z:,} responses<extra></extra>"))
    fig.update_layout(**BASE_LAYOUT, height=520)
    fig.update_layout(margin=dict(l=10, r=10, t=20, b=10))
    fig.update_yaxes(autorange="reversed")
    return fig
