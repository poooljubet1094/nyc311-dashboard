"""NYC311 Customer Satisfaction — management dashboards (Streamlit).

Run locally:  streamlit run app.py
"""
import streamlit as st

from common import load_data, page_setup

st.set_page_config(page_title="NYC311 CSAT Dashboards", page_icon=":material/support_agent:", layout="wide")
page_setup()

pages = [
    st.Page("views/overview.py", title="Overview", icon=":material/home:", default=True),
    st.Page("views/lower.py", title="Lower level · Operational", icon=":material/today:", url_path="operational"),
    st.Page("views/middle.py", title="Middle level · Tactical", icon=":material/insights:", url_path="tactical"),
    st.Page("views/top.py", title="Top level · Strategic", icon=":material/flag:", url_path="strategic"),
    st.Page("views/levels.py", title="Visualization map", icon=":material/account_tree:", url_path="visualization-map"),
]
nav = st.navigation(pages)

with st.sidebar:
    st.toggle("Show analysis notes", value=True, key="show_analysis",
              help="A short written analysis under each visual: what it shows, what it means and what to do.")
    df = load_data()
    st.caption(f"{len(df):,} survey responses · {df['start_datetime'].min():%b %Y} – {df['start_datetime'].max():%b %Y}")
    st.caption("Source: [NYC311 Customer Satisfaction Survey, NYC Open Data]"
               "(https://data.cityofnewyork.us/Social-Services/311-Customer-Satisfaction-Survey/kizp-4dfk)")

nav.run()
