from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import request

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/student/<id>')
def finds(id):
    return find_student(id)


@app.route('/student/all')
def find_all_students():
    students = db.session.query(Student).all()
    sts = {}
    for student in students:
        sts[student.index] = student.name + " " + student.surname
    return sts


@app.route('/course/all')
def find_all_courses():
    courses = db.session.query(Course).all()
    crs = {}
    for course in courses:
        crs[course.id] = course.name
    return crs


@app.route('/student/create', methods=['POST'])
def create_student():
    index = request.json['index']
    name = request.json['name']
    surname = request.json['surname']
    student = Student(index=index, name=name, surname=surname)
    db.session.add(student)
    db.session.commit()
    return {'index': index, 'name': name}


@app.route('/course/create', methods=['POST'])
def create_course():
    name = request.json['name']
    course = Course(name=name)
    db.session.add(course)
    db.session.commit()
    return {'name': name}


@app.route('/course/delete/<courseId>')
def delete_course(courseId):
    found_course = find_course(courseId)
    db.session.delete(found_course)
    db.session.commit()
    return "200"


@app.route('/student/delete/<studentId>')
def delete_student(studentId):
    found_student = find_student(studentId)
    db.session.delete(found_student)
    db.session.commit()
    return "200"


@app.route('/student/edit/<studentId>', methods=['POST'])
def edit_student(studentId):
    name = request.json['name']
    surname = request.json['surname']
    student = find_student(studentId)
    student.name = name
    student.surname = surname
    db.session.add(student)
    db.session.commit()
    return {'name': name, 'surname': surname}


@app.route('/course/edit/<courseId>', methods=['POST'])
def edit_course(courseId):
    name = request.json['name']
    course = find_course(courseId)
    course.name = name
    db.session.add(course)
    db.session.commit()
    return {'name': name}


@app.route('/add/<studentId>/<courseId>')
def add_student_in_course(studentId, courseId):
    found_student = find_student(studentId)
    if found_student == "404":
        return "error"
    found_course = find_course(courseId)
    if found_course == "404":
        return "error"
    found_student.listens.append(found_course)
    db.session.commit()
    return "200"


def find_course(id):
    found_course = db.session.query(Course).filter_by(id=id).first()
    if found_course:
        return found_course
    else:
        return "404"


def find_student(id):
    found_student = db.session.query(Student).filter_by(index=id).first()
    if found_student:
        return found_student
    else:
        return "404"


from models import Student
from models import Course

if __name__ == '__main__':
    app.run(debug=True)
