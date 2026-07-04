import streamlit as st
from datetime import datetime


def page_header(title, subtitle):

    today = datetime.now().strftime("%d %B %Y")

    st.markdown(f"""
    <div style="
    background:linear-gradient(90deg,#0f172a,#1e3a8a,#2563eb);
    padding:25px;
    border-radius:20px;
    margin-bottom:20px;
    ">

    <h1 style="color:white;margin-bottom:5px;">
    {title}
    </h1>

    <h4 style="color:#cbd5e1;">
    {subtitle}
    </h4>

    <hr>

    <div style="
    display:flex;
    justify-content:space-between;
    color:white;
    ">

    <span>📅 Last Refresh : {today}</span>

    <span>📊 Business Intelligence Dashboard</span>

    </div>

    </div>
    """, unsafe_allow_html=True)