from flask import request
from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import jwt_required
from models.enrollment import Enrollment
from models.student import Student
from models.course import Course
from extensions import db

enrollments_ns = Namespace('enrollments', description='Enrollment management operations')

enrollment_model = enrollments_ns.model('Enrollment', {
    'student_id': fields.Integer(required=True, description='Student ID'),
    'course_id': fields.Integer(required=True, description='Course ID'),
    'grade': fields.String(description='Grade (optional)')
})

enrollment_update_model = enrollments_ns.model('EnrollmentUpdate', {
    'grade': fields.String(description='Grade')
})

@enrollments_ns.route('')
class EnrollmentList(Resource):
    @enrollments_ns.doc('get_enrollments', security='Bearer')
    @jwt_required()
    def get(self):
        enrollments = Enrollment.query.all()
        return [enrollment.to_dict() for enrollment in enrollments]
    @enrollments_ns.expect(enrollment_model)
    @enrollments_ns.doc('create_enrollment', security='Bearer')
    @jwt_required()
    def post(self):
        data = request.get_json()
        if not data or not all(key in data for key in ['student_id', 'course_id']):
            enrollments_ns.abort(400, 'student_id and course_id are required')
        student = Student.query.get(data['student_id'])
        course = Course.query.get(data['course_id'])
        if not student:
            enrollments_ns.abort(404, 'Student not found')
        if not course:
            enrollments_ns.abort(404, 'Course not found')
        existing_enrollment = Enrollment.query.filter_by(
            student_id=data['student_id'],
            course_id=data['course_id']
        ).first()
        if existing_enrollment:
            enrollments_ns.abort(400, 'Student already enrolled in this course')
        enrollment = Enrollment(
            student_id=data['student_id'],
            course_id=data['course_id'],
            grade=data.get('grade')
        )
        db.session.add(enrollment)
        db.session.commit()
        return enrollment.to_dict(), 201

@enrollments_ns.route('/<int:enrollment_id>')
class EnrollmentResource(Resource):
    @enrollments_ns.expect(enrollment_update_model)
    @enrollments_ns.doc('update_enrollment', security='Bearer')
    @jwt_required()
    def put(self, enrollment_id):
        enrollment = Enrollment.query.get_or_404(enrollment_id)
        data = request.get_json()
        if not data:
            enrollments_ns.abort(400, 'No data provided')
        if 'grade' in data:
            enrollment.grade = data['grade']
        db.session.commit()
        return enrollment.to_dict()
    @enrollments_ns.doc('delete_enrollment', security='Bearer')
    @jwt_required()
    def delete(self, enrollment_id):
        enrollment = Enrollment.query.get_or_404(enrollment_id)
        db.session.delete(enrollment)
        db.session.commit()
        return {'message': 'Enrollment deleted successfully'} 