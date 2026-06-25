import speech_recognition as sr

r = sr.Recognizer()

with sr.Microphone() as source:
    print("🎤 Adjusting for noise... wait 2 seconds")
    r.adjust_for_ambient_noise(source, duration=2)

    print("🎤 Now speak clearly...")
    audio = r.listen(source)

try:
    text = r.recognize_google(audio)
    print("📝 You said:", text)

except sr.UnknownValueError:
    print("❌ Could not understand audio (try speaking louder/clearer)")

except sr.RequestError:
    print("❌ Network error with Google Speech API")