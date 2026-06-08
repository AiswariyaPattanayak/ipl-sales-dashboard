"""
IPL & E-Commerce Sales Dashboard
Tech: Python, Pandas, NumPy, Plotly, Dash
Run: python app.py  →  http://127.0.0.1:8050
"""

import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# ── Synthetic but realistic datasets ─────────────────────────────────────────

def make_ipl_data():
    np.random.seed(42)
    teams = ["Mumbai Indians", "Chennai Super Kings", "Royal Challengers Bangalore",
             "Kolkata Knight Riders", "Delhi Capitals", "Sunrisers Hyderabad",
             "Rajasthan Royals", "Punjab Kings"]
    seasons = list(range(2010, 2024))
    rows = []
    for season in seasons:
        for _ in range(60):
            t1, t2 = np.random.choice(teams, 2, replace=False)
            winner = np.random.choice([t1, t2], p=[0.55, 0.45])
            rows.append({
                "season": season,
                "team1": t1,
                "team2": t2,
                "winner": winner,
                "venue": np.random.choice(["Wankhede", "Chepauk", "Eden Gardens",
                                           "Chinnaswamy", "Feroz Shah Kotla",
                                           "Rajiv Gandhi", "Sawai Man Singh"], 1)[0],
                "toss_winner": np.random.choice([t1, t2]),
                "runs": np.random.randint(120, 230),
                "wickets": np.random.randint(2, 10),
            })
    return pd.DataFrame(rows)

def make_sales_data():
    np.random.seed(7)
    categories = ["Technology", "Furniture", "Office Supplies"]
    sub_cats = {
        "Technology": ["Phones", "Computers", "Accessories"],
        "Furniture": ["Chairs", "Tables", "Bookcases"],
        "Office Supplies": ["Paper", "Binders", "Storage"]
    }
    regions = ["West", "East", "South", "Central"]
    states = {
        "West": ["California", "Washington", "Oregon"],
        "East": ["New York", "Pennsylvania", "Ohio"],
        "South": ["Texas", "Florida", "Georgia"],
        "Central": ["Illinois", "Michigan", "Indiana"]
    }
    rows = []
    for year in range(2020, 2024):
        for month in range(1, 13):
            n = np.random.randint(80, 160)
            for _ in range(n):
                cat = np.random.choice(categories)
                region = np.random.choice(regions)
                base_sales = {"Technology": 800, "Furniture": 450, "Office Supplies": 120}[cat]
                rows.append({
                    "order_date": pd.Timestamp(year=year, month=month,
                                               day=np.random.randint(1, 28)),
                    "category": cat,
                    "sub_category": np.random.choice(sub_cats[cat]),
                    "region": region,
                    "state": np.random.choice(states[region]),
                    "sales": round(base_sales * np.random.uniform(0.4, 2.5), 2),
                    "profit": round(base_sales * np.random.uniform(-0.1, 0.6), 2),
                    "quantity": np.random.randint(1, 8),
                    "discount": round(np.random.choice([0, 0.1, 0.2, 0.3], p=[0.5, 0.2, 0.2, 0.1]), 1),
                })
    df = pd.DataFrame(rows)
    df["year"] = df["order_date"].dt.year
    df["month"] = df["order_date"].dt.month
    df["month_name"] = df["order_date"].dt.strftime("%b")
    df["quarter"] = df["order_date"].dt.quarter.map(lambda q: f"Q{q}")
    return df

IPL = make_ipl_data()
SALES = make_sales_data()

# ── App ───────────────────────────────────────────────────────────────────────
app = dash.Dash(__name__, title="IPL & Sales Dashboard")
server = app.server   # for Gunicorn / Render deployment

DARK_BG = "#0f1117"
CARD_BG = "#1a1d27"
ACCENT  = "#6c63ff"
TEXT    = "#e8e8f0"
MUTED   = "#9b9bb4"
GREEN   = "#22c55e"
AMBER   = "#f59e0b"
RED     = "#ef4444"
TEAL    = "#14b8a6"

CARD = {
    "background": CARD_BG,
    "borderRadius": "12px",
    "padding": "20px",
    "border": "1px solid #2a2d3e",
}

def kpi(label, value, delta=None, color=TEXT):
    delta_el = html.Span(delta, style={"fontSize": "12px", "color": GREEN, "marginLeft": "8px"}) if delta else None
    return html.Div([
        html.P(label, style={"color": MUTED, "fontSize": "12px", "margin": "0 0 4px 0",
                             "textTransform": "uppercase", "letterSpacing": "1px"}),
        html.Div([
            html.Span(value, style={"fontSize": "26px", "fontWeight": "700", "color": color}),
            delta_el
        ], style={"display": "flex", "alignItems": "baseline"}),
    ], style={**CARD, "flex": "1", "minWidth": "140px"})

# ── Layout ───────────────────────────────────────────────────────────────────
app.layout = html.Div([
    # Header
    html.Div([
        html.H1("📊 IPL & Sales Analytics Dashboard",
                style={"color": TEXT, "margin": "0", "fontSize": "22px", "fontWeight": "700"}),
        html.P("2010–2023 IPL Season Data  ·  2020–2023 E-Commerce Sales",
               style={"color": MUTED, "margin": "4px 0 0 0", "fontSize": "13px"}),
    ], style={"padding": "24px 32px 16px", "borderBottom": "1px solid #2a2d3e"}),

    # Tabs
    dcc.Tabs(id="tabs", value="ipl", children=[
        dcc.Tab(label="🏏  IPL Analytics", value="ipl",
                style={"backgroundColor": DARK_BG, "color": MUTED, "border": "none", "padding": "12px 24px"},
                selected_style={"backgroundColor": ACCENT, "color": "white", "border": "none", "padding": "12px 24px"}),
        dcc.Tab(label="🛒  Sales Dashboard", value="sales",
                style={"backgroundColor": DARK_BG, "color": MUTED, "border": "none", "padding": "12px 24px"},
                selected_style={"backgroundColor": ACCENT, "color": "white", "border": "none", "padding": "12px 24px"}),
    ], style={"backgroundColor": DARK_BG, "borderBottom": "1px solid #2a2d3e"}),

    html.Div(id="tab-content", style={"padding": "24px 32px"}),
], style={"backgroundColor": DARK_BG, "minHeight": "100vh", "fontFamily": "'Inter', sans-serif", "color": TEXT})


# ── IPL Tab ───────────────────────────────────────────────────────────────────
def ipl_layout():
    teams = sorted(IPL["team1"].unique())
    seasons = sorted(IPL["season"].unique())
    wins = IPL["winner"].value_counts()
    total_matches = len(IPL)
    top_team = wins.idxmax()

    return html.Div([
        # Filters
        html.Div([
            html.Div([
                html.Label("Season Range", style={"color": MUTED, "fontSize": "12px"}),
                dcc.RangeSlider(id="ipl-season", min=2010, max=2023, step=1,
                                value=[2010, 2023],
                                marks={y: str(y) for y in range(2010, 2024, 2)},
                                tooltip={"placement": "bottom"}),
            ], style={"flex": "2"}),
            html.Div([
                html.Label("Team", style={"color": MUTED, "fontSize": "12px"}),
                dcc.Dropdown(id="ipl-team", options=[{"label": t, "value": t} for t in teams],
                             value=None, placeholder="All teams",
                             style={"backgroundColor": CARD_BG, "color": TEXT, "border": "1px solid #2a2d3e"},
                             className="dark-drop"),
            ], style={"flex": "1", "minWidth": "180px"}),
        ], style={"display": "flex", "gap": "24px", "alignItems": "flex-end",
                  "marginBottom": "24px", **CARD}),

        # KPIs
        html.Div(id="ipl-kpis", style={"display": "flex", "gap": "16px", "flexWrap": "wrap",
                                        "marginBottom": "24px"}),

        # Charts row 1
        html.Div([
            html.Div(dcc.Graph(id="ipl-winrate"), style={**CARD, "flex": "1"}),
            html.Div(dcc.Graph(id="ipl-toss"),    style={**CARD, "flex": "1"}),
        ], style={"display": "flex", "gap": "16px", "marginBottom": "16px"}),

        # Charts row 2
        html.Div([
            html.Div(dcc.Graph(id="ipl-season-wins"), style={**CARD, "flex": "2"}),
            html.Div(dcc.Graph(id="ipl-venue"),       style={**CARD, "flex": "1"}),
        ], style={"display": "flex", "gap": "16px"}),
    ])


# ── Sales Tab ────────────────────────────────────────────────────────────────
def sales_layout():
    return html.Div([
        # Filters
        html.Div([
            html.Div([
                html.Label("Year", style={"color": MUTED, "fontSize": "12px"}),
                dcc.Dropdown(id="sales-year",
                             options=[{"label": str(y), "value": y} for y in [2020,2021,2022,2023]] +
                                     [{"label": "All Years", "value": 0}],
                             value=0, clearable=False,
                             style={"backgroundColor": CARD_BG, "color": TEXT, "border": "1px solid #2a2d3e"}),
            ], style={"flex": "1", "minWidth": "130px"}),
            html.Div([
                html.Label("Region", style={"color": MUTED, "fontSize": "12px"}),
                dcc.Dropdown(id="sales-region",
                             options=[{"label": r, "value": r} for r in ["West","East","South","Central"]],
                             value=None, placeholder="All regions",
                             style={"backgroundColor": CARD_BG, "color": TEXT, "border": "1px solid #2a2d3e"}),
            ], style={"flex": "1", "minWidth": "150px"}),
            html.Div([
                html.Label("Category", style={"color": MUTED, "fontSize": "12px"}),
                dcc.Dropdown(id="sales-cat",
                             options=[{"label": c, "value": c} for c in
                                      ["Technology","Furniture","Office Supplies"]],
                             value=None, placeholder="All categories",
                             style={"backgroundColor": CARD_BG, "color": TEXT, "border": "1px solid #2a2d3e"}),
            ], style={"flex": "1", "minWidth": "180px"}),
        ], style={"display": "flex", "gap": "24px", "alignItems": "flex-end",
                  "marginBottom": "24px", **CARD}),

        # KPIs
        html.Div(id="sales-kpis", style={"display": "flex", "gap": "16px", "flexWrap": "wrap",
                                          "marginBottom": "24px"}),

        # Charts row 1
        html.Div([
            html.Div(dcc.Graph(id="sales-timeseries"), style={**CARD, "flex": "3"}),
            html.Div(dcc.Graph(id="sales-pie"),        style={**CARD, "flex": "1"}),
        ], style={"display": "flex", "gap": "16px", "marginBottom": "16px"}),

        # Charts row 2
        html.Div([
            html.Div(dcc.Graph(id="sales-region-bar"),   style={**CARD, "flex": "1"}),
            html.Div(dcc.Graph(id="sales-subcat-bar"),   style={**CARD, "flex": "1"}),
            html.Div(dcc.Graph(id="sales-profit-scatter"), style={**CARD, "flex": "1"}),
        ], style={"display": "flex", "gap": "16px"}),
    ])


# ── Tab render callback ───────────────────────────────────────────────────────
@app.callback(Output("tab-content", "children"), Input("tabs", "value"))
def render_tab(tab):
    return ipl_layout() if tab == "ipl" else sales_layout()


# ── IPL callbacks ─────────────────────────────────────────────────────────────
CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color=TEXT, size=12),
    margin=dict(l=10, r=10, t=36, b=10),
    legend=dict(bgcolor="rgba(0,0,0,0)"),
)

@app.callback(
    Output("ipl-kpis", "children"),
    Output("ipl-winrate", "figure"),
    Output("ipl-toss", "figure"),
    Output("ipl-season-wins", "figure"),
    Output("ipl-venue", "figure"),
    Input("ipl-season", "value"),
    Input("ipl-team", "value"),
)
def update_ipl(season_range, team):
    df = IPL[(IPL["season"] >= season_range[0]) & (IPL["season"] <= season_range[1])].copy()
    total = len(df)
    wins = df["winner"].value_counts()

    if team:
        team_matches = df[(df["team1"] == team) | (df["team2"] == team)]
        team_wins = (team_matches["winner"] == team).sum()
        win_pct = f"{team_wins / len(team_matches) * 100:.1f}%" if len(team_matches) else "N/A"
        kpis = [
            kpi("Matches Played", len(team_matches), color=ACCENT),
            kpi("Wins", team_wins, color=GREEN),
            kpi("Win Rate", win_pct, color=AMBER),
            kpi("Seasons", f"{season_range[0]}–{season_range[1]}", color=TEAL),
        ]
    else:
        kpis = [
            kpi("Total Matches", f"{total:,}", color=ACCENT),
            kpi("Top Team", wins.idxmax().split()[0], color=GREEN),
            kpi("Most Wins", f"{wins.max()}", color=AMBER),
            kpi("Seasons", f"{season_range[1]-season_range[0]+1}", color=TEAL),
        ]

    # Win rate chart
    top8 = wins.head(8).reset_index()
    top8.columns = ["team", "wins"]
    top8["short"] = top8["team"].apply(lambda x: "".join(w[0] for w in x.split()))
    fig_wr = px.bar(top8, x="short", y="wins", title="Wins by Team",
                    color="wins", color_continuous_scale=["#2d2b55", ACCENT])
    fig_wr.update_layout(**CHART_LAYOUT, coloraxis_showscale=False)
    fig_wr.update_traces(marker_line_width=0)

    # Toss win vs match win
    toss_win_match_win = df[df["toss_winner"] == df["winner"]].shape[0]
    toss_fig = go.Figure(go.Pie(
        labels=["Toss=Win", "Toss≠Win"],
        values=[toss_win_match_win, total - toss_win_match_win],
        hole=0.6,
        marker_colors=[ACCENT, "#2d2b55"],
        textinfo="percent+label",
        textfont_color=TEXT,
    ))
    toss_fig.update_layout(**CHART_LAYOUT, title="Toss → Match Win")

    # Wins per season
    season_wins = df.groupby(["season", "winner"]).size().reset_index(name="wins")
    top_teams = wins.head(4).index.tolist()
    season_wins = season_wins[season_wins["winner"].isin(top_teams)]
    fig_sw = px.line(season_wins, x="season", y="wins", color="winner",
                     title="Season-by-Season Wins (Top 4 Teams)",
                     markers=True)
    fig_sw.update_layout(**CHART_LAYOUT)

    # Venue
    venue_counts = df["venue"].value_counts().head(7).reset_index()
    venue_counts.columns = ["venue", "matches"]
    fig_v = px.bar(venue_counts, x="matches", y="venue", orientation="h",
                   title="Matches by Venue", color="matches",
                   color_continuous_scale=["#1a2a3a", TEAL])
    fig_v.update_layout(**CHART_LAYOUT, coloraxis_showscale=False)

    return kpis, fig_wr, toss_fig, fig_sw, fig_v


# ── Sales callbacks ───────────────────────────────────────────────────────────
@app.callback(
    Output("sales-kpis", "children"),
    Output("sales-timeseries", "figure"),
    Output("sales-pie", "figure"),
    Output("sales-region-bar", "figure"),
    Output("sales-subcat-bar", "figure"),
    Output("sales-profit-scatter", "figure"),
    Input("sales-year", "value"),
    Input("sales-region", "value"),
    Input("sales-cat", "value"),
)
def update_sales(year, region, category):
    df = SALES.copy()
    if year:
        df = df[df["year"] == year]
    if region:
        df = df[df["region"] == region]
    if category:
        df = df[df["category"] == category]

    total_sales  = df["sales"].sum()
    total_profit = df["profit"].sum()
    margin       = total_profit / total_sales * 100 if total_sales else 0
    orders       = len(df)

    kpis = [
        kpi("Total Revenue",  f"${total_sales/1e6:.2f}M", color=ACCENT),
        kpi("Total Profit",   f"${total_profit/1e3:.1f}K",
            color=GREEN if total_profit >= 0 else RED),
        kpi("Profit Margin",  f"{margin:.1f}%", color=AMBER),
        kpi("Orders",         f"{orders:,}", color=TEAL),
        kpi("Avg Order Value",f"${total_sales/orders:.0f}" if orders else "$0", color=TEXT),
    ]

    # Time series
    monthly = df.groupby(["year", "month"])["sales"].sum().reset_index()
    monthly["period"] = pd.to_datetime(
        monthly["year"].astype(str) + "-" + monthly["month"].astype(str).str.zfill(2))
    fig_ts = px.area(monthly, x="period", y="sales", title="Monthly Revenue Trend",
                     color_discrete_sequence=[ACCENT])
    fig_ts.update_traces(fill="tozeroy", fillcolor="rgba(108,99,255,0.15)")
    fig_ts.update_layout(**CHART_LAYOUT)
    fig_ts.update_yaxes(tickprefix="$", tickformat=",.0f")

    # Category pie
    cat_sales = df.groupby("category")["sales"].sum().reset_index()
    fig_pie = px.pie(cat_sales, values="sales", names="category",
                     title="Revenue by Category",
                     color_discrete_sequence=[ACCENT, TEAL, AMBER])
    fig_pie.update_layout(**CHART_LAYOUT)
    fig_pie.update_traces(textfont_color=TEXT)

    # Region bar
    region_df = df.groupby("region").agg(sales=("sales","sum"), profit=("profit","sum")).reset_index()
    fig_reg = px.bar(region_df, x="region", y=["sales","profit"],
                     barmode="group", title="Revenue & Profit by Region",
                     color_discrete_sequence=[ACCENT, GREEN])
    fig_reg.update_layout(**CHART_LAYOUT)
    fig_reg.update_yaxes(tickprefix="$", tickformat=",.0f")

    # Sub-category
    sub_df = df.groupby("sub_category")["sales"].sum().nlargest(8).reset_index()
    fig_sub = px.bar(sub_df, x="sales", y="sub_category", orientation="h",
                     title="Top Sub-Categories", color="sales",
                     color_continuous_scale=["#1a2a3a", AMBER])
    fig_sub.update_layout(**CHART_LAYOUT, coloraxis_showscale=False)
    fig_sub.update_xaxes(tickprefix="$", tickformat=",.0f")

    # Profit scatter
    scatter_df = df.groupby("sub_category").agg(
        sales=("sales","sum"), profit=("profit","sum"), qty=("quantity","sum")).reset_index()
    fig_sc = px.scatter(scatter_df, x="sales", y="profit", size="qty",
                        text="sub_category", title="Sales vs Profit (bubble=qty)",
                        color="profit", color_continuous_scale=["#7f1d1d", "#14532d"])
    fig_sc.update_traces(textposition="top center", textfont_size=9, textfont_color=TEXT)
    fig_sc.update_layout(**CHART_LAYOUT, coloraxis_showscale=False)
    fig_sc.update_xaxes(tickprefix="$")
    fig_sc.update_yaxes(tickprefix="$")

    return kpis, fig_ts, fig_pie, fig_reg, fig_sub, fig_sc


if __name__ == "__main__":
    app.run(debug=True, port=8050)
