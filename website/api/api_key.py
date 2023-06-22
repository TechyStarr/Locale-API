# from uuid import uuid4
# from flask import Flask, request
# from flask_restx import Api, Resource, fields, Namespace, abort
# from website.utils.utils import db
# from ..models.users import User, ApiKey




# api_key_model = api_key_ns.model(
#     "api_key", {
#         "id": fields.String(required=True, description="API Key ID"),
#         "key": fields.String(required=True, description="API Key"),
#         "user_id": fields.String(required=True, description="User"),
#         "user_name": fields.String(required=True, description="User")
#     }
# )


# @api_key_ns.route('/generate-api-key')
# class GenerateApiKey(Resource):
#     @api_key_ns.doc('generate_api_key')
#     @api_key_ns.marshal_with(api_key_model)
#     def post(self):
#         """Generate API Key"""
        # pass
        






# def api_key():
#     gen_api_key = secrets.token_hex(16)
#     return gen_api_key


# @api_key_ns.route("/generate-api-key")

# def get_api_key():
#     user = User.query.filter_by(email=user.email).first()
#     if user:
#         api_key = ApiKey(
#             key = str(uuid4()),
#             developer_name=api_key_ns.payload['developer_name']
#         )
#         db.save(api_key)
#         return api_key
    



# @api_key_ns.route('api/keys')


