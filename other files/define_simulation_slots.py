import cv2
import numpy as np
import json
import os

# load parking map
image = cv2.imread("parking_layout.png")

if image is None:
    print("parking_layout.png not found")
    exit()

points = []

# load existing map slots
if os.path.exists("map_slots.json"):

    with open("map_slots.json", "r") as f:
        map_slots = json.load(f)

else:

    map_slots = {}

current_slot_id = input(
    "Enter slot ID (example: E1): "
)


def save_slots():

    with open("map_slots.json", "w") as f:
        json.dump(map_slots, f, indent=4)

    print("Saved")


def mouse_click(event, x, y, flags, param):

    global points
    global current_slot_id

    if event == cv2.EVENT_LBUTTONDOWN:

        points.append((x, y))

        cv2.circle(
            image,
            (x, y),
            5,
            (0, 0, 255),
            -1
        )

        # 4 points = complete slot
        if len(points) == 4:

            map_slots[current_slot_id] = points.copy()

            pts = np.array(points, np.int32)

            cv2.polylines(
                image,
                [pts],
                isClosed=True,
                color=(0, 255, 0),
                thickness=2
            )

            cv2.putText(
                image,
                current_slot_id,
                points[0],
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

            save_slots()

            print(f"{current_slot_id} saved")

            points.clear()

            current_slot_id = input(
                "Next slot ID: "
            )

        cv2.imshow(
            "Define Map Slots",
            image
        )


# redraw saved slots
for slot_id, coords in map_slots.items():

    pts = np.array(coords, np.int32)

    cv2.polylines(
        image,
        [pts],
        isClosed=True,
        color=(0, 255, 0),
        thickness=2
    )

    cv2.putText(
        image,
        slot_id,
        tuple(coords[0]),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 255, 0),
        2
    )

cv2.imshow(
    "Define Map Slots",
    image
)

cv2.setMouseCallback(
    "Define Map Slots",
    mouse_click
)

print("Click 4 points per slot")
print("Press q to quit")

while True:

    cv2.imshow(
        "Define Map Slots",
        image
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()