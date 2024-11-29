from flask import Flask, render_template, jsonify, request, redirect, url_for, flash, session
import os
import hashlib

app = Flask(__name__)
app.secret_key = "supersecretkey"  # For sessions and flashing messages

# Configuration for image uploads
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# In-memory storage
users = {
}  # Format: {"username": {"password": <hashed_password>, "activities": []}}
activities = [
    {
        "id": 1,
        "type": "Movie",
        "host": "Admin",
        "details": "Watching a new blockbuster!",
        "time": "2024-12-01T18:00",
        "people": 10,
        "image": None
    },
    {
        "id": 2,
        "type": "Trekking",
        "host": "Admin",
        "details": "Explore the hills this weekend!",
        "time": "2024-12-02T06:00",
        "people": 15,
        "image": None
    },
    {
        "id": 3,
        "type": "Games",
        "host": "Admin",
        "details": "Board games night with snacks!",
        "time": "2024-12-01T20:00",
        "people": 8,
        "image": None
    },
    {
        "id": 4,
        "type": "Bike Ride",
        "host": "Admin",
        "details": "Morning bike ride to the lake.",
        "time": "2024-12-02T07:00",
        "people": 5,
        "image": None
    },
    {
        "id": 5,
        "type": "Get-together",
        "host": "Admin",
        "details": "Casual meet-up with friends.",
        "time": "2024-12-03T19:00",
        "people": 12,
        "image": None
    },
]


def hash_password(password):
    """Hashes a password for secure storage."""
    return hashlib.sha256(password.encode()).hexdigest()


@app.route("/")
def index():
    return render_template("index.html", username=session.get("username"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            flash("Username and password are required.", "error")
            return redirect(url_for("register"))

        if username in users:
            flash("Username already exists. Please choose another.", "error")
            return redirect(url_for("register"))

        users[username] = {
            "password": hash_password(password),
            "activities": []
        }
        flash("Registration successful! You can now log in.", "success")
        return redirect(url_for("index"))

    return render_template("register.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    if username in users and users[username]["password"] == hash_password(
            password):
        session["username"] = username
        flash("Login successful!", "success")
    else:
        flash("Invalid username or password.", "error")

    return redirect(url_for("index"))


@app.route("/logout")
def logout():
    session.pop("username", None)
    flash("You have logged out.", "success")
    return redirect(url_for("index"))


@app.route("/activities", methods=["GET"])
def get_activities():
    return jsonify(activities)


@app.route("/my-activities", methods=["GET"])
def get_my_activities():
    if "username" not in session:
        return jsonify([])  # Return an empty list if not logged in

    username = session["username"]
    return jsonify(users[username]["activities"])


@app.route("/add-activity", methods=["POST"])
def add_activity():
    if "username" not in session:
        return redirect(url_for("index"))

    new_activity = request.form.to_dict()
    new_activity["id"] = len(activities) + 1  # Assign a unique ID
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
    return redirect(url_for("index"))


@app.route("/join-activity/<int:activity_id>", methods=["POST"])
def join_activity(activity_id):
    if "username" not in session:
        return redirect(url_for("index"))

    username = session["username"]

    # Find the activity to join
    for activity in activities:
        if activity.get("id") == activity_id:
            users[username]["activities"].append(activity)
            flash("You have joined the activity!", "success")
            break

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
