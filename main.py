from flask import Flask, render_template, jsonify, request, redirect, url_for, flash
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Needed for flashing messages

# Configuration for image uploads
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# In-memory activity storage
activities = [
    {
        "id": 1,
        "type": "Movie",
        "host": "Alice",
        "details": "Watching a new blockbuster!",
        "time": "2024-12-01T18:00",
        "people": 10,
        "image": None
    },
    {
        "id": 2,
        "type": "Trekking",
        "host": "Bob",
        "details": "Explore the hills this weekend!",
        "time": "2024-12-02T06:00",
        "people": 15,
        "image": None
    },
    {
        "id": 3,
        "type": "Games",
        "host": "Charlie",
        "details": "Board games night with snacks!",
        "time": "2024-12-01T20:00",
        "people": 8,
        "image": None
    },
    {
        "id": 4,
        "type": "Bike Ride",
        "host": "David",
        "details": "Morning bike ride to the lake.",
        "time": "2024-12-02T07:00",
        "people": 5,
        "image": None
    },
    {
        "id": 5,
        "type": "Get-together",
        "host": "Eve",
        "details": "Casual meet-up with friends.",
        "time": "2024-12-03T19:00",
        "people": 12,
        "image": None
    },
]
my_activities = []


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/activities", methods=["GET"])
def get_activities():
    return jsonify(activities)


@app.route("/my-activities", methods=["GET"])
def get_my_activities():
    return jsonify(my_activities)


@app.route("/add-activity", methods=["POST"])
def add_activity():
    # Handle activity data
    new_activity = request.form.to_dict()
    new_activity["id"] = len(activities) + len(
        my_activities) + 1  # Assign a unique ID
    image_file = request.files.get("image")

    # Save uploaded image if present
    if image_file:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'],
                                  image_file.filename)
        image_file.save(image_path)
        new_activity["image"] = f"/{image_path}"
    else:
        new_activity["image"] = None

    activities.append(new_activity)
    flash("Activity created successfully!", "success")
    return redirect(url_for("host"))


@app.route("/join-activity/<int:activity_id>", methods=["POST"])
def join_activity(activity_id):
    global activities, my_activities

    # Find the activity to join
    for activity in activities:
        if activity.get("id") == activity_id:
            activities.remove(activity)  # Remove from the active list
            my_activities.append(activity)  # Add to My Activities list
            flash("You have joined the activity!", "success")
            break

    return redirect(url_for("index"))


@app.route("/host")
def host():
    return render_template("index.html", section="host")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
