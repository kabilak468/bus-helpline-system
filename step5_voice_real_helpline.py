import speech_recognition as sr
import re

# ---------------- BUS DATABASE ----------------
buses = [
    {
        "bus_no": "111",
        "route": ["Gandhipuram", "Saravanampatti"],
        "eta_to_source": 7,
        "travel_time": 18
    },
    {
        "bus_no": "102",
        "route": ["Gandhipuram", "Saravanampatti"],
        "eta_to_source": 12,
        "travel_time": 14
    }
]

# ---------------- SPEECH INPUT ----------------
r = sr.Recognizer()

with sr.Microphone() as source:
    print("🎤 Speak your route...")
    r.adjust_for_ambient_noise(source, duration=2)
    audio = r.listen(source)

try:
    text = r.recognize_google(audio)
    print("📝 You said:", text)

except Exception:
    print("❌ Could not understand")
    exit()

# ---------------- ROUTE EXTRACTION ----------------
text = text.lower()

source = None
destination = None

# Pattern 1: "Gandhipuram la irundhu KCT poganum"
match = re.search(r"(.*)\s+la\s+irundhu\s+(.*)\s+poganum", text)

if match:
    source = match.group(1).strip().title()
    destination = match.group(2).strip().title()

# Pattern 2: "Gandhipuram to KCT"
elif " to " in text:
    parts = text.split(" to ")

    if len(parts) == 2:
        source = parts[0].strip().title()
        destination = parts[1].strip().title()

if not source or not destination:
    print("❌ Route not understood")
    exit()

print("📍 Source:", source)
print("📍 Destination:", destination)

# ---------------- BEST BUS ----------------
best_bus = None
best_time = 999

for bus in buses:
    total = bus["eta_to_source"] + bus["travel_time"]

    if total < best_time:
        best_time = total
        best_bus = bus

print("\n🚍 BEST BUS")
print("Bus No:", best_bus["bus_no"])
print("Arrival + Travel Time:", best_time, "minutes")