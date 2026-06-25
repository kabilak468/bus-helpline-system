import speech_recognition as sr

r = sr.Recognizer()

with sr.Microphone() as source:
    print("🎤 Wait 3 seconds...")
    r.adjust_for_ambient_noise(source, duration=3)

    print("🎤 NOW SPEAK")
    audio = r.listen(source)

print("⏳ Processing...")

try:
    text = r.recognize_google(audio, language="en-IN")

    print("\n====================")
    print("RAW TEXT RECEIVED:")
    print(text)
    print("====================")

except Exception as e:
    print("Error:", e)