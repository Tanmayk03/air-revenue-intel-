import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit.components.v1 as components
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Airline Revenue & Pricing Intelligence Console",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM BESPOKE EXECUTIVE COCKPIT THEME ---
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700&family=Inter:wght@300;400;500;600;700&family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap" rel="stylesheet">

<style>
    /* Global Background & Typography */
    .stApp {
        background-color: #080C14;
        color: #E2E8F0;
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Default Streamlit Chrome */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background: #0D1322 !important;
        border-right: 1px solid #1E293B !important;
        box-shadow: 4px 0 20px rgba(0, 0, 0, 0.4);
    }
    
    .sidebar-brand-card {
        background: linear-gradient(180deg, #182238 0%, #0F172A 100%);
        border: 1px solid #26354A;
        border-radius: 10px;
        padding: 18px 14px;
        text-align: center;
        margin-bottom: 22px;
    }
    
    .sidebar-brand-title {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 15px;
        font-weight: 800;
        color: #F8FAFC;
        letter-spacing: 1px;
        text-transform: uppercase;
    }

    .sidebar-brand-sub {
        font-size: 10px;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-top: 4px;
    }

    /* Bespoke Executive Telemetry Metric Cards */
    .telemetry-card {
        background: #0F172A;
        border: 1px solid #1E293B;
        border-radius: 12px;
        padding: 16px 14px;
        position: relative;
        overflow: hidden;
        transition: all 0.25s ease;
    }
    
    .telemetry-card:hover {
        border-color: #38BDF8;
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
    }

    .telemetry-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;
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
        font-size: 9px;
        font-weight: 700;
        padding: 2px 6px;
        border-radius: 4px;
        letter-spacing: 0.5px;
        background: #1E293B;
        color: #64748B;
    }

    .telemetry-value {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 25px;
        font-weight: 800;
        color: #F8FAFC;
        margin-bottom: 4px;
    }

    .telemetry-footer {
        font-size: 11px;
        color: #64748B;
        display: flex;
        justify-content: space-between;
    }

    /* Progress Indicator Bar inside Cards */
    .progress-bar-bg {
        width: 100%;
        height: 4px;
        background: #1E293B;
        border-radius: 2px;
        margin-top: 8px;
        overflow: hidden;
    }
    
    .progress-bar-fill {
        height: 100%;
        border-radius: 2px;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background: #0D1322;
        padding: 6px;
        border-radius: 10px;
        border: 1px solid #1E293B;
    }

    .stTabs [data-baseweb="tab"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-weight: 600;
        font-size: 13px;
        color: #94A3B8;
        border-radius: 8px;
        padding: 8px 16px;
        border: none !important;
        transition: all 0.2s ease;
    }

    .stTabs [aria-selected="true"] {
        background: #1E293B !important;
        color: #38BDF8 !important;
        border: 1px solid #334155 !important;
    }

    /* Section Headers */
    .section-header {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 16px;
        font-weight: 700;
        color: #F8FAFC;
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 14px;
    }

    .section-badge {
        background: #1E293B;
        border: 1px solid #334155;
        color: #38BDF8;
        font-size: 10px;
        font-weight: 700;
        padding: 2px 8px;
        border-radius: 4px;
        letter-spacing: 0.5px;
    }
</style>
""", unsafe_allow_html=True)

# --- THREE.JS 3D FLIGHT RADAR & FRONT-VIEW JET CANVAS ---
def render_3d_flight_control_hero():
    three_js_code = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {
                margin: 0;
                overflow: hidden;
                background: transparent;
                font-family: 'Plus Jakarta Sans', 'Inter', sans-serif;
            }
            #canvas-container {
                width: 100%;
                height: 245px;
                position: relative;
                border-radius: 12px;
                overflow: hidden;
                background: radial-gradient(ellipse at center, #0F172A 0%, #080C14 100%);
                border: 1px solid #1E293B;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
            }
            .hud-overlay {
                position: absolute;
                top: 18px;
                left: 24px;
                z-index: 10;
                pointer-events: none;
            }
            .hud-tag {
                display: inline-block;
                background: #182238;
                border: 1px solid #26354A;
                color: #38BDF8;
                font-size: 10px;
                font-weight: 700;
                padding: 3px 10px;
                border-radius: 4px;
                letter-spacing: 1.5px;
                margin-bottom: 6px;
                text-transform: uppercase;
            }
            .hud-main-title {
                color: #F8FAFC;
                font-size: 22px;
                font-weight: 800;
                letter-spacing: 0.5px;
                margin: 0;
            }
            .hud-sub-title {
                color: #94A3B8;
                font-size: 13px;
                margin-top: 4px;
            }
            .hud-status-panel {
                position: absolute;
                top: 18px;
                right: 24px;
                z-index: 10;
                text-align: right;
                pointer-events: none;
            }
            .status-badge {
                display: inline-flex;
                align-items: center;
                gap: 6px;
                background: #064E3B;
                border: 1px solid #059669;
                color: #34D399;
                font-size: 11px;
                font-weight: 700;
                padding: 4px 10px;
                border-radius: 6px;
                letter-spacing: 0.5px;
            }
            .status-dot {
                width: 6px;
                height: 6px;
                background-color: #34D399;
                border-radius: 50%;
            }
        </style>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    </head>
    <body>
        <div id="canvas-container">
            <div class="hud-overlay">
                <div class="hud-tag">FLIGHT DISPATCH & YIELD COMMAND</div>
                <h1 class="hud-main-title">Airline Revenue Leakage & Pricing Intelligence</h1>
                <div class="hud-sub-title">Machine Learning Expected Fare Benchmark | Exposure & Dynamic Yield Analytics</div>
            </div>
            <div class="hud-status-panel">
                <div class="status-badge"><span class="status-dot"></span>ANALYTICS ENGINE ONLINE</div>
                <div style="color: #64748B; font-size: 11px; font-weight: 600; margin-top: 6px;">COVERAGE: 300,153 METRO FLIGHTS</div>
            </div>
        </div>

        <script>
            const container = document.getElementById('canvas-container');
            const scene = new THREE.Scene();

            const camera = new THREE.PerspectiveCamera(40, container.clientWidth / container.clientHeight, 0.1, 1000);
            camera.position.set(0, 2.5, 12);

            const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
            renderer.setSize(container.clientWidth, container.clientHeight);
            renderer.setPixelRatio(window.devicePixelRatio);
            container.appendChild(renderer.domElement);

            // Lighting setup for front-facing jet
            const ambientLight = new THREE.AmbientLight(0xffffff, 0.9);
            scene.add(ambientLight);

            const frontSunLight = new THREE.DirectionalLight(0xF8FAFC, 2.2);
            frontSunLight.position.set(0, 10, 15);
            scene.add(frontSunLight);

            const sideLight = new THREE.DirectionalLight(0x38BDF8, 1.2);
            sideLight.position.set(-10, 5, 5);
            scene.add(sideLight);

            // 3D Animated Radar Grid Plane
            const gridHelper = new THREE.GridHelper(24, 24, 0x38BDF8, 0x1E293B);
            gridHelper.position.y = -2;
            scene.add(gridHelper);

            // Sleek Jet Aircraft Construction
            const jetGroup = new THREE.Group();

            // Fuselage (Cone Apex pointing forward towards viewer +Z)
            const bodyGeo = new THREE.ConeGeometry(0.75, 5.8, 24);
            // Rotate cone so apex points along +Z towards viewer
            bodyGeo.rotateX(-Math.PI / 2);
            
            const bodyMat = new THREE.MeshStandardMaterial({ color: 0x1E293B, metalness: 0.85, roughness: 0.2 });
            const body = new THREE.Mesh(bodyGeo, bodyMat);
            jetGroup.add(body);

            // Front Cockpit Glass Canopy
            const glassGeo = new THREE.SphereGeometry(0.46, 16, 16);
            glassGeo.scale(0.82, 0.52, 1.5);
            const glassMat = new THREE.MeshStandardMaterial({ color: 0x38BDF8, metalness: 0.95, roughness: 0.1, transparent: true, opacity: 0.92 });
            const glass = new THREE.Mesh(glassGeo, glassMat);
            glass.position.set(0, 0.38, 0.7);
            jetGroup.add(glass);

            // Swept Wings (facing forward)
            const wingShape = new THREE.Shape();
            wingShape.moveTo(0, 0);
            wingShape.lineTo(4.6, -1.8);
            wingShape.lineTo(4.3, -2.6);
            wingShape.lineTo(0, -0.9);
            wingShape.closePath();

            const wingGeo = new THREE.ExtrudeGeometry(wingShape, { depth: 0.06, bevelEnabled: true, bevelSize: 0.02, bevelThickness: 0.02 });
            const wingMat = new THREE.MeshStandardMaterial({ color: 0x334155, metalness: 0.7, roughness: 0.3 });
            
            const rWing = new THREE.Mesh(wingGeo, wingMat);
            rWing.rotation.x = -Math.PI / 2;
            rWing.position.set(0, 0, -0.2);
            jetGroup.add(rWing);

            const lWing = rWing.clone();
            lWing.scale.set(-1, 1, 1);
            jetGroup.add(lWing);

            // Vertical Tail Fin
            const tailShape = new THREE.Shape();
            tailShape.moveTo(0, 0);
            tailShape.lineTo(0, 1.6);
            tailShape.lineTo(-1.0, 1.2);
            tailShape.lineTo(-1.3, 0);
            tailShape.closePath();

            const tailGeo = new THREE.ExtrudeGeometry(tailShape, { depth: 0.06, bevelEnabled: true, bevelSize: 0.02, bevelThickness: 0.02 });
            const tailMat = new THREE.MeshStandardMaterial({ color: 0x2563EB, metalness: 0.6, roughness: 0.3 });
            const tail = new THREE.Mesh(tailGeo, tailMat);
            tail.rotation.y = Math.PI;
            tail.position.set(0, 0, -2.1);
            jetGroup.add(tail);

            // Jet Engines
            const engineGeo = new THREE.CylinderGeometry(0.28, 0.28, 1.5, 20);
            engineGeo.rotateX(Math.PI / 2);
            const engineMat = new THREE.MeshStandardMaterial({ color: 0x475569, metalness: 0.9, roughness: 0.2 });
            
            const rEngine = new THREE.Mesh(engineGeo, engineMat);
            rEngine.position.set(1.5, -0.3, -0.3);
            jetGroup.add(rEngine);

            const lEngine = rEngine.clone();
            lEngine.position.set(-1.5, -0.3, -0.3);
            jetGroup.add(lEngine);

            scene.add(jetGroup);
            
            // POSITION & FRONT-QUARTER ROTATION TOWARDS USER
            jetGroup.position.set(3.4, 0.1, 1.2);
            jetGroup.rotation.y = -0.42;  // Angled nose cone towards user
            jetGroup.rotation.x = 0.22;   // Pitched up to show top cockpit & wings
            jetGroup.rotation.z = -0.12;  // Slight bank turn

            // Flight Trajectory Nodes
            const nodeGeo = new THREE.SphereGeometry(0.12, 12, 12);
            const nodeMat = new THREE.MeshBasicMaterial({ color: 0x38BDF8 });
            
            const nodePositions = [
                [-6, -1.9, 2], [-2, -1.9, -4], [4, -1.9, -3], [-4, -1.9, -6], [2, -1.9, 4]
            ];
            
            nodePositions.forEach(pos => {
                const node = new THREE.Mesh(nodeGeo, nodeMat);
                node.position.set(pos[0], pos[1], pos[2]);
                scene.add(node);
            });

            // Render Loop
            let clock = new THREE.Clock();
            function animate() {
                requestAnimationFrame(animate);
                const t = clock.getElapsedTime();

                // Smooth Front Jet Flight Float
                jetGroup.position.y = 0.1 + Math.sin(t * 1.5) * 0.2;
                jetGroup.rotation.y = -0.42 + Math.sin(t * 0.8) * 0.04;
                jetGroup.rotation.z = -0.12 + Math.cos(t * 1.0) * 0.03;

                gridHelper.rotation.y = t * 0.05;

                renderer.render(scene, camera);
            }

            window.addEventListener('resize', () => {
                camera.aspect = container.clientWidth / container.clientHeight;
                camera.updateProjectionMatrix();
                renderer.setSize(container.clientWidth, container.clientHeight);
            });

            animate();
        </script>
    </body>
    </html>
    """
    components.html(three_js_code, height=260)

# Render 3D Radar Hero
render_3d_flight_control_hero()

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

# --- SIDEBAR CONTROL PANEL ---
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand-card">
        <div class="sidebar-brand-title">DISPATCH CONTROL</div>
        <div class="sidebar-brand-sub">PRICING INTELLIGENCE SUITE</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='color: #94A3B8; font-weight: 700; font-size: 11px; letter-spacing: 1px; margin-bottom: 10px; text-transform: uppercase;'>GLOBAL FILTERS</div>", unsafe_allow_html=True)
    
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
    <div style='background: #0F172A; border: 1px solid #1E293B; border-radius: 8px; padding: 14px;'>
        <div style='color: #38BDF8; font-size: 11px; font-weight: 700; letter-spacing: 0.5px;'>BENCHMARK HYPOTHESIS</div>
        <div style='color: #94A3B8; font-size: 11px; margin-top: 6px; line-height: 1.4;'>Long-haul flights in the 31+ Days booking window exhibit severe revenue leakage (-24% to -28%) due to static advance price floors.</div>
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

# --- BESPOKE EXECUTIVE TELEMETRY WIDGETS ---
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
            <span class="telemetry-title">FLIGHT VOLUME</span>
            <span class="telemetry-tag">ACTIVE</span>
        </div>
        <div class="telemetry-value">{total_flights:,}</div>
        <div class="telemetry-footer"><span>Analyzed Segment</span><span>100%</span></div>
        <div class="progress-bar-bg"><div class="progress-bar-fill" style="width: 100%; background: #3B82F6;"></div></div>
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
        <div class="progress-bar-bg"><div class="progress-bar-fill" style="width: 75%; background: #64748B;"></div></div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="telemetry-card">
        <div class="telemetry-header">
            <span class="telemetry-title">EXPECTED FARE</span>
            <span class="telemetry-tag" style="background: #1E3A8A; color: #38BDF8;">ML MODEL</span>
        </div>
        <div class="telemetry-value" style="color: #38BDF8;">₹{avg_expected:,.0f}</div>
        <div class="telemetry-footer"><span>Benchmark Baseline</span><span>R² 91%</span></div>
        <div class="progress-bar-bg"><div class="progress-bar-fill" style="width: 85%; background: #38BDF8;"></div></div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    status_bg = "#7F1D1D" if overall_leakage < 0 else "#064E3B"
    status_color = "#F87171" if overall_leakage < 0 else "#34D399"
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
            <span class="telemetry-title">EXPOSURE UPSIDE</span>
            <span class="telemetry-tag" style="background: #064E3B; color: #34D399;">OPPORTUNITY</span>
        </div>
        <div class="telemetry-value" style="color: #34D399;">₹{total_exposure_crs:.2f} Cr</div>
        <div class="telemetry-footer"><span>Uncaptured Revenue</span><span>Target</span></div>
        <div class="progress-bar-bg"><div class="progress-bar-fill" style="width: 90%; background: #10B981;"></div></div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- PLOTLY EXECUTIVE CHART STYLING ---
def style_plotly_chart(fig, height=360):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0F172A",
        plot_bgcolor="#0F172A",
        font=dict(family="Inter, sans-serif", color="#94A3B8", size=12),
        margin=dict(l=20, r=20, t=35, b=20),
        height=height,
        xaxis=dict(gridcolor="#1E293B", zerolinecolor="#334155"),
        yaxis=dict(gridcolor="#1E293B", zerolinecolor="#334155"),
        legend=dict(bgcolor="#0B0F19", bordercolor="#1E293B", borderwidth=1)
    )
    return fig

# --- EXECUTIVE NAVIGATION TABS ---
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
            color_continuous_scale=['#1E3A8A', '#2563EB', '#38BDF8']
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
            color_continuous_scale=['#EF4444', '#F59E0B', '#10B981']
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
        line=dict(color='#38BDF8', width=3),
        marker=dict(size=6, color='#38BDF8')
    ))
    fig3.add_trace(go.Scatter(
        x=curve_df['days_left'], y=curve_df['Expected_Benchmark'],
        mode='lines+markers', name='ML Expected Benchmark',
        line=dict(color='#F43F5E', width=3, dash='dash'),
        marker=dict(size=6, color='#F43F5E')
    ))
    
    fig3.update_layout(
        title=f"Yield Progression Curve for {selected_route}",
        xaxis_title="Days Left to Departure (1 = Departure Day)",
        yaxis_title="Average Fare (INR)",
        xaxis=dict(autorange="reversed")
    )
    fig3 = style_plotly_chart(fig3, height=410)
    st.plotly_chart(fig3, use_container_width=True)

# --- TAB 3: COMPETITOR BENCHMARK ---
with tab3:
    st.markdown('<div class="section-header"><span>Airline Market Price Benchmark</span><span class="section-badge">COMPETITION</span></div>', unsafe_allow_html=True)
    
    comp_df = filtered_df.groupby(['airline', 'days_bucket'])['price'].mean().reset_index()
    
    fig4 = px.bar(
        comp_df, x='days_bucket', y='price', color='airline', barmode='group',
        labels={'price': 'Average Fare (INR)', 'days_bucket': 'Booking Window', 'airline': 'Airline'},
        color_discrete_sequence=['#2563EB', '#38BDF8', '#10B981', '#F59E0B', '#6366F1', '#EC4899']
    )
    fig4 = style_plotly_chart(fig4, height=410)
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
        <div style="background: #0F172A; border: 1px solid #1E293B; border-top: 3px solid #10B981; border-radius: 12px; padding: 22px; text-align: center; margin-top: 15px;">
            <div style="font-size: 11px; color: #94A3B8; text-transform: uppercase; letter-spacing: 1px; font-weight: 600;">SIMULATED REVENUE UPSIDE</div>
            <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 34px; font-weight: 800; color: #10B981; margin: 8px 0;">
                +₹{rev_gain_crs:.2f} Cr
            </div>
            <div style="font-size: 12px; color: #38BDF8;">(₹{rev_gain_lakhs:,.2f} Lakhs with +{adjustment_pct}% Price Floor Step)</div>
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
        fig5 = style_plotly_chart(fig5, height=290)
        st.plotly_chart(fig5, use_container_width=True)

st.markdown("---")
st.markdown("<div style='text-align: center; color: #64748B; font-size: 11px; font-family: monospace;'>AIRLINE REVENUE LEAKAGE & PRICING INTELLIGENCE // EXECUTIVE DISPATCH CONSOLE</div>", unsafe_allow_html=True)
