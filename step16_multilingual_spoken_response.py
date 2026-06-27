import json
import os
import time

from gtts import gTTS
import pygame


# ---------------- LOAD DATABASE ----------------

with open("bus_data.json", "r") as file:
    buses = json.load(file)


# ---------------- USER INPUT ----------------

source = input("Enter Source Stop: ").strip()
destination = input("Enter Destination Stop: ").strip()


# ---------------- FIND BEST BUS ----------------

valid_buses = []

for bus in buses:

    if source in bus["route"] and destination in bus["route"]:

        total = bus["eta_to_source"] + bus["travel_time_to_destination"]

        valid_buses.append((bus, total))


if len(valid_buses) == 0:

    print("No buses found.")
    exit()


best_bus, total_time = min(valid_buses, key=lambda x: x[1])


print("\nBEST BUS FOUND")
print(best_bus["bus_no"])


# ---------------- MULTILINGUAL MESSAGES ----------------

english = (
    f"Bus number {best_bus['bus_no']} is currently at {best_bus['route'][0]}. "
    f"It will reach {destination} in {total_time} minutes. "
    f"This is the best bus for your journey."
)

tamil = (
    f"{best_bus['bus_no']} பேருந்து தற்போது "
    f"{best_bus['route'][0]} இல் உள்ளது. "
    f"இது {destination} ஐ "
    f"{total_time} நிமிடங்களில் அடையும். "
    f"இது உங்கள் பயணத்திற்கு சிறந்த பேருந்து."
)

hindi = (
    f"बस नंबर {best_bus['bus_no']} अभी "
    f"{best_bus['route'][0]} में है। "
    f"यह {destination} तक "
    f"{total_time} मिनट में पहुँचेगी। "
    f"यह आपकी यात्रा के लिए सबसे अच्छा विकल्प है।"
)


# ---------------- SPEAK FUNCTION ----------------

pygame.mixer.init()


def speak(text, language):

    filename = "voice.mp3"

    tts = gTTS(text=text, lang=language)

    tts.save(filename)

    pygame.mixer.music.load(filename)

    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():

        time.sleep(0.2)

    pygame.mixer.music.unload()

    os.remove(filename)


# ---------------- SPEAK ----------------

print("\n🇬🇧 English")
print(english)
speak(english, "en")

print("\n🇮🇳 தமிழ்")
print(tamil)
speak(tamil, "ta")

print("\n🇮🇳 Hindi")
print(hindi)
speak(hindi, "hi")

print("\n✅ Finished")