import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time

st.title("💧 Pompa 3D Gacor Edition")

run = st.toggle("Jalankan Animasi")

placeholder = st.empty()

debit = st.slider("Debit", 0.01, 0.2, 0.05)

def create_frame(angle):
    theta = np.linspace(0, 2*np.pi, 40)
    z = np.linspace(0, 5, 20)
    theta, z = np.meshgrid(theta, z)

    r = 1.5
    x = r * np.cos(theta)
    y = r * np.sin(theta)

    fig = go.Figure()

    # BODY POMPA (silinder transparan)
    fig.add_surface(x=x, y=y, z=z, opacity=0.3, showscale=False)

    # IMPELLER (4 blade)
    for k in range(4):
        a = np.radians(angle + k*90)
        fig.add_trace(go.Scatter3d(
            x=[0, np.cos(a)],
            y=[0, np.sin(a)],
            z=[2.5, 2.5],
            mode='lines',
            line=dict(width=6)
        ))

    # AIR PARTIKEL
    t = np.linspace(0, 1, 20)
    fig.add_trace(go.Scatter3d(
        x=np.sin(t*10 + angle/10),
        y=np.zeros_like(t),
        z=t*5,
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


if run:
    angle = 0
    while True:
        fig = create_frame(angle)
        placeholder.plotly_chart(fig, use_container_width=True)
        angle += 10
        time.sleep(0.05)
