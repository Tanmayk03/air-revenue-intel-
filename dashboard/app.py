import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Airline Revenue & Pricing Intelligence",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ROYAL SAPPHIRE & CHAMPAGNE GOLD COLOR PALETTE ---
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap" rel="stylesheet">

<style>
    /* Global Page Dark Theme - Deep Midnight Navy */
    .stApp {
        background-color: #060B19;
        color: #F8FAFC;
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Default Streamlit Chrome */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background: #0A1128 !important;
        border-right: 1px solid #1E2942 !important;
        box-shadow: 4px 0 20px rgba(0, 0, 0, 0.5);
    }
    
    .sidebar-brand-card {
        background: linear-gradient(180deg, #101A36 0%, #060B19 100%);
        border: 1px solid #2B3A67;
        border-top: 2px solid #F59E0B;
        border-radius: 12px;
        padding: 18px 14px;
        text-align: center;
        margin-bottom: 22px;
    }
    
    .sidebar-brand-title {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 15px;
        font-weight: 800;
        color: #FBBF24;
        letter-spacing: 1px;
        text-transform: uppercase;
    }

    .sidebar-brand-sub {
        font-size: 10px;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-top: 4px;
    }

    /* Enterprise Hero Banner - Royal Sapphire & Gold Accent */
    .hero-banner {
        background: linear-gradient(135deg, #101A36 0%, #162244 50%, #0A1128 100%);
        border: 1px solid #2B3A67;
        border-left: 4px solid #F59E0B;
        border-radius: 16px;
        padding: 24px 30px;
        margin-bottom: 24px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
        position: relative;
        overflow: hidden;
    }

    .hero-banner::after {
        content: '';
        position: absolute;
        top: -50%;
        right: -10%;
        width: 300px;
        height: 300px;
        background: radial-gradient(circle, rgba(245, 158, 11, 0.08) 0%, transparent 70%);
        pointer-events: none;
    }

    .hero-title-tag {
        display: inline-block;
        background: rgba(245, 158, 11, 0.12);
        border: 1px solid #D97706;
        color: #FBBF24;
        font-size: 11px;
        font-weight: 700;
        padding: 4px 12px;
        border-radius: 6px;
        letter-spacing: 1.5px;
        margin-bottom: 8px;
        text-transform: uppercase;
    }

    .hero-main-title {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 24px;
        font-weight: 800;
        color: #F8FAFC;
        margin: 0;
        letter-spacing: 0.5px;
    }

    .hero-subtitle {
        color: #94A3B8;
        font-size: 13px;
        margin-top: 6px;
    }

    .hero-status-pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(37, 99, 235, 0.2);
        border: 1px solid #2563EB;
        color: #60A5FA;
        font-size: 12px;
        font-weight: 700;
        padding: 6px 14px;
        border-radius: 8px;
    }

    .status-pulse {
        width: 8px;
        height: 8px;
        background-color: #60A5FA;
        border-radius: 50%;
    }

    /* Executive Telemetry Metric Cards - Sapphire & Gold */
    .telemetry-card {
        background: #101A36;
        border: 1px solid #2B3A67;
        border-radius: 14px;
        padding: 18px 16px;
        position: relative;
        overflow: hidden;
        transition: all 0.2s ease-in-out;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }
    
    .telemetry-card:hover {
        border-color: #F59E0B;
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(245, 158, 11, 0.15);
    }

    .telemetry-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 10px;
    }

    .telemetry-title {
        font-family: 'Inter', sans-serif;
        font-size: 11px;
        color: #94A3B8;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }

    .telemetry-tag {
        font-size: 10px;
        font-weight: 700;
        padding: 2px 8px;
        border-radius: 4px;
        letter-spacing: 0.5px;
        background: #1A284D;
        color: #94A3B8;
    }

    .telemetry-value {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 26px;
        font-weight: 800;
        color: #F8FAFC;
        margin-bottom: 6px;
    }

    .telemetry-footer {
        font-size: 11px;
        color: #94A3B8;
        display: flex;
        justify-content: space-between;
    }

    .progress-bar-bg {
        width: 100%;
        height: 4px;
        background: #1A284D;
        border-radius: 2px;
        margin-top: 10px;
        overflow: hidden;
    }
    
    .progress-bar-fill {
        height: 100%;
        border-radius: 2px;
    }

    /* Tabs Styling - Sapphire Blue & Gold Active */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: #0A1128;
        padding: 6px;
        border-radius: 12px;
        border: 1px solid #1E2942;
    }

    .stTabs [data-baseweb="tab"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-weight: 600;
        font-size: 14px;
        color: #94A3B8;
        border-radius: 8px;
        padding: 10px 20px;
        border: none !important;
        transition: all 0.2s ease;
    }

    .stTabs [aria-selected="true"] {
        background: #162244 !important;
        color: #FBBF24 !important;
        border: 1px solid #D97706 !important;
        box-shadow: 0 4px 12px rgba(245, 158, 11, 0.15);
    }

    /* Section Headers */
    .section-header {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 17px;
        font-weight: 700;
        color: #F8FAFC;
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 16px;
    }

    .section-badge {
        background: rgba(245, 158, 11, 0.12);
        border: 1px solid #D97706;
        color: #FBBF24;
        font-size: 10px;
        font-weight: 700;
        padding: 3px 9px;
        border-radius: 4px;
        letter-spacing: 0.5px;
    }

    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    ::-webkit-scrollbar-track {
        background: #060B19;
    }
    ::-webkit-scrollbar-thumb {
        background: #2B3A67;
        border-radius: 3px;
    }
</style>
""", unsafe_allow_html=True)

# --- ENTERPRISE HERO HEADER ---
st.markdown("""
<div class="hero-banner">
    <div>
        <div class="hero-title-tag">EXECUTIVE PRICING INTELLIGENCE ENGINE</div>
        <h1 class="hero-main-title">Airline Revenue Leakage & Pricing Benchmark Console</h1>
        <div class="hero-subtitle">ML Expected Fare Modeling | Segment Exposure Analytics | Dynamic Yield Optimization</div>
    </div>
    <div style="text-align: right;">
        <div class="hero-status-pill"><span class="status-pulse"></span>SYSTEM ONLINE</div>
        <div style="color: #94A3B8; font-size: 11px; font-weight: 600; margin-top: 8px;">300,153 FLIGHTS | MODEL R² 91.29%</div>
    </div>
</div>
""", unsafe_allow_html=True)

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
    st.error(f"Error loading dataset. Please run the notebook export step first. Details: {e}")
    st.stop()

# --- SIDEBAR FILTERS ---
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand-card">
        <div class="sidebar-brand-title">PRICING CONTROL</div>
        <div class="sidebar-brand-sub">ROYAL SAPPHIRE SUITE</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='color: #F8FAFC; font-weight: 700; font-size: 11px; letter-spacing: 1px; margin-bottom: 12px; text-transform: uppercase;'>FILTER PARAMETERS</div>", unsafe_allow_html=True)
    
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
    <div style='background: #101A36; border: 1px solid #2B3A67; border-radius: 10px; padding: 14px;'>
        <div style='color: #FBBF24; font-size: 11px; font-weight: 700; letter-spacing: 0.5px;'>EXECUTIVE NOTE</div>
        <div style='color: #94A3B8; font-size: 11px; margin-top: 6px; line-height: 1.4;'>Long-haul flights in advance windows (31+ Days) exhibit ~24-28% price variance vs expected market benchmarks.</div>
    </div>
    """, unsafe_allow_html=True)

# --- DATA FILTERING LOGIC ---
filtered_df = df.copy()

if selected_class != "All":
    filtered_df = filtered_df[filtered_df['class'] == selected_class]

if selected_airlines and "All" not in selected_airlines:
    filtered_df = filtered_df[filtered_df['airline'].isin(selected_airlines)]

if selected_days and "All" not in selected_days:
    filtered_df = filtered_df[filtered_df['days_bucket'].isin(selected_days)]

if selected_route_filter != "All":
    filtered_df = filtered_df[filtered_df['route'] == selected_route_filter]

# --- EXECUTIVE TELEMETRY WIDGETS ---
total_flights = len(filtered_df)
avg_actual = filtered_df['price'].mean() if total_flights > 0 else 0
avg_expected = filtered_df['expected_fare'].mean() if total_flights > 0 else 0
overall_leakage = ((avg_actual - avg_expected) / avg_expected * 100) if avg_expected > 0 else 0

underpriced = filtered_df[filtered_df['expected_fare'] > filtered_df['price']]
total_exposure_crs = (underpriced['expected_fare'] - underpriced['price']).sum() / 10000000

k1, k2, k3, k4, k5 = st.columns(5)

with k1:
    st.markdown(f"""
    <div class="telemetry-card">
        <div class="telemetry-header">
            <span class="telemetry-title">TOTAL FLIGHTS</span>
            <span class="telemetry-tag">COVERAGE</span>
        </div>
        <div class="telemetry-value">{total_flights:,}</div>
        <div class="telemetry-footer"><span>Evaluated Segment</span><span>100%</span></div>
        <div class="progress-bar-bg"><div class="progress-bar-fill" style="width: 100%; background: #2563EB;"></div></div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="telemetry-card">
        <div class="telemetry-header">
            <span class="telemetry-title">REALIZED FARE</span>
            <span class="telemetry-tag">ACTUAL</span>
        </div>
        <div class="telemetry-value">₹{avg_actual:,.0f}</div>
        <div class="telemetry-footer"><span>Mean Ticket Price</span><span>INR</span></div>
        <div class="progress-bar-bg"><div class="progress-bar-fill" style="width: 75%; background: #60A5FA;"></div></div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="telemetry-card">
        <div class="telemetry-header">
            <span class="telemetry-title">EXPECTED FARE</span>
            <span class="telemetry-tag" style="background: rgba(245, 158, 11, 0.2); color: #FBBF24;">ML MODEL</span>
        </div>
        <div class="telemetry-value" style="color: #FBBF24;">₹{avg_expected:,.0f}</div>
        <div class="telemetry-footer"><span>Benchmark Baseline</span><span>R² 91%</span></div>
        <div class="progress-bar-bg"><div class="progress-bar-fill" style="width: 85%; background: #F59E0B;"></div></div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    status_bg = "rgba(244, 63, 94, 0.2)" if overall_leakage < 0 else "rgba(16, 185, 129, 0.2)"
    status_color = "#FB7185" if overall_leakage < 0 else "#34D399"
    status_txt = "LEAKAGE" if overall_leakage < 0 else "OPTIMAL"
    
    st.markdown(f"""
    <div class="telemetry-card">
        <div class="telemetry-header">
            <span class="telemetry-title">LEAKAGE SCORE</span>
            <span class="telemetry-tag" style="background: {status_bg}; color: {status_color};">{status_txt}</span>
        </div>
        <div class="telemetry-value" style="color: {status_color};">{overall_leakage:+.2f}%</div>
        <div class="telemetry-footer"><span>Variance vs ML</span><span>Delta</span></div>
        <div class="progress-bar-bg"><div class="progress-bar-fill" style="width: {min(abs(overall_leakage)*3, 100)}%; background: {status_color};"></div></div>
    </div>
    """, unsafe_allow_html=True)

with k5:
    st.markdown(f"""
    <div class="telemetry-card">
        <div class="telemetry-header">
            <span class="telemetry-title">REVENUE OPPORTUNITY</span>
            <span class="telemetry-tag" style="background: rgba(245, 158, 11, 0.2); color: #FBBF24;">OPPORTUNITY</span>
        </div>
        <div class="telemetry-value" style="color: #FBBF24;">₹{total_exposure_crs:.2f} Cr</div>
        <div class="telemetry-footer"><span>Uncaptured Revenue</span><span>Target</span></div>
        <div class="progress-bar-bg"><div class="progress-bar-fill" style="width: 90%; background: #F59E0B;"></div></div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- PLOTLY SAPPHIRE & GOLD CHART STYLING ---
def style_plotly_chart(fig, height=370):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#101A36",
        plot_bgcolor="#101A36",
        font=dict(family="Inter, sans-serif", color="#94A3B8", size=12),
        margin=dict(l=20, r=20, t=35, b=20),
        height=height,
        xaxis=dict(gridcolor="#1E2942", zerolinecolor="#2B3A67"),
        yaxis=dict(gridcolor="#1E2942", zerolinecolor="#2B3A67"),
        legend=dict(bgcolor="#060B19", bordercolor="#2B3A67", borderwidth=1)
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
    c_left, c_right = st.columns(2)
    
    with c_left:
        st.markdown('<div class="section-header"><span>Top Exposure Routes</span><span class="section-badge">REVENUE OPPORTUNITY</span></div>', unsafe_allow_html=True)
        
        route_exp = filtered_df.groupby('route').apply(
            lambda g: (g[g['expected_fare'] > g['price']]['expected_fare'] - g[g['expected_fare'] > g['price']]['price']).sum() / 100000
        ).reset_index(name='exposure_lakhs').sort_values(by='exposure_lakhs', ascending=False).head(10)
        
        fig1 = px.bar(
            route_exp, x='exposure_lakhs', y='route', orientation='h',
            labels={'exposure_lakhs': 'Opportunity (₹ Lakhs)', 'route': 'Route'},
            color='exposure_lakhs',
            color_continuous_scale=['#1D4ED8', '#D97706', '#FBBF24']
        )
        fig1.update_layout(yaxis={'categoryorder':'total ascending'}, coloraxis_showscale=False)
        fig1 = style_plotly_chart(fig1)
        st.plotly_chart(fig1, use_container_width=True)

    with c_right:
        st.markdown('<div class="section-header"><span>Leakage Score by Window</span><span class="section-badge">VARIANCE %</span></div>', unsafe_allow_html=True)
        
        bucket_summary = filtered_df.groupby('days_bucket').agg(
            avg_actual=('price', 'mean'),
            avg_expected=('expected_fare', 'mean')
        ).reset_index()
        bucket_summary['leakage_pct'] = ((bucket_summary['avg_actual'] - bucket_summary['avg_expected']) / bucket_summary['avg_expected']) * 100
        
        fig2 = px.bar(
            bucket_summary, x='days_bucket', y='leakage_pct',
            labels={'days_bucket': 'Booking Window', 'leakage_pct': 'Leakage Score (%)'},
            color='leakage_pct',
            color_continuous_scale=['#F43F5E', '#F59E0B', '#10B981']
        )
        fig2 = style_plotly_chart(fig2)
        st.plotly_chart(fig2, use_container_width=True)

# --- TAB 2: ROUTE YIELD EXPLORER ---
with tab2:
    st.markdown('<div class="section-header"><span>Days to Departure Yield Curve</span><span class="section-badge">YIELD PROGRESSION</span></div>', unsafe_allow_html=True)
    
    available_routes = sorted(filtered_df['route'].unique())
    selected_route = st.selectbox("Inspect Route Fare Curve", available_routes if available_routes else sorted(df['route'].unique()))
    
    route_df = filtered_df[filtered_df['route'] == selected_route] if not filtered_df.empty else df[df['route'] == selected_route]
    
    curve_df = route_df.groupby('days_left').agg(
        Actual_Price=('price', 'mean'),
        Expected_Benchmark=('expected_fare', 'mean')
    ).reset_index()
    
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(
        x=curve_df['days_left'], y=curve_df['Actual_Price'],
        mode='lines+markers', name='Actual Realized Fare',
        line=dict(color='#60A5FA', width=3),
        marker=dict(size=6, color='#60A5FA')
    ))
    fig3.add_trace(go.Scatter(
        x=curve_df['days_left'], y=curve_df['Expected_Benchmark'],
        mode='lines+markers', name='ML Expected Benchmark',
        line=dict(color='#FBBF24', width=3, dash='dash'),
        marker=dict(size=6, color='#FBBF24')
    ))
    
    fig3.update_layout(
        title=f"Yield Progression Curve for {selected_route}",
        xaxis_title="Days Left to Departure (1 = Departure Day)",
        yaxis_title="Average Fare (INR)",
        xaxis=dict(autorange="reversed")
    )
    fig3 = style_plotly_chart(fig3, height=420)
    st.plotly_chart(fig3, use_container_width=True)

# --- TAB 3: COMPETITOR BENCHMARK ---
with tab3:
    st.markdown('<div class="section-header"><span>Airline Market Price Benchmark</span><span class="section-badge">COMPETITION</span></div>', unsafe_allow_html=True)
    
    comp_df = filtered_df.groupby(['airline', 'days_bucket'])['price'].mean().reset_index()
    
    fig4 = px.bar(
        comp_df, x='days_bucket', y='price', color='airline', barmode='group',
        labels={'price': 'Average Fare (INR)', 'days_bucket': 'Booking Window', 'airline': 'Airline'},
        color_discrete_sequence=['#2563EB', '#F59E0B', '#10B981', '#38BDF8', '#8B5CF6', '#EC4899']
    )
    fig4 = style_plotly_chart(fig4, height=420)
    st.plotly_chart(fig4, use_container_width=True)

# --- TAB 4: WHAT-IF SCENARIO SIMULATOR ---
with tab4:
    st.markdown('<div class="section-header"><span>Dynamic Pricing What-If Simulator</span><span class="section-badge">SIMULATION</span></div>', unsafe_allow_html=True)
    st.markdown("Simulate the revenue optimization impact of stepping up price floors on underpriced flights.")
    
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
        <div style="background: #101A36; border: 1px solid #2B3A67; border-top: 3px solid #F59E0B; border-radius: 14px; padding: 22px; text-align: center; margin-top: 15px;">
            <div style="font-size: 11px; color: #94A3B8; text-transform: uppercase; letter-spacing: 1px; font-weight: 600;">SIMULATED REVENUE UPSIDE</div>
            <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 34px; font-weight: 800; color: #FBBF24; margin: 8px 0;">
                +₹{rev_gain_crs:.2f} Cr
            </div>
            <div style="font-size: 12px; color: #60A5FA;">(₹{rev_gain_lakhs:,.2f} Lakhs with +{adjustment_pct}% Price Floor Step)</div>
        </div>
        """, unsafe_allow_html=True)
    
    with s_col2:
        sim_summary = pd.DataFrame({
            'Scenario': ['Current Revenue', 'Simulated Revenue'],
            'Revenue_Cr': [current_rev / 10000000, adjusted_rev / 10000000]
        })
        
        fig5 = px.bar(
            sim_summary, x='Scenario', y='Revenue_Cr', color='Scenario',
            color_discrete_map={'Current Revenue': '#2563EB', 'Simulated Revenue': '#F59E0B'},
            labels={'Revenue_Cr': 'Revenue (₹ Crores)'}
        )
        fig5 = style_plotly_chart(fig5, height=300)
        st.plotly_chart(fig5, use_container_width=True)

st.markdown("---")
st.markdown("<div style='text-align: center; color: #94A3B8; font-size: 11px; font-family: monospace;'>AIRLINE REVENUE LEAKAGE & PRICING INTELLIGENCE DASHBOARD</div>", unsafe_allow_html=True)
