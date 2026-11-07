"""Visualization map: which visual serves which management level, and why."""
import streamlit as st

st.markdown("<div class='level-tag'>Design rationale</div>", unsafe_allow_html=True)
st.title("Visualization map")
st.caption("Which visualization belongs to which management level, the question it answers from the project brief, "
           "and why its form fits that audience.")

st.subheader("How the three levels differ", help="Audience, time horizon, detail level and decisions for each management level.")
st.markdown("""
| | **Lower · Operational** | **Middle · Tactical** | **Top · Strategic** |
| --- | --- | --- | --- |
| **Audience** | Floor supervisors, team leads, QA leads | Operations and QA managers | NYC311 leadership |
| **Time horizon** | Today, this week, this campaign | Quarters and campaigns, 2020–2025 | Years, plus the 2026 outlook |
| **Granularity** | Single days, single responses, language queues | Drivers, campaigns, language segments | Organization-wide KPIs |
| **Decision it supports** | Who to call back, which day to review, which queue to coach | Which driver to fix, which segment needs a program | Are we meeting goals, where to invest, what the risks are |
| **Typical forms** | KPI cards, control chart, tables, heat map | Trend lines, comparative bars, stacked bars, scatter and matrix | Scorecard, forecast, executive summary cards |
""")

LEVELS = {
    "Lower level · Operational": [
        ("KPI cards with sparklines", "What happened (this campaign)?", "KPI cards",
         "Six numbers a supervisor checks first, with the change from the last campaign and a six-campaign sparkline for context.",
         "Sparklines added"),
        ("Alert banner", "What happened today?", "Status message",
         "Applies the escalation rules automatically, so supervisors don't have to spot runs by eye.", "New"),
        ("Daily control chart + responses", "What happened today?", "p-chart with 3σ limits, daily bars",
         "Day-level granularity; limits separate real problems from noise on small days. Clicking a day opens its snapshot.",
         "Upgraded from fixed-threshold dots"),
        ("Day snapshot", "What happened today?", "Metric row",
         "Drill-down for a single selected day: the operational view of one shift's results.", "New"),
        ("Campaign pacing vs last year", "Is this campaign on track?", "Cumulative line",
         "Lets a supervisor judge an in-progress campaign by day 7 or 14 instead of waiting for the end.", "New"),
        ("Rating mix by service area", "Which services were rated poorly?", "Diverging stacked bar",
         "Shows where this campaign's callers are unhappy, the analogue of 'which products sold'.", "—"),
        ("Weekly problem map", "Which areas performed poorly, and when?", "Heat map",
         "Week × service area pinpoints when a problem started within the campaign.", "—"),
        ("Language queue performance", "Which departments performed poorly?", "Dot-and-whisker (95% CI) + table",
         "Queue-level comparison for the current campaign; intervals stop coaching decisions based on small queues.",
         "Confidence intervals added"),
        ("Daily exceptions report", "Which days need investigation?", "Detailed table with status",
         "A classic operational report, now with a statistical control check beside each business-rule flag.",
         "Control check added"),
        ("Customer follow-up log", "Which transactions occurred?", "Transaction table + CSV export",
         "Row-level records, filterable by day, queue and priority: the work list for QA.", "Filters and export added"),
    ],
    "Middle level · Tactical": [
        ("KPI strip", "How is the operation performing overall?", "KPI cards",
         "Period headline figures for managers who plan by quarter and campaign.", "Kept"),
        ("CSAT and NPS trend", "What are the monthly trends?", "Two-panel line chart, Campaign / Quarter / Month switch, trend test",
         "The brief asks for monthly trends; the switch adds month and campaign views, and the test shows CSAT is flat while NPS rises.",
         "Edited: period switch added"),
        ("Departmental performance heat map", "Which department performs best?", "Group × KPI heat map vs average",
         "A departmental performance dashboard in one view: every language group on every KPI, colored above or below average.", "Added"),
        ("Satisfaction mix by campaign", "Which campaign performs best?", "100% stacked bar",
         "Stacked chart recommended for this level; compares the full rating mix across campaigns.", "Kept"),
        ("Segments scatter", "Do segments experience service differently?", "Bubble scatter",
         "Scatter plot recommended for this level; relates two drivers across segments, sized by volume.", "Kept"),
        ("Fix-first matrix", "What factors influence performance?", "Impact × performance quadrant",
         "Turns the drivers into a priority list; each point carries its % favorable, so the old driver bar chart was redundant.",
         "Kept; driver bar chart removed"),
        ("Feature importance + decision tree", "What factors influence performance?", "Bar + tree diagram",
         "Explains which ratings decide NPS: an analytical tool for managers designing coaching and standards.", "Moved here from Top"),
        ("Survey responses by month", "When does feedback arrive?", "Month × year heat map",
         "Detailed survey-operations view used to plan QA and campaign-over-campaign comparisons.", "Moved here from Top"),
    ],
    "Top level · Strategic": [
        ("Summary indicators", "How did we do this year?", "KPI tiles with year-over-year change + NPS mix",
         "Latest-year headline numbers with growth, rather than all-time totals that never change.", "Edited: now latest year with YoY"),
        ("Strategic scorecard", "Is the organization meeting its goals?", "Scorecard vs targets",
         "Targets, status flags and five-year sparklines answer the brief's first strategic question.", "Kept"),
        ("Year-over-year growth", "Are results increasing?", "Bar charts with YoY change labels",
         "The satisfaction equivalent of the brief's yearly growth rate.", "Added"),
        ("CSAT and NPS forecast", "What comes next?", "Forecast with 95% prediction band",
         "Projects the five 2026 campaigns; the gap to target sizes the change needed.", "Kept"),
        ("Local Law 26 compliance", "Are we meeting our legal mandate?", "Campaigns vs legal minimum + responses per year",
         "Replaces the detailed month heat map with the strategic question behind it: is the five-campaign mandate met?",
         "Edited: heat map moved to Middle"),
        ("Opportunity and risk cards (Apriori)", "What are the future opportunities and risks?", "Executive summary cards",
         "Plain-language promoter drivers, passive conversion opportunities and detractor risks.", "Kept, relabelled"),
    ],
}

for level, rows in LEVELS.items():
    st.subheader(level)
    md = "| Visualization | Question it answers | Chart type | Why it fits this level | Upgrade |\n|---|---|---|---|---|\n"
    md += "\n".join(f"| **{v}** | {q} | {c} | {w} | {u} |" for v, q, c, w, u in rows)
    st.markdown(md)

st.subheader("Fit assessment", help="Our check of each page against the project brief's questions and recommended chart types.")
st.markdown("""
- **Lower level: strong fit.** Every visual works at day, response or queue level and supports an immediate action.
- **Middle level: validated and adjusted.** The brief's three tactical questions now each have a visual: *which department performs best* (new department heat map, campaign mix, segments scatter), *monthly trends* (trend chart with a Month view) and *what factors influence performance* (fix-first matrix, feature importance, decision tree). The driver bar chart was removed because the matrix shows the same percentages plus their impact. The decision tree and month heat map moved here from the top level because they are analytical and operational-planning tools, not executive summaries.
- **Top level: validated and adjusted.** It now uses only the brief's strategic forms: summary indicators, a strategic scorecard, growth rates, a forecast, and summary cards for opportunities and risks. Detailed diagnostics moved down to the tactical level. Survey volume is kept only as a compliance check against Local Law 26.
- **Not possible with this data:** the brief's *geographic map* for top management. The public survey has no borough, ZIP code or other location field. Agent- or team-level views are also impossible, because the data has no agent or team IDs.
""")
