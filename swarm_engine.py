import json
import time
import os
import sys

# Attempt rich printing if available, fallback to ANSI colors
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    console = Console()
    HAS_RICH = True
except ImportError:
    HAS_RICH = False

state_file_path = os.path.join(os.path.dirname(__file__), "state.json")

def print_log(agent_name, color, message):
    if HAS_RICH:
        color_map = {"red": "bold red", "green": "bold green", "blue": "bold cyan", "yellow": "bold yellow"}
        console.print(Panel(message, title=f"[bold]{agent_name}[/bold]", style=color_map.get(color, "white")))
    else:
        colors = {
            "red": "\033[91m",
            "green": "\033[92m",
            "blue": "\033[94m",
            "yellow": "\033[93m",
            "reset": "\033[0m"
        }
        c = colors.get(color, "")
        r = colors["reset"]
        print(f"\n{c}=== [{agent_name}] ==={r}\n{message}\n")

def read_state():
    try:
        with open(state_file_path, "r") as f:
            return json.load(f)
    except Exception:
        return {"base_campus_kw": 330.0, "apex_kw": 120.0, "ai_target": "none", "ai_throttle_percent": 0}

def update_state_ai_fix(target="STP_blowers", throttle_percent=40):
    try:
        with open(state_file_path, "r") as f:
            st_data = json.load(f)
    except Exception:
        st_data = {"base_campus_kw": 330.0, "apex_kw": 180.0}
    
    st_data["ai_target"] = target
    st_data["ai_throttle_percent"] = throttle_percent
    
    temp_path = state_file_path + ".tmp"
    with open(temp_path, "w") as f:
        json.dump(st_data, f, indent=2)
    os.replace(temp_path, state_file_path)

def run_adversarial_swarm_debate(current_kva, apex_kw):
    print_log("SYSTEM WATCHDOG", "yellow", f"🚨 CRITICAL ALERT: Campus Demand reached {current_kva:.1f} kVA (Apex Block: {apex_kw:.1f} kW). Exceeds 500 kVA Maximum Demand Limit! 15:00 countdown initiated.")
    time.sleep(1)

    # 1. Grid Economist
    grid_msg = (
        f"URGENT TARIFF DEFENSE: Campus load is at {current_kva:.1f} kVA. BESCOM HT-2b penalty is ₹85,000 for a 15-minute violation! "
        "PROPOSAL: Immediately cut 100% of STP Aeration Blowers (100 kW shed) and stop Hostel Water Pumps to drop total load down to 410 kVA!"
    )
    print_log("GRID ECONOMIST AGENT", "red", grid_msg)
    time.sleep(1.5)

    # 2. Safety Engineer
    safety_msg = (
        "VETO EXERCISED: Shutting down STP blowers 100% will cause Dissolved Oxygen (DO) to collapse below 0.5 mg/L in 10 minutes, "
        "killing the biological active sludge bacteria! "
        "COUNTER-PROPOSAL: Throttle STP aeration blowers by exactly 40%. The DO level will coast safely at 1.2 mg/L on biological latency. "
        "This sheds 40 kW instantly, dropping campus demand to 470 kVA—below the 500 kVA penalty threshold without environmental damage."
    )
    print_log("SAFETY ENGINEER AGENT", "green", safety_msg)
    time.sleep(1.5)

    # 3. Chief Engineer Verdict
    chief_msg = (
        "COMPROMISE APPROVED: Safety Engineer's counter-proposal strictly satisfies both financial constraints (dropping load < 500 kVA) "
        "and biological safety guardrails (DO >= 1.0 mg/L).\n"
        "DISPATCHING COMMAND: execute_load_shed(target_asset='STP_blowers', shed_percentage=40, justification='Hydro-Biochemical Virtual Battery engaged')."
    )
    print_log("CHIEF ENGINEER AGENT", "blue", chief_msg)
    time.sleep(1)

    # Apply fix to state.json
    update_state_ai_fix("STP_blowers", 40)
    print_log("SYSTEM", "green", "✅ Command executed successfully! state.json updated with ai_throttle_percent = 40.")

def main():
    print("Sandeep's Antigravity Swarm Engine is watching state.json...")
    handled_fault = False
    
    while True:
        st_data = read_state()
        base = st_data.get("base_campus_kw", 330.0)
        apex = st_data.get("apex_kw", 120.0)
        throttle = st_data.get("ai_throttle_percent", 0)
        total_kva = base + apex
        
        # Reset handled state if fault cleared
        if apex < 150.0 and throttle == 0:
            handled_fault = False

        if total_kva > 500.0 and throttle == 0 and not handled_fault:
            handled_fault = True
            run_adversarial_swarm_debate(total_kva, apex)
            
        time.sleep(1)

if __name__ == "__main__":
    main()
