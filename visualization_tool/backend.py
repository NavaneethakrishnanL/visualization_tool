from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dashboards.db"
db = SQLAlchemy(app)

class Dashboard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(100), nullable=False)
    config = db.Column(db.JSON, nullable=False)  # Stores filters & settings

with app.app_context():
    db.create_all()

@app.route("/save_dashboard", methods=["POST"])
def save_dashboard():
    data = request.json
    new_dashboard = Dashboard(user=data["user"], config=data["config"])
    db.session.add(new_dashboard)
    db.session.commit()
    return jsonify({"message": "Dashboard saved!"}), 200

@app.route("/load_dashboard/<user>", methods=["GET"])
def load_dashboard(user):
    dashboard = Dashboard.query.filter_by(user=user).first()
    if dashboard:
        return jsonify(dashboard.config), 200
    return jsonify({"message": "No dashboard found"}), 404

if __name__ == "__main__":
    app.run(port=5001)
