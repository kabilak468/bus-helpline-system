import json
import speech_recognition as sr
from difflib import get_close_matches
from gtts import gTTS
import pygame
import os
import time

# ---------------- LOAD DATABASE ----------------

with open("bus_data.json", "r") as file:
    buses = json.load(file)

# ---------------- BUILD STOP LIST ----------------

stops = []

for bus in buses:
    for stop in bus["route"]:
        if stop not in stops:
            stops.append(stop)

# ---------------- SETTINGS ----------------

WAIT_TIME = 5
minutes_per_stop = 3

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

# ---------------- STOP DETECTION (FIXED) ----------------

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

choice = input("\nPress 1 to Confirm\nPress 2 to Exit\nChoice: ")

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

# ---------------- ETA ENGINE ----------------

def calculate_eta():

    route = best_bus["route"]
    current_index = route.index(best_bus["current_stop"])
    user_index = route.index(source)
    destination_index = route.index(destination)

    # Passenger direction
    if user_index < destination_index:
        passenger_direction = "UP"
    else:
        passenger_direction = "DOWN"

    # ARRIVED
    if current_index == user_index:
        return 0, "arrived"

    # UP + UP
    if passenger_direction == "UP" and best_bus["direction"] == "UP":

        if current_index < user_index:
            eta = (user_index - current_index) * minutes_per_stop
            return eta, "coming"

        else:
            eta = (
                (len(route) - current_index - 1) * minutes_per_stop +
                WAIT_TIME +
                len(route) * minutes_per_stop +
                WAIT_TIME +
                user_index * minutes_per_stop
            )
            return eta, "passed"

    # DOWN + DOWN
    if passenger_direction == "DOWN" and best_bus["direction"] == "DOWN":

        if current_index > user_index:
            eta = (current_index - user_index) * minutes_per_stop
            return eta, "coming"

        else:
            eta = (
                current_index * minutes_per_stop +
                WAIT_TIME +
                len(route) * minutes_per_stop +
                WAIT_TIME +
                (len(route) - user_index - 1) * minutes_per_stop
            )
            return eta, "passed"

    # OPPOSITE CASES
    if passenger_direction == "UP" and best_bus["direction"] == "DOWN":

        eta = (
            current_index * minutes_per_stop +
            WAIT_TIME +
            user_index * minutes_per_stop
        )
        return eta, "opposite"

    if passenger_direction == "DOWN" and best_bus["direction"] == "UP":

        eta = (
            (len(route) - current_index - 1) * minutes_per_stop +
            WAIT_TIME +
            (len(route) - user_index - 1) * minutes_per_stop
        )
        return eta, "opposite"


eta, status = calculate_eta()

# ---------------- OUTPUT ----------------

print("\n========================")
print("SMART HELPLINE RESPONSE")
print("========================")

if status == "arrived":

    english = f"Bus {best_bus['bus_no']} is already at your stop {source}."

elif status == "coming":

    english = f"Bus {best_bus['bus_no']} will reach {source} in {eta} minutes."

elif status == "passed":

    english = f"Bus {best_bus['bus_no']} has already crossed your stop. Wait {eta} minutes."

else:

    english = f"Bus {best_bus['bus_no']} is in opposite direction. It will reach in {eta} minutes."

print("\n🇬🇧", english)

# ---------------- SPEECH ----------------

pygame.mixer.init()

def speak(text, lang):
    filename = "voice.mp3"
    gTTS(text=text, lang=lang).save(filename)

    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        time.sleep(0.2)

    pygame.mixer.music.unload()
    os.remove(filename)

print("\n🔊 Speaking...")
speak(english, "en")

print("\n✅ DONE")