import re

# ---------------- BUS DATABASE ----------------
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

# ---------------- INTENT PARSER ----------------
def extract_locations(text):
    text = text.lower()
    match = re.search(r"(.*)\s+la\s+irundhu\s+(.*)\s+poganum", text)

    if match:
        return match.group(1).strip().title(), match.group(2).strip().title()

    return None, None


# ---------------- FILTER BUSES ----------------
def find_valid_buses(source, destination):
    return [
        bus for bus in buses
        if source in bus["route"] and destination in bus["route"]
    ]


# ---------------- BEST BUS ----------------
def find_best_bus(valid_buses):
    best = None
    min_time = float("inf")

    for bus in valid_buses:
        total = bus["eta_to_source"] + bus["travel_time_to_destination"]
        if total < min_time:
            min_time = total
            best = bus

    return best, min_time


# ---------------- MULTI-LANGUAGE RESPONSE ----------------
def generate_voice_response(bus, time, source, destination):
    tamil = f"{time} நிமிடங்களில் {bus['bus_no']} பஸ் {source}-க்கு வந்தடையும். இது உங்களுக்கான சிறந்த பஸ்."
    english = f"Bus {bus['bus_no']} will arrive at {source} in {time} minutes. This is the best option."
    hindi = f"{bus['bus_no']} बस {time} मिनट में {source} पहुंचेगी। यह सबसे अच्छा विकल्प है।"

    print("\n📞 HELPLINE RESPONSE (SIMULATED VOICE)\n")
    print("🇮🇳 Tamil:", tamil)
    print("🇬🇧 English:", english)
    print("🇮🇳 Hindi:", hindi)


# ---------------- MAIN SYSTEM ----------------
user_input = input("Say your travel request: ")

source, destination = extract_locations(user_input)

if not source or not destination:
    print("Could not understand input 😕")
    exit()

valid_buses = find_valid_buses(source, destination)

if not valid_buses:
    print("No buses found 🚌")
    exit()

best_bus, time = find_best_bus(valid_buses)

generate_voice_response(best_bus, time, source, destination)