
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    course = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "course": self.course
        }

@app.route("/")
def home():
    
    return render_template("index.html")

# 1. GET API - VIEW ALL STUDENTS
@app.route("/api/students", methods=["GET"])
def get_students():

    students = Student.query.order_by(Student.id).all()

    return jsonify([student.to_dict() for student in students])

# 2. POST API - ADD STUDENT
@app.route("/api/students", methods=["POST"])
def add_student():

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Invalid JSON data"}), 400

    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    course = data.get("course", "").strip()

    if not name or not email or not course:
        return jsonify({"error": "All fields are required"}), 400

    student = Student(
        name=name,
        email=email,
        course=course
    )

    try:
        db.session.add(student)
        db.session.commit()

        return jsonify({
            "message": "Student added successfully",
            "student": student.to_dict()
        }), 201

    except Exception:
        db.session.rollback()
        return jsonify({"error": "Could not add student. Check whether the email already exists."}), 400

# 3. PUT API - UPDATE STUDENT
@app.route("/api/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):

    student = db.session.get(Student, student_id)

    if student is None:
        return jsonify({"error": "Student not found"}), 404

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Invalid JSON data"}), 400

    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    course = data.get("course", "").strip()

    if not name or not email or not course:
        return jsonify({"error": "All fields are required"}), 400

    student.name = name
    student.email = email
    student.course = course

    try:
        db.session.commit()
        return jsonify({
            "message": "Student updated successfully",
            "student": student.to_dict()
        })

    except Exception:
        db.session.rollback()
        return jsonify({"error": "Could not update student. Check the email."}), 400

# 4. DELETE API - DELETE STUDENT
@app.route("/api/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):

    student = db.session.get(Student, student_id)

    if student is None:
        return jsonify({"error": "Student not found"}), 404

    db.session.delete(student)
    db.session.commit()

    return jsonify({"message": "Student deleted successfully"})

if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    app.run(debug=True)