import streamlit as st
import plotly.graph_objects as go
import numpy as np

# Set layout halaman menjadi lebar agar dashboard terlihat profesional
st.set_page_config(layout="wide", page_title="Kalkulator Daya Pompa Air")

st.title("🚰 Kalkulator Daya Pompa Air & Kurva Performa")
st.caption("Estimasi daya listrik dan analisis grafik karakteristik pompa")

# --- GRID ATAS: INPUT PARAMETER & OUTPUT DAYA ---
col_input, col_output = st.columns([4, 4])

with col_input:
    st.write("### PARAMETER INPUT")
    # Slider Input sesuai gambar
    debit = st.slider("Debit air (Q)", min_value=0.001, max_value=0.200, value=0.086, step=0.001, format="%.3f m³/s")
    head = st.slider("Head pompa (H)", min_value=1, max_value=200, value=122, step=1, format="%d m")
    efisiensi_persen = st.slider("Efisiensi (η)", min_value=10, max_value=100, value=93, step=1, format="%d %%")

# --- PERHITUNGAN FISIKA ---
rho = 1000  # Massa jenis air (kg/m³)
g = 9.81    # Gravitasi (m/s²)
efisiensi = efisiensi_persen / 100.0

# Rumus Daya Hidrolik & Daya Motor
daya_hidrolik_kw = (rho * g * debit * head) / 1000
daya_motor_kw = daya_hidrolik_kw / efisiensi

with col_output:
    st.write("### DAYA YANG DIBUTUHKAN")
    st.markdown(f"""
    <div style="background-color: #f8f9fa; border: 1px solid #e9ecef; padding: 20px; border-radius: 10px; text-align: center;">
        <h1 style="margin: 0; color: #1e293b; font-size: 3rem;">{daya_motor_kw:.2f}</h1>
        <p style="margin: 0; font-weight: bold; color: #64748b; font-size: 1.2rem;">kW</p>
        <span style="background-color: #fee2e2; color: #ef4444; padding: 3px 10px; border-radius: 5px; font-size: 0.8rem; font-weight: bold;">
            Daya Aktif Sistem
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    col_sub1, col_sub2 = st.columns(2)
    with col_sub1:
        st.markdown(f"""
        <div style="background-color: #f1f5f9; padding: 10px; border-radius: 5px; text-align: center; margin-top: 10px;">
            <small style="color: #64748b;">Daya hidrolik</small>
            <h4 style="margin:0; color: #334155;">{daya_hidrolik_kw:.2f} kW</h4>
        </div>
        """, unsafe_allow_html=True)
    with col_sub2:
        st.markdown(f"""
        <div style="background-color: #f1f5f9; padding: 10px; border-radius: 5px; text-align: center; margin-top: 10px;">
            <small style="color: #64748b;">Setara kW</small>
            <h4 style="margin:0; color: #334155;">{daya_motor_kw:.3f} kW</h4>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# --- GRID TENGAH: VISUALISASI SKEMA PIPA ---
st.write("### VISUALISASI SISTEM POMPA")
fig_sys = go.Figure()

# Menggambar Jalur Pipa (Garis Abu-abu)
fig_sys.add_trace(go.Scatter(x=[1, 2.5, 2.5, 4, 4, 4.8], y=[1, 1, 3.5, 3.5, 3.2, 3.2], mode='lines', line=dict(color='#cbd5e1', width=12), hoverinfo='skip'))
# Reservoir Bawah & Atas
fig_sys.add_shape(type="rect", x0=0.2, y0=0.6, x1=1.2, y1=1.2, fillcolor="#bfdbfe", line=dict(color="#2563eb", width=2))
fig_sys.add_annotation(x=0.7, y=0.9, text="Reservoir<br>Bawah", showarrow=False, font=dict(color="#1e40af"))
fig_sys.add_shape(type="rect", x0=4.8, y0=2.7, x1=5.8, y1=3.5, fillcolor="#bfdbfe", line=dict(color="#2563eb", width=2))
fig_sys.add_annotation(x=5.3, y=3.1, text="Reservoir<br>Atas", showarrow=False, font=dict(color="#1e40af"))
# Motor Pompa
fig_sys.add_trace(go.Scatter(x=[2.0], y=[1.0], mode='markers', marker=dict(size=45, color='#bbf7d0', line=dict(color='#22c55e', width=3)), hoverinfo='skip'))
fig_sys.add_annotation(x=2.0, y=1.0, text="🔆", font=dict(size=18, color='#15803d'), showarrow=False)
fig_sys.add_annotation(x=2.0, y=0.5, text="<b>Motor Pompa</b>", font=dict(color='#b45309'), showarrow=False)
# Indikator Head Putus-putus
fig_sys.add_trace(go.Scatter(x=[6.1, 6.1], y=[1, 3.5], mode='lines', line=dict(color='#ef4444', width=2, dash='dash'), hoverinfo='skip'))
fig_sys.add_annotation(x=6.5, y=2.25, text=f"<b>H = {head} m</b>", font=dict(color='#ef4444'), showarrow=False)
# Badge Daya Aktual
fig_sys.add_annotation(x=0.6, y=3.5, text=f"🟢 P: {daya_motor_kw:.2f} kW", showarrow=False, bordercolor="#e2e8f0", borderpad=6, bgcolor="#334155", font=dict(color="#ffffff", size=12))

fig_sys.update_layout(xaxis=dict(visible=False, range=[0, 7]), yaxis=dict(visible=False, range=[0, 4]), margin=dict(l=0, r=0, t=10, b=10), height=280, showlegend=False, plot_bgcolor="white")
st.plotly_chart(fig_sys, use_container_width=True)

st.markdown("---")

# --- GRID BAWAH: GRAFIK KARAKTERISTIK (DEBIT VS HEAD & DAYA) ---
st.write("### GRAFIK ANALISIS KARAKTERISTIK POMPA")

col_chart1, col_chart2 = st.columns(2)

# Generate rentang nilai Q untuk visualisasi kurva kontinu
q_range = np.linspace(0.001, 0.250, 100)

with col_chart1:
    st.write("#### 📈 Kurva Performa: Head (H) vs Debit (Q)")
    # Simulasi kurva H-Q pompa sentrifugal aktual (makin besar debit, head turun)
    h_curve = 180 - (q_range**2 * 1500) 
    
    fig_hq = go.Figure()
    # Kurva referensi pompa
    fig_hq.add_trace(go.Scatter(x=q_range, y=h_curve, mode='lines', name='Karakteristik Pompa', line=dict(color='#64748b', width=3)))
    # Titik Operasi Kerja Saat ini berdasarkan slider
    fig_hq.add_trace(go.Scatter(x=[debit], y=[head], mode='markers', name='Titik Kerja', marker=dict(color='#ef4444', size=14, symbol='cross')))
    
    
