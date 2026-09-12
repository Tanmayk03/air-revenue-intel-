import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit.components.v1 as components
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Airline Revenue Intelligence",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- BESPOKE MOBILE-RESPONSIVE ENTERPRISE CSS THEME ---
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">

<style>
    /* Global Page Styling */
    .stApp {
        background-color: #F8FAFC;
        color: #0F172A;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Hide Default Streamlit Chrome */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background: #FFFFFF !important;
        border-right: 1px solid #E2E8F0 !important;
        box-shadow: 2px 0 15px rgba(0, 0, 0, 0.02);
    }
    
    .sidebar-brand {
        padding: 16px 12px;
        border-bottom: 1px solid #E2E8F0;
        margin-bottom: 20px;
    }
    
    .brand-title {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 16px;
        font-weight: 800;
        color: #1E293B;
        letter-spacing: -0.3px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .brand-badge {
        background: #EFF6FF;
        border: 1px solid #BFDBFE;
        color: #2563EB;
        font-size: 10px;
        font-weight: 700;
        padding: 2px 6px;
        border-radius: 4px;
    }

    /* Top Executive Navigation Bar */
    .top-navbar {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 14px 24px;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
    }

    .nav-left {
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .nav-title {
        font-size: 18px;
        font-weight: 800;
        color: #0F172A;
        letter-spacing: -0.4px;
    }

    .nav-right {
        display: flex;
        align-items: center;
        gap: 16px;
    }

    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: #ECFDF5;
        border: 1px solid #A7F3D0;
        color: #047857;
        font-size: 12px;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 20px;
    }

    .status-dot {
        width: 6px;
        height: 6px;
        background-color: #10B981;
        border-radius: 50%;
    }

    .model-badge {
        background: #F1F5F9;
        border: 1px solid #CBD5E1;
        color: #475569;
        font-size: 11px;
        font-weight: 600;
        padding: 4px 10px;
        border-radius: 6px;
    }

    /* Executive KPI Cards */
    .kpi-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 18px 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.03);
        transition: all 0.2s ease;
        position: relative;
    }

    .kpi-card:hover {
        border-color: #CBD5E1;
        box-shadow: 0 4px 12px rgba(0,0,0,0.06);
    }

    .kpi-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;
    }

    .kpi-label {
        font-size: 12px;
        font-weight: 600;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .kpi-pill {
        font-size: 11px;
        font-weight: 700;
        padding: 2px 8px;
        border-radius: 12px;
    }

    .kpi-value {
        font-size: 28px;
        font-weight: 800;
        color: #0F172A;
        letter-spacing: -0.5px;
    }

    .kpi-subtext {
        font-size: 12px;
        color: #94A3B8;
        margin-top: 4px;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: #F1F5F9;
        padding: 5px;
        border-radius: 10px;
        border: 1px solid #E2E8F0;
    }

    .stTabs [data-baseweb="tab"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-weight: 600;
        font-size: 13px;
        color: #64748B;
        border-radius: 7px;
        padding: 8px 16px;
        border: none !important;
    }

    .stTabs [aria-selected="true"] {
        background: #FFFFFF !important;
        color: #1E293B !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }

    /* Section Cards */
    .content-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.03);
    }

    .card-title {
        font-size: 15px;
        font-weight: 700;
        color: #0F172A;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    /* --- MOBILE RESPONSIVE MEDIA QUERIES --- */
    @media (max-width: 768px) {
        /* Sidebar Menu Mobile View Optimization */
        section[data-testid="stSidebar"] {
            width: 85vw !important;
        }

        .sidebar-brand {
            padding: 12px 8px;
            margin-bottom: 12px;
        }

        .brand-title {
            font-size: 14px;
        }

        .top-navbar {
            flex-direction: column;
            align-items: flex-start;
            gap: 12px;
            padding: 14px 16px;
        }

        .nav-title {
            font-size: 15px;
        }

        .nav-right {
            width: 100%;
            justify-content: space-between;
        }

        .kpi-card {
            padding: 14px 14px;
            margin-bottom: 12px;
        }

        .kpi-value {
            font-size: 22px;
        }

        .stTabs [data-baseweb="tab-list"] {
            overflow-x: auto;
            flex-wrap: nowrap;
        }

        .stTabs [data-baseweb="tab"] {
            font-size: 12px;
            padding: 6px 12px;
            white-space: nowrap;
        }
    }
</style>
""", unsafe_allow_html=True)

# --- TOP EXECUTIVE NAVIGATION BAR ---
st.markdown("""
<div class="top-navbar">
    <div class="nav-left">
        <div class="nav-title">Airline Revenue & Pricing Intelligence</div>
        <span class="brand-badge">v3.2 PROD</span>
    </div>
    <div class="nav-right">
        <div class="status-pill"><span class="status-dot"></span> 300,153 FLIGHTS AUDITED</div>
        <div class="model-badge">ML BENCHMARK R² 91.29%</div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- HIGH-DEFINITION MOBILE-RESPONSIVE AIRPLANE HUD HERO ---
def render_3d_hero_header():
    airplane_hud_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {
                margin: 0;
                overflow: hidden;
                background: transparent;
                font-family: 'Plus Jakarta Sans', sans-serif;
            }
            #hero-container {
                width: 100%;
                min-height: 220px;
                position: relative;
                border-radius: 14px;
                overflow: hidden;
                background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
                border: 1px solid #334155;
                box-shadow: 0 4px 20px rgba(15, 23, 42, 0.15);
                display: flex;
                align-items: center;
                justify-content: space-between;
                padding: 20px 24px;
                box-sizing: border-box;
            }
            .hero-left {
                max-width: 58%;
                z-index: 10;
            }
            .hero-tag {
                display: inline-block;
                background: rgba(56, 189, 248, 0.15);
                border: 1px solid #38BDF8;
                color: #38BDF8;
                font-size: 10px;
                font-weight: 700;
                padding: 3px 10px;
                border-radius: 4px;
                letter-spacing: 1.5px;
                margin-bottom: 8px;
                text-transform: uppercase;
            }
            .hero-title {
                color: #FFFFFF;
                font-size: 22px;
                font-weight: 800;
                letter-spacing: -0.3px;
                margin: 0;
            }
            .hero-sub {
                color: #94A3B8;
                font-size: 13px;
                margin-top: 6px;
            }
            
            /* Realistic 3D Flight Telemetry Graphic */
            .flight-graphic-container {
                position: relative;
                width: 280px;
                height: 170px;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            
            .radar-ring {
                position: absolute;
                width: 140px;
                height: 140px;
                border: 1px stroke rgba(56, 189, 248, 0.2);
                border-radius: 50%;
                border-top: 2px solid #38BDF8;
                animation: spin 8s linear infinite;
            }
            
            @keyframes spin {
                100% { transform: rotate(360deg); }
            }

            .airliner-svg {
                width: 200px;
                height: 130px;
                filter: drop-shadow(0 10px 15px rgba(0,0,0,0.5));
                animation: floatFlight 3s ease-in-out infinite alternate;
                transform: rotate(-5deg);
            }

            @keyframes floatFlight {
                0% { transform: translateY(-5px) rotate(-4deg); }
                100% { transform: translateY(8px) rotate(-7deg); }
            }

            .badge-dot {
                display: inline-block;
                width: 6px;
                height: 6px;
                background-color: #34D399;
                border-radius: 50%;
            }
            .telemetry-overlay-box {
                position: absolute;
                bottom: 8px;
                right: 12px;
                background: rgba(15, 23, 42, 0.85);
                border: 1px solid rgba(255, 255, 255, 0.1);
                padding: 4px 8px;
                border-radius: 4px;
                color: #38BDF8;
                font-family: monospace;
                font-size: 10px;
            }

            /* Mobile Responsive Layout for Header */
            @media (max-width: 768px) {
                #hero-container {
                    flex-direction: column;
                    align-items: flex-start;
                    padding: 16px;
                }
                .hero-left {
                    max-width: 100%;
                    margin-bottom: 12px;
                }
                .hero-title {
                    font-size: 17px;
                }
                .hero-sub {
                    font-size: 11px;
                }
                .flight-graphic-container {
                    width: 100%;
                    height: 130px;
                }
                .airliner-svg {
                    width: 160px;
                    height: 100px;
                }
            }
        </style>
    </head>
    <body>
        <div id="hero-container">
            <div class="hero-left">
                <div class="hero-tag">COMMERCIAL FLIGHT TELEMETRY HUD</div>
                <h1 class="hero-title">Airline Revenue Leakage & Pricing Intelligence</h1>
                <div class="hero-sub">ML Expected Fare Benchmark | Exposure & Dynamic Yield Analytics</div>
            </div>
            
            <div class="flight-graphic-container">
                <div class="radar-ring"></div>
                
                <svg class="airliner-svg" viewBox="0 0 512 512" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M40 320 C 120 300, 200 280, 300 260" stroke="#38BDF8" stroke-width="3" stroke-dasharray="6 6" opacity="0.6"/>
                    
                    <g transform="translate(60, 80) scale(0.75)">
                        <path d="M 240 180 L 100 320 L 130 335 L 260 210 Z" fill="#2563EB"/>
                        <path d="M 260 170 L 400 320 L 370 335 L 240 200 Z" fill="#1D4ED8"/>
                        
                        <path d="M 100 320 L 95 300 L 115 325 Z" fill="#38BDF8"/>
                        <path d="M 400 320 L 405 300 L 385 325 Z" fill="#38BDF8"/>
                        
                        <path d="M 250 40 C 275 40, 280 120, 280 340 C 280 380, 250 410, 250 410 C 250 410, 220 380, 220 340 C 220 120, 225 40, 250 40 Z" fill="#F8FAFC"/>
                        
                        <path d="M 250 40 C 265 40, 275 70, 275 100 L 225 100 C 225 70, 235 40, 250 40 Z" fill="#E2E8F0"/>
                        
                        <path d="M 235 85 C 240 80, 260 80, 265 85 L 270 95 L 230 95 Z" fill="#0F172A"/>
                        
                        <rect x="170" y="240" width="22" height="55" rx="10" fill="#334155"/>
                        <rect x="308" y="240" width="22" height="55" rx="10" fill="#334155"/>
                        <circle cx="181" cy="245" r="9" fill="#38BDF8"/>
                        <circle cx="319" cy="245" r="9" fill="#38BDF8"/>
                        
                        <path d="M 250 360 L 160 410 L 170 425 L 250 385 Z" fill="#94A3B8"/>
                        <path d="M 250 360 L 340 410 L 330 425 L 250 385 Z" fill="#64748B"/>
                        
                        <path d="M 250 310 L 250 420 L 244 420 L 244 310 Z" fill="#1E3A8A"/>
                        <path d="M 250 330 L 250 420 L 256 420 L 250 330 Z" fill="#2563EB"/>
                    </g>
                </svg>

                <div class="telemetry-overlay-box">
                    <div><span class="badge-dot"></span> 300,153 FLIGHTS</div>
                    <div style="color: #94A3B8; margin-top: 2px;">MODEL R²: 91.29%</div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    components.html(airplane_hud_html, height=230)

# Render Hero Header
render_3d_hero_header()

# --- DATA LOADING WITH CACHING ---
@st.cache_data
def load_data():
    file_path = "data/processed/airline_revenue_processed.csv"
    if not os.path.exists(file_path):
        file_path = "../data/processed/airline_revenue_processed.csv"
    df = pd.read_csv(file_path)
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading dataset. Details: {e}")
    st.stop()

# --- SIDEBAR CONTROLS ---
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="brand-title">Pricing Intelligence <span class="brand-badge">PRO</span></div>
        <div style="font-size: 11px; color: #64748B; margin-top: 4px;">Executive Analytics Suite</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='font-size: 11px; font-weight: 700; color: #475569; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 10px;'>FILTER PARAMETERS</div>", unsafe_allow_html=True)
    
    # Cabin Class Filter
    class_options = ["All"] + list(df['class'].unique())
    selected_class = st.selectbox("Cabin Class", class_options, index=1 if "Economy" in class_options else 0)
    
    # Airline Filter
    airline_options = ["All"] + list(df['airline'].unique())
    selected_airlines = st.multiselect("Select Airlines", airline_options, default=["All"])
    
    # Booking Window Filter
    days_options = ["All"] + list(df['days_bucket'].dropna().unique())
    selected_days = st.multiselect("Booking Window", days_options, default=["All"])
    
    # Route Filter
    route_options = ["All"] + sorted(list(df['route'].unique()))
    selected_route_filter = st.selectbox("Specific Route", route_options, index=0)

    st.markdown("---")
    st.markdown("""
    <div style='background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 12px;'>
        <div style='font-size: 11px; font-weight: 700; color: #1E293B;'>KEY FINDING (H1)</div>
        <div style='font-size: 11px; color: #64748B; margin-top: 4px; line-height: 1.4;'>Long-haul flights in advance windows (31+ Days) are underpriced by 24-28% vs ML benchmark.</div>
    </div>
    """, unsafe_allow_html=True)

# --- DATA FILTERING ---
filtered_df = df.copy()

if selected_class != "All":
    filtered_df = filtered_df[filtered_df['class'] == selected_class]

if selected_airlines and "All" not in selected_airlines:
    filtered_df = filtered_df[filtered_df['airline'].isin(selected_airlines)]

if selected_days and "All" not in selected_days:
    filtered_df = filtered_df[filtered_df['days_bucket'].isin(selected_days)]

if selected_route_filter != "All":
    filtered_df = filtered_df[filtered_df['route'] == selected_route_filter]

# --- EXECUTIVE KPI CARDS ---
total_flights = len(filtered_df)
avg_actual = filtered_df['price'].mean() if total_flights > 0 else 0
avg_expected = filtered_df['expected_fare'].mean() if total_flights > 0 else 0
overall_leakage = ((avg_actual - avg_expected) / avg_expected * 100) if avg_expected > 0 else 0

underpriced = filtered_df[filtered_df['expected_fare'] > filtered_df['price']]
total_exposure_crs = (underpriced['expected_fare'] - underpriced['price']).sum() / 10000000

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-header">
            <span class="kpi-label">Audited Flights</span>
            <span class="kpi-pill" style="background: #F1F5F9; color: #475569;">100% Volume</span>
        </div>
        <div class="kpi-value">{total_flights:,}</div>
        <div class="kpi-subtext">Evaluated Domestic Segment</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-header">
            <span class="kpi-label">Avg Realized Fare</span>
            <span class="kpi-pill" style="background: #EFF6FF; color: #2563EB;">Actual</span>
        </div>
        <div class="kpi-value">₹{avg_actual:,.0f}</div>
        <div class="kpi-subtext">Realized Ticket Average</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    leak_bg = "#FEF2F2" if overall_leakage < 0 else "#ECFDF5"
    leak_fg = "#DC2626" if overall_leakage < 0 else "#059669"
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-header">
            <span class="kpi-label">Benchmark & Leakage</span>
            <span class="kpi-pill" style="background: {leak_bg}; color: {leak_fg};">{overall_leakage:+.2f}%</span>
        </div>
        <div class="kpi-value">₹{avg_expected:,.0f}</div>
        <div class="kpi-subtext">ML Benchmark Baseline</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-header">
            <span class="kpi-label">Revenue Opportunity</span>
            <span class="kpi-pill" style="background: #ECFDF5; color: #059669;">Target Upside</span>
        </div>
        <div class="kpi-value" style="color: #059669;">₹{total_exposure_crs:.2f} Cr</div>
        <div class="kpi-subtext">Uncaptured Exposure</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- PLOTLY DESIGNER STYLE ---
def style_plotly(fig, height=360):
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(family="Plus Jakarta Sans, sans-serif", color="#475569", size=12),
        margin=dict(l=15, r=15, t=30, b=15),
        height=height,
        xaxis=dict(gridcolor="#F1F5F9", zerolinecolor="#E2E8F0"),
        yaxis=dict(gridcolor="#F1F5F9", zerolinecolor="#E2E8F0"),
        legend=dict(bgcolor="#FFFFFF", bordercolor="#E2E8F0", borderwidth=1)
    )
    return fig

# --- NAVIGATION TABS ---
tab1, tab2, tab3, tab4 = st.tabs([
    "Executive Summary", 
    "Route Yield Explorer", 
    "Competitor Benchmark", 
    "Scenario Simulator"
])

# --- TAB 1: EXECUTIVE SUMMARY ---
with tab1:
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown('<div class="card-title">Top Exposure Routes <span>(₹ Lakhs)</span></div>', unsafe_allow_html=True)
        route_exp = filtered_df.groupby('route').apply(
            lambda g: (g[g['expected_fare'] > g['price']]['expected_fare'] - g[g['expected_fare'] > g['price']]['price']).sum() / 100000
        ).reset_index(name='exposure_lakhs').sort_values(by='exposure_lakhs', ascending=False).head(10)
        
        fig1 = px.bar(
            route_exp, x='exposure_lakhs', y='route', orientation='h',
            labels={'exposure_lakhs': 'Opportunity (₹ Lakhs)', 'route': 'Route'},
            color='exposure_lakhs',
            color_continuous_scale=['#93C5FD', '#2563EB', '#1E3A8A']
        )
        fig1.update_layout(yaxis={'categoryorder':'total ascending'}, coloraxis_showscale=False)
        fig1 = style_plotly(fig1)
        st.plotly_chart(fig1, use_container_width=True)

    with col_b:
        st.markdown('<div class="card-title">Leakage Score by Booking Window <span>(%)</span></div>', unsafe_allow_html=True)
        bucket_summary = filtered_df.groupby('days_bucket').agg(
            avg_actual=('price', 'mean'),
            avg_expected=('expected_fare', 'mean')
        ).reset_index()
        bucket_summary['leakage_pct'] = ((bucket_summary['avg_actual'] - bucket_summary['avg_expected']) / bucket_summary['avg_expected']) * 100
        
        fig2 = px.bar(
            bucket_summary, x='days_bucket', y='leakage_pct',
            labels={'days_bucket': 'Booking Window', 'leakage_pct': 'Leakage Score (%)'},
            color='leakage_pct',
            color_continuous_scale=['#EF4444', '#F59E0B', '#10B981']
        )
        fig2 = style_plotly(fig2)
        st.plotly_chart(fig2, use_container_width=True)

    # Clean Styled Executive Data Table
    st.markdown('<div class="card-title">High-Exposure Route Detail Matrix</div>', unsafe_allow_html=True)
    table_df = filtered_df.groupby(['route', 'days_bucket']).agg(
        Flights=('price', 'count'),
        Avg_Actual_Fare=('price', 'mean'),
        Avg_Expected_Fare=('expected_fare', 'mean')
    ).reset_index()
    table_df['Leakage_Score_%'] = ((table_df['Avg_Actual_Fare'] - table_df['Avg_Expected_Fare']) / table_df['Avg_Expected_Fare']) * 100
    table_df['Avg_Actual_Fare'] = table_df['Avg_Actual_Fare'].map('₹{:,.0f}'.format)
    table_df['Avg_Expected_Fare'] = table_df['Avg_Expected_Fare'].map('₹{:,.0f}'.format)
    table_df['Leakage_Score_%'] = table_df['Leakage_Score_%'].map('{:+.2f}%'.format)
    
    st.dataframe(table_df.head(15), use_container_width=True, hide_index=True)

# --- TAB 2: ROUTE YIELD EXPLORER ---
with tab2:
    st.markdown('<div class="card-title">Days to Departure Yield Progression Curve</div>', unsafe_allow_html=True)
    
    available_routes = sorted(filtered_df['route'].unique())
    selected_route = st.selectbox("Inspect Specific Route", available_routes if available_routes else sorted(df['route'].unique()))
    
    route_df = filtered_df[filtered_df['route'] == selected_route] if not filtered_df.empty else df[df['route'] == selected_route]
    
    curve_df = route_df.groupby('days_left').agg(
        Actual_Price=('price', 'mean'),
        Expected_Benchmark=('expected_fare', 'mean')
    ).reset_index()
    
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(
        x=curve_df['days_left'], y=curve_df['Actual_Price'],
        mode='lines+markers', name='Actual Realized Fare',
        line=dict(color='#2563EB', width=3),
        marker=dict(size=6, color='#2563EB')
    ))
    fig3.add_trace(go.Scatter(
        x=curve_df['days_left'], y=curve_df['Expected_Benchmark'],
        mode='lines+markers', name='ML Benchmark Baseline',
        line=dict(color='#DC2626', width=3, dash='dash'),
        marker=dict(size=6, color='#DC2626')
    ))
    
    fig3.update_layout(
        title=f"Fare Curve for {selected_route} (Days to Departure)",
        xaxis_title="Days Left to Departure (1 = Departure Day)",
        yaxis_title="Average Fare (INR)",
        xaxis=dict(autorange="reversed")
    )
    fig3 = style_plotly(fig3, height=420)
    st.plotly_chart(fig3, use_container_width=True)

# --- TAB 3: COMPETITOR BENCHMARK ---
with tab3:
    st.markdown('<div class="card-title">Airline Benchmark Comparison across Windows</div>', unsafe_allow_html=True)
    
    comp_df = filtered_df.groupby(['airline', 'days_bucket'])['price'].mean().reset_index()
    
    fig4 = px.bar(
        comp_df, x='days_bucket', y='price', color='airline', barmode='group',
        labels={'price': 'Average Fare (INR)', 'days_bucket': 'Booking Window', 'airline': 'Airline'},
        color_discrete_sequence=['#2563EB', '#D97706', '#10B981', '#0EA5E9', '#7C3AED', '#DB2777']
    )
    fig4 = style_plotly(fig4, height=420)
    st.plotly_chart(fig4, use_container_width=True)

# --- TAB 4: WHAT-IF SCENARIO SIMULATOR ---
with tab4:
    st.markdown('<div class="card-title">Dynamic Pricing What-If Impact Simulator</div>', unsafe_allow_html=True)
    st.markdown("Simulate the financial upside of stepping up advance booking price floors on underpriced flights.")
    
    s_col1, s_col2 = st.columns([1, 1])
    
    with s_col1:
        adjustment_pct = st.slider(
            "Price Floor Adjustment (%) for Underpriced Segments", 
            min_value=0.0, max_value=30.0, value=10.0, step=1.0
        )
        
        underpriced_filtered = filtered_df[filtered_df['expected_fare'] > filtered_df['price']].copy()
        current_rev = underpriced_filtered['price'].sum()
        adjusted_rev = (underpriced_filtered['price'] * (1 + adjustment_pct/100)).sum()
        rev_gain_lakhs = (adjusted_rev - current_rev) / 100000
        rev_gain_crs = rev_gain_lakhs / 100
        
        st.markdown(f"""
        <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-top: 3px solid #10B981; border-radius: 12px; padding: 22px; text-align: center; margin-top: 15px; box-shadow: 0 2px 8px rgba(0,0,0,0.04);">
            <div style="font-size: 11px; color: #64748B; text-transform: uppercase; letter-spacing: 0.5px; font-weight: 600;">SIMULATED REVENUE UPSIDE</div>
            <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 34px; font-weight: 800; color: #059669; margin: 8px 0;">
                +₹{rev_gain_crs:.2f} Cr
            </div>
            <div style="font-size: 12px; color: #2563EB;">(₹{rev_gain_lakhs:,.2f} Lakhs gain at +{adjustment_pct}% price floor)</div>
        </div>
        """, unsafe_allow_html=True)
    
    with s_col2:
        sim_summary = pd.DataFrame({
            'Scenario': ['Current Revenue', 'Simulated Revenue'],
            'Revenue_Cr': [current_rev / 10000000, adjusted_rev / 10000000]
        })
        
        fig5 = px.bar(
            sim_summary, x='Scenario', y='Revenue_Cr', color='Scenario',
            color_discrete_map={'Current Revenue': '#2563EB', 'Simulated Revenue': '#10B981'},
            labels={'Revenue_Cr': 'Revenue (₹ Crores)'}
        )
        fig5 = style_plotly(fig5, height=300)
        st.plotly_chart(fig5, use_container_width=True)

st.markdown("---")
st.markdown("<div style='text-align: center; color: #94A3B8; font-size: 11px; font-family: monospace;'>AIRLINE REVENUE LEAKAGE & PRICING INTELLIGENCE PLATFORM</div>", unsafe_allow_html=True)
