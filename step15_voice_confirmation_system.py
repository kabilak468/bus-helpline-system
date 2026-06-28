import json
import speech_recognition as sr
from difflib import get_close_matches

# ---------------- LOAD DATABASE ----------------

with open("bus_data.json", "r") as file:
    buses = json.load(file)

# ---------------- BUILD STOP LIST ----------------

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
except:
    print("Speech not recognized.")
    exit()

print("\nGoogle Heard:")
print(text)

# ---------------- STOP DETECTION ----------------

text = text.lower()
stops_lower = [s.lower() for s in stops]

words = text.split()
found = []

skip_words = ["to", "from", "go", "bus", "need", "i", "want"]

for word in words:

    if word in skip_words:
        continue

    match = get_close_matches(word, stops_lower, n=1, cutoff=0.3)

    if match:

        original = stops[stops_lower.index(match[0])]

        if original not in found:
            found.append(original)

if len(found) < 2:
    print("Could not identify both stops.")
    exit()

source = found[0]
destination = found[1]

print("\nDetected Route")
print(source, "->", destination)

print("\nConfirm Route")
print(source, "->", destination)

choice = input("\nPress 1 to Confirm\nPress 2 to Exit\nEnter Choice: ")

if choice != "1":
    exit()

# ---------------- FIND BEST BUS ----------------

best_bus = None

for bus in buses:

    if source in bus["route"] and destination in bus["route"]:

        s = bus["route"].index(source)
        d = bus["route"].index(destination)

        if s < d:
            best_bus = bus
            break

if best_bus is None:
    print("No bus available.")
    exit()

print("\nSelected Bus:", best_bus["bus_no"])

# ---------------- ETA CALCULATION ----------------

def calculate_eta(bus, source, destination):

    route = bus["route"]

    current_index = route.index(bus["current_stop"])
    user_index = route.index(source)
    destination_index = route.index(destination)

    minutes_per_stop = bus.get("minutes_per_stop", 3)
    wait_time = bus.get("wait_time", 5)

    # ARRIVED
    if current_index == user_index:
        return 0, "arrived"

    # Passenger direction
    if user_index < destination_index:
        passenger_direction = "UP"
    else:
        passenger_direction = "DOWN"

    # UP + UP
    if passenger_direction == "UP" and bus["direction"] == "UP":

        if current_index < user_index:
            eta = (user_index - current_index) * minutes_per_stop
            return eta, "coming"

        else:
            eta = (
                (len(route) - current_index - 1) * minutes_per_stop +
                wait_time +
                len(route) * minutes_per_stop +
                wait_time +
                user_index * minutes_per_stop
            )
            return eta, "passed"

    # DOWN + DOWN
    if passenger_direction == "DOWN" and bus["direction"] == "DOWN":

        if current_index > user_index:
            eta = (current_index - user_index) * minutes_per_stop
            return eta, "coming"

        else:
            eta = (
                current_index * minutes_per_stop +
                wait_time +
                len(route) * minutes_per_stop +
                wait_time +
                (len(route) - user_index - 1) * minutes_per_stop
            )
            return eta, "passed"

    # OPPOSITE CASES
    if passenger_direction == "UP" and bus["direction"] == "DOWN":

        eta = (
            current_index * minutes_per_stop +
            wait_time +
            user_index * minutes_per_stop
        )
        return eta, "opposite"

    if passenger_direction == "DOWN" and bus["direction"] == "UP":

        eta = (
            (len(route) - current_index - 1) * minutes_per_stop +
            wait_time +
            (len(route) - user_index - 1) * minutes_per_stop
        )
        return eta, "opposite"

    return 0, "unknown"

# ---------------- RUN ETA ----------------

eta, status = calculate_eta(best_bus, source, destination)

# ---------------- OUTPUT ----------------

print("\n========================")
print("SMART HELPLINE RESPONSE")
print("========================")

if status == "arrived":

    print(f"Bus {best_bus['bus_no']} is already at your stop {source}.")

elif status == "coming":

    print(f"Bus {best_bus['bus_no']} will reach {source} in {eta} minutes.")

elif status == "passed":

    print(f"Bus {best_bus['bus_no']} has already crossed your stop. Wait {eta} minutes.")

else:

    print(f"Bus {best_bus['bus_no']} is in opposite direction. ETA {eta} minutes.")

print("\n✅ Done")