from flask import Flask, request
from flask_restx import Api, Resource, fields, Namespace, abort
from website.utils.utils import db

from website.models.apiKey import ApiKey


api_key_ns = Namespace('api_key', description='Generate API Key')

api_key_model = api_key_ns.model(
    "api_key", {
        "id": fields.String(required=True, description="API Key ID"),
        "key": fields.String(required=True, description="API Key"),
        "user_id": fields.String(required=True, description="User"),
        "user_name": fields.String(required=True, description="User")
    }
)


@api_key_ns.route('/generate-api-key')
class GenerateApiKey(Resource):
    pass
