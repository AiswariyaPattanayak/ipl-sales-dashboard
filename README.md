# IPL & E-Commerce Sales Dashboard

> Interactive analytics dashboard built with Python, Pandas, NumPy, Plotly & Dash.

![Dashboard Preview](screenshot.png)

## Features

- **IPL Analytics Tab** — win rates, toss analysis, season trends, venue breakdown, team drill-down
- **Sales Dashboard Tab** — revenue/profit KPIs, monthly time-series, regional breakdown, sub-category rankings, profit scatter
- **Fully interactive** — dropdown filters, range sliders, cross-chart filtering
- **Dark theme** — production-ready dark UI

---

## Quick Start (Local)

```bash
# 1. Clone or unzip
cd ipl-sales-dashboard

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run
python app.py

# 5. Open browser
# http://127.0.0.1:8050
```

---

## Deploy to Render (Free)

1. Push this folder to a GitHub repo
2. Go to https://render.com → **New Web Service**
3. Connect your GitHub repo
4. Render auto-detects `render.yaml` — click **Deploy**
5. Live URL in ~2 minutes ✅

---

## Deploy to Heroku

```bash
heroku login
heroku create your-app-name
git push heroku main
heroku open
```

---

## Deploy to Railway

```bash
railway init
railway up
```

---

## Deploy to PythonAnywhere (Free tier)

1. Upload zip → extract in `/home/<username>/ipl-sales-dashboard`
2. Go to **Web** tab → Add new web app → Manual config → Python 3.11
3. Set source code: `/home/<username>/ipl-sales-dashboard`
4. WSGI file — paste:
```python
import sys
sys.path.insert(0, '/home/<username>/ipl-sales-dashboard')
from app import server as application
```
5. Reload → visit `<username>.pythonanywhere.com`

---

## Project Structure

```
ipl-sales-dashboard/
├── app.py              # Main Dash application + data generation
├── requirements.txt    # Python dependencies
├── Procfile            # Heroku/Render process file
├── render.yaml         # Render one-click deploy config
└── README.md
```

---

## Resume Bullet Points

- Built an interactive IPL + e-commerce analytics dashboard using Python, Pandas, and Plotly/Dash with dual-tab layout and live drill-down filters
- Engineered synthetic datasets (1,000+ IPL matches, 15,000+ sales records) with realistic distributions using NumPy for EDA simulation
- Delivered KPI cards, time-series area charts, pie charts, scatter plots, and horizontal bar charts with dark-themed responsive UI
- Deployed as a production web service via Gunicorn on Render with zero-config `render.yaml`

---

## Tech Stack

| Tool | Use |
|------|-----|
| Python 3.11 | Core language |
| Pandas | Data manipulation & aggregation |
| NumPy | Synthetic data, numerical ops |
| Plotly | Interactive chart library |
| Dash | Web framework for analytics apps |
| Gunicorn | WSGI server for production |
