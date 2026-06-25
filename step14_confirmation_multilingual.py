import json

# ---------------- LOAD DATABASE ----------------

with open("bus_data.json", "r") as file:
    buses = json.load(file)

# ---------------- USER INPUT ----------------

source = input("Enter Source Stop: ")
destination = input("Enter Destination Stop: ")

# ---------------- CONFIRMATION ----------------

print("\n============================")
print("CONFIRMATION")
print("============================\n")

print("🇬🇧 English")
print(f"Did you mean {source} to {destination}?")
print("Press 1 to Confirm")
print("Press 2 to Speak Again")

print("\n🇮🇳 தமிழ்")
print(f"{source} இலிருந்து {destination} செல்ல விரும்புகிறீர்களா?")
print("உறுதிப்படுத்த 1 அழுத்தவும்")
print("மீண்டும் பேச 2 அழுத்தவும்")

print("\n🇮🇳 Hindi")
print(f"क्या आपका मतलब {source} से {destination} है?")
print("पुष्टि करने के लिए 1 दबाएं")
print("दोबारा बोलने के लिए 2 दबाएं")

choice = input("\nEnter Choice: ")

if choice != "1":
    print("Please speak again.")
    exit()

# ---------------- FIND VALID BUSES ----------------

valid_buses = []

for bus in buses:
    if source in bus["route"] and destination in bus["route"]:
        valid_buses.append(bus)

if not valid_buses:
    print("❌ No buses found")
    exit()

# ---------------- FIND BEST BUS ----------------

best_bus = None
best_time = float("inf")

for bus in valid_buses:

    total_time = (
        bus["eta_to_source"]
        + bus["travel_time_to_destination"]
    )

    if total_time < best_time:
        best_time = total_time
        best_bus = bus

# ---------------- LIVE LOCATION SIMULATION ----------------

current_location = best_bus["route"][0]

# ---------------- RESPONSE ----------------

print("\n============================")
print("HELPLINE RESPONSE")
print("============================\n")

print("🇬🇧 English")
print(f"Bus {best_bus['bus_no']} is currently at {current_location}.")
print(f"It will reach {destination} in {best_time} minutes.")
print("This is the best bus for your journey.")

print("\n🇮🇳 தமிழ்")
print(f"{best_bus['bus_no']} பேருந்து தற்போது {current_location} இல் உள்ளது.")
print(f"இது {destination} ஐ {best_time} நிமிடங்களில் அடையும்.")
print("இது உங்களுக்கான சிறந்த பேருந்து.")

print("\n🇮🇳 Hindi")
print(f"{best_bus['bus_no']} बस अभी {current_location} में है।")
print(f"यह {destination} तक {best_time} मिनट में पहुंचेगी।")
print("यह आपके लिए सबसे अच्छा विकल्प है।")