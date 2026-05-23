import streamlit as st
import numpy as np
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh

# Mengatur layout menjadi wide (lebar) agar muat 2 kolom sampingan
st.set_page_config(layout="wide")

st.title("🚰 Pompa (Improved Animation & Real-Time Chart)")

# Kontrol diletakkan di Sidebar agar tampilan utama fokus pada visual
st.sidebar.header("Kontrol Simulasi")
run = st.sidebar.toggle("Jalankan Animasi", value=True)
debit = st.sidebar.slider("Debit Air", 0.01, 0.20, 0.05, step=0.01)

# Inisialisasi session state untuk menyimpan data animasi dan grafik
if "angle" not in st.session_state:
    st.session_state.angle = 0
if "chart_time" not in st.session_state:
    st.session_state.chart_time = list(range(20))
if "chart_debit" not in st.session_state:
    st.session_state.chart_debit = [debit] * 20

# Trigger refresh otomatis setiap 50ms jika tombol "Jalankan Animasi" aktif
if run:
    st_autorefresh(interval=50, key="pump_refresh")
    # Naikkan sudut putaran baling-baling setiap refresh
    st.session_state.angle = (st.session_state.angle + 10) % 360
    
    # Update data grafik (geser data lama, masukkan data debit terbaru)
    st.session_state.chart_debit.pop(0)
    st.session_state.chart_debit.append(debit)

# Membagi halaman menjadi 2 kolom
col1, col2 = st.columns(2)

# --- KOLOM 1: ANIMASI POMPA 3D ---
with col1:
    st.subheader("Visualisasi Pompa 3D")
    
    # Membuat bodi tabung pompa
    theta = np.linspace(0, 2 * np.pi, 40)
    z = np.linspace(0, 5, 20)
    theta, z = np.meshgrid(theta, z)
    r = 1.5
    x = r * np.cos(theta)
    y = r * np.sin(theta)

    fig_pump = go.Figure()

    # 1. BODY POMPA (Silinder Transparan)
    fig_pump.add_surface(x=x, y=y, z=z, opacity=0.15, showscale=False, colorscale='Blues')

    # 2. IMPELLER / BALING-BALING (Berputar di tengah tabung)
    for k in range(4):
        a = np.radians(st.session_state.angle + k * 90)
        fig_pump.add_trace(go.Scatter3d(
            x=[0, 1.3 * np.cos(a)],
            y=[0, 1.3 * np.sin(a)],
            z=[2.5, 2.5],
            mode='lines',
            line=dict(width=8, color='orange'),
            showlegend=False
        ))

    # 3. ALIRAN AIR (Efek spiral naik, kecepatannya dipengaruhi nilai debit)
    t = np.linspace(0, 5, 50)
    flow_speed = 5 + (debit * 80)  # Semakin besar debit, putaran air makin cepat naik
    water_x = 0.8 * np.cos(t * flow_speed + np.radians(st.session_state.angle))
    water_y = 0.8 * np.sin(t * flow_speed + np.radians(st.session_state.angle))
    
    fig_pump.add_trace(go.Scatter3d(
        x=water_x, y=water_y, z=t,
        mode='markers',
        marker=dict(size=4, color='cyan', opacity=0.8),
        showlegend=False
    ))

    # Pengaturan sudut pandang & menghilangkan akses sumbu xyz agar estetik
    fig_pump.update_layout(
        scene=dict(
            xaxis=dict(visible=False, range=[-2, 2]),
            yaxis=dict(visible=False, range=[-2, 2]),
            zaxis=dict(visible=False, range=[0, 5]),
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        height=450
    )
    
    st.plotly_chart(fig_pump, use_container_width=True)

# --- KOLOM 2: GRAFIK MONITORING DEBIT ---
with col2:
    st.subheader("Grafik Monitoring Debit")
    
    fig_chart = go.Figure()
    fig_chart.add_trace(go.Scatter(
        x=st.session_state.chart_time,
        y=st.session_state.chart_debit,
        mode='lines+markers',
        line=dict(color='dodgerblue', width=3),
        marker=dict(size=6)
    ))
    
    fig_chart.update_layout(
        xaxis=dict(title="Waktu (Siklus)", showgrid=True),
        yaxis=dict(title="Debit Air", range=[0, 0.25], showgrid=True),
        margin=dict(l=40, r=20, t=20, b=40),
        height=450
    )
    
    st.plotly_chart(fig_chart, use_container_width=True)

# Teks Informasi Status
if not run:
    st.info("💡 Animasi sedang dihentikan. Aktifkan 'Jalankan Animasi' pada sidebar untuk mulai memutar pompa.")
