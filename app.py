from flask import Flask, render_template, jsonify, request
import json
import os

app = Flask(__name__)


# =========================
# Home Page
# =========================
@app.route("/")
def home():

    user_id = request.args.get(
        "user_id"
    )

    return render_template(

        "index.html",

        user_id=user_id

    )


# =========================
# Live Parking Status
# =========================
@app.route("/status")
def status():

    if os.path.exists(
        "parking_status.json"
    ):

        with open(
            "parking_status.json",
            "r"
        ) as f:

            data = json.load(f)

    else:

        data = {}

    return jsonify(data)


# =========================
# Map Slot Coordinates
# =========================
@app.route("/map_slots")
def map_slots():

    if os.path.exists(
        "map_slots.json"
    ):

        with open(
            "map_slots.json",
            "r"
        ) as f:

            data = json.load(f)

    else:

        data = {}

    return jsonify(data)


# =========================
# Save Parking Location
# =========================
@app.route(
    "/save_location",
    methods=["POST"]
)
def save_location():

    data = request.json

    user_id = data.get(
        "user_id"
    )

    slot_id = data.get(
        "slot_id"
    )

    # validation
    if not user_id or not slot_id:

        return jsonify({

            "success": False,
            "message":
                "Missing data"

        }), 400

    # load existing locations
    if os.path.exists(
        "saved_locations.json"
    ):

        with open(
            "saved_locations.json",
            "r"
        ) as f:

            saved = json.load(f)

    else:

        saved = {}

    # save latest location
    
    from datetime import datetime
    saved[user_id] = {
        "slot_id": slot_id,
        "timestamp": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    }        

    with open(
        "saved_locations.json",
        "w"
    ) as f:

        json.dump(
            saved,
            f,
            indent=4
        )

    return jsonify({

        "success": True,
        "message":
            "Location saved",

        "slot_id": slot_id

    })

@app.route("/park/<slot_id>")
def park(slot_id):

    return jsonify({

        "slot_id": slot_id

    })

# =========================
# Get Latest Saved Location
# =========================
@app.route(
    "/get_location/<user_id>"
)
def get_location(user_id):

    if os.path.exists(
        "saved_locations.json"
    ):

        with open(
            "saved_locations.json",
            "r"
        ) as f:

            saved = json.load(f)

    else:

        saved = {}

    location = saved.get(
        user_id,
        None
    )

    if location:
        return jsonify({
            "slot_id":
                location["slot_id"],
            "timestamp":
                location["timestamp"]
        })
    return jsonify({
        "slot_id": None
    })


# =========================
# Server Start
# =========================
# if __name__ == "__main__":

#    app.run(

#        host="0.0.0.0",
#        port=5001,
#        debug=True

#    )

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5001
    )