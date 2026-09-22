import threading
import time
import random
import json
import os

# --- STEP 3: THE CHAOS TRIGGER (Threaded Listener) ---
fault_active = False

def user_input_listener():
    global fault_active
    while True:
        try:
            cmd = input("\n[CHAOS ENGINE] Press '1' to inject 60kW Apex fault, '0' to clear: \n")
            if cmd.strip() == '1':
                fault_active = True
                print("\n🚨 >>> CRITICAL FAULT INJECTED: Apex Block +60 kW <<< 🚨\n")
            elif cmd.strip() == '0':
                fault_active = False
                print("\n✅ >>> Fault cleared. Normalizing load. <<< ✅\n")
        except (EOFError, KeyboardInterrupt):
            break

# Start the terminal listener in the background so it doesn't block data generation
threading.Thread(target=user_input_listener, daemon=True).start()

print("Chaos Engine is live. Injecting telemetry data into state.json every 1 second...")

# --- STEP 2: THE BASELINE GENERATOR & STEP 1: LOCKED SCHEMA ---
state_file_path = os.path.join(os.path.dirname(__file__), "state.json")

while True:
    # 1. READ current state.json to avoid overwriting AI commands
    current_state = {
        "base_campus_kw": 330.0,
        "apex_kw": 120.0,
        "ai_target": "none",
        "ai_throttle_percent": 0
    }
    
    if os.path.exists(state_file_path):
        try:
            with open(state_file_path, "r") as f:
                loaded = json.load(f)
                if isinstance(loaded, dict):
                    current_state.update(loaded)
        except (json.JSONDecodeError, IOError):
            pass

    # 2. GENERATE telemetry data with realistic fluctuations
    base_campus = 330.0 + random.uniform(-1.5, 1.5)
    apex_base = 120.0 + random.uniform(-2.0, 2.0)
    
    # Apply +60 kW spike if fault is active
    if fault_active:
        apex_base += 60.0  

    # 3. UPDATE variables in state dictionary
    current_state["base_campus_kw"] = round(base_campus, 2)
    current_state["apex_kw"] = round(apex_base, 2)

    # 4. WRITE back to state.json using atomic temp file replacement to avoid read collisions
    temp_path = state_file_path + ".tmp"
    try:
        with open(temp_path, "w") as f:
            json.dump(current_state, f, indent=2)
        os.replace(temp_path, state_file_path)
    except IOError:
        pass
        
    time.sleep(1)
