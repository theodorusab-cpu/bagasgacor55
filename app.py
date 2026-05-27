# ===============================
# 🔥 VISUALISASI SISTEM + FLOW ANIMASI
# ===============================
st.write("### VISUALISASI SISTEM POMPA (ANIMASI)")

t = np.linspace(1, 4.8, 30)

fig_sys = go.Figure()

# Pipa utama
fig_sys.add_trace(go.Scatter(
    x=[1, 2.5, 2.5, 4, 4, 4.8],
    y=[1, 1, 3.5, 3.5, 3.2, 3.2],
    mode='lines',
    line=dict(color='#cbd5e1', width=12),
    hoverinfo='skip'
))

# Flow animasi (gelembung air)
frames_pipe = []
for i in range(len(t)):
    frames_pipe.append(go.Frame(
        data=[go.Scatter(
            x=[t[i]],
            y=[np.interp(t[i], [1, 2.5, 4.8], [1, 3.5, 3.2])],
            mode='markers',
            marker=dict(size=10, color='blue')
        )]
    ))

fig_sys.add_trace(go.Scatter(
    x=[t[0]],
    y=[1],
    mode='markers',
    marker=dict(size=10, color='blue')
))

fig_sys.frames = frames_pipe

fig_sys.update_layout(
    updatemenus=[{
        "type": "buttons",
        "buttons": [
            {"label": "▶ Flow", "method": "animate", "args": [None]},
            {"label": "⏸ Stop", "method": "animate", "args": [[None], {"mode": "immediate"}]}
        ]
    }],
    xaxis=dict(visible=False, range=[0, 7]),
    yaxis=dict(visible=False, range=[0, 4]),
    height=300,
    plot_bgcolor="white"
)

st.plotly_chart(fig_sys, use_container_width=True)


# ===============================
# 🔥 GRAFIK 3D INTERAKTIF
# ===============================
st.write("### GRAFIK 3D PERFORMA POMPA")

q_range = np.linspace(0.001, 0.25, 100)
h_curve = 180 - (q_range**2 * 1500)
power_curve = (rho * g * q_range * h_curve) / 1000

fig_3d = go.Figure()

fig_3d.add_trace(go.Scatter3d(
    x=q_range,
    y=h_curve,
    z=power_curve,
    mode='lines',
    line=dict(width=6, color=power_curve, colorscale='Viridis'),
    name='Kurva Pompa'
))

fig_3d.add_trace(go.Scatter3d(
    x=[debit],
    y=[head],
    z=[daya_motor_kw],
    mode='markers',
    marker=dict(size=6, color='red'),
    name='Titik Kerja'
))

fig_3d.update_layout(
    scene=dict(
        xaxis_title='Debit (Q)',
        yaxis_title='Head (H)',
        zaxis_title='Daya (kW)'
    ),
    height=500
)

st.plotly_chart(fig_3d, use_container_width=True)


# ===============================
# 🔥 ANIMASI KURVA (AIR MENGALIR)
# ===============================
st.write("### ANIMASI KURVA ALIRAN")

frames = []
for i in range(len(q_range)):
    frames.append(go.Frame(
        data=[
            go.Scatter(
                x=q_range[:i+1],
                y=h_curve[:i+1],
                mode='lines',
                line=dict(color='#64748b', width=3)
            ),
            go.Scatter(
                x=[q_range[i]],
                y=[h_curve[i]],
                mode='markers',
                marker=dict(size=12, color='blue')
            )
        ]
    ))

fig_anim = go.Figure(
    data=[
        go.Scatter(x=q_range, y=h_curve, mode='lines', line=dict(color='lightgray')),
        go.Scatter(x=[q_range[0]], y=[h_curve[0]], mode='markers')
    ],
    frames=frames
)

fig_anim.update_layout(
    updatemenus=[{
        "type": "buttons",
        "buttons": [
            {"label": "▶ Play", "method": "animate", "args": [None]},
            {"label": "⏸ Pause", "method": "animate", "args": [[None], {"mode": "immediate"}]}
        ]
    }],
    height=400
)

st.plotly_chart(fig_anim, use_container_width=True)
