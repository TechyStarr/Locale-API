from flask import Flask, request
from flask_restx import Api, Resource, fields, Namespace, abort
from website.utils.utils import db, cache, limiter, generate_reset_token
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

reset_password_model = user_ns.model(
    'ResetPassword', {
        'email': fields.String(required=True, description="Email"),
    }
)

reset_request_model = user_ns.model(
    'ResetRequest', {
        'email': fields.String(required=True, description="Email"),
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
    @user_ns.marshal_with(user_model)

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
        

    def delete(self):
        """
            Delete user
        """
        user = User.query.filter_by(email='email').first()
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
        


@user_ns.route('/request-reset')
class Reset(Resource):
    @user_ns.doc(
        description='Reset',
    )
    @user_ns.expect(reset_request_model, validate=True)
    @user_ns.marshal_with(reset_request_model,  skip_none=True) #skip_none=True removes null values from response
    
    def post(self):
        """
            Request reset
        """
        data = request.get_json()
        email = data.get('email')
        user = User.query.filter_by(email=email).first()
        if user is None:
            abort(404, message="User not found")

        reset_token = generate_reset_token(user.id)
        return {'reset_token': reset_token}, HTTPStatus.OK
        

@user_ns.route('/reset-password')
class ResetPassword(Resource):
    @jwt_required
    @user_ns.doc(
        description='Reset Password',
    )
    @user_ns.marshal_with(reset_password_model,  skip_none=True) #skip_none=True removes null values from response

    def post(self):
        """
            Reset password
        """
        data = request.get_json()

        user = User.query.filter_by(email=data['email']).first()
        if not user:
            abort(404, message="User not found")

        reset_token = generate_reset_token(user.id)
        reset_token_obj = ResetToken(token=reset_token, user_id=user.id)
        reset_token_obj.save()
        

        return reset_token_obj, HTTPStatus.OK


app = Flask(__name__)
jwt = JWTManager(app)

@user_ns.route('/reset-password/<string:token>')
class ResetPasswordConfirm(Resource):
    @jwt_required
    @user_ns.doc(
        description='Confirm Reset Password',
    )
    @user_ns.marshal_with(reset_password_model)

    def post(self, token):
        try:
            decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithm='HS256')
            user_id = decoded_token['user_id']
        except jwt.ExpiredSignatureError:
            return {
                'message': 'Token has expired'
            }, HTTPStatus.BAD_REQUEST
        except jwt.InvalidTokenError:
            return {
                'message': 'Invalid token'
            }, HTTPStatus.BAD_REQUEST
        
        user = User.query.filter_by(id=user_id).first()
        if not user:
            abort(404, message="User not found")

        new_password = request.get_json()['new_password']
        user.password_hash = generate_password_hash(new_password)
        db.session.delete(ResetToken.query.filter_by(token=token).first())
        user.save()












# 2nd approach for reset password
# import secrets



# Temporary storage for password reset tokens
# reset_tokens = {}

# # Password reset API endpoints
# @user_ns.route('/reset-password/request')
# class PasswordResetRequest(Resource):

#     @user_ns.expect(reset_password_model)
#     @user_ns.marshal_with(reset_password_model)
#     @user_ns.doc(security='apikey')
#     @cache.cached(timeout=60)
#     def post(self):
#         data = request.get_json()
#         email = data.get('email')

#         # Check if the email exists in the user database
#         user = User.query.filter_by(email=email).first()

#         if user:
#             # Generate a unique token
#             token = secrets.token_urlsafe(32)

#             # Store the token in the reset_tokens dictionary
#             reset_tokens[token] = user.id

#             # Send the reset email
#             # ... implement email sending logic here ...

#             return {'message': 'Password reset email sent'}

#         return {'message': 'User not found'}, 404

# @user_ns.route('/reset-password/confirm/<token>')
# class ResetPassword(Resource):
#     def put(self, token):
#         # Check if the token exists and is valid
#         user_id = reset_tokens.get(token)

#         if user_id:
#             data = request.get_json()
#             password = data.get('password')

#             # Update the user's password
#             user = User.query.get(user_id)
#             user.password = generate_password_hash(password)
#             db.session.commit()

#             # Remove the token from reset_tokens
#             del reset_tokens[token]

#             return {'message': 'Password updated successfully'}

#         return {'message': 'Invalid token'}, 400

