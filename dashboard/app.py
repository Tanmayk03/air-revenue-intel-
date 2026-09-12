import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit.components.v1 as components
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Airline Revenue & Pricing Intelligence",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CLASSIC EXECUTIVE STYLING ---
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap" rel="stylesheet">

<style>
    /* Global Page Styling */
    .stApp {
        background-color: #0B0F19;
        color: #E2E8F0;
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Default Streamlit Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background: #111827 !important;
        border-right: 1px solid #1E293B !important;
        box-shadow: 4px 0 15px rgba(0, 0, 0, 0.3);
    }
    
    /* Custom Sidebar Header Card */
    .sidebar-brand-card {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 16px;
        text-align: center;
        margin-bottom: 20px;
    }
    
    .sidebar-brand-title {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 16px;
        font-weight: 700;
        color: #F8FAFC;
        letter-spacing: 0.5px;
    }

    /* Classic Executive Metric Cards */
    .metric-card-container {
        background: #131C2E;
        border: 1px solid #1E293B;
        border-top: 3px solid #2563EB;
        border-radius: 12px;
        padding: 18px 16px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
        transition: all 0.2s ease-in-out;
    }
    
    .metric-card-container:hover {
        transform: translateY(-2px);
        border-color: #3B82F6;
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.35);
    }

    .metric-label {
        font-family: 'Inter', sans-serif;
        font-size: 12px;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-bottom: 6px;
        font-weight: 600;
    }

    .metric-value {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 26px;
        font-weight: 800;
        color: #F8FAFC;
    }

    .metric-subtext {
        font-size: 11px;
        color: #64748B;
        margin-top: 4px;
    }

    /* Custom Streamlit Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: #111827;
        padding: 6px;
        border-radius: 10px;
        border: 1px solid #1E293B;
    }

    .stTabs [data-baseweb="tab"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-weight: 600;
        font-size: 14px;
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

    /* Section Titles */
    .hud-title {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 18px;
        font-weight: 700;
        color: #F8FAFC;
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 12px;
    }
    
    .hud-badge {
        background: #1E293B;
        border: 1px solid #334155;
        color: #38BDF8;
        font-size: 10px;
        font-weight: 600;
        padding: 2px 8px;
        border-radius: 6px;
        letter-spacing: 0.5px;
    }

    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    ::-webkit-scrollbar-track {
        background: #0B0F19;
    }
    ::-webkit-scrollbar-thumb {
        background: #334155;
        border-radius: 3px;
    }
</style>
""", unsafe_allow_html=True)

# --- THREE.JS CLASSIC EXECUTIVE 3D JET CANVAS ---
def render_3d_airplane_hero():
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
                height: 230px;
                position: relative;
                border-radius: 14px;
                overflow: hidden;
                background: linear-gradient(135deg, #0F172A 0%, #090D16 100%);
                border: 1px solid #1E293B;
                box-shadow: 0 4px 20px rgba(0,0,0,0.4);
            }
            .hud-overlay {
                position: absolute;
                top: 16px;
                left: 22px;
                z-index: 10;
                pointer-events: none;
            }
            .hud-tag {
                display: inline-block;
                background: #1E293B;
                border: 1px solid #334155;
                color: #38BDF8;
                font-size: 11px;
                font-weight: 600;
                padding: 3px 9px;
                border-radius: 4px;
                letter-spacing: 1px;
                margin-bottom: 6px;
            }
            .hud-main-title {
                color: #F8FAFC;
                font-size: 21px;
                font-weight: 800;
                letter-spacing: 0.5px;
                margin: 0;
            }
            .hud-sub-title {
                color: #94A3B8;
                font-size: 13px;
                margin-top: 3px;
            }
            .hud-status-panel {
                position: absolute;
                top: 16px;
                right: 22px;
                z-index: 10;
                text-align: right;
                pointer-events: none;
            }
            .status-dot {
                display: inline-block;
                width: 8px;
                height: 8px;
                background-color: #10B981;
                border-radius: 50%;
                margin-right: 6px;
            }
            .status-text {
                color: #10B981;
                font-size: 11px;
                font-weight: 600;
                letter-spacing: 0.5px;
            }
        </style>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    </head>
    <body>
        <div id="canvas-container">
            <div class="hud-overlay">
                <div class="hud-tag">AIRLINE ANALYTICS DASHBOARD</div>
                <h1 class="hud-main-title">Revenue Leakage & Pricing Benchmark Engine</h1>
                <div class="hud-sub-title">ML-Based Expected Fare Benchmark & Directional Revenue Exposure</div>
            </div>
            <div class="hud-status-panel">
                <div><span class="status-dot"></span><span class="status-text">DATABASE ONLINE</span></div>
                <div style="color: #94A3B8; font-size: 11px; font-weight: 500; margin-top: 3px;">Model Accuracy: 91.29% R²</div>
            </div>
        </div>

        <script>
            const container = document.getElementById('canvas-container');
            const scene = new THREE.Scene();
            
            // Camera
            const camera = new THREE.PerspectiveCamera(40, container.clientWidth / container.clientHeight, 0.1, 1000);
            camera.position.set(0, 1.8, 13);

            // Renderer
            const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
            renderer.setSize(container.clientWidth, container.clientHeight);
            renderer.setPixelRatio(window.devicePixelRatio);
            container.appendChild(renderer.domElement);

            // Classic Executive Lighting
            const ambientLight = new THREE.AmbientLight(0xffffff, 0.9);
            scene.add(ambientLight);

            const sunLight = new THREE.DirectionalLight(0xF8FAFC, 1.8);
            sunLight.position.set(10, 15, 12);
            scene.add(sunLight);

            const fillLight = new THREE.DirectionalLight(0x3B82F6, 0.8);
            fillLight.position.set(-10, -5, -10);
            scene.add(fillLight);

            // Sleek Jet Aircraft Model Group
            const airplaneGroup = new THREE.Group();

            // Fuselage (Sleek Executive Body)
            const bodyGeo = new THREE.ConeGeometry(0.75, 6.2, 24);
            bodyGeo.rotateX(Math.PI / 2);
            const bodyMat = new THREE.MeshStandardMaterial({ 
                color: 0x1E293B, 
                metalness: 0.8, 
                roughness: 0.2 
            });
            const fuselage = new THREE.Mesh(bodyGeo, bodyMat);
            airplaneGroup.add(fuselage);

            // Cockpit Glass Window
            const cockpitGeo = new THREE.SphereGeometry(0.48, 16, 16);
            cockpitGeo.scale(0.85, 0.55, 1.6);
            const cockpitMat = new THREE.MeshStandardMaterial({ 
                color: 0x38BDF8, 
                metalness: 0.9, 
                roughness: 0.1,
                transparent: true,
                opacity: 0.95 
            });
            const cockpit = new THREE.Mesh(cockpitGeo, cockpitMat);
            cockpit.position.set(0, 0.38, 0.85);
            airplaneGroup.add(cockpit);

            // Main Swept Wings
            const wingShape = new THREE.Shape();
            wingShape.moveTo(0, 0);
            wingShape.lineTo(4.6, -1.9);
            wingShape.lineTo(4.3, -2.7);
            wingShape.lineTo(0, -1.1);
            wingShape.closePath();

            const extrudeSettings = { depth: 0.08, bevelEnabled: true, bevelSegments: 2, steps: 1, bevelSize: 0.03, bevelThickness: 0.03 };
            const wingGeo = new THREE.ExtrudeGeometry(wingShape, extrudeSettings);
            const wingMat = new THREE.MeshStandardMaterial({ color: 0x334155, metalness: 0.7, roughness: 0.3 });
            
            const rightWing = new THREE.Mesh(wingGeo, wingMat);
            rightWing.rotation.x = Math.PI / 2;
            rightWing.position.set(0, 0, 0.4);
            airplaneGroup.add(rightWing);

            const leftWing = rightWing.clone();
            leftWing.scale.set(-1, 1, 1);
            airplaneGroup.add(leftWing);

            // Vertical Stabilizer / Tail Fin
            const tailShape = new THREE.Shape();
            tailShape.moveTo(0, 0);
            tailShape.lineTo(0, 1.7);
            tailShape.lineTo(-1.1, 1.3);
            tailShape.lineTo(-1.4, 0);
            tailShape.closePath();

            const tailGeo = new THREE.ExtrudeGeometry(tailShape, extrudeSettings);
            const tailMat = new THREE.MeshStandardMaterial({ color: 0x2563EB, metalness: 0.6, roughness: 0.3 });
            const tailFin = new THREE.Mesh(tailGeo, tailMat);
            tailFin.position.set(0, 0, -2.2);
            airplaneGroup.add(tailFin);

            // Jet Engines
            const engineGeo = new THREE.CylinderGeometry(0.28, 0.28, 1.5, 20);
            engineGeo.rotateX(Math.PI / 2);
            const engineMat = new THREE.MeshStandardMaterial({ color: 0x475569, metalness: 0.9, roughness: 0.2 });
            
            const rightEngine = new THREE.Mesh(engineGeo, engineMat);
            rightEngine.position.set(1.5, -0.3, -0.1);
            airplaneGroup.add(rightEngine);

            const leftEngine = rightEngine.clone();
            leftEngine.position.set(-1.5, -0.3, -0.1);
            airplaneGroup.add(leftEngine);

            scene.add(airplaneGroup);
            airplaneGroup.position.set(3.8, -0.2, 0);
            airplaneGroup.rotation.y = -Math.PI / 5.5;
            airplaneGroup.rotation.x = 0.12;
            airplaneGroup.rotation.z = -0.08;

            // Subtle Background Particles
            const particlesGeo = new THREE.BufferGeometry();
            const count = 120;
            const posArray = new Float32Array(count * 3);

            for(let i=0; i<count*3; i+=3) {
                posArray[i] = (Math.random() - 0.5) * 35;
                posArray[i+1] = (Math.random() - 0.5) * 15;
                posArray[i+2] = (Math.random() - 0.5) * 35;
            }

            particlesGeo.setAttribute('position', new THREE.BufferAttribute(posArray, 3));
            const particlesMat = new THREE.PointsMaterial({ size: 0.06, color: 0x94A3B8, transparent: true, opacity: 0.4 });
            const particleField = new THREE.Points(particlesGeo, particlesMat);
            scene.add(particleField);

            // Animation Loop
            let clock = new THREE.Clock();
            function animate() {
                requestAnimationFrame(animate);
                const elapsedTime = clock.getElapsedTime();

                // Smooth Floating Flight Motion
                airplaneGroup.position.y = -0.2 + Math.sin(elapsedTime * 1.2) * 0.25;
                airplaneGroup.rotation.y = -Math.PI / 5.5 + Math.sin(elapsedTime * 0.6) * 0.04;
                airplaneGroup.rotation.z = -0.08 + Math.cos(elapsedTime * 0.9) * 0.03;

                const positions = particlesGeo.attributes.position.array;
                for(let i=2; i<count*3; i+=3) {
                    positions[i] += 0.08;
                    if(positions[i] > 15) positions[i] = -15;
                }
                particlesGeo.attributes.position.needsUpdate = true;

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
    components.html(three_js_code, height=245)

# Render 3D Canvas Header
render_3d_airplane_hero()

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
        <div class="sidebar-brand-title">PRICING INTELLIGENCE</div>
        <div style="font-size: 11px; color: #94A3B8; margin-top: 2px;">Executive Benchmark Suite</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='color: #F8FAFC; font-weight: 700; font-size: 12px; letter-spacing: 0.5px; margin-bottom: 10px;'>FILTER PARAMETERS</div>", unsafe_allow_html=True)
    
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
    selected_route_filter = st.selectbox("Filter Specific Route", route_options, index=0)

    st.markdown("---")
    st.markdown("""
    <div style='background: #131C2E; border: 1px solid #1E293B; border-radius: 8px; padding: 12px;'>
        <div style='color: #38BDF8; font-size: 11px; font-weight: 700;'>EXECUTIVE SUMMARY NOTE</div>
        <div style='color: #94A3B8; font-size: 11px; margin-top: 4px;'>Advance booking windows (31+ Days) show ~24-28% price variance vs expected market benchmarks.</div>
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

# --- TOP KPI METRIC CARDS ---
total_flights = len(filtered_df)
avg_actual = filtered_df['price'].mean() if total_flights > 0 else 0
avg_expected = filtered_df['expected_fare'].mean() if total_flights > 0 else 0
overall_leakage = ((avg_actual - avg_expected) / avg_expected * 100) if avg_expected > 0 else 0

underpriced = filtered_df[filtered_df['expected_fare'] > filtered_df['price']]
total_exposure_crs = (underpriced['expected_fare'] - underpriced['price']).sum() / 10000000

kpi_col1, kpi_col2, kpi_col3, kpi_col4, kpi_col5 = st.columns(5)

with kpi_col1:
    st.markdown(f"""
    <div class="metric-card-container">
        <div class="metric-label">Total Flights</div>
        <div class="metric-value">{total_flights:,}</div>
        <div class="metric-subtext">Evaluated Flight Routes</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_col2:
    st.markdown(f"""
    <div class="metric-card-container">
        <div class="metric-label">Avg Actual Fare</div>
        <div class="metric-value">₹{avg_actual:,.0f}</div>
        <div class="metric-subtext">Realized Ticket Fare</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_col3:
    st.markdown(f"""
    <div class="metric-card-container">
        <div class="metric-label">Avg Benchmark</div>
        <div class="metric-value" style="color: #38BDF8;">₹{avg_expected:,.0f}</div>
        <div class="metric-subtext">Expected Benchmark</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_col4:
    leak_color = "#EF4444" if overall_leakage < 0 else "#10B981"
    st.markdown(f"""
    <div class="metric-card-container">
        <div class="metric-label">Leakage Score</div>
        <div class="metric-value" style="color: {leak_color};">{overall_leakage:+.2f}%</div>
        <div class="metric-subtext">Variance vs Benchmark</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_col5:
    st.markdown(f"""
    <div class="metric-card-container">
        <div class="metric-label">Revenue Opportunity</div>
        <div class="metric-value" style="color: #10B981;">₹{total_exposure_crs:.2f} Cr</div>
        <div class="metric-subtext">Directional Exposure</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- CLASSIC EXECUTIVE PLOTLY STYLE ---
def style_plotly_chart(fig, height=370):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#131C2E",
        plot_bgcolor="#131C2E",
        font=dict(family="Inter, sans-serif", color="#94A3B8", size=12),
        margin=dict(l=20, r=20, t=40, b=20),
        height=height,
        xaxis=dict(
            gridcolor="#1E293B",
            zerolinecolor="#334155"
        ),
        yaxis=dict(
            gridcolor="#1E293B",
            zerolinecolor="#334155"
        ),
        legend=dict(
            bgcolor="#0B0F19",
            bordercolor="#1E293B",
            borderwidth=1
        )
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
        st.markdown('<div class="hud-title"><span>Top 10 Exposure Routes</span><span class="hud-badge">REVENUE OPPORTUNITY</span></div>', unsafe_allow_html=True)
        
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

    with col_b:
        st.markdown('<div class="hud-title"><span>Leakage Score by Booking Window</span><span class="hud-badge">BENCHMARK VARIANCE %</span></div>', unsafe_allow_html=True)
        
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
    st.markdown('<div class="hud-title"><span>Days to Departure Yield Curve</span><span class="hud-badge">FARE PROGRESSION</span></div>', unsafe_allow_html=True)
    
    available_routes = sorted(filtered_df['route'].unique())
    selected_route = st.selectbox("Select Route to Inspect", available_routes if available_routes else sorted(df['route'].unique()))
    
    route_df = filtered_df[filtered_df['route'] == selected_route] if not filtered_df.empty else df[df['route'] == selected_route]
    
    curve_df = route_df.groupby('days_left').agg(
        Actual_Price=('price', 'mean'),
        Expected_Benchmark=('expected_fare', 'mean')
    ).reset_index()
    
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(
        x=curve_df['days_left'], y=curve_df['Actual_Price'],
        mode='lines+markers', name='Actual Fare',
        line=dict(color='#38BDF8', width=3),
        marker=dict(size=6, color='#38BDF8')
    ))
    fig3.add_trace(go.Scatter(
        x=curve_df['days_left'], y=curve_df['Expected_Benchmark'],
        mode='lines+markers', name='ML Benchmark',
        line=dict(color='#F43F5E', width=3, dash='dash'),
        marker=dict(size=6, color='#F43F5E')
    ))
    
    fig3.update_layout(
        title=f"Yield Curve for {selected_route} (Days to Departure)",
        xaxis_title="Days Left to Departure (1 = Departure Day)",
        yaxis_title="Average Fare (INR)",
        xaxis=dict(autorange="reversed")
    )
    fig3 = style_plotly_chart(fig3, height=420)
    st.plotly_chart(fig3, use_container_width=True)

# --- TAB 3: COMPETITOR BENCHMARK ---
with tab3:
    st.markdown('<div class="hud-title"><span>Airline Pricing Benchmark</span><span class="hud-badge">MARKET COMPETITION</span></div>', unsafe_allow_html=True)
    
    comp_df = filtered_df.groupby(['airline', 'days_bucket'])['price'].mean().reset_index()
    
    fig4 = px.bar(
        comp_df, x='days_bucket', y='price', color='airline', barmode='group',
        labels={'price': 'Average Fare (INR)', 'days_bucket': 'Booking Window', 'airline': 'Airline'},
        color_discrete_sequence=['#2563EB', '#38BDF8', '#10B981', '#F59E0B', '#6366F1', '#EC4899']
    )
    fig4 = style_plotly_chart(fig4, height=420)
    st.plotly_chart(fig4, use_container_width=True)

# --- TAB 4: WHAT-IF SCENARIO SIMULATOR ---
with tab4:
    st.markdown('<div class="hud-title"><span>Dynamic Pricing What-If Simulator</span><span class="hud-badge">REVENUE SIMULATION</span></div>', unsafe_allow_html=True)
    st.markdown("Simulate the financial impact of adjusting price floors on underpriced advance booking flights.")
    
    sim_col1, sim_col2 = st.columns([1, 1])
    
    with sim_col1:
        adjustment_pct = st.slider(
            "Target Price Adjustment (%) for Underpriced Segments", 
            min_value=0.0, max_value=30.0, value=10.0, step=1.0
        )
        
        underpriced_filtered = filtered_df[filtered_df['expected_fare'] > filtered_df['price']].copy()
        current_rev = underpriced_filtered['price'].sum()
        adjusted_rev = (underpriced_filtered['price'] * (1 + adjustment_pct/100)).sum()
        rev_gain_lakhs = (adjusted_rev - current_rev) / 100000
        rev_gain_crs = rev_gain_lakhs / 100
        
        st.markdown(f"""
        <div style="background: #131C2E; border: 1px solid #1E293B; border-top: 3px solid #10B981; border-radius: 12px; padding: 20px; text-align: center; margin-top: 15px;">
            <div style="font-size: 12px; color: #94A3B8; text-transform: uppercase; letter-spacing: 1px;">Simulated Revenue Upside</div>
            <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 34px; font-weight: 800; color: #10B981; margin: 8px 0;">
                +₹{rev_gain_crs:.2f} Cr
            </div>
            <div style="font-size: 12px; color: #38BDF8;">(₹{rev_gain_lakhs:,.2f} Lakhs with +{adjustment_pct}% Floor)</div>
        </div>
        """, unsafe_allow_html=True)
    
    with sim_col2:
        sim_summary = pd.DataFrame({
            'Scenario': ['Current Underpriced Revenue', 'Simulated Adjusted Revenue'],
            'Revenue_Cr': [current_rev / 10000000, adjusted_rev / 10000000]
        })
        
        fig5 = px.bar(
            sim_summary, x='Scenario', y='Revenue_Cr', color='Scenario',
            color_discrete_map={'Current Underpriced Revenue': '#2563EB', 'Simulated Adjusted Revenue': '#10B981'},
            labels={'Revenue_Cr': 'Revenue (₹ Crores)'}
        )
        fig5 = style_plotly_chart(fig5, height=300)
        st.plotly_chart(fig5, use_container_width=True)

st.markdown("---")
st.markdown("<div style='text-align: center; color: #64748B; font-size: 12px; font-family: monospace;'>AIRLINE REVENUE LEAKAGE & PRICING INTELLIGENCE DASHBOARD | BUILT WITH STREAMLIT & THREE.JS</div>", unsafe_allow_html=True)
