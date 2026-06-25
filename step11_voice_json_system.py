import speech_recognition as sr
import pyttsx3
import json
from difflib import get_close_matches

# ---------------- LOAD BUS DATABASE ----------------

with open("bus_data.json", "r") as file:
    buses = json.load(file)

# ---------------- CREATE STOPS LIST ----------------

stops = []

for bus in buses:
    for stop in bus["route"]:
        if stop not in stops:
            stops.append(stop)

# ---------------- SPEECH INPUT ----------------

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

# ---------------- RESULT ----------------

print("\n🚍 BEST BUS FOUND")
print("Bus No:", best_bus["bus_no"])
print("From:", source)
print("To:", destination)
print("Arrival + Travel Time:", best_time, "minutes")

# ---------------- VOICE OUTPUT ----------------

engine = pyttsx3.init()

message = (
    f"Bus number {best_bus['bus_no']} "
    f"is the best bus. "
    f"Total travel time is {best_time} minutes."
)

engine.say(message)
engine.runAndWait()