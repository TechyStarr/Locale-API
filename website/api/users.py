from datetime import datetime, timedelta
import random
import string
import secrets
from flask import Flask, request
from flask_restx import Api, Resource, fields, Namespace, abort
from website.utils.utils import db, cache, limiter, generate_reset_token
from website.utils.mail import send_reset_email
from website.models.auth import User, ApiKey, ResetToken
from website.models.blocklist import TokenBlocklist
from http import HTTPStatus
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt, JWTManager
from .auth import validate_api_key


user_ns = Namespace('User', description = 'User related operations')

user_model = user_ns.model(
    'User', {
        'username': fields.String(required=True, description="Username"),
        'email': fields.String(required=True, description="Email"),
    }
)

request_reset_model = user_ns.model(
    'RequestReset', {
        'email': fields.String(required=True, description="Email"),
    }
)

reset_password_model = user_ns.model(
    'ResetPassword', {
        'email': fields.String(required=True, description="Email"),
        'password': fields.String(required=True, description="Password"),
        'confirm_password': fields.String(required=True, description="Confirm Password"),
    }
)

reset_token_model = user_ns.model(
    'ResetToken', {
        'token': fields.String(required=True, description="Token"),
    }
)

@user_ns.route('/users')
class UserList(Resource):
    # @jwt_required
    @user_ns.marshal_with(user_model)
    @user_ns.doc(
        description='Get all users',
    )
    @jwt_required()
    def get(self):
        """
            Get all users
        """
        users = User.query.all()
        if users is None:
            abort(404, message="No users found")

        return users, HTTPStatus.OK


@user_ns.route('/user/<int:user_id>')
class GetUser(Resource):
    @user_ns.marshal_with(user_model)
    @user_ns.doc(
        description='Get a User by id',
    )
    @jwt_required()
    def get(self, user_id):
        """
            Get a User by id
        """

        user = User.query.filter_by(id=user_id).first()
        
        if not user:        
                    abort(404, message="User does not exist")
        
        try:    
            return user, HTTPStatus.OK
        except Exception as e:
            return {
                'message': 'An error occured while retrieving user'
            }, HTTPStatus.BAD_REQUEST

    @user_ns.expect(user_model, validate=True)
    # @user_ns.marshal_with(user_model)
    @user_ns.doc(
        description='Update a User by id',
    )
    @jwt_required()
    def patch(self, user_id):
        """
            Update a student by id
        """
        data = user_ns.payload

        update_user = User.query.filter_by(id=user_id).first()

        if not update_user:
            abort(404, message="User does not exist")

        update_user.username = data['username']
        update_user.email = data['email']

        try:
            update_user.update()
            return update_user, HTTPStatus.OK, {
            'message': 'User updated successfully'
            }
        
        except Exception as e:
            return {
                'message': 'An error occured while updating user information'
            }, HTTPStatus.BAD_REQUEST


    @user_ns.doc(
        description='Delete a User by id',
    )
    @jwt_required()
    def delete(self, user_id):
        """
            Delete user
        """
        user = User.query.filter_by(id=user_id).first()
        if not user:
            abort(404, message="User not found")

        try:
            db.session.delete(user)
            # user.delete()
            return {
                'message': 'User deleted successfully'
            }, HTTPStatus.OK
        except Exception as e:
            return {
                'message': 'User not found'
            }, HTTPStatus.NOT_FOUND
        




def generate_reset_code(length = 6):
    return ''.join(random.choices(string.digits, k=length))

@user_ns.route('/forgot-password')
class ForgotPassword(Resource):
    @user_ns.doc(
        description='Forgot Password',
    )
    @user_ns.expect(request_reset_model, validate=True)
    @user_ns.marshal_with(request_reset_model,  skip_none=True) #skip_none=True removes null values from response
    
    def post(self):
        """
            Request reset
        """
        data = request.get_json()
        email = data.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
            reset_token = generate_reset_code()
            # print(f"Reset code for {email}: {reset_token}")  # Print reset code for debugging purposes

            user.reset_token = reset_token
            user.reset_token_expiration = datetime.utcnow() + timedelta(minutes=30)  # Use timedelta properly

            db.session.commit()
            print(f"Reset code for {email}: {reset_token}")  # Print reset token for debugging purposes
            send_reset_email(email, reset_token)
            return {
                'message': 'Reset token sent successfully'
            }, reset_token, HTTPStatus.OK
        else:
            return {
                'message': 'User not found'
            }, HTTPStatus.NOT_FOUND
        

@user_ns.route('/reset-token')
class ResetToken(Resource):
    @user_ns.doc(
        description='Reset Token',
    )
    @user_ns.expect(reset_token_model, validate=True)
    @user_ns.marshal_with(reset_token_model,  skip_none=True) #skip_none=True removes null values from response
    @jwt_required()
    def post(self):
        """
            Reset token
        """
        data = request.get_json()
        email = get_jwt_identity()
        reset_token = data.get('reset_token')

        user = User.query.filter_by(email=email).first()
        if user and reset_token and user.reset_token_expiration > datetime.utcnow():
            abort(404, message="User not found")

            return {
                'message': 'Reset token is valid'
            }, HTTPStatus.OK
        else:
            return {
                'message': 'Reset token is invalid or expired'
            }, HTTPStatus.BAD_REQUEST
    



@user_ns.route('/reset-password')
class ResetPassword(Resource):
    @user_ns.doc(
        description='Reset Password',
    )
    @user_ns.expect(reset_password_model, validate=True)
    @user_ns.marshal_with(reset_password_model,  skip_none=True) #skip_none=True removes null values from response

    def post(self):
        """
            Reset password
        """
        data = request.get_json()
        email = data.get('email')
        reset_token = data.get('reset_token')

        user = User.query.filter_by(email=email).first()
        if user and reset_token and user.reset_token_expiration > datetime.utcnow():
            password = data.get('password')
            confirm_password = data.get('confirm_password')
            if password != confirm_password:
                return {
                    'message': 'Passwords do not match'
                }, HTTPStatus.BAD_REQUEST
            user.password = generate_password_hash(password)
            user.confirm_password = generate_password_hash(confirm_password)
            user.reset_token = None # Reset token after password reset is successful
            user.reset_token_expiration = None 
            db.session.commit()
            return {
                'message': 'Password reset successfully'
            }, HTTPStatus.OK
            
        else:
            return {
                'message': "We couldn't reset your password. Please try again"
            }


        

send_email_model = user_ns.model(
    'SendEmail', {
        'email': fields.String(required=True, description="Email"),
        'message': fields.String(required=True, description="Message"),
    }
)




# @user_ns.route('/request-reset')
# class Reset(Resource):
#     @user_ns.doc(
#         description='Reset',
#     )
#     @user_ns.expect(reset_request_model, validate=True)
#     @user_ns.marshal_with(reset_request_model,  skip_none=True) #skip_none=True removes null values from response
    
#     def post(self):
#         """
#             Request reset
#         """
#         data = request.get_json()
#         email = data.get('email')
#         user = User.query.filter_by(email=email).first()
#         if user is None:
#             abort(404, message="User not found")

#         reset_token = generate_reset_token(user.id)
#         return reset_token, HTTPStatus.OK
        



# app = Flask(__name__)
# jwt = JWTManager(app)

# @user_ns.route('/reset-password/<string:token>')
# class ResetPasswordConfirm(Resource):
#     @jwt_required
#     @user_ns.doc(
#         description='Confirm Reset Password',
#     )
#     @user_ns.marshal_with(reset_password_model)

#     def post(self, token):
#         try:
#             decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithm='HS256')
#             user_id = decoded_token['user_id']
#         except jwt.ExpiredSignatureError:
#             return {
#                 'message': 'Token has expired'
#             }, HTTPStatus.BAD_REQUEST
#         except jwt.InvalidTokenError:
#             return {
#                 'message': 'Invalid token'
#             }, HTTPStatus.BAD_REQUEST
        
#         user = User.query.filter_by(id=user_id).first()
#         if not user:
#             abort(404, message="User not found")

#         new_password = request.get_json()['new_password']
#         user.password_hash = generate_password_hash(new_password)
#         db.session.delete(ResetToken.query.filter_by(token=token).first())
#         user.save()











