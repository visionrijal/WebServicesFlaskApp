from flask import request
from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import jwt_required
from models.student import Student
from models.enrollment import Enrollment
from extensions import db

students_ns = Namespace('students', description='Student management operations')

student_model = students_ns.model('Student', {
    'student_id': fields.String(required=True, description='Unique student identifier'),
    'name': fields.String(required=True, description='Full name of the student'),
    'email': fields.String(required=True, description='Email address'),
    'phone': fields.String(description='Phone number'),
    'date_of_birth': fields.String(description='Date of birth (YYYY-MM-DD)'),
    'address': fields.String(description='Home address')
})

@students_ns.route('')
class StudentList(Resource):
    @students_ns.doc('get_students', security='Bearer')
    @jwt_required()
    def get(self):
        students = Student.query.all()
        return [student.to_dict() for student in students]
    @students_ns.expect(student_model)
    @students_ns.doc('create_student', security='Bearer')
    @jwt_required()
    def post(self):
        data = request.get_json()
        if not data or not all(key in data for key in ['student_id', 'name', 'email']):
            students_ns.abort(400, 'student_id, name, and email are required')
        if Student.query.filter_by(student_id=data['student_id']).first():
            students_ns.abort(400, 'Student ID already exists')
        if Student.query.filter_by(email=data['email']).first():
            students_ns.abort(400, 'Email already exists')
        student = Student(
            student_id=data['student_id'],
            name=data['name'],
            email=data['email'],
            phone=data.get('phone'),
            address=data.get('address')
        )
        if data.get('date_of_birth'):
            from datetime import datetime
            try:
                student.date_of_birth = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
            except ValueError:
                students_ns.abort(400, 'Invalid date format. Use YYYY-MM-DD')
        db.session.add(student)
        db.session.commit()
        return student.to_dict(), 201

@students_ns.route('/<int:student_id>')
class StudentResource(Resource):
    @students_ns.doc('get_student', security='Bearer')
    @jwt_required()
    def get(self, student_id):
        student = Student.query.get_or_404(student_id)
        return student.to_dict()
    @students_ns.expect(student_model)
    @students_ns.doc('update_student', security='Bearer')
    @jwt_required()
    def put(self, student_id):
        student = Student.query.get_or_404(student_id)
        data = request.get_json()
        if not data:
            students_ns.abort(400, 'No data provided')
        if 'student_id' in data and data['student_id'] != student.student_id:
            if Student.query.filter_by(student_id=data['student_id']).first():
                students_ns.abort(400, 'Student ID already exists')
        if 'email' in data and data['email'] != student.email:
            if Student.query.filter_by(email=data['email']).first():
                students_ns.abort(400, 'Email already exists')
        for field in ['student_id', 'name', 'email', 'phone', 'address']:
            if field in data:
                setattr(student, field, data[field])
        if 'date_of_birth' in data:
            from datetime import datetime
            try:
                student.date_of_birth = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
            except ValueError:
                students_ns.abort(400, 'Invalid date format. Use YYYY-MM-DD')
        db.session.commit()
        return student.to_dict()
    @students_ns.doc('delete_student', security='Bearer')
    @jwt_required()
    def delete(self, student_id):
        student = Student.query.get_or_404(student_id)
        db.session.delete(student)
        db.session.commit()
        return {'message': 'Student deleted successfully'}

@students_ns.route('/<int:student_id>/courses')
class StudentCourses(Resource):
    @students_ns.doc('get_student_courses', security='Bearer')
    @jwt_required()
    def get(self, student_id):
        student = Student.query.get_or_404(student_id)
        enrollments = Enrollment.query.filter_by(student_id=student_id).all()
        courses = [enrollment.course.to_dict() for enrollment in enrollments]
        return courses 