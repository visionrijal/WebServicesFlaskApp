from flask import request
from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import jwt_required
from models.course import Course
from models.enrollment import Enrollment
from extensions import db

courses_ns = Namespace('courses', description='Course management operations')

course_model = courses_ns.model('Course', {
    'course_code': fields.String(required=True, description='Unique course code'),
    'name': fields.String(required=True, description='Course name'),
    'description': fields.String(description='Course description'),
    'credits': fields.Integer(required=True, description='Number of credits'),
    'instructor': fields.String(description='Instructor name'),
    'semester': fields.String(description='Semester')
})

@courses_ns.route('')
class CourseList(Resource):
    @courses_ns.doc('get_courses', security='Bearer')
    @jwt_required()
    def get(self):
        courses = Course.query.all()
        return [course.to_dict() for course in courses]
    @courses_ns.expect(course_model)
    @courses_ns.doc('create_course', security='Bearer')
    @jwt_required()
    def post(self):
        data = request.get_json()
        if not data or not all(key in data for key in ['course_code', 'name', 'credits']):
            courses_ns.abort(400, 'course_code, name, and credits are required')
        if Course.query.filter_by(course_code=data['course_code']).first():
            courses_ns.abort(400, 'Course code already exists')
        course = Course(
            course_code=data['course_code'],
            name=data['name'],
            description=data.get('description'),
            credits=data['credits'],
            instructor=data.get('instructor'),
            semester=data.get('semester')
        )
        db.session.add(course)
        db.session.commit()
        return course.to_dict(), 201

@courses_ns.route('/<int:course_id>')
class CourseResource(Resource):
    @courses_ns.doc('get_course', security='Bearer')
    @jwt_required()
    def get(self, course_id):
        course = Course.query.get_or_404(course_id)
        return course.to_dict()
    @courses_ns.expect(course_model)
    @courses_ns.doc('update_course', security='Bearer')
    @jwt_required()
    def put(self, course_id):
        course = Course.query.get_or_404(course_id)
        data = request.get_json()
        if not data:
            courses_ns.abort(400, 'No data provided')
        if 'course_code' in data and data['course_code'] != course.course_code:
            if Course.query.filter_by(course_code=data['course_code']).first():
                courses_ns.abort(400, 'Course code already exists')
        for field in ['course_code', 'name', 'description', 'credits', 'instructor', 'semester']:
            if field in data:
                setattr(course, field, data[field])
        db.session.commit()
        return course.to_dict()
    @courses_ns.doc('delete_course', security='Bearer')
    @jwt_required()
    def delete(self, course_id):
        course = Course.query.get_or_404(course_id)
        db.session.delete(course)
        db.session.commit()
        return {'message': 'Course deleted successfully'}

@courses_ns.route('/<int:course_id>/students')
class CourseStudents(Resource):
    @courses_ns.doc('get_course_students', security='Bearer')
    @jwt_required()
    def get(self, course_id):
        course = Course.query.get_or_404(course_id)
        enrollments = Enrollment.query.filter_by(course_id=course_id).all()
        students = [enrollment.student.to_dict() for enrollment in enrollments]
        return students 