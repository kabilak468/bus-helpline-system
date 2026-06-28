import json
import speech_recognition as sr
from difflib import get_close_matches
from gtts import gTTS
import pygame
import os
import time

# ================= LOAD DATA =================

with open("bus_data.json", "r", encoding="utf-8") as file:
    buses = json.load(file)

bus = buses[0]

route = bus["route"]
stops = route
stops_lower = [s.lower() for s in stops]

WAIT_TIME = bus.get("wait_time", 5)
minutes_per_stop = bus.get("minutes_per_stop", 3)

# ================= SPEECH ENGINE =================

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

# ================= VOICE INPUT (GUIDED) =================

r = sr.Recognizer()

with sr.Microphone() as source:

    speak("Vanakkam", "ta")
    time.sleep(0.5)

    speak("Where are you now? And where do you want to go?", "en")
    speak("நீங்கள் இப்போது எங்கு இருக்கிறீர்கள் மற்றும் எங்கு செல்ல விரும்புகிறீர்கள்?", "ta")
    speak("आप अभी कहाँ हैं और कहाँ जाना चाहते हैं?", "hi")

    print("\n🎤 Listening...")

    r.adjust_for_ambient_noise(source, duration=2)
    audio = r.listen(source)

try:
    text = r.recognize_google(audio, language="en-IN")
except:
    print("Speech not recognized.")
    exit()

print("\nHeard:", text)

# ================= STOP DETECTION =================

text = text.lower()
found = []

for word in text.split():

    match = get_close_matches(word, stops_lower, n=1, cutoff=0.5)

    if match:
        original = stops[stops_lower.index(match[0])]
        if original not in found:
            found.append(original)

if len(found) < 2:
    print("Could not identify both stops.")
    exit()

source = found[0]
destination = found[1]

print("\nDetected Route:", source, "->", destination)

# ================= CONFIRMATION =================

speak(f"You said {source} to {destination}. Press 1 to confirm.", "en")
speak(f"நீங்கள் {source} முதல் {destination} வரை சொன்னீர்கள். உறுதிப்படுத்த 1 அழுத்தவும்.", "ta")
speak(f"आपने {source} से {destination} बताया है। पुष्टि करने के लिए 1 दबाएँ।", "hi")

choice = input("\nPress 1 to Confirm: ")

if choice != "1":
    print("User exited")
    exit()

# ================= CORE DATA =================

current_stop = bus["current_stop"]
direction = bus["direction"]

current_index = route.index(current_stop)
user_index = route.index(source)
destination_index = route.index(destination)

# ================= ETA ENGINE (FINAL LOGIC) =================

def calculate_eta():

    route_len = len(route)
    last_index = route_len - 1

    passenger_direction = "UP" if user_index < destination_index else "DOWN"
    bus_direction = direction

    # ---------------- ARRIVED ----------------
    if current_index == user_index:
        return 0, "arrived"

    # ---------------- SAME DIRECTION ----------------
    if passenger_direction == bus_direction:

        # BUS BEFORE PASSENGER
        if (bus_direction == "UP" and current_index < user_index) or \
           (bus_direction == "DOWN" and current_index > user_index):

            eta = abs(user_index - current_index) * minutes_per_stop
            return eta, "coming"

        # BUS AFTER PASSENGER (CROSSED)
        else:

            eta = (
                abs(last_index - current_index) * minutes_per_stop +
                WAIT_TIME +
                route_len * minutes_per_stop +
                WAIT_TIME +
                abs(user_index) * minutes_per_stop
            )

            return eta, "passed"

    # ---------------- OPPOSITE DIRECTION ----------------
    else:

        eta = (
            abs(last_index - current_index) * minutes_per_stop +
            WAIT_TIME +
            abs(user_index) * minutes_per_stop
        )

        return eta, "opposite"

eta, status = calculate_eta()

# ================= OUTPUT =================

current_loc = current_stop

print("\n========================")
print("SMART HELPLINE RESPONSE")
print("========================")

# ---------------- ENGLISH ----------------

if status == "arrived":
    english = f"Bus {bus['bus_no']} is already at your stop {source}. Please board."

elif status == "coming":
    english = f"Bus {bus['bus_no']} is at {current_loc}. Please wait {eta} minutes."

elif status == "passed":
    english = f"Bus {bus['bus_no']} has crossed your stop and is at {current_loc}. Please wait {eta} minutes."

else:
    english = f"Bus {bus['bus_no']} is in opposite direction. Please wait {eta} minutes."

# ---------------- TAMIL ----------------

if status == "arrived":
    tamil = f"பேருந்து {bus['bus_no']} உங்கள் நிறுத்தமான {source} இல் உள்ளது. ஏறவும்."

elif status == "coming":
    tamil = f"பேருந்து {bus['bus_no']} தற்போது {current_loc} இல் உள்ளது. {eta} நிமிடங்கள் காத்திருக்கவும்."

elif status == "passed":
    tamil = f"பேருந்து உங்கள் நிறுத்தத்தை கடந்துவிட்டது. அது தற்போது {current_loc} இல் உள்ளது. {eta} நிமிடங்கள் காத்திருக்கவும்."

else:
    tamil = f"பேருந்து எதிர்திசையில் உள்ளது. {eta} நிமிடங்கள் காத்திருக்கவும்."

# ---------------- HINDI ----------------

if status == "arrived":
    hindi = f"बस {bus['bus_no']} अभी आपके स्टॉप {source} पर है। चढ़ें।"

elif status == "coming":
    hindi = f"बस {bus['bus_no']} अभी {current_loc} में है। {eta} मिनट प्रतीक्षा करें।"

elif status == "passed":
    hindi = f"बस आपके स्टॉप को पार कर चुकी है और अभी {current_loc} में है। {eta} मिनट प्रतीक्षा करें।"

else:
    hindi = f"बस विपरीत दिशा में है। कृपया प्रतीक्षा करें।"

# ================= PRINT =================

print("\nENGLISH:\n", english)
print("\nTAMIL:\n", tamil)
print("\nHINDI:\n", hindi)

# ================= SPEECH OUTPUT =================

speak(english, "en")
speak(tamil, "ta")
speak(hindi, "hi")

print("\n✅ STEP 17 v3.1 COMPLETE - STABLE SYSTEM")