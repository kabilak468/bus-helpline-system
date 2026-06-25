import speech_recognition as sr

r = sr.Recognizer()

with sr.Microphone() as source:
    print("Speak...")
    r.adjust_for_ambient_noise(source, duration=2)
    audio = r.listen(source)

try:
    text = r.recognize_google(audio, language="en-IN")
    print("Recognized:", text)

except Exception as e:
    print(type(e).__name__)
    print(e)