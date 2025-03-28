from enum import unique
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True, nullable=False)
  password = db.Column(db.String(120), nullable=False)

  def __init__(self, username, password):
    self.username = username
    self.set_password(password)

  def set_password(self, password):
    self.password = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.password, password)


class Student(db.Model):
  id = db.Column(db.String(9), primary_key=True)
  first_name = db.Column(db.String(80), nullable=False)
  last_name = db.Column(db.String(80), nullable=False)
  image = db.Column(db.String(120), nullable=False)
  programme = db.Column(db.String(120), nullable=False)
  start_year = db.Column(db.Integer, nullable=False)

  courses = db.relationship('Course',
                            secondary='student_course',
                            backref='students')

  def is_enrolled(self, code):
    return StudentCourse.query.filter_by(student_id=self.id,
                                         code=code).first() is not None

  def enroll(self, code):
    student_course = StudentCourse(student_id=self.id, code=code)
    db.session.add(student_course)
    db.session.commit()

    return

  def unenroll(self, code):
    student_course = StudentCourse.query.filter_by(student_id=self.id,
                                                   code=code).first()
    if student_course:
      print(student_course.id)
      db.session.delete(student_course)
      db.session.commit()

    return

  def __init__(self, id, first_name, last_name, image, programme, start_year):
    self.id = id
    self.first_name = first_name
    self.last_name = last_name
    self.image = image
    self.programme = programme
    self.start_year = start_year


class Course(db.Model):
  code = db.Column(db.String(9), primary_key=True, unique=True)
  name = db.Column(db.String(120), nullable=False)


class StudentCourse(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  code = db.Column(db.String(9), db.ForeignKey('course.code'), nullable=False)
  student_id = db.Column(db.String(9),
                         db.ForeignKey('student.id'),
                         nullable=False)
