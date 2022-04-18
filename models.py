from app import db


student_course = db.Table("student_course",
                          db.Column("student_id", db.Integer, db.ForeignKey("student.index")),
                          db.Column("course_id", db.Integer, db.ForeignKey("course.id")))

class Student(db.Model):
    index = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    surname = db.Column(db.String(128))
    listens = db.relationship("Course", secondary = student_course, backref="listens")


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))


def init_db():
    db.drop_all()
    db.create_all()


if __name__ == '__main__':
    init_db()
