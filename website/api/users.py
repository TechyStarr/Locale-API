from flask import Flask, request
from flask_restx import Api, Resource, fields, Namespace, abort
from website.utils.utils import db, cache, limiter
from website.models.auth import User
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from .auth import validate_api_key

user_ns = Namespace('User', description = 'User related operations')

user_model = user_ns.model(
    'User', {
        'username': fields.String(required=True, description="Username"),
        'email': fields.String(required=True, description="Email"),
        'password': fields.String(required=True, description="Password"),
    }
)


@user_ns.route('/users')
class UserList(Resource):
    @jwt_required

    def get(self):
        """
            Get all users
        """
        users = User.get_all_users()

        return {
            'users': users
        }, HTTPStatus.OK


@user_ns.route('/update')
class UpdateUser(Resource):
    @jwt_required
    @validate_api_key
    def patch(self):
        """
            Update user
        """
        data = request.get_json()

        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()

        if user:
            user.email = email
            user.password_hash = password
            user.save()
            return {
                'message': 'User updated successfully'
            }, HTTPStatus.OK

        else:
            return {
                'message': 'User does not exist'
            }, HTTPStatus.NOT_FOUND


# @auth_namespace.route('/reset-password')
# class ResetPassword(Resource):
# 	@jwt_required
# 	def post(self):
# 		"""
# 			Reset password
# 		"""
# 		data = request.get_json()


# 		email = data.get('email')
# 		password = data.get('password')
# 		confirm_password = data.get('confirm_password')

# 		user = User.query.filter_by(email=email).first()

# 		if user:
# 			user.password_hash = generate_password_hash(password)
# 			user.save()
# 			return {
# 				'message': 'Password reset successful'
# 			}, HTTPStatus.OK

# 		else:
# 			return {
# 				'message': 'User does not exist'
# 			}, HTTPStatus.NOT_FOUND
