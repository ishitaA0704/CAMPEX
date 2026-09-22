import threading
import time
import random
import json
import datetime

fault_active = False

# 1. Move the data generator to the background thread
def telemetry_generator():
    global fault_active
    while True:
        apex = 120.0 + random.uniform(-2.0, 2.0)
        desh = 110.0 + random.uniform(-1.0, 1.0)
        hostel = 95.0 + random.uniform(-1.5, 1.5)
        
        if fault_active:
            apex += 60.0  

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

        with open("telemetry.json", "w") as f:
            json.dump(payload, f, indent=2)
            
        time.sleep(1)

# Start the generator immediately
threading.Thread(target=telemetry_generator, daemon=True).start()

print("Chaos Engine is live. Injecting telemetry data into telemetry.json every 1 second...")

# 2. Keep the terminal listener in the main thread to prevent freezing
while True:
    cmd = input("\n[CHAOS ENGINE] Press '1' to inject 60kW Apex fault, '0' to clear: \n")
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    
    if cmd.strip() == '1':
        fault_active = True
        print(f"\n🚨 [{current_time}] >>> CRITICAL FAULT INJECTED: Apex Block +60 kW <<< 🚨\n")
    elif cmd.strip() == '0':
        fault_active = False
        print(f"\n✅ [{current_time}] >>> Fault cleared. Normalizing load. <<< ✅\n")