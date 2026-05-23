import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.title("🚰 Pompa (Improved Animation)")

run = st.toggle("Jalankan Animasi")

debit = st.slider("Debit", 0.01, 0.2, 0.05)

placeholder = st.empty()

# simpan angle di session_state biar tidak reset terus
if "angle" not in st.session_state:
    st.session_state.angle = 0


def create_frame(angle, debit):
    theta = np.linspace(0, 2*np.pi, 40)
    z = np.linspace(0, 5, 20)
    theta, z = np.meshgrid(theta, z)

    r = 1.5
    x = r * np.cos(theta)
    y = r * np.sin(theta)

    fig = go.Figure()

    # BODY POMPA
    fig.add_surface(x=x, y=y, z=z, opacity=0.25, showscale=False)

    # IMPELLER (berputar)
    for k in range(4):
        a = np.radians(angle + k * 90)
        fig.add_trace(go.Scatter3d(
            x=[0, np.cos(a)],
            y=[0, np.sin(a)],
            z=[2.5, 2.5],
            mode='lines',
            line=dict(width=6, color='orange')
        ))

    # AIR FLOW (dipengaruhi debit)
    t = np.linspace(0, 1, 30)
    flow_speed = 10 + debit * 50

    fig.add_trace(go.Scatter3d(
        x=np.sin(t * flow_speed + angle/10),
        y=np.zeros_like(t),
        z=t * 5,
        mode='markers',
        marker=dict(size=3, color='cyan')
    ))

    fig.update_layout(
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
        ),
        margin=dict(l=0, r=0, t=0, b=0)
    )

    return fig


# ANIMASI LOOP AMAN (tanpa while True)
if run:
    st.session_state.angle += 8
    fig = create_frame(st.session_state.angle, debit)
    placeholder.plotly_chart(fig, use_container_width=True)
    st.autorefresh(interval=50, key="pump_refresh")
else:
    placeholder.info("Matikan toggle untuk menghentikan animasi.")
