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

# ---------------- CREATE STOP LIST ----------------

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

# ---------------- FIND STOPS ----------------

words = text.split()

found = []

for word in words:

    match = get_close_matches(word, stops, n=1, cutoff=0.4)

    if match:

        if match[0] not in found:
            found.append(match[0])

if len(found) < 2:

    print("Could not identify both stops.")
    exit()

source = found[0]
destination = found[1]

print("\nDetected Route")
print(source, "->", destination)

print("\nDid you mean?")
print(source, "->", destination)

choice = input("\nPress 1 to Confirm\nPress 2 to Exit\n\nChoice : ")

if choice != "1":
    exit()

# ---------------- FIND BEST BUS ----------------

best_bus = None

for bus in buses:

    if source in bus["route"] and destination in bus["route"]:

        source_index = bus["route"].index(source)
        destination_index = bus["route"].index(destination)

        if source_index < destination_index:

            if best_bus is None:
                best_bus = bus

if best_bus is None:

    print("No bus available.")
    exit()

# ---------------- ETA CALCULATION ----------------

current_index = best_bus["route"].index(best_bus["current_stop"])
user_index = best_bus["route"].index(source)

minutes_per_stop = 3

difference = user_index - current_index

if difference < 0:

    status = "passed"

elif difference == 0:

    status = "arrived"

else:

    status = "coming"

eta = difference * minutes_per_stop

# ---------------- PRINT ----------------

print("\n========================")
print("SMART HELPLINE RESPONSE")
print("========================")

if status == "arrived":

    english = (
        f"Bus {best_bus['bus_no']} is already at your stop {source}. "
        f"This is the best bus for your journey."
    )

elif status == "coming":

    english = (
        f"Bus {best_bus['bus_no']} is currently at {best_bus['current_stop']}. "
        f"It will reach your stop {source} in {eta} minutes. "
        f"This is the best bus for your journey."
    )

else:

    english = (
        f"Bus {best_bus['bus_no']} has already crossed your stop. "
        f"Please wait for the next bus."
    )

print("\n🇬🇧")
print(english)

# ---------------- TAMIL ----------------

if status == "arrived":

    tamil = (
        f"{best_bus['bus_no']} பேருந்து தற்போது உங்கள் நிறுத்தமான "
        f"{source} இல் உள்ளது. "
        f"இது உங்களுக்கான சிறந்த பேருந்து."
    )

elif status == "coming":

    tamil = (
        f"{best_bus['bus_no']} பேருந்து தற்போது "
        f"{best_bus['current_stop']} இல் உள்ளது. "
        f"இது உங்கள் நிறுத்தமான {source} ஐ "
        f"{eta} நிமிடங்களில் அடையும். "
        f"இது உங்களுக்கான சிறந்த பேருந்து."
    )

else:

    tamil = (
        f"{best_bus['bus_no']} பேருந்து உங்கள் நிறுத்தத்தை ஏற்கனவே கடந்துவிட்டது."
    )

print("\n🇮🇳")
print(tamil)

# ---------------- HINDI ----------------

if status == "arrived":

    hindi = (
        f"बस नंबर {best_bus['bus_no']} अभी आपके स्टॉप "
        f"{source} पर है। "
        f"यही आपके लिए सबसे अच्छी बस है।"
    )

elif status == "coming":

    hindi = (
        f"बस नंबर {best_bus['bus_no']} अभी "
        f"{best_bus['current_stop']} में है। "
        f"यह आपके स्टॉप {source} तक "
        f"{eta} मिनट में पहुँचेगी। "
        f"यही आपके लिए सबसे अच्छी बस है।"
    )

else:

    hindi = (
        f"बस नंबर {best_bus['bus_no']} आपका स्टॉप पार कर चुकी है।"
    )

print("\n🇮🇳")
print(hindi)

# ---------------- SPEAK ----------------

pygame.mixer.init()

def speak(message, lang):

    filename = "voice.mp3"

    gTTS(text=message, lang=lang).save(filename)

    pygame.mixer.music.load(filename)

    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        time.sleep(0.2)

    pygame.mixer.music.unload()

    os.remove(filename)

print("\n🔊 Speaking English...")
speak(english, "en")

print("🔊 Speaking Tamil...")
speak(tamil, "ta")

print("🔊 Speaking Hindi...")
speak(hindi, "hi")

print("\n✅ Finished")