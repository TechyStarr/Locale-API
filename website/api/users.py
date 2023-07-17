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
    }
)


@user_ns.route('/users')
class UserList(Resource):
    # @jwt_required
    @user_ns.marshal_with(user_model)

    def get(self):
        """
            Get all users
        """
        users = User.query.all()
        if users is None:
            abort(404, message="No users found")

        return users, HTTPStatus.OK


@user_ns.route('/user/<int:id>')
class GetUser(Resource):
    # @jwt_required
    @user_ns.expect(user_model)

    @user_ns.marshal_with(user_model)

    @validate_api_key

    def get(self, user_id):
        """
            Get user by id
        """
        user = User.query.filter_by(id=user_id).first()
        if not user:
            abort(404, message="User not found")

        try:
            return user, HTTPStatus.OK
        except Exception as e:
            return {
                'message': 'User not found'
            }, HTTPStatus.NOT_FOUND


    def patch(self):
        """
            Update user
        """
        data = user_ns.payload
        user = User.query.filter_by(id=id).first()

        if not user:
            abort(404, message="User not found")
        user.username = data['username']
        user.email = data['email']
        
        try:
            user.update()
            return user, HTTPStatus.OK
        except Exception as e:
            return {
                'message': 'User not found'
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
