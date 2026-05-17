import streamlit as st
import pandas as pd
import time
import numpy as np
import sounddevice as sd
from streamlit_autorefresh import st_autorefresh

# 1. Page Config
st.set_page_config(page_title="EcoEcho Pro", page_icon="🔊", layout="wide")

# 2. Initialize Session State
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'monitoring' not in st.session_state:
    st.session_state.monitoring = False

# 3. Sidebar Logic
with st.sidebar:
    st.title("🔐 Authentication")
    if not st.session_state.logged_in:
        user_input = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if user_input == "admin" and password == "pune123":
                st.session_state.logged_in = True
                st.rerun()
    else:
        st.write(f"Welcome, Admin!")
        # Start/Stop Buttons
        st.markdown("---")
        st.subheader("Process Control")
        if not st.session_state.monitoring:
            if st.button("▶️ Start Monitoring", use_container_width=True):
                st.session_state.monitoring = True
                st.rerun()
        else:
            if st.button("🛑 Stop Monitoring", use_container_width=True, type="primary"):
                st.session_state.monitoring = False
                st.rerun()
        
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.monitoring = False
            st.rerun()

# 4. Main App Interface
if st.session_state.logged_in:
    st.title("🔊 Noise Pollution Dashboard")

    if st.session_state.monitoring:
        # Trigger refresh only when monitoring is active
        st_autorefresh(interval=2000, key="datarefresh")
        
        try:
            df = pd.read_csv("noise_log.csv")
            
            # 4-Column Metric Layout
            col1, col2, col3, col4 = st.columns(4)
            current_val = round(df['Decibel_Level'].iloc[-1], 1)
            max_val = round(df['Decibel_Level'].max(), 1)
            min_val = round(df['Decibel_Level'].min(), 1)

            col1.metric("Live (dB)", f"{current_val}")
            col2.metric("Peak (dB)", f"{max_val}")
            col3.metric("Min (dB)", f"{min_val}")
            col4.metric("Status", "Safe ✅" if current_val < 70 else "Loud ⚠️")

            st.area_chart(df.tail(100).set_index('Timestamp')['Decibel_Level'], color="#1E3A8A")
            
        except Exception:
            st.info("Waiting for data from monitor.py...")
    else:
        st.warning("Monitoring is currently PAUSED. Click 'Start Monitoring' in the sidebar to begin.")