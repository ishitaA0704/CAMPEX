import streamlit as st
import json
import time
import os
import pandas as pd

# 1. Page Config
st.set_page_config(page_title="CAMPEX: MSRIT BESCOM Shield", layout="wide", page_icon="⚡")

# Custom CSS for polished aesthetic
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
        color: #e0e0e0;
    }
    .metric-card {
        background-color: #1e222b;
        border-radius: 10px;
        padding: 15px;
        border: 1px solid #30363d;
    }
</style>
""", unsafe_allow_html=True)

st.title("⚡ CAMPEX: MSRIT Autonomous Power Shield")
st.caption("Campus Resource & Anomaly Exchange | HT-2b BESCOM Demand Manager")

# 2. Session state history for live chart
if "power_history" not in st.session_state:
    st.session_state.power_history = []

# 3. Read shared state JSON
state_file_path = os.path.join(os.path.dirname(__file__), "state.json")

def read_state():
    try:
        with open(state_file_path, "r") as f:
            return json.load(f)
    except Exception:
        return {
            "base_campus_kw": 330.0,
            "apex_kw": 120.0,
            "ai_target": "none",
            "ai_throttle_percent": 0
        }

state = read_state()

# 4. Physics Engine calculations
stp_max_kw = 100.0
throttle_pct = state.get("ai_throttle_percent", 0)
stp_current_kw = stp_max_kw * (1.0 - (throttle_pct / 100.0))

total_kva = state.get("base_campus_kw", 330.0) + state.get("apex_kw", 120.0)

if throttle_pct > 0:
    total_kva = total_kva - (stp_max_kw - stp_current_kw)
    do_level = 1.2
    esg_message = "✅ Crisis Averted. BESCOM Penalty Avoided: ₹85,000. Biological Safety of MSRIT STP Maintained."
else:
    do_level = 2.5
    esg_message = "Normal Operations."

st.session_state.power_history.append(total_kva)
if len(st.session_state.power_history) > 60:
    st.session_state.power_history.pop(0)

# 5. UI Banner Alerts
if total_kva > 500:
    st.error("🚨 WARNING: MAXIMUM DEMAND EXCEEDED (500 kVA limit). 15:00 UNTIL ₹85,000 BESCOM PENALTY!")
elif throttle_pct > 0:
    st.success(esg_message)

# Metric Display Columns
col1, col2, col3 = st.columns(3)

with col1:
    delta_val = total_kva - 450.0
    st.metric(
        label="Total Campus Demand (kVA)",
        value=f"{total_kva:.1f} kVA",
        delta=f"{delta_val:+.1f} kVA vs nominal" if abs(delta_val) > 0.1 else "Nominal",
        delta_color="inverse"
    )

with col2:
    st.metric(
        label="STP Blowers Load (kW)",
        value=f"{stp_current_kw:.1f} kW",
        delta=f"-{throttle_pct}% Throttled" if throttle_pct > 0 else "100% Full Power"
    )

with col3:
    st.metric(
        label="STP Dissolved Oxygen (mg/L)",
        value=f"{do_level:.1f} mg/L",
        delta="-1.3 mg/L (Safe Latency)" if do_level < 2.0 else "Optimal"
    )

st.markdown("---")

# 6. Live Chart Section
st.subheader("📈 Live Campus Load vs. BESCOM 500 kVA Threshold")
chart_df = pd.DataFrame({
    "Campus Load (kVA)": st.session_state.power_history,
    "BESCOM Max Demand Limit (500 kVA)": [500.0] * len(st.session_state.power_history)
})
st.line_chart(chart_df, color=["#ff4b4b" if total_kva > 500 else "#00d4b1", "#ff0000"])

# 7. Auto-refresh every 1 second
time.sleep(1)
st.rerun()
