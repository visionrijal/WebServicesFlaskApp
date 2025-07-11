from flask import Flask
from flask_restx import Api
from config import Config
from extensions import db, jwt
from routes import auth_ns, students_ns, courses_ns, enrollments_ns
from models import *

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    jwt.init_app(app)
    api = Api(app, doc='/docs/', title=Config.API_TITLE, version=Config.API_VERSION, description=Config.API_DESCRIPTION)
    api.add_namespace(auth_ns, path='/auth')
    api.add_namespace(students_ns, path='/students')
    api.add_namespace(courses_ns, path='/courses')
    api.add_namespace(enrollments_ns, path='/enrollments')
    @app.route('/health')
    def health():
        from datetime import datetime
        return {'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()}
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Resource not found'}, 404
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return {'error': 'Internal server error'}, 500
    return app

def create_tables(app):
    with app.app_context():
        db.create_all()
        from models.user import User
        if not User.query.filter_by(username=Config.ADMIN_USERNAME).first():
            admin_user = User(username=Config.ADMIN_USERNAME)
            admin_user.set_password(Config.ADMIN_PASSWORD)
            db.session.add(admin_user)
            db.session.commit()

if __name__ == '__main__':
    app = create_app()
    create_tables(app)
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG) 