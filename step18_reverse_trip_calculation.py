import json

# ---------------- LOAD DATABASE ----------------

with open("bus_data.json", "r") as file:
    buses = json.load(file)

bus = buses[0]

route = bus["route"]
times = bus["travel_time"]

WAIT = bus["wait_time"]

current = bus["current_stop"]
direction = bus["direction"]

# ---------------- USER INPUT ----------------

source = input("Current Location : ").strip()
destination = input("Destination : ").strip()

# ---------------- HELPER ----------------

def segment_time(a, b):
    key = f"{a}-{b}"

    if key in times:
        return times[key]

    key = f"{b}-{a}"
    return times[key]


def forward_time(start, end):

    total = 0

    s = route.index(start)
    e = route.index(end)

    for i in range(s, e):
        total += segment_time(route[i], route[i+1])

    return total


def reverse_time(start, end):

    total = 0

    s = route.index(start)
    e = route.index(end)

    for i in range(s, e, -1):
        total += segment_time(route[i], route[i-1])

    return total


# ---------------- CASE 1 ----------------

current_index = route.index(current)
user_index = route.index(source)

if direction == "UP":

    # bus not crossed user

    if current_index <= user_index:

        eta = forward_time(current, source)

        print("\nNEXT BUS AVAILABLE")
        print("-----------------------")
        print("Bus :", bus["bus_no"])
        print("Current :", current)
        print("Will reach you in", eta, "minutes")

    else:

        # ---------------- CASE 2 ----------------

        up_remaining = forward_time(current, route[-1])

        down_trip = reverse_time(route[-1], route[0])

        second_up = forward_time(route[0], source)

        total = (
            up_remaining
            + WAIT
            + down_trip
            + WAIT
            + second_up
        )

        print("\nNO BUS BEFORE YOU")
        print("-----------------------")

        print("Current Bus :", current)

        print("\nCalculation")

        print(
            f"{current} -> {route[-1]} =",
            up_remaining,
            "minutes"
        )

        print(
            "Wait at Thudiyalur =",
            WAIT,
            "minutes"
        )

        print(
            "Return Trip =",
            down_trip,
            "minutes"
        )

        print(
            "Wait at Gandhipuram =",
            WAIT,
            "minutes"
        )

        print(
            f"Gandhipuram -> {source} =",
            second_up,
            "minutes"
        )

        print("-----------------------")

        print(
            "\nBus will reach",
            source,
            "after",
            total,
            "minutes"
        )