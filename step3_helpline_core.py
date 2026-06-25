import re

# ---------------- STEP 1: BUS DATABASE ----------------
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

# ---------------- STEP 2: INTENT PARSER ----------------
def extract_locations(text):
    text = text.lower()

    match = re.search(r"(.*)\s+la\s+irundhu\s+(.*)\s+poganum", text)

    if match:
        source = match.group(1).strip().title()
        destination = match.group(2).strip().title()

        return source, destination

    return None, None


# ---------------- STEP 3: FILTER VALID BUSES ----------------
def find_valid_buses(source, destination):
    valid = []

    for bus in buses:
        if source in bus["route"] and destination in bus["route"]:
            valid.append(bus)

    return valid


# ---------------- STEP 4: FIND BEST BUS ----------------
def find_best_bus(valid_buses):
    best_bus = None
    min_time = float("inf")

    for bus in valid_buses:
        total_time = bus["eta_to_source"] + bus["travel_time_to_destination"]

        if total_time < min_time:
            min_time = total_time
            best_bus = bus

    return best_bus, min_time


# ---------------- MAIN SYSTEM ----------------
user_input = input("Say your travel request: ")

source, destination = extract_locations(user_input)

if not source or not destination:
    print("Could not understand input 😕")
    exit()

valid_buses = find_valid_buses(source, destination)

if not valid_buses:
    print("No buses found for this route 🚌")
    exit()

best_bus, time = find_best_bus(valid_buses)

print("\n🚍 BEST BUS RECOMMENDATION")
print("Bus No:", best_bus["bus_no"])
print("From:", source)
print("To:", destination)
print("Total Travel Time:", time, "minutes")