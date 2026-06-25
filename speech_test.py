import speech_recognition as sr

r = sr.Recognizer()

with sr.Microphone() as source:
    print("🎤 Wait...")
    r.adjust_for_ambient_noise(source, duration=3)

    print("🎤 Speak AFTER this message")
    audio = r.listen(source)

print("Processing...")

try:
    text = r.recognize_google(audio)
    print("✅ Recognized:", text)

except sr.UnknownValueError:
    print("❌ Google could not understand")

except Exception as e:
    print("❌", e)