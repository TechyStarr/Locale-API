from uuid import uuid4
from flask import Flask, request
from flask_restx import Resource, fields, Namespace, abort
from website.models.users import User, ApiKey
from website.utils.utils import db
from werkzeug.security import generate_password_hash, check_password_hash
from http import HTTPStatus
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
from flask_jwt_extended.exceptions import NoAuthorizationError
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


auth_namespace = Namespace('Auth', description='Authentication Endpoints')

app = Flask(__name__)

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
    )



signup_model = auth_namespace.model(
    'Signup', {
		'username': fields.String(required=True, description="User's Username"),
		'email': fields.String(required=True, description='User Email Address'),
		'password_hash': fields.String(required=True, description='User Password')
	}
)



login_model = auth_namespace.model(
    'Login', {
		'email': fields.String(required=True, description='User email address'),
		'password': fields.String(required=True, description='User Password')
	}
)



# def api_key():
#     gen_api_key = secrets.token_hex(16)
#     return gen_api_key



@auth_namespace.route("/generate-api-key")
class ApiKey(Resource):
	def get_api_key():
		user = User.query.filter_by(email=user.email).first()
		if user:
			key = ApiKey.query.filter_by(user_id=user.id).first()

			if key:
				return key
			api_key = ApiKey(
				key = str(uuid4()),
				developer_name=auth_namespace.payload['developer_name']
			)
			db.save(api_key)
			return api_key
		return {"message": "User not found"}, 404
    
	






@auth_namespace.route('/signup')
class SignUp(Resource):
	@cache.cached(timeout=60) # Cache the response for 60 seconds
	@limiter.limit("100/minute")  # Rate limit of 100 requests per minute (adjust as needed)

	@auth_namespace.expect(signup_model)
	@auth_namespace.marshal_with(signup_model)
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
			password_hash = generate_password_hash(data.get('password_hash')),
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

			response = {
				'message': 'Logged in as {}'.format(user.username),
				'access_token': access_token,
				'refresh_token': refresh_token
			}
			return response, HTTPStatus.ACCEPTED

		if not user:
			abort(401, message='Invalid Credentials')



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

