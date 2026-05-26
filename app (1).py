# ╔══════════════════════════════════════════════════════════════╗
# ║   SDG 4 — Quality Education Dashboard                       ║
# ║   Color Palette: #3D348B #7678ED #F7B801 #F18701 #F35B04   ║
# ╚══════════════════════════════════════════════════════════════╝

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ── PAGE CONFIG ────────────────────────────────────────────────
st.set_page_config(
    page_title="SDG 4 · Quality Education",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── COLOR PALETTE ──────────────────────────────────────────────
C1 = "#3D348B"   # Deep Indigo   — primary background / headers
C2 = "#7678ED"   # Periwinkle    — secondary / accents
C3 = "#F7B801"   # Amber         — highlights / KPI borders
C4 = "#F18701"   # Orange        — chart accent
C5 = "#F35B04"   # Burnt Orange  — alerts / strong accent
WHITE = "#FFFFFF"
LIGHT_BG = "#F0EFF9"  # very light indigo tint for cards

# ── GLOBAL CSS ─────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* ── App background */
.stApp {{
    background: linear-gradient(135deg, {C1} 0%, #2a2568 60%, #1a1545 100%);
    font-family: 'DM Sans', sans-serif;
}}

/* ── Sidebar */
[data-testid="stSidebar"] {{
    background: rgba(255,255,255,0.06) !important;
    border-right: 1px solid rgba(118,120,237,0.3);
    backdrop-filter: blur(10px);
}}
[data-testid="stSidebar"] * {{ color: {WHITE} !important; }}
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stSlider label {{ color: {C3} !important; font-weight: 600; }}

/* ── Main title */
.hero-title {{
    font-family: 'Syne', sans-serif;
    font-size: 58px;
    font-weight: 800;
    color: {WHITE};
    line-height: 1.1;
    letter-spacing: -1px;
}}
.hero-sub {{
    font-family: 'Syne', sans-serif;
    font-size: 16px;
    font-weight: 400;
    color: {C2};
    letter-spacing: 4px;
    text-transform: uppercase;
    margin-top: 6px;
}}
.hero-divider {{
    width: 80px; height: 4px;
    background: linear-gradient(90deg, {C3}, {C5});
    border-radius: 2px;
    margin: 16px 0 24px 0;
}}

/* ── Section headers */
.section-header {{
    font-family: 'Syne', sans-serif;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: {C3};
    margin: 32px 0 12px 0;
    display: flex;
    align-items: center;
    gap: 10px;
}}
.section-header::after {{
    content: '';
    flex: 1;
    height: 1px;
    background: rgba(118,120,237,0.3);
}}

/* ── KPI Cards */
.kpi-card {{
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(118,120,237,0.35);
    border-top: 3px solid {C3};
    border-radius: 14px;
    padding: 22px 20px;
    backdrop-filter: blur(8px);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    margin-bottom: 12px;
}}
.kpi-card:hover {{
    transform: translateY(-3px);
    box-shadow: 0 12px 30px rgba(0,0,0,0.25);
}}
.kpi-label {{
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: {C2};
    margin-bottom: 8px;
}}
.kpi-value {{
    font-family: 'Syne', sans-serif;
    font-size: 36px;
    font-weight: 800;
    color: {WHITE};
    line-height: 1;
}}
.kpi-unit {{
    font-size: 13px;
    color: rgba(255,255,255,0.5);
    margin-top: 4px;
}}
.kpi-badge {{
    display: inline-block;
    background: rgba(247,184,1,0.18);
    border: 1px solid {C3};
    color: {C3};
    font-size: 11px;
    font-weight: 700;
    padding: 3px 10px;
    border-radius: 20px;
    margin-top: 8px;
}}

/* ── Chart cards */
.chart-card {{
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(118,120,237,0.25);
    border-radius: 16px;
    padding: 20px;
    backdrop-filter: blur(6px);
    margin-bottom: 16px;
}}
.chart-title {{
    font-family: 'Syne', sans-serif;
    font-size: 14px;
    font-weight: 700;
    color: {WHITE};
    margin-bottom: 4px;
}}
.chart-sub {{
    font-size: 11px;
    color: rgba(255,255,255,0.45);
    margin-bottom: 14px;
}}

/* ── Insight box */
.insight-box {{
    background: linear-gradient(135deg, rgba(247,184,1,0.12), rgba(243,91,4,0.08));
    border: 1px solid rgba(247,184,1,0.35);
    border-left: 4px solid {C3};
    border-radius: 10px;
    padding: 18px 22px;
    margin-top: 14px;
    color: rgba(255,255,255,0.85);
    font-size: 13.5px;
    line-height: 1.7;
}}
.insight-box strong {{ color: {C3}; }}

/* ── Year badge */
.year-badge {{
    font-family: 'Syne', sans-serif;
    font-size: 72px;
    font-weight: 800;
    color: rgba(118,120,237,0.15);
    position: absolute;
    top: -10px;
    right: 20px;
    line-height: 1;
    pointer-events: none;
    user-select: none;
}}

/* ── Plotly charts text override */
[data-testid="stPlotlyChart"] {{ border-radius: 10px; overflow: hidden; }}

/* ── Hide streamlit branding */
#MainMenu, footer {{ visibility: hidden; }}
header[data-testid="stHeader"] {{ background: transparent; }}

/* ── Scrollbar */
::-webkit-scrollbar {{ width: 5px; }}
::-webkit-scrollbar-track {{ background: transparent; }}
::-webkit-scrollbar-thumb {{ background: {C2}; border-radius: 10px; }}
</style>
""", unsafe_allow_html=True)

# ── CHART THEME HELPER ─────────────────────────────────────────
def chart_layout(title="", height=380):
    return dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.04)",
        font=dict(family="DM Sans", color="rgba(255,255,255,0.75)", size=11),
        title=dict(text=title, font=dict(family="Syne", size=14, color=WHITE)),
        height=height,
        margin=dict(l=40, r=20, t=40, b=40),
        xaxis=dict(gridcolor="rgba(118,120,237,0.15)", linecolor="rgba(255,255,255,0.1)"),
        yaxis=dict(gridcolor="rgba(118,120,237,0.15)", linecolor="rgba(255,255,255,0.1)"),
        colorway=[C2, C3, C4, C5, C1],
        showlegend=True,
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=WHITE, size=10))
    )

PALETTE = [C2, C3, C4, C5, "#9B59B6", "#2ECC71", "#E74C3C", "#1ABC9C"]

# ── DATA ───────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("sdg4_cleaned.csv")
    df["log_gdp"] = np.log(df["gdp_per_capita"])
    return df

df = load_data()

# ── SIDEBAR ────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style='text-align:center; padding: 20px 0 28px 0;'>
        <div style='font-family:Syne; font-size:22px; font-weight:800; color:{WHITE};'>🎓 SDG 4</div>
        <div style='font-size:10px; letter-spacing:3px; color:{C3}; text-transform:uppercase; margin-top:4px;'>Quality Education</div>
        <div style='width:40px; height:3px; background:linear-gradient(90deg,{C3},{C5}); border-radius:2px; margin:12px auto 0;'></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"<p style='font-size:11px; letter-spacing:2px; color:{C3}; font-weight:700; text-transform:uppercase;'>⏱ SELECT YEAR</p>", unsafe_allow_html=True)
    selected_year = st.slider("", int(df["Year"].min()), int(df["Year"].max()), 2015, label_visibility="collapsed")

    st.markdown(f"<p style='font-size:11px; letter-spacing:2px; color:{C3}; font-weight:700; text-transform:uppercase; margin-top:20px;'>🌍 COMPARE COUNTRIES</p>", unsafe_allow_html=True)
    all_countries = sorted(df["Entity"].unique())
    default_countries = ["Philippines", "United States", "Japan", "Niger", "Norway", "Brazil"]
    selected_countries = st.multiselect("", all_countries, default=default_countries, label_visibility="collapsed")

    st.markdown(f"<p style='font-size:11px; letter-spacing:2px; color:{C3}; font-weight:700; text-transform:uppercase; margin-top:20px;'>📊 DRIVER VARIABLE</p>", unsafe_allow_html=True)
    driver_map = {
        "Log GDP per Capita": "log_gdp",
        "Gov. Education Spending (%)": "gov_edu_spending_pct",
        "Female/Male Labor Ratio": "female_male_labor_ratio",
        "Internet Usage (%)": "internet_usage_pct",
    }
    selected_driver_label = st.selectbox("", list(driver_map.keys()), label_visibility="collapsed")
    selected_driver = driver_map[selected_driver_label]

    st.markdown(f"""
    <div style='margin-top:40px; padding:14px; background:rgba(118,120,237,0.12); border-radius:10px; border:1px solid rgba(118,120,237,0.25);'>
        <p style='font-size:10px; color:rgba(255,255,255,0.4); margin:0; line-height:1.6;'>
        Sources: Our World in Data, World Bank, ILO, UNESCO<br>
        Coverage: 191 countries · 2000–2023
        </p>
    </div>
    """, unsafe_allow_html=True)

# ── FILTERED DATA ──────────────────────────────────────────────
df_year  = df[df["Year"] == selected_year]
df_world = df.groupby("Year").agg(
    avg_schooling=("avg_years_schooling", "mean"),
    avg_internet=("internet_usage_pct", "mean"),
    avg_gdp=("gdp_per_capita", "mean"),
    avg_gov=("gov_edu_spending_pct", "mean"),
    avg_labor=("female_male_labor_ratio", "mean"),
).reset_index()

prev_year_data = df[df["Year"] == max(selected_year - 1, 2000)]

# ── HEADER ─────────────────────────────────────────────────────
col_title, col_year = st.columns([3, 1])
with col_title:
    st.markdown(f"""
    <div style='position:relative;'>
        <div class='hero-sub'>United Nations · Sustainable Development Goal 4</div>
        <div class='hero-title'>Quality<br>Education</div>
        <div class='hero-divider'></div>
        <div style='color:rgba(255,255,255,0.5); font-size:13px;'>
            What socioeconomic factors drive years of schooling across countries?
        </div>
    </div>
    """, unsafe_allow_html=True)
with col_year:
    st.markdown(f"""
    <div style='text-align:right; padding-top:10px;'>
        <div style='font-size:11px; letter-spacing:2px; color:{C2}; font-weight:600; text-transform:uppercase;'>Viewing Year</div>
        <div style='font-family:Syne; font-size:80px; font-weight:800; color:{C3}; line-height:1;'>{selected_year}</div>
        <div style='font-size:11px; color:rgba(255,255,255,0.35);'>{df_year["Entity"].nunique()} countries · {len(df_year)} records</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr style='border:none; border-top:1px solid rgba(118,120,237,0.2); margin:20px 0;'>", unsafe_allow_html=True)

# ── KPI SECTION ────────────────────────────────────────────────
st.markdown(f"<div class='section-header'>📌 Key Indicators — {selected_year}</div>", unsafe_allow_html=True)

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

def delta_str(curr, prev, fmt=".2f"):
    if prev == 0: return ""
    d = curr - prev
    arrow = "▲" if d >= 0 else "▼"
    color = C3 if d >= 0 else C5
    return f"<span style='color:{color}; font-size:12px;'>{arrow} {abs(d):{fmt}}</span>"

curr_school = df_year["avg_years_schooling"].mean()
prev_school = prev_year_data["avg_years_schooling"].mean() if not prev_year_data.empty else curr_school

curr_internet = df_year["internet_usage_pct"].mean()
prev_internet = prev_year_data["internet_usage_pct"].mean() if not prev_year_data.empty else curr_internet

curr_gdp = df_year["gdp_per_capita"].mean()
curr_gov = df_year["gov_edu_spending_pct"].mean()
curr_labor = df_year["female_male_labor_ratio"].mean()

top_country  = df_year.loc[df_year["avg_years_schooling"].idxmax(), "Entity"]
bot_country  = df_year.loc[df_year["avg_years_schooling"].idxmin(), "Entity"]

with kpi1:
    st.markdown(f"""
    <div class='kpi-card'>
        <div class='kpi-label'>🌍 Avg Schooling</div>
        <div class='kpi-value'>{curr_school:.2f}</div>
        <div class='kpi-unit'>years globally</div>
        <div style='margin-top:8px;'>{delta_str(curr_school, prev_school)}</div>
    </div>""", unsafe_allow_html=True)

with kpi2:
    st.markdown(f"""
    <div class='kpi-card' style='border-top-color:{C2};'>
        <div class='kpi-label'>🌐 Internet Access</div>
        <div class='kpi-value'>{curr_internet:.1f}%</div>
        <div class='kpi-unit'>of population</div>
        <div style='margin-top:8px;'>{delta_str(curr_internet, prev_internet, ".1f")}</div>
    </div>""", unsafe_allow_html=True)

with kpi3:
    st.markdown(f"""
    <div class='kpi-card' style='border-top-color:{C4};'>
        <div class='kpi-label'>💰 Avg GDP/Capita</div>
        <div class='kpi-value'>${curr_gdp:,.0f}</div>
        <div class='kpi-unit'>USD per person</div>
        <div class='kpi-badge'>Economic Driver</div>
    </div>""", unsafe_allow_html=True)

with kpi4:
    st.markdown(f"""
    <div class='kpi-card' style='border-top-color:{C5};'>
        <div class='kpi-label'>🏆 Top Country</div>
        <div class='kpi-value' style='font-size:22px; margin-top:4px;'>{top_country}</div>
        <div class='kpi-unit'>{df_year["avg_years_schooling"].max():.1f} yrs schooling</div>
        <div class='kpi-badge' style='border-color:{C5}; color:{C5}; background:rgba(243,91,4,0.12);'>Highest</div>
    </div>""", unsafe_allow_html=True)

with kpi5:
    st.markdown(f"""
    <div class='kpi-card' style='border-top-color:rgba(255,255,255,0.2);'>
        <div class='kpi-label'>📚 Gov. Edu Spend</div>
        <div class='kpi-value'>{curr_gov:.1f}%</div>
        <div class='kpi-unit'>of total spending</div>
        <div class='kpi-badge' style='border-color:{C2}; color:{C2}; background:rgba(118,120,237,0.12);'>Policy Driver</div>
    </div>""", unsafe_allow_html=True)

# ── ROW 1: GLOBAL TREND + CHOROPLETH MAP ──────────────────────
st.markdown(f"<div class='section-header'>📈 Global Trends Over Time</div>", unsafe_allow_html=True)

col_trend, col_map = st.columns([1, 1.4])

with col_trend:
    st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
    st.markdown(f"<div class='chart-title'>Average Years of Schooling (2000–2023)</div><div class='chart-sub'>Global mean with all-country range band</div>", unsafe_allow_html=True)

    yearly_stats = df.groupby("Year")["avg_years_schooling"].agg(["mean","min","max"]).reset_index()

    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(
        x=yearly_stats["Year"], y=yearly_stats["max"],
        fill=None, mode="lines", line=dict(width=0),
        showlegend=False, name="Max"
    ))
    fig_trend.add_trace(go.Scatter(
        x=yearly_stats["Year"], y=yearly_stats["min"],
        fill="tonexty", mode="lines", line=dict(width=0),
        fillcolor="rgba(118,120,237,0.15)", showlegend=False, name="Min"
    ))
    fig_trend.add_trace(go.Scatter(
        x=yearly_stats["Year"], y=yearly_stats["mean"],
        mode="lines+markers", name="Global Avg",
        line=dict(color=C3, width=3),
        marker=dict(size=6, color=C3)
    ))
    fig_trend.add_vline(x=selected_year, line_dash="dash", line_color=C5, line_width=1.5,
                        annotation_text=str(selected_year), annotation_font_color=C5)
    fig_trend.update_layout(**chart_layout(height=320))
    st.plotly_chart(fig_trend, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_map:
    st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
    st.markdown(f"<div class='chart-title'>World Map — Avg Years of Schooling ({selected_year})</div><div class='chart-sub'>Darker = more schooling years</div>", unsafe_allow_html=True)

    fig_map = px.choropleth(
        df_year, locations="Code",
        color="avg_years_schooling",
        hover_name="Entity",
        hover_data={"avg_years_schooling": ":.2f", "Code": False},
        color_continuous_scale=[[0, C1],[0.3, C2],[0.6, C3],[0.8, C4],[1.0, C5]],
        range_color=[0, df["avg_years_schooling"].max()],
        labels={"avg_years_schooling": "Avg Years"}
    )
    fig_map.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        geo=dict(bgcolor="rgba(0,0,0,0)", showframe=False,
                 showcoastlines=True, coastlinecolor="rgba(255,255,255,0.15)",
                 landcolor="rgba(61,52,139,0.4)", showocean=True,
                 oceancolor="rgba(20,18,60,0.6)"),
        coloraxis_colorbar=dict(
            tickfont=dict(color=WHITE, size=10),
            title=dict(text="Years", font=dict(color=WHITE, size=10))
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        height=320,
        font=dict(color=WHITE)
    )
    st.plotly_chart(fig_map, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ── ROW 2: COUNTRY COMPARISON + DRIVER SCATTER ────────────────
st.markdown(f"<div class='section-header'>🔍 Country Comparison & Driver Analysis</div>", unsafe_allow_html=True)

col_bar, col_scatter = st.columns([1, 1])

with col_bar:
    st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
    st.markdown(f"<div class='chart-title'>Country Comparison ({selected_year})</div><div class='chart-sub'>Selected countries ranked by schooling years</div>", unsafe_allow_html=True)

    if selected_countries:
        df_compare = df_year[df_year["Entity"].isin(selected_countries)].sort_values("avg_years_schooling", ascending=True)
        fig_bar = px.bar(
            df_compare, x="avg_years_schooling", y="Entity",
            orientation="h",
            color="avg_years_schooling",
            color_continuous_scale=[[0, C1],[0.4, C2],[0.7, C3],[1.0, C4]],
            labels={"avg_years_schooling": "Avg Years of Schooling", "Entity": ""},
            text=df_compare["avg_years_schooling"].round(1)
        )
        fig_bar.update_traces(textposition="outside", textfont=dict(color=WHITE, size=11))
        fig_bar.update_layout(**chart_layout(height=350))
        fig_bar.update_coloraxes(showscale=False)
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("Select countries from the sidebar to compare.")
    st.markdown("</div>", unsafe_allow_html=True)

with col_scatter:
    st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
    st.markdown(f"<div class='chart-title'>{selected_driver_label} vs. Schooling ({selected_year})</div><div class='chart-sub'>Each dot = one country · regression line shown</div>", unsafe_allow_html=True)

    fig_scatter = px.scatter(
        df_year.dropna(subset=[selected_driver]),
        x=selected_driver, y="avg_years_schooling",
        hover_name="Entity",
        trendline="ols",
        color_discrete_sequence=[C2],
        labels={selected_driver: selected_driver_label, "avg_years_schooling": "Avg Years of Schooling"}
    )
    fig_scatter.update_traces(marker=dict(size=7, opacity=0.7, line=dict(width=0.5, color="rgba(255,255,255,0.3)")))
    fig_scatter.data[1].line.color = C3
    fig_scatter.data[1].line.width = 2.5
    fig_scatter.update_layout(**chart_layout(height=350))
    st.plotly_chart(fig_scatter, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ── ROW 3: MULTI-LINE TRENDS + TOP/BOTTOM 10 ─────────────────
st.markdown(f"<div class='section-header'>📊 Regression Drivers Over Time & Rankings</div>", unsafe_allow_html=True)

col_multi, col_rank = st.columns([1.3, 1])

with col_multi:
    st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
    st.markdown(f"<div class='chart-title'>Key Drivers Trend (Selected Countries)</div><div class='chart-sub'>Track how {selected_driver_label} changes over time</div>", unsafe_allow_html=True)

    if selected_countries:
        df_mc = df[df["Entity"].isin(selected_countries)].sort_values("Year")
        fig_multi = px.line(
            df_mc, x="Year", y=selected_driver, color="Entity",
            labels={selected_driver: selected_driver_label},
            color_discrete_sequence=PALETTE,
            markers=False
        )
        fig_multi.update_traces(line=dict(width=2))
        fig_multi.add_vline(x=selected_year, line_dash="dash", line_color="rgba(255,255,255,0.3)", line_width=1)
        fig_multi.update_layout(**chart_layout(height=320))
        st.plotly_chart(fig_multi, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_rank:
    st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
    st.markdown(f"<div class='chart-title'>Top 5 & Bottom 5 Countries ({selected_year})</div><div class='chart-sub'>By average years of schooling</div>", unsafe_allow_html=True)

    top5    = df_year.nlargest(5, "avg_years_schooling")[["Entity","avg_years_schooling"]]
    bottom5 = df_year.nsmallest(5, "avg_years_schooling")[["Entity","avg_years_schooling"]]
    combined = pd.concat([top5, bottom5])
    combined["Group"] = ["🏆 Top"] * 5 + ["⚠️ Bottom"] * 5

    fig_rank = px.bar(
        combined, x="avg_years_schooling", y="Entity", color="Group",
        orientation="h",
        color_discrete_map={"🏆 Top": C3, "⚠️ Bottom": C5},
        labels={"avg_years_schooling": "Avg Years", "Entity": ""},
        text=combined["avg_years_schooling"].round(1)
    )
    fig_rank.update_traces(textposition="outside", textfont=dict(color=WHITE, size=10))
    fig_rank.update_layout(**chart_layout(height=320))
    st.plotly_chart(fig_rank, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ── REGRESSION SUMMARY INSIGHT BOX ────────────────────────────
st.markdown(f"<div class='section-header'>🔬 Regression Findings</div>", unsafe_allow_html=True)

col_i1, col_i2, col_i3, col_i4 = st.columns(4)

drivers_info = [
    (C3, "🥇 Log GDP per Capita", "β = +1.64 ***", "Strongest driver. Wealthier nations invest more in education infrastructure and teacher quality."),
    (C2, "🥈 Internet Usage", "β = +0.93 ***", "Digital access enables remote learning, e-resources, and broader educational participation."),
    (C4, "🥉 Female/Male Labor Ratio", "β = +0.41 ***", "Gender equity in the workforce reflects and reinforces girls' access to schooling."),
    (C5, "4️⃣ Gov. Education Spending", "β = +0.12 ***", "Public investment in education improves access and quality, though effect is smaller when controlled."),
]

for col, (color, title, beta, desc) in zip([col_i1, col_i2, col_i3, col_i4], drivers_info):
    with col:
        st.markdown(f"""
        <div style='background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.1);
                    border-top:3px solid {color}; border-radius:12px; padding:18px; height:100%;'>
            <div style='font-family:Syne; font-size:13px; font-weight:700; color:{WHITE}; margin-bottom:6px;'>{title}</div>
            <div style='font-size:18px; font-weight:800; color:{color}; font-family:Syne; margin-bottom:10px;'>{beta}</div>
            <div style='font-size:12px; color:rgba(255,255,255,0.55); line-height:1.6;'>{desc}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown(f"""
<div class='insight-box' style='margin-top:20px;'>
    📌 <strong>Model Summary:</strong> The OLS regression model achieved an R² of <strong>0.647</strong>, 
    meaning the four drivers explain <strong>64.7%</strong> of the variation in average years of schooling 
    across 191 countries (2000–2023). All variables are statistically significant at the 
    <strong>p &lt; 0.001</strong> level. The Robust Regression (RLM) confirmed consistent results, 
    validating findings against outliers. <strong>GDP per capita</strong> is the single most powerful 
    predictor of education outcomes globally.
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
