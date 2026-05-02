import cv2
import numpy as np
import json
import os

image = cv2.imread("parking_frame.jpg")

if image is None:
    print("Image not found")
    exit()

points = []

# load existing slots if file exists
if os.path.exists("slots.json"):

    with open("slots.json", "r") as f:
        slots = json.load(f)

else:
    slots = {}

current_slot_id = input("Enter slot ID (example: E1): ")


def save_slots():

    with open("slots.json", "w") as f:
        json.dump(slots, f, indent=4)

    print("Slots saved")


def mouse_click(event, x, y, flags, param):

    global points, slots, current_slot_id

    if event == cv2.EVENT_LBUTTONDOWN:

        points.append((x, y))

        cv2.circle(image, (x, y), 5, (0, 0, 255), -1)

        if len(points) == 4:

            slots[current_slot_id] = points.copy()

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
                0.7,
                (0, 255, 0),
                2
            )

            save_slots()

            print(f"{current_slot_id} saved")

            points.clear()

            current_slot_id = input(
                "Enter next slot ID: "
            )

        cv2.imshow("Define Parking Slots", image)


# redraw saved slots
for slot_id, coords in slots.items():

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
        coords[0],
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 0),
        2
    )

cv2.imshow("Define Parking Slots", image)

cv2.setMouseCallback(
    "Define Parking Slots",
    mouse_click
)

print("Click 4 points for each slot")
print("Press q to quit")

while True:

    cv2.imshow("Define Parking Slots", image)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()