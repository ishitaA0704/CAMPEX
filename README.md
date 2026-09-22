# ⚡ CAMPEX: MSRIT BESCOM Shield

> **Campus Resource & Anomaly Exchange**: Level-5 Autonomous Adversarial Twin for MSRIT Campus & BESCOM HT-2b Maximum Demand Management.

---

## 🚀 Live Demo Choreography (How to Run)

To run the complete live simulation, open three separate terminal windows in the `CAMPEX` project folder:

### 1. Terminal 1: Launch Pragati's Streamlit Dashboard
```bash
streamlit run app.py
```
*(Displays the real-time MSRIT physics twin, Campus Power vs. 500 kVA BESCOM red line, STP Dissolved Oxygen gauge, and ESG Ledger receipt)*

### 2. Terminal 2: Launch Sandeep's Antigravity AI Swarm
```bash
python swarm_engine.py
```
*(Watches for campus load breaches > 500 kVA, triggers the adversarial war room debate between Grid Economist & Safety Engineer, and issues the JSON load-shed command)*

### 3. Terminal 3: Launch Ishita's Chaos Engine
```bash
python chaos_engine.py
```
*(Simulates real-time campus telemetry generation and listens for terminal keypresses to inject/clear mechanical faults)*

---

## 🎬 Live Demo Sequence

1. **Normal Operations**: Pragati's UI shows MSRIT operating smoothly at ~450 kVA.
2. **The Crisis**: In Terminal 3 (Chaos Engine), press `1` and hit `Enter`. Apex Block power spikes +60 kW, pushing total demand to ~510 kVA (> 500 kVA limit).
3. **The War Room**: In Terminal 2, the Watchdog detects the breach and initiates the agent debate:
   - 🔴 **Grid Economist**: Demands 100% STP shutdown.
   - 🟢 **Safety Engineer**: Vetoes 100% shutdown to prevent bacterial die-off; counter-proposes 40% throttle on STP aeration blowers.
   - 🔵 **Chief Engineer**: Approves the compromise and executes `ai_throttle_percent = 40`.
4. **The Fix & ESG Receipt**: Pragati's dashboard instantly drops total demand back to ~470 kVA (< 500 kVA limit), updates DO to safe biological latency (1.2 mg/L), and prints the ESG receipt:
   > *"Crisis Averted. BESCOM Penalty Avoided: ₹85,000. Biological Safety of MSRIT STP Maintained."*
5. **Reset**: In Terminal 3, press `0` and hit `Enter` to clear the fault.
