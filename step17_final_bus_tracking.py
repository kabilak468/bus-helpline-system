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

import speech_recognition as sr
import time

r = sr.Recognizer()

# ===================== SOURCE =====================

with sr.Microphone() as source:

    speak("Vanakkam", "ta")

    time.sleep(0.5)

    speak("Where are you now? Please say your current stop.", "en")
    speak("நீங்கள் இப்போது எங்கு இருக்கிறீர்கள்? உங்கள் தற்போதைய நிறுத்தத்தை சொல்லுங்கள்.", "ta")
    speak("आप अभी कहाँ हैं? अपना वर्तमान स्टॉप बताइए।", "hi")

    print("\n🎤 Listening for current location...")

    r.adjust_for_ambient_noise(source, duration=2)
    audio = r.listen(source)

try:
    source_text = r.recognize_google(audio, language="en-IN")
except:
    print("Could not understand source.")
    exit()

print("\nSource Heard:", source_text)


# ===================== DESTINATION =====================

with sr.Microphone() as source:

    speak("Where do you want to go?", "en")
    speak("நீங்கள் எங்கு செல்ல விரும்புகிறீர்கள்?", "ta")
    speak("आप कहाँ जाना चाहते हैं?", "hi")

    print("\n🎤 Listening for destination...")

    r.adjust_for_ambient_noise(source, duration=2)
    audio = r.listen(source)

try:
    destination_text = r.recognize_google(audio, language="en-IN")
except:
    print("Could not understand destination.")
    exit()

print("\nDestination Heard:", destination_text)

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

        # accept ANY valid bus containing both stops
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

current_loc = best_bus["current_stop"]

# ---------------- ENGLISH ----------------

if status == "arrived":

    english = f"Bus {best_bus['bus_no']} is already at your stop {source}. Please board the bus."

elif status == "coming":

    english = f"Bus {best_bus['bus_no']} is currently at {current_loc}. Please wait {eta} minutes."

elif status == "passed":

    english = f"Bus {best_bus['bus_no']} has already crossed your stop and is at {current_loc}. Please wait {eta} minutes."

else:

    english = f"Bus {best_bus['bus_no']} is in opposite direction. Please wait {eta} minutes."

print("\n🇬🇧 ENGLISH:\n", english)

# ---------------- TAMIL ----------------

if status == "arrived":

    tamil = f"{best_bus['bus_no']} பேருந்து தற்போது உங்கள் நிறுத்தமான {source} இல் உள்ளது. தயவுசெய்து ஏறவும்."

elif status == "coming":

    tamil = f"{best_bus['bus_no']} பேருந்து தற்போது {current_loc} இல் உள்ளது. {eta} நிமிடங்கள் காத்திருக்கவும்."

elif status == "passed":

    tamil = f"{best_bus['bus_no']} பேருந்து உங்கள் நிறுத்தத்தை கடந்துவிட்டது. அது தற்போது {current_loc} இல் உள்ளது. {eta} நிமிடங்கள் காத்திருக்கவும்."

else:

    tamil = f"{best_bus['bus_no']} பேருந்து எதிர்திசையில் உள்ளது. {eta} நிமிடங்கள் காத்திருக்கவும்."

print("\n🇮🇳 TAMIL:\n", tamil)

# ---------------- HINDI ----------------

if status == "arrived":

    hindi = f"बस नंबर {best_bus['bus_no']} अभी आपके स्टॉप {source} पर है। कृपया चढ़ें।"

elif status == "coming":

    hindi = f"बस नंबर {best_bus['bus_no']} अभी {current_loc} में है। कृपया {eta} मिनट प्रतीक्षा करें।"

elif status == "passed":

    hindi = f"बस आपके स्टॉप को पार कर चुकी है और अभी {current_loc} में है। कृपया {eta} मिनट प्रतीक्षा करें।"

else:

    hindi = f"बस विपरीत दिशा में है। कृपया प्रतीक्षा करें।"

print("\n🇮🇳 HINDI:\n", hindi)

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

# ---------------- VOICE OUTPUT ----------------

print("\n🔊 Speaking English...")
speak(english, "en")

print("🔊 Speaking Tamil...")
speak(tamil, "ta")

print("🔊 Speaking Hindi...")
speak(hindi, "hi")

print("\n✅ DONE")