# NYC311 Customer Satisfaction Dashboards

An interactive Python (Streamlit + Plotly) web dashboard with one page for each management level:

| Page | Audience | What it shows |
| --- | --- | --- |
| **Overview** | Everyone | Headline KPIs, business context, data cleaning |
| **Lower level · Operational** | Floor supervisors, team leads, QA leads | KPI cards with six-campaign sparklines, automatic alert banner, daily **control chart (p-chart, 3σ limits)** with **click-a-day snapshot**, campaign pacing vs the same campaign last year, rating mix, weekly problem heat map, language queues with **95% confidence intervals**, exceptions report with a control check, filterable follow-up log with **CSV export**. Filter: campaign |
| **Middle level · Tactical** | Operations and QA managers | KPI strip, CSAT and NPS trend by **campaign, quarter or month** with **significance tests**, **department × KPI heat map**, satisfaction mix by campaign, language bubble chart, **fix-first matrix**, feature importance and **decision tree**, survey responses by month. Filter: year range |
| **Top level · Strategic** | NYC311 leadership | **Summary indicators** with year-over-year change, **strategic scorecard vs targets**, **year-over-year growth**, **2026 forecast with 95% prediction intervals**, **Local Law 26 compliance**, Apriori opportunity and risk cards |
| **Visualization map** | Everyone | Which visual serves which management level, the brief's question it answers, and why its form fits |

Every visual has a collapsible **Analysis** panel written like the conclusion and recommendation section of a research paper: first a description of the graph, then a conclusion paragraph (the findings, ending in *"It can be concluded that…"*), then a recommendation paragraph (*"It is recommended that…"*). Each level page ends with an overall **Conclusion and recommendations** section with numbered recommendations and owners. The sidebar switch **Show analysis notes** hides them all for a clean demo.

**Hover to learn what things mean:** KPI labels (dotted underline), section headings and filters (ⓘ icons), table column headers, scorecard KPI names and Apriori card terms all show a short definition on hover. Definitions live in `TIPS` in `common.py`.

Data: [NYC311 Customer Satisfaction Survey](https://data.cityofnewyork.us/Social-Services/311-Customer-Satisfaction-Survey/kizp-4dfk) (NYC Open Data), included in `data/`.

---

## Run it on your computer

```bash
cd nyc311_dashboard
python -m venv .venv
# Windows: .venv\Scripts\activate      macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

The dashboard opens at http://localhost:8501.

## Deploy it to the web (free): Streamlit Community Cloud

1. **Put the folder on GitHub.** Create a new public repository (for example `nyc311-dashboard`) and upload the *contents* of this folder: `app.py`, `common.py`, `narrative.py`, `requirements.txt`, the `views/`, `data/` and `.streamlit/` folders. (The CSV is about 7 MB, which GitHub accepts.)
2. Go to **https://share.streamlit.io**, sign in with GitHub, and click **Create app → Deploy a public app from GitHub**.
3. Choose your repository, branch `main`, and main file path **`app.py`**.
4. Open **Advanced settings** and pick **Python 3.12** (3.13 also works).
5. Click **Deploy**. The first build takes a few minutes; you then get a public link such as `https://nyc311-dashboard.streamlit.app`, which you can share or open during the presentation.

Every push to the repository redeploys the app automatically.

### Other hosts

The app is a standard Streamlit app, so it also runs on Render, Railway or Hugging Face Spaces. Use the start command:

```bash
streamlit run app.py --server.port $PORT --server.address 0.0.0.0
```

---

## Project structure

```
nyc311_dashboard/
├── app.py              # entry point: page config, navigation, sidebar
├── common.py           # data loading + cleaning, KPI helpers, colours, card styles
├── models.py           # Apriori rules, decision tree and shared figures
├── narrative.py        # written analysis for every visual (edit text here)
├── views/
│   ├── overview.py
│   ├── lower.py        # Operational dashboard
│   ├── middle.py       # Tactical dashboard
│   ├── top.py          # Strategic dashboard
│   └── levels.py       # Visualization map (level-fit analysis)
├── data/311_Customer_Satisfaction_Survey.csv
├── .streamlit/config.toml
└── requirements.txt
```

## Data cleaning (shared by all pages)

- Column names to snake_case; agreement scale mapped to 1–5.
- `Agree+I1030` → Agree; `SATISFACTORIO` → Neutral.
- 26 incomplete records dropped (1 blank Job Knowledge, 25 blank NPS): **28,816 → 28,790** rows.
- Languages tidied; the lower level groups them as English / Spanish / Chinese / Others, the middle level keeps each language.

## Notes

- The written analysis on the lower level describes **2025 Campaign 5**, and the middle level's describes the **full 2020–2025 range**. When you change those filters, the charts update and the analysis notes are hidden.
- The 80% CSAT target is a working target for this dashboard (historical CSAT is 80.9%), not an official NYC311 figure.
- Top-level scorecard targets: CSAT 85% and Answer Satisfaction 75% come from the middle-level recommendations; NPS 60 and % Unfavorable 10% are illustrative. Change them in `views/top.py` (`SCORECARD`).
- The forecast is a straight-line projection of the 26 past campaigns with a 95% prediction interval. It shows where the current path leads, not what a new program could achieve.
