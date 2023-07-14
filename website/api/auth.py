import json
import secrets
from functools import wraps
from uuid import uuid4
from flask import Flask, request
from flask_restx import Resource, fields, Namespace, abort
from website.models.auth import User, ApiKey
from website.utils.utils import db, cache, limiter
from werkzeug.security import generate_password_hash, check_password_hash
from http import HTTPStatus
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
from flask_jwt_extended.exceptions import NoAuthorizationError
# from flask_caching import Cache
# from flask_limiter import Limiter
# from flask_limiter.util import get_remote_address
from website.models.data import load_dataset, clear_dataset


auth_namespace = Namespace('Auth', description='Authentication Endpoints')

# app = Flask(__name__)

# cache = Cache(app, config={'CACHE_TYPE': 'simple'})

# limiter = Limiter(
#     get_remote_address,
#     app=app,
#     default_limits=["200 per day", "50 per hour"],
#     storage_uri="memory://",
#     )



signup_model = auth_namespace.model(
    'Signup', {
		'username': fields.String(required=True, description="User's Username"),
		'email': fields.String(required=True, description='User Email Address'),
		'password': fields.String(required=True, description='User Password')
	}
)



login_model = auth_namespace.model(
    'Login', {
		'email': fields.String(required=True, description='User email address'),
		'password': fields.String(required=True, description='User Password')
	}
)

api_key_model = auth_namespace.model(
	'ApiKey', {
		'key': fields.String(required=True, description='API Key'),
		# 'user_id': fields.Integer(required=True, description='User id')
	}
)

@auth_namespace.route('/generate-api-key')
class GenerateApiKey(Resource):
	@auth_namespace.marshal_with(api_key_model)
	@jwt_required()
	def post(self):
		"""
			Generate API Key
		"""
		key = secrets.token_hex(16)
		api_key = ApiKey(
			key=key,
		)
		api_key.save()

		return api_key, HTTPStatus.CREATED, {
			"message": "Api key generated successfully"
		}
	


def validate_api_key(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		api_key = request.headers.get('X-API-KEY')
		if not api_key:
			abort(401, message='No API Key provided')
		key = ApiKey.query.filter_by(key=api_key).first()
		if not key:
			abort(404, message='Invalid API Key')
		return func(*args, **kwargs)
	return wrapper


@auth_namespace.route('/apikeys')
class UserApiKeys(Resource):
	@auth_namespace.marshal_with(api_key_model, as_list=True)
	@jwt_required()
	def get(self):
		"""
			Get all API Keys generated by a user
		"""
		# user_id = get_jwt_identity()
		# api_keys = ApiKey.query.filter_by(user_id=user_id).all()
		# return api_keys, HTTPStatus.OK
		# abort(404, message=f'User {user} not found')

		api_keys = ApiKey.query.all()
		return api_keys, HTTPStatus.OK



@auth_namespace.route('/signup')
class SignUp(Resource):
	@cache.cached(timeout=60) # Cache the response for 60 seconds
	@limiter.limit("100/minute")  # Rate limit of 100 requests per minute (adjust as needed)
	@auth_namespace.expect(signup_model)
	@auth_namespace.marshal_with(signup_model)
	# @validate_api_key
	@auth_namespace.doc(security='apikey')
	def post(self):
		"""
			Register a user
		"""
		data = request.get_json()

		# check if user already exists
		user = User.query.filter_by(email=data.get('email')).first()
		if user:
			abort(409, message=f'User {user.username} already exists')


		new_user = User(
			username = data.get('username'),
			email = data.get('email'),
			password = generate_password_hash(data.get('password')),
			# is_admin = True
		)
		try:
			new_user.save()
			return new_user, HTTPStatus.CREATED, {
				'message': f'User {new_user.username} created successfully'
			}
		except Exception as e:
			# db.session.rollback()
			return {
				'message': 'Something went wrong'
			}, HTTPStatus.INTERNAL_SERVER_ERROR



@auth_namespace.route('/login')
class UserLogin(Resource):
	@cache.cached(timeout=60) # Cache the response for 60 seconds
	@auth_namespace.expect(login_model)
	def post(self):
		"""
			Generate JWT Token for user
		"""
		data = request.get_json()

		email = data.get('email')
		password = data.get('password')

		user = User.query.filter_by(email=email).first()
		
		if (user is not None) and email and check_password_hash(user.password, password): 
			access_token = create_access_token(identity=user.username)
			refresh_token = create_refresh_token(identity=user.username)

			clear_dataset()
			load_dataset()
			response = {
				'message': 'Logged in as {}'.format(user.username),
				'message': 'Dataset loaded successfully',
				'access_token': access_token,
				'refresh_token': refresh_token,
				'logged_in_as': user.username,
				'isLoggedIn': True
			}
			return response, HTTPStatus.ACCEPTED

		if not user:
			abort(401, message='Invalid Credentials')

@auth_namespace.route('/validate_token')
class ValidateToken(Resource):
	@cache.cached(timeout=60) # Cache the response for 60 seconds
	@jwt_required()
	def get(self):
		"""
			Validate JWT Token
		"""
		current_identity = get_jwt_identity()
		response = {
			'message': 'Token is valid',
			'logged_in_as': current_identity,
		}
		return response, HTTPStatus.OK



@auth_namespace.route('/refresh')
class Refresh(Resource):
	@cache.cached(timeout=60) # Cache the response for 60 seconds
	@jwt_required(refresh=True)
	def post(self):
		"""
			Refresh JWT access Token
		"""

		identity = get_jwt_identity()

		access_token = create_access_token(identity=identity)

		response = {
			'message': 'Access Token Refreshed',
			'access_token': access_token
		}
		return response, HTTPStatus.OK


blacklist = set()

# def check_token_blacklist(decrypted_token):
# 	jti = decrypted_token['jti']
# 	return jti in blacklist

# @jwt.expired_token_loader
# def my_expired_token_callback():
# 	return {
# 		'message': 'The token has expired.',
# 		'error': 'token_expired'
# 	}, HTTPStatus.UNAUTHORIZED

# @jwt.invalid_token_loader
# def invalid_token_callback(error):
# 	return {'message': 'Invalid token'}, 401

# @jwt.unauthorized_loader
# def unauthorized_callback(error):
# 	return {'message': 'Missing or Invalid authorization'}, 401


	
@auth_namespace.route('/logout')
class Logout(Resource):
	@cache.cached(timeout=60) # Cache the response for 60 seconds
	@jwt_required()
	def post(self):
		"""
			Logout user
		"""
		jti = get_jwt()['jti']
		blacklist.add(jti)
		response = {
			'message': 'Successfully logged out'
		}
		return response, HTTPStatus.OK