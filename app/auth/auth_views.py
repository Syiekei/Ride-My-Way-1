from flask import request
from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity, jwt_required
)

from ..models import UserRegister


class Signup(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username', required=True,
                        help='This field cannot be left blank')
    parser.add_argument('email', required=True,
                        help='This field cannot be left blank')
    parser.add_argument('password', required=True,
                        help='This field cannot be left blank')
    parser.add_argument('permission', required=True,
                        help='This field cannot be left blank')

    def post(self):
        request_data = Signup.parser.parse_args()

        username = request_data['username']
        email = request_data['email']
        password = request_data['password']
        permission = request_data['permission']

        user_reg = UserRegister()
        if user_reg.get_user_by_username(username):
            return {'message': 'user with the username {} already exists'
                    .format(username)}, 400

        user = UserRegister(username, email, password, permission)
        user.add_user()
        return {'message': 'user created successfully'}, 201


class Login(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username', required=True,
                        help='This field cannot be left blank')
    parser.add_argument('password', required=True,
                        help='This field cannot be left blank')

    def post(self):
        request_data = Login.parser.parse_args()

        username = request_data['username']

        user_reg = UserRegister()
        user = user_reg.get_user_by_username(username)

        if user:
            token = create_access_token(user.username)
            return {'token': token}, 200
        return {'message': 'user not found'}, 404
