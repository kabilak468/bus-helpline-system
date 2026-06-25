stops = [
    "Gandhipuram",
    "Saravanampatti",
    "KCT",
    "Pooram"
]

text = input("Enter recognized text: ")

found = []

for stop in stops:
    if stop.lower() in text.lower():
        found.append(stop)

print(found)