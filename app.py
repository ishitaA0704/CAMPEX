import streamlit as st
import json
import time
import pandas as pd

st.set_page_config(page_title="CAMPEX: MSRIT BESCOM Shield", layout="wide")
st.title("⚡ CAMPEX: Level-5 Autonomous Adversarial Twin")

# 1. State Management for the Graph
if "kva_history" not in st.session_state:
    st.session_state.kva_history = [450] * 50 # Pre-fill with normal data

# 2. Safe File Readers
def read_json_safe(filepath, fallback_data):
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except: # If Ishita/Sandeep are mid-write, don't crash. Use fallback.
        return fallback_data

telemetry = read_json_safe("telemetry.json", {
    "fault_active": False,
    "telemetry": {"apex_block_kw": 120, "desh_block_kw": 110, "hostel_grid_kw": 95, "stp_blowers_kw": 70, "water_pumps_kw": 35}
})

action = read_json_safe("action.json", {
    "status": "standby", "target_asset": "none", "shed_percentage": 0, "justification": ""
})

# 3. The Physics & Math Engine
t_data = telemetry["telemetry"]
raw_total_kw = sum(t_data.values())

# Apply Sandeep's AI Fix if executed
stp_actual_kw = t_data["stp_blowers_kw"]
if action["status"] == "executed" and action["target_asset"] == "STP_blowers":
    shed_amount = t_data["stp_blowers_kw"] * (action["shed_percentage"] / 100.0)
    raw_total_kw -= shed_amount
    stp_actual_kw -= shed_amount
    do_level = 1.4 # Biological consequence of throttling
else:
    do_level = 2.2 # Normal operations

# Convert to kVA (Assuming 0.95 Power Factor)
current_kva = raw_total_kw / 0.95

# Update History
st.session_state.kva_history.append(current_kva)
if len(st.session_state.kva_history) > 60:
    st.session_state.kva_history.pop(0)

# 4. The War Room UI
col1, col2, col3 = st.columns(3)

# Critical Alerts
if current_kva > 500 and action["status"] != "executed":
    st.error("🚨 CRITICAL: MAXIMUM DEMAND EXCEEDED (500 kVA). 15:00 UNTIL ₹85,000 PENALTY.")
elif action["status"] == "executed":
    st.success(f"🤖 AI SWARM INTERVENTION: {action['justification']}")

with col1:
    st.metric("MSRIT Total Load (kVA)", f"{current_kva:.1f}", delta=f"{current_kva - 452:.1f} from baseline" if telemetry["fault_active"] else None, delta_color="inverse")
with col2:
    st.metric("STP Blower Power (kW)", f"{stp_actual_kw:.1f}", delta=f"-{action['shed_percentage']}%" if action["status"] == "executed" else None)
with col3:
    st.metric("STP Dissolved Oxygen (mg/L)", f"{do_level}", delta="-0.8 (Safe Limit: 1.0)" if do_level < 2.0 else None)

# 5. Live Adversarial Graph
st.subheader("Live Power Grid vs. BESCOM Limit")
chart_data = pd.DataFrame({
    "Actual Campus Load (kVA)": st.session_state.kva_history,
    "BESCOM Penalty Limit": [500] * len(st.session_state.kva_history)
})
st.line_chart(chart_data, color=["#1f77b4", "#d62728"])

# 6. Auto-Refresh Loop
time.sleep(1)
st.rerun()
