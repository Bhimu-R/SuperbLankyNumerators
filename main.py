from flask import Flask, render_template, jsonify, request, redirect, url_for, flash
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Needed for flashing messages

# Configuration for image uploads
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# In-memory activity storage
activities = []


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/activities", methods=["GET"])
def get_activities():
    return jsonify(activities)


@app.route("/add-activity", methods=["POST"])
def add_activity():
    # Handle activity data
    new_activity = request.form.to_dict()
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


@app.route("/host")
def host():
    return render_template("index.html", section="host")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
