import re

def extract_locations(text):
    # Normalize text
    text = text.lower()

    # Very simple rule-based extraction
    # pattern: "X la irundhu Y poganum"
    match = re.search(r"(.*)\s+la\s+irundhu\s+(.*)\s+poganum", text)

    if match:
        source = match.group(1).strip().title()
        destination = match.group(2).strip().title()

        return {
            "from": source,
            "to": destination
        }

    return None


# TEST INPUT (simulate voice input)
user_input = input("Say your travel request: ")

result = extract_locations(user_input)

if result:
    print("\nEXTRACTED DATA:")
    print("From:", result["from"])
    print("To:", result["to"])
else:
    print("Could not understand input 😕")