from difflib import get_close_matches

stops = [
    "Gandhipuram",
    "Saravanampatti",
    "KCT",
    "Pooram",
    "Peelamedu",
    "Hope College",
    "Lakshmi Mills"
]

text = input("Enter recognized text: ")

words = text.split()

found = []

for word in words:

    match = get_close_matches(
        word,
        stops,
        n=1,
        cutoff=0.4
    )

    if match:
        found.append(match[0])

print("\nMatched Stops:")
print(found)
