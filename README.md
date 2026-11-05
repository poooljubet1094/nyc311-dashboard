# NYC311 Customer Satisfaction Dashboards

An interactive Python (Streamlit + Plotly) web dashboard with one page for each management level:

| Page | Audience | What it shows |
| --- | --- | --- |
| **Overview** | Everyone | Headline KPIs, business context, data cleaning |
| **Lower level · Operational** | Floor supervisors, team leads, QA leads | KPI scorecard vs the previous campaign, daily CSAT trend, rating mix by service area, weekly problem heat map, language queue performance, daily exceptions report, customer follow-up log. Filter: campaign |
| **Middle level · Tactical** | Operations and QA managers | KPI strip, quarterly CSAT and NPS trend, favorable rating by driver, satisfaction mix by campaign, language segment bubble chart. Filter: year range |
| **Top level · Strategic** | NYC311 leadership | Overall NPS split, survey volume heat map and yearly growth, decision-tree feature importance and tipping points, Apriori NPS driver cards |

Every visual has a collapsible **Analysis** panel with its Description, Insight, Interpretation and Recommendation. The sidebar switch **Show analysis notes** hides them all for a clean demo.

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
├── narrative.py        # written analysis for every visual (edit text here)
├── views/
│   ├── overview.py
│   ├── lower.py        # Operational dashboard
│   ├── middle.py       # Tactical dashboard
│   └── top.py          # Strategic dashboard
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
