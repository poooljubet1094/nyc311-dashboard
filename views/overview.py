"""Landing page: business context and the three management-level dashboards."""
import streamlit as st

from common import bottom2, campaign_order, kpi_card, load_data, nps_score, top2

df = load_data()

st.title("NYC311 Customer Satisfaction Dashboards")
st.caption("Executive dashboards and data visualizations for three management levels · "
           "Data: NYC311 Customer Satisfaction Survey, NYC Open Data")

c = st.columns(4)
with c[0]:
    kpi_card("Survey responses", f"{len(df):,}", "", f"{df['start_datetime'].min():%b %Y} – {df['start_datetime'].max():%b %Y}")
with c[1]:
    kpi_card("CSAT (% favorable)", f"{top2(df['overall_satisfaction']):.1f}%", "", "Overall Satisfaction 4–5")
with c[2]:
    kpi_card("Net Promoter Score", f"{nps_score(df['nps']):+.1f}", "", "Promoters − detractors")
with c[3]:
    kpi_card("Answer satisfaction", f"{top2(df['answer_satisfaction']):.1f}%", "", "The weakest service driver")

st.subheader("Choose a management level")
cols = st.columns(3, gap="medium")
levels = [
    ("views/lower.py", "Lower level · Operational", "Floor supervisors, team leads, QA leads",
     "What happened each day, which responses need follow-up, which service areas and language queues performed poorly. "
     "Filter by campaign."),
    ("views/middle.py", "Middle level · Tactical", "Operations and quality-assurance managers",
     "Quarterly CSAT and NPS trends, service-driver comparison, campaign mix and language segments. Filter by year."),
    ("views/top.py", "Top level · Strategic", "NYC311 leadership",
     "Overall NPS, survey coverage growth, the decision tree and Apriori rules that show what actually drives NPS."),
]
for col, (path, title, who, what) in zip(cols, levels):
    with col:
        with st.container(border=True):
            st.markdown(f"**{title}**")
            st.caption(who)
            st.write(what)
            st.page_link(path, label="Open dashboard", icon=":material/arrow_forward:")

st.subheader("Business context")
st.markdown(f"""
| | |
| --- | --- |
| **Organization** | NYC311, the City of New York's contact center for non-emergency government services and information |
| **Industry** | Public sector, government customer service (contact center) |
| **Business problem** | Callers rate the agents highly but are much less satisfied with the *answer* they receive; overall CSAT has been flat at about 77–84% for five years |
| **Business objectives** | Raise customer satisfaction and NPS by improving answer quality and first-contact resolution, and reduce the share of dissatisfied callers ({bottom2(df['overall_satisfaction']):.1f}% today) |
| **Dataset** | {len(df):,} survey responses across {len(campaign_order(df))} survey campaigns. Each row is one caller's ratings of Overall Satisfaction, Wait Time, Agent Customer Service, Agent Job Knowledge and Answer Satisfaction (1–5) plus a 0–10 recommend score |
""")

with st.expander("Data cleaning"):
    st.markdown("""
- Column names standardised to snake_case; the 1–5 agreement scale mapped to numbers (Strongly Disagree = 1 … Strongly Agree = 5).
- Two typos fixed: `Agree+I1030` → Agree and `SATISFACTORIO` → Neutral.
- 26 incomplete records dropped (one blank Job Knowledge rating, 25 blank NPS scores): 28,816 → 28,790 rows.
- Survey languages tidied (invisible marks removed, codes such as `ht`, `bn`, `ur` expanded). The lower level groups them into English, Spanish, Chinese and Others; the middle level keeps each language.
- Channel and Survey Type each have a single value, so they are not used.
""")
