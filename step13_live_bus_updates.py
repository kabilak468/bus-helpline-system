import json
import time

# ---------------- LOAD DATABASE ----------------

with open("bus_data.json", "r") as file:
    buses = json.load(file)

print("\n🛰️ LIVE BUS TRACKING STARTED\n")

# ---------------- SIMULATE LIVE UPDATES ----------------

for cycle in range(5):

    print(f"\n===== UPDATE {cycle + 1} =====\n")

    for bus in buses:

        print(
            f"Bus {bus['bus_no']} "
            f"-> {bus['eta_to_source']} minutes away"
        )

        # simulate bus moving closer
        if bus["eta_to_source"] > 0:
            bus["eta_to_source"] -= 1

    time.sleep(3)

print("\n✅ Simulation Completed")