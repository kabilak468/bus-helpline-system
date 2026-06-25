buses = [
    {
        "bus_no": "111",
        "route": ["Gandhipuram", "Lakshmi Mills", "Peelamedu", "Saravanampatti"],
        "eta_to_source": 7,
        "travel_time_to_destination": 18
    },
    {
        "bus_no": "102",
        "route": ["Gandhipuram", "Hope College", "Saravanampatti"],
        "eta_to_source": 12,
        "travel_time_to_destination": 14
    },
    {
        "bus_no": "118",
        "route": ["Gandhipuram", "Airport", "Saravanampatti"],
        "eta_to_source": 10,
        "travel_time_to_destination": 16
    }
]

def find_best_bus(buses):
    best_bus = None
    min_time = float("inf")

    for bus in buses:
        total_time = bus["eta_to_source"] + bus["travel_time_to_destination"]

        if total_time < min_time:
            min_time = total_time
            best_bus = bus

    return best_bus, min_time


best_bus, time = find_best_bus(buses)

print("BEST BUS FOUND:")
print("Bus No:", best_bus["bus_no"])
print("Total Time:", time, "minutes")