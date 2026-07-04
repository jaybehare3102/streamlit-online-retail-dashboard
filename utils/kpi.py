import streamlit as st

def render_kpi_cards(metrics):

    cols = st.columns(len(metrics))

    for col, (icon, title, value) in zip(cols, metrics):

        with col:
            st.markdown(
                f"""
<div class="kpi-card">
    <div class="kpi-icon">{icon}</div>
    <div class="kpi-title">{title}</div>
    <div class="kpi-value">{value}</div>
</div>
""",
                unsafe_allow_html=True
            )