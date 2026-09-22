import threading
import time
import random
import json

fault_active = False

def user_input_listener():
    global fault_active
    while True:
        cmd = input("\n[CHAOS ENGINE] Press '1' to inject 60kW Apex fault, '0' to clear: \n")
        if cmd.strip() == '1':
            fault_active = True
            print("\n🚨 >>> CRITICAL FAULT INJECTED: Apex Block +60 kW <<< 🚨\n")
        elif cmd.strip() == '0':
            fault_active = False
            print("\n✅ >>> Fault cleared. Normalizing load. <<< ✅\n")

# Run terminal listener in the background
threading.Thread(target=user_input_listener, daemon=True).start()

print("Chaos Engine is live. Injecting telemetry data into telemetry.json every 1 second...")

while True:
    # 1. Generate base values with tiny realistic fluctuations
    apex = 120.0 + random.uniform(-2.0, 2.0)
    desh = 110.0 + random.uniform(-1.0, 1.0)
    hostel = 95.0 + random.uniform(-1.5, 1.5)
    
    # 2. Apply the massive spike if triggered
    if fault_active:
        apex += 60.0  

    # 3. Match Pragati's EXACT new schema
    payload = {
        "fault_active": fault_active,
        "telemetry": {
            "apex_block_kw": round(apex, 2),
            "desh_block_kw": round(desh, 2),
            "hostel_grid_kw": round(hostel, 2),
            "stp_blowers_kw": 70.0,
            "water_pumps_kw": 35.0
        }
    }

    # 4. Write to your dedicated file (telemetry.json)
    with open("telemetry.json", "w") as f:
        json.dump(payload, f, indent=2)
        
    time.sleep(1)