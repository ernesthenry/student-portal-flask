from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

# In-memory 'database'
students = []

@app.route('/')
def index():
    return render_template('index.html', students=students)

@app.route('/student/<int:student_id>')
def view_student(student_id):
    student = next((s for s in students if s['id'] == student_id), None)
    if not student:
        return "Student not found", 404
    return render_template('student.html', student=student)

@app.route('/add-student', methods=['POST'])
def add_student():
    name = request.form.get('name')
    course = request.form.get('course')
    student_id = len(students) + 1
    students.append({'id': student_id, 'name': name, 'course': course})
    return redirect(url_for('index'))

@app.route('/api/students')
def get_students_json():
    return jsonify(students)

if __name__ == '__main__':
    app.run(debug=True)
