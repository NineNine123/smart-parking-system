from ultralytics import YOLO
import cv2
import numpy as np
import json
import requests

# =========================
# LOAD MODEL
# =========================

model = YOLO("best.pt")

# =========================
# LOAD PARKING SLOTS
# =========================

with open("slots.json", "r") as f:
    parking_slots = json.load(f)

# =========================
# LOAD VIDEO
# =========================

cap = cv2.VideoCapture(
    "parking_test2.mov"
)

frame_count = 0

# =========================
# MAIN LOOP
# =========================

while True:

    ret, frame = cap.read()

    if not ret:
        break

    frame_count += 1

    # skip frames for speed

    if frame_count % 30 != 0:
        continue

    # =========================
    # RUN DETECTION
    # =========================

    results = model(

        frame,

        conf=0.10,

        imgsz=640

    )

    # =========================
    # RESET STATUS
    # =========================

    parking_status = {}

    for slot_id in parking_slots:

        parking_status[
            slot_id
        ] = "AVAILABLE"

    # =========================
    # CHECK DETECTIONS
    # =========================

    for box in results[0].boxes:

        x1, y1, x2, y2 = map(

            int,

            box.xyxy[0]

        )

        # detection center

        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2

        # check slots

        for (
            slot_id,
            points

        ) in parking_slots.items():

            pts = np.array(
                points,
                np.int32
            )

            inside = cv2.pointPolygonTest(

                pts,

                (cx, cy),

                False

            )

            # occupied

            if inside >= 0:

                parking_status[
                    slot_id
                ] = "OCCUPIED"

                break

    # =========================
    # DRAW SLOTS
    # =========================

    for (
        slot_id,
        points

    ) in parking_slots.items():

        pts = np.array(
            points,
            np.int32
        )

        status = parking_status[
            slot_id
        ]

        # occupied

        if (
            status ==
            "OCCUPIED"
        ):

            color = (
                0,
                0,
                255
            )

        # available

        else:

            color = (
                0,
                255,
                0
            )

        # draw polygon

        cv2.polylines(

            frame,

            [pts],

            isClosed=True,

            color=color,

            thickness=2

        )

        # slot label

        cv2.putText(

            frame,

            slot_id,

            tuple(points[0]),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.6,

            color,

            2

        )

    # =========================
    # SEND LIVE STATUS
    # =========================

    try:

        response = requests.post(

            "https://smart-parking-system-qx7c.onrender.com/update_status",

            json=parking_status,

            timeout=5

        )

        print(
            "Server response:",
            response.status_code
        )

    except Exception as e:

        print(
            "Failed to update server:",
            e
        )

    # =========================
    # SHOW FRAME
    # =========================

    cv2.imshow(

        "Parking Occupancy Detection",

        frame

    )

    # =========================
    # QUIT
    # =========================

    if cv2.waitKey(1) & 0xFF == ord("q"):

        break

# =========================
# CLEANUP
# =========================

cap.release()

cv2.destroyAllWindows()