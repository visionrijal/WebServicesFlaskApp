from extensions import db
from datetime import datetime

class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    enrollment_date = db.Column(db.Date, default=datetime.utcnow)
    grade = db.Column(db.String(5))
    __table_args__ = (db.UniqueConstraint('student_id', 'course_id'),)
    
    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'course_id': self.course_id,
            'enrollment_date': self.enrollment_date.isoformat() if self.enrollment_date else None,
            'grade': self.grade,
            'student_name': self.student.name if self.student else None,
            'course_name': self.course.name if self.course else None
        } 