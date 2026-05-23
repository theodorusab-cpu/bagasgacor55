import streamlit as st
import plotly.graph_objects as go

# Set layout halaman menjadi lebar agar mirip dashboard profesional
st.set_page_config(layout="wide", page_title="Kalkulator Daya Pompa Air")

st.title("🚰 Daya Pompa Air")
st.caption("Estimasi daya listrik yang dibutuhkan berdasarkan parameter pompa")

# --- GRID ATAS: INPUT PARAMETER & OUTPUT DAYA ---
col_input, col_output = st.columns([4, 4])

with col_input:
    st.write("## INPUT")
    
    # Slider Input sesuai gambar
    debit = st.slider("Debit air (Q)", min_value=0.001, max_value=0.200, value=0.086, step=0.001, format="%.3f m³/s")
    head = st.slider("Head pompa (H)", min_value=1, max_value=200, value=122, step=1, format="%d m")
    efisiensi_persen = st.slider("Efisiensi (η)", min_value=10, max_value=100, value=93, step=1, format="%d %%")

# --- PERHITUNGAN FISIKA ---
# Massa jenis air (rho) = 1000 kg/m³
# Percepatan gravitasi (g) = 9.81 m/s²
rho = 1000
g = 9.81
efisiensi = efisiensi_persen / 100.0

# Rumus Daya Hidrolik (Water Power): P_hidrolik = rho * g * Q * H (dalam Watt)
daya_hidrolik_w = rho * g * debit * head
daya_hidrolik_kw = daya_hidrolik_w / 1000

# Rumus Daya Poros/Listrik Motor: P_motor = P_hidrolik / efisiensi
daya_motor_kw = daya_hidrolik_kw / efisiensi

with col_output:
    st.write("### DAYA YANG DIBUTUHKAN")
    
    # Desain kotak nilai utama menggunakan HTML/CSS bawaan Streamlit
    st.markdown(f"""
    <div style="background-color: #f8f9fa; border: 1px solid #e9ecef; padding: 20px; border-radius: 10px; text-align: center;">
        <h1 style="margin: 0; color: #1e293b; font-size: 3rem;">{daya_motor_kw:.2f}</h1>
        <p style="margin: 0; font-weight: bold; color: #64748b; font-size: 1.2rem;">kW</p>
        <span style="background-color: #fee2e2; color: #ef4444; padding: 3px 10px; border-radius: 5px; font-size: 0.8rem; font-weight: bold;">
            Daya sangat besar
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    # Sub-informasi daya hidrolik dan kW setara di bawahnya
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

# --- GRID BAWAH: VISUALISASI SISTEM PIPING (2D PLOTLY) ---
st.write("### VISUALISASI SISTEM POMPA")

# Membuat skema pipa dan komponen menggunakan grafik Scatter Plotly
fig_sys = go.Figure()

# 1. Menggambar Jalur Pipa (Garis Abu-abu Tebal)
pipa_x = [1, 2.5, 2.5, 4, 4, 4.8]
pipa_y = [1, 1, 3.5, 3.5, 3.2, 3.2]
fig_sys.add_trace(go.Scatter(
    x=pipa_x, y=pipa_y,
    mode='lines',
    line=dict(color='#cbd5e1', width=12),
    hoverinfo='skip'
))

# 2. Reservoir Bawah (Kotak Biru Kiri)
fig_sys.add_shape(type="rect", x0=0.2, y0=0.6, x1=1.2, y1=1.2,
    fillcolor="#bfdbfe", line=dict(color="#2563eb", width=2))
fig_sys.add_annotation(x=0.7, y=0.9, text="Reservoir<br>Bawah", showarrow=False, font=dict(color="#1e40af"))

# 3. Reservoir Atas (Kotak Biru Kanan)
fig_sys.add_shape(type="rect", x0=4.8, y0=2.7, x1=5.8, y1=3.5,
    fillcolor="#bfdbfe", line=dict(color="#2563eb", width=2))
fig_sys.add_annotation(x=5.3, y=3.1, text="Reservoir<br>Atas", showarrow=False, font=dict(color="#1e40af"))

# 4. Motor Pompa (Lingkaran Hijau di Tengah)
fig_sys.add_trace(go.Scatter(
    x=[2.0], y=[1.0],
    mode='markers+text',
    marker=dict(size=45, color='#bbf7d0', line=dict(color='#22c55e', width=3)),
    hoverinfo='skip'
))
# Simbol impeller di dalam lingkaran pompa
fig_sys.add_annotation(x=2.0, y=1.0, text="🔆", font=dict(size=18, color='#15803d'), showarrow=False)
fig_sys.add_annotation(x=2.0, y=0.5, text="<b>Motor Pompa</b>", font=dict(color='#b45309'), showarrow=False)

# 5. Indikator Panah Aliran Air
fig_sys.add_annotation(x=1.6, y=1.1, text="▶", font=dict(size=12, color='#2563eb'), showarrow=False)
fig_sys.add_annotation(x=4.4, y=3.6, text="▶", font=dict(size=12, color='#2563eb'), showarrow=False)

# 6. Garis Indikator Head Pompa (H) di sebelah kanan
fig_sys.add_trace(go.Scatter(
    x=[6.1, 6.1], y=[1, 3.5],
    mode='lines',
    line=dict(color='#ef4444', width=2, dash='dash'),
    hoverinfo='skip'
))
fig_sys.add_annotation(x=6.5, y=2.25, text=f"<b>H = {head} m</b>", font=dict(color='#ef4444'), showarrow=False)

# 7. Badge Indikator Daya Listrik Aktif (P) di pojok kiri atas visualisasi
fig_sys.add_annotation(
    x=0.6, y=3.5,
    text=f"🟢 P: {daya_motor_kw:.2f} kW",
    showarrow=False,
    bordercolor="#e2e8f0",
    borderpad=6,
    bgcolor="#334155",
    font=dict(color="#ffffff", size=12)
)

# Pengaturan Layout diagram supaya bersih tanpa sumbu grid
fig_sys.update_layout(
    xaxis=dict(visible=False, range=[0, 7]),
    yaxis=dict(visible=False, range=[0, 4]),
    margin=dict(l=0, r=0, t=10, b=10),
    height=350,
    showlegend=False,
    plot_bgcolor="white"
)

st.plotly_chart(fig_sys, use_container_width=True)
