import streamlit as st
import plotly.graph_objects as go
import numpy as np

# Layout
st.set_page_config(layout="wide", page_title="Kalkulator Daya Pompa Air")

st.title("🚰 Daya Pompa Air & Kurva Performa")
st.caption("Estimasi daya listrik dan analisis grafik karakteristik pompa")

# --- INPUT & OUTPUT ---
col_input, col_output = st.columns([4, 4])

with col_input:
    st.write("### PARAMETER INPUT")
    debit = st.slider("Debit air (Q)", 0.001, 0.200, 0.086, step=0.001)
    head = st.slider("Head pompa (H)", 1, 200, 122)
    efisiensi_persen = st.slider("Efisiensi (%)", 10, 100, 93)

# --- PERHITUNGAN ---
rho = 1000
g = 9.81
efisiensi = efisiensi_persen / 100

daya_hidrolik_kw = (rho * g * debit * head) / 1000
daya_motor_kw = daya_hidrolik_kw / efisiensi

with col_output:
    st.write("### DAYA YANG DIBUTUHKAN")
    st.metric("Daya Motor (kW)", f"{daya_motor_kw:.2f}")
    st.metric("Daya Hidrolik (kW)", f"{daya_hidrolik_kw:.2f}")

st.markdown("---")

# --- VISUALISASI SISTEM ---
st.write("### VISUALISASI SISTEM POMPA")

fig_sys = go.Figure()

fig_sys.add_trace(go.Scatter(
    x=[1, 2.5, 2.5, 4, 4, 4.8],
    y=[1, 1, 3.5, 3.5, 3.2, 3.2],
    mode='lines',
    line=dict(color='gray', width=10),
    showlegend=False
))

fig_sys.add_annotation(x=2, y=1, text="Pompa", showarrow=False)

fig_sys.update_layout(
    xaxis=dict(visible=False),
    yaxis=dict(visible=False),
    height=300
)

st.plotly_chart(fig_sys, use_container_width=True)

st.markdown("---")

# --- GRAFIK ---
st.write("### GRAFIK KARAKTERISTIK POMPA")

col1, col2 = st.columns(2)

q_range = np.linspace(0.001, 0.25, 100)

# Kurva Head
with col1:
    st.write("#### Kurva Head vs Debit")

    h_curve = 180 - (q_range**2 * 1500)

    fig_hq = go.Figure()

    fig_hq.add_trace(go.Scatter(
        x=q_range,
        y=h_curve,
        mode='lines',
        name='Kurva Pompa'
    ))

    fig_hq.add_trace(go.Scatter(
        x=[debit],
        y=[head],
        mode='markers',
        name='Titik Kerja',
        marker=dict(size=12)
    ))

    fig_hq.update_layout(
        xaxis_title="Debit (m³/s)",
        yaxis_title="Head (m)"
    )

    st.plotly_chart(fig_hq, use_container_width=True)

# Kurva Daya
with col2:
    st.write("#### Kurva Daya vs Debit")

    power_curve = (rho * g * q_range * head) / (1000 * efisiensi)

    fig_pq = go.Figure()

    fig_pq.add_trace(go.Scatter(
        x=q_range,
        y=power_curve,
        mode='lines',
        name='Kurva Daya'
    ))

    fig_pq.add_trace(go.Scatter(
        x=[debit],
        y=[daya_motor_kw],
        mode='markers',
        name='Titik Kerja',
        marker=dict(size=12)
    ))

    fig_pq.update_layout(
        xaxis_title="Debit (m³/s)",
        yaxis_title="Daya (kW)"
    )

    st.plotly_chart(fig_pq, use_container_width=True)
