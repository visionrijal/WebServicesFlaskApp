from extensions import db

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    credits = db.Column(db.Integer, nullable=False)
    instructor = db.Column(db.String(100))
    semester = db.Column(db.String(20))
    enrollments = db.relationship('Enrollment', backref='course', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'course_code': self.course_code,
            'name': self.name,
            'description': self.description,
            'credits': self.credits,
            'instructor': self.instructor,
            'semester': self.semester
        } 