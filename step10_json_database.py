import json

# ---------------- LOAD DATABASE ----------------

with open("bus_data.json", "r") as file:
    buses = json.load(file)

# ---------------- SHOW DATA ----------------

print("\n🚌 BUSES LOADED FROM DATABASE\n")

for bus in buses:
    print("Bus No:", bus["bus_no"])
    print("Route:", " -> ".join(bus["route"]))
    print("ETA:", bus["eta_to_source"], "minutes")
    print("Travel Time:", bus["travel_time_to_destination"], "minutes")
    print("-" * 40)