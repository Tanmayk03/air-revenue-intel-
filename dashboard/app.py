import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Airline Revenue Intelligence",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- NATIVE BUG-FREE ENTERPRISE CSS THEME ---
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">

<style>
    /* Reset & Prevent Any Layout Glitches */
    *, ::before, ::after {
        box-sizing: border-box !important;
    }

    /* Global Page Theme - Clean Executive Light Mode */
    .stApp {
        background-color: #F8FAFC;
        color: #0F172A;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Clean Container Padding */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
        max-width: 1200px !important;
        margin: 0 auto !important;
    }
    
    /* Hide Default Streamlit Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background: #FFFFFF !important;
        border-right: 1px solid #E2E8F0 !important;
        box-shadow: 2px 0 10px rgba(0, 0, 0, 0.02);
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
    }

    .brand-badge {
        background: #EFF6FF;
        border: 1px solid #BFDBFE;
        color: #2563EB;
        font-size: 10px;
        font-weight: 700;
        padding: 2px 6px;
        border-radius: 4px;
        margin-left: 6px;
    }

    /* Native Hero Banner Card */
    .hero-card {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        border-radius: 14px;
        padding: 24px 28px;
        margin-bottom: 24px;
        color: #FFFFFF;
        box-shadow: 0 4px 15px rgba(15, 23, 42, 0.1);
        position: relative;
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
        letter-spacing: 1.2px;
        margin-bottom: 8px;
        text-transform: uppercase;
    }

    .hero-title {
        font-size: 22px;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.4px;
        color: #FFFFFF;
    }

    .hero-sub {
        font-size: 13px;
        color: #94A3B8;
        margin-top: 4px;
    }

    /* Native KPI Cards */
    .kpi-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 16px 18px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.03);
        margin-bottom: 12px;
    }

    .kpi-label {
        font-size: 11px;
        font-weight: 700;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 6px;
    }

    .kpi-value {
        font-size: 26px;
        font-weight: 800;
        color: #0F172A;
        letter-spacing: -0.5px;
    }

    .kpi-subtext {
        font-size: 11px;
        color: #94A3B8;
        margin-top: 4px;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background: #F1F5F9;
        padding: 4px;
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

    .stTabs [data-baseweb="tab-panel"] {
        padding-top: 14px !important;
    }

    .card-title {
        font-size: 15px;
        font-weight: 700;
        color: #0F172A;
        margin-bottom: 12px;
    }

    /* Mobile Responsive Tweaks */
    @media (max-width: 768px) {
        .block-container {
            padding-top: 1rem !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        .hero-title {
            font-size: 18px;
        }
        .kpi-value {
            font-size: 22px;
        }
    }
</style>
""", unsafe_allow_html=True)

# --- HERO EXECUTIVE BANNER CARD ---
st.markdown("""
<div class="hero-card">
    <div class="hero-tag">AIRLINE PRICING BENCHMARK PLATFORM</div>
    <h1 class="hero-title">Airline Revenue Leakage & Pricing Intelligence Console</h1>
    <div class="hero-sub">Machine Learning Expected Fare Benchmark | Exposure & Dynamic Yield Analytics</div>
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
    st.error(f"Error loading dataset. Details: {e}")
    st.stop()

# --- SIDEBAR CONTROLS ---
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="brand-title">Pricing Intel <span class="brand-badge">PRO</span></div>
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
        <div class="kpi-label">Audited Flights</div>
        <div class="kpi-value">{total_flights:,}</div>
        <div class="kpi-subtext">Evaluated Flight Volume</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Avg Realized Fare</div>
        <div class="kpi-value">₹{avg_actual:,.0f}</div>
        <div class="kpi-subtext">Realized Ticket Average</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    leak_color = "#DC2626" if overall_leakage < 0 else "#059669"
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Benchmark & Leakage Score</div>
        <div class="kpi-value" style="color: {leak_color};">₹{avg_expected:,.0f} ({overall_leakage:+.1f}%)</div>
        <div class="kpi-subtext">ML Benchmark Baseline</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Revenue Opportunity</div>
        <div class="kpi-value" style="color: #059669;">₹{total_exposure_crs:.2f} Cr</div>
        <div class="kpi-subtext">Uncaptured Exposure Upside</div>
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
        st.markdown('<div class="card-title">Top Exposure Routes (₹ Lakhs)</div>', unsafe_allow_html=True)
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
        st.markdown('<div class="card-title">Leakage Score by Booking Window (%)</div>', unsafe_allow_html=True)
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

    # Executive Data Table
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
