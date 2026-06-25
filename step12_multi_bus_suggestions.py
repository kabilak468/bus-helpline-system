import speech_recognition as sr
import pyttsx3
import json
from difflib import get_close_matches

# ---------------- LOAD DATABASE ----------------

with open("bus_data.json", "r") as file:
    buses = json.load(file)

# ---------------- CREATE STOPS LIST ----------------

stops = []

for bus in buses:
    for stop in bus["route"]:
        if stop not in stops:
            stops.append(stop)

# ---------------- VOICE INPUT ----------------

r = sr.Recognizer()

with sr.Microphone() as source:
    print("🎤 Wait 3 seconds...")
    r.adjust_for_ambient_noise(source, duration=3)

    print("🎤 Speak your route...")
    audio = r.listen(source)

try:
    text = r.recognize_google(audio, language="en-IN")

    print("\n📝 Google Heard:")
    print(text)

except Exception as e:
    print("❌ Speech Error:", e)
    exit()

# ---------------- FUZZY MATCH ----------------

words = text.split()

found_stops = []

for word in words:
    match = get_close_matches(word, stops, n=1, cutoff=0.4)

    if match and match[0] not in found_stops:
        found_stops.append(match[0])

print("\n📍 Detected Stops:")
print(found_stops)

if len(found_stops) < 2:
    print("❌ Could not identify route")
    exit()

source = found_stops[0]
destination = found_stops[1]

# ---------------- FIND ALL VALID BUSES ----------------

valid_buses = []

for bus in buses:

    if source in bus["route"] and destination in bus["route"]:

        total_time = (
            bus["eta_to_source"]
            + bus["travel_time_to_destination"]
        )

        valid_buses.append(
            {
                "bus_no": bus["bus_no"],
                "time": total_time
            }
        )

if not valid_buses:
    print("❌ No buses found")
    exit()

# ---------------- SORT BY TIME ----------------

valid_buses.sort(key=lambda x: x["time"])

# ---------------- DISPLAY RESULTS ----------------

print("\n🚍 AVAILABLE BUSES\n")

for i, bus in enumerate(valid_buses, start=1):
    print(
        f"{i}. Bus {bus['bus_no']} "
        f"-> {bus['time']} minutes"
    )

best_bus = valid_buses[0]

print("\n🏆 BEST OPTION")
print(
    f"Bus {best_bus['bus_no']} "
    f"({best_bus['time']} minutes)"
)

# ---------------- VOICE OUTPUT ----------------

engine = pyttsx3.init()

message = (
    f"The best bus is {best_bus['bus_no']}. "
    f"Travel time is {best_bus['time']} minutes."
)

engine.say(message)
engine.runAndWait()