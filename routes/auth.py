from flask import request
from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import create_access_token
from models.user import User
from extensions import db

auth_ns = Namespace('auth', description='Authentication operations')

login_model = auth_ns.model('Login', {
    'username': fields.String(required=True, description='Username'),
    'password': fields.String(required=True, description='Password')
})

@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(login_model)
    def post(self):
        data = request.get_json()
        if not data or not data.get('username') or not data.get('password'):
            auth_ns.abort(400, 'Username and password required')
        user = User.query.filter_by(username=data['username']).first()
        if user and user.check_password(data['password']):
            access_token = create_access_token(identity=user.username)
            return {
                'access_token': access_token,
                'user': {'username': user.username}
            }
        auth_ns.abort(401, 'Invalid credentials') 