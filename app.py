import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time

st.set_page_config(layout="wide") # Mengubah layout jadi lebar agar grafik muat di samping

st.title("🚰 Simulasi Pompa & Grafik Debit")

# Sidebar untuk Kontrol
st.sidebar.header("Kontrol Simulasi")
run = st.sidebar.toggle("Jalankan Animasi", value=False)
debit = st.sidebar.slider("Debit Air (L/s)", 0.01, 0.20, 0.05, step=0.01)

# Menggunakan kolom agar animasi pompa dan grafik berada berdampingan
col1, col2 = st.columns(2)

with col1:
    st.subheader("Animasi Pompa 3D")
    pump_placeholder = st.empty()

with col2:
    st.subheader("Grafik Debit Real-Time")
    chart_placeholder = st.empty()

# Menyimpan riwayat data untuk grafik di session state
if "time_steps" not in st.session_state:
    st.session_state.time_steps = []
if "debit_history" not in st.session_state:
    st.session_state.debit_history = []
if "angle" not in st.session_state:
    st.session_state.angle = 0

def create_pump_frame(angle, debit):
    # Buat bodi pompa (Cylinder)
    theta = np.linspace(0, 2*np.pi, 40)
    z = np.linspace(0, 5, 20)
    theta, z = np.meshgrid(theta, z)
    r = 1.5
    x = r * np.cos(theta)
    y = r * np.sin(theta)

    fig = go.Figure()
    # 1. BODY POMPA
    fig.add_surface(x=x, y=y, z=z, opacity=0.15, showscale=False, colorscale='Blues')

    # 2. IMPELLER / BALING-BALING (berputar)
    for k in range(4):
        a = np.radians(angle + k * 90)
        fig.add_trace(go.Scatter3d(
            x=[0, 1.4 * np.cos(a)],
            y=[0, 1.4 * np.sin(a)],
            z=[2.5, 2.5],
            mode='lines',
            line=dict(width=8, color='darkorange'),
            name=f'Baling {k+1}'
        ))

    # 3. ALIRAN AIR (Efek spiral naik dipengaruhi debit)
    t = np.linspace(0, 5, 60)
    flow_speed = 5 + debit * 100
    water_x = 0.8 * np.cos(t * flow_speed + np.radians(angle))
    water_y = 0.8 * np.sin(t * flow_speed + np.radians(angle))
    
    fig.add_trace(go.Scatter3d(
        x=water_x, y=water_y, z=t,
        mode='markers',
        marker=dict(size=4, color='deepskyblue', opacity=0.7),
        name='Aliran Air'
    ))

    fig.update_layout(
        scene=dict(
            xaxis=dict(visible=False, range=[-2, 2]),
            yaxis=dict(visible=False, range=[-2, 2]),
            zaxis=dict(visible=False, range=[0, 5]),
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False,
        height=450
    )
    return fig

def create_chart_frame(time_steps, debit_history):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=time_steps, 
        y=debit_history, 
        mode='lines+markers', 
        line=dict(color='royalblue', width=3),
        marker=dict(size=6)
    ))
    fig.update_layout(
        xaxis_title="Waktu (Detik Ke-)",
        yaxis_title="Debit Air (L/s)",
        yaxis=dict(range=[0, 0.25]),
        margin=dict(l=40, r=20, t=20, b=40),
        height=450
    )
    return fig

# --- LOOP ANIMASI UTAMA ---
if run:
    # Ambil penanda waktu mulai jika belum ada
    start_time = time.time()
    
    # Loop animasi berjalan terus selama tombol toggle "Jalankan Animasi" bernilai True
    while run:
        # 1. Update sudut rotasi baling-baling
        st.session_state.angle = (st.session_state.angle + 12) % 360
        
        # 2. Update data grafik berdasarkan waktu berjalan
        current_tick = round(time.time() - start_time, 1)
        
        # Batasi riwayat grafik hanya sampai 20 data terakhir agar tidak berat
        if len(st.session_state.time_steps) == 0 or st.session_state.time_steps[-1] != current_tick:
            st.session_state.time_steps.append(current_tick)
            st.session_state.debit_history.append(debit)
            
            if len(st.session_state.time_steps) > 20:
                st.session_state.time_steps.pop(0)
                st.session_state.debit_history.pop(0)

        # 3. Render komponen 3D ke kolom 1
        fig_pump = create_pump_frame(st.session_state.angle, debit)
        pump_placeholder.plotly_chart(fig_pump, use_container_width=True, key=f"pump_{st.session_state.angle}")

        # 4. Render komponen Grafik ke kolom 2
        fig_chart = create_chart_frame(st.session_state.time_steps, st.session_state.debit_history)
        chart_placeholder.plotly_chart(fig_chart, use_container_width=True, key=f"chart_{current_tick}")

        # 5. Jeda waktu kecil agar animasi halus (smooth)
        time.sleep(0.05)
        
else:
    # Kondisi saat animasi dimatikan / standby
    fig_pump_static = create_pump_frame(st.session_state.angle, debit)
    pump_placeholder.plotly_chart(fig_pump_static, use_container_width=True)
    
    if st.session_state.time_steps:
        fig_chart_static = create_chart_frame(st.session_state.time_steps, st.session_state.debit_history)
        chart_placeholder.plotly_chart(fig_chart_static, use_container_width=True)
    else:
        chart_placeholder.info("Nyalakan toggle di sidebar untuk melihat pergerakan grafik debit secara real-time.")
