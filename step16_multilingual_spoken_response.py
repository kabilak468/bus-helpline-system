import json
import pyttsx3

# ---------------- LOAD DATABASE ----------------

with open("bus_data.json", "r") as file:
    buses = json.load(file)

# ---------------- USER INPUT ----------------

source = input("Enter Source Stop: ")
destination = input("Enter Destination Stop: ")

# ---------------- FIND VALID BUSES ----------------

valid_buses = []

for bus in buses:
    if source in bus["route"] and destination in bus["route"]:
        total_time = (
            bus["eta_to_source"]
            + bus["travel_time_to_destination"]
        )

        valid_buses.append((bus, total_time))

if len(valid_buses) == 0:
    print("❌ No buses found")
    exit()

# ---------------- BEST BUS ----------------

best_bus = min(valid_buses, key=lambda x: x[1])

bus = best_bus[0]
travel_time = best_bus[1]

# ---------------- DISPLAY RESPONSE ----------------

print("\n============================")
print("MULTILINGUAL RESPONSE")
print("============================")

print("\n🇬🇧 English")
print(
    f"Bus {bus['bus_no']} is currently at {source}. "
    f"It will reach {destination} in {travel_time} minutes. "
    f"This is the best bus for your journey."
)

print("\n🇮🇳 தமிழ்")
print(
    f"{bus['bus_no']} பேருந்து தற்போது {source} இல் உள்ளது. "
    f"இது {destination} ஐ {travel_time} நிமிடங்களில் அடையும். "
    f"இது உங்களுக்கான சிறந்த பேருந்து."
)

print("\n🇮🇳 Hindi")
print(
    f"{bus['bus_no']} बस अभी {source} में है। "
    f"यह {destination} तक {travel_time} मिनट में पहुंचेगी। "
    f"यह आपके लिए सबसे अच्छा विकल्प है।"
)

# ---------------- VOICE OUTPUT ----------------

engine = pyttsx3.init()

english_message = (
    f"Bus {bus['bus_no']} is currently at {source}. "
    f"It will reach {destination} in {travel_time} minutes. "
    f"This is the best bus for your journey."
)

print("\n🔊 Speaking English Response...")
engine.say(english_message)
engine.runAndWait()

# ---------------- TAMIL SPEECH ----------------

tamil_message = (
    f"{bus['bus_no']} பேருந்து தற்போது {source} இல் உள்ளது. "
    f"இது {destination} ஐ {travel_time} நிமிடங்களில் அடையும்."
)

print("🔊 Speaking Tamil Response...")
engine.say(tamil_message)
engine.runAndWait()

# ---------------- HINDI SPEECH ----------------

hindi_message = (
    f"{bus['bus_no']} बस अभी {source} में है। "
    f"यह {destination} तक {travel_time} मिनट में पहुंचेगी।"
)

print("🔊 Speaking Hindi Response...")
engine.say(hindi_message)
engine.runAndWait()