from flask import Flask, render_template, request, redirect, url_for
from models import db, Course, Student, Enrollment

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123@localhost/enrollment_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    enrollments = Enrollment.query.all()
    return render_template('index.html', enrollments=enrollments)

@app.route('/add', methods=['GET', 'POST'])
def add_enrollment():
    students = Student.query.all()
    courses = Course.query.all()
    if request.method == 'POST':
        student_id = request.form['student']
        course_id = request.form['course']
        enrollment = Enrollment(student_id=student_id, course_id=course_id)
        db.session.add(enrollment)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html', students=students, courses=courses)

@app.route('/delete/<int:id>')
def delete_enrollment(id):
    enrollment = Enrollment.query.get_or_404(id)
    db.session.delete(enrollment)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
